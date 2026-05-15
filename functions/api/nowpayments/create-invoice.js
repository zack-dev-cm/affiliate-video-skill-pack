import { paidOfferFor } from "../../_shared/monetization-offers.js";

const NOWPAYMENTS_INVOICE_URL = "https://api.nowpayments.io/v1/invoice";

const JSON_HEADERS = {
  "Content-Type": "application/json; charset=utf-8",
  "Cache-Control": "no-store",
};

function json(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: JSON_HEADERS,
  });
}

function originFor(request) {
  const url = new URL(request.url);
  return `${url.protocol}//${url.host}`;
}

function orderIdFor(offerId) {
  const suffix =
    typeof crypto.randomUUID === "function"
      ? crypto.randomUUID().slice(0, 8)
      : Math.random().toString(16).slice(2, 10);
  return `av-${offerId}-${Date.now()}-${suffix}`;
}

function publicProviderError(status, payload) {
  const providerCode =
    payload && typeof payload === "object" && typeof payload.code === "string" ? payload.code : undefined;
  return {
    error: "invoice_create_failed",
    provider_status: status,
    provider_code: providerCode,
    message: "NOWPayments could not create the invoice. Retry or use support with the offer name.",
  };
}

export async function onRequestOptions() {
  return new Response(null, {
    status: 204,
    headers: JSON_HEADERS,
  });
}

export async function onRequestPost({ request, env }) {
  let payload = {};
  try {
    payload = await request.json();
  } catch (error) {
    return json({ error: "invalid_json", message: "Expected JSON body with an offer id." }, 400);
  }

  const offerId = typeof payload.offer === "string" ? payload.offer.trim().toLowerCase() : "";
  const offer = paidOfferFor(offerId);
  if (!offer) {
    return json(
      {
        error: "unknown_offer",
        message: "Choose setup-review or managed-launch. The template pack is a free public download.",
      },
      400,
    );
  }

  if (!env.NOWPAYMENTS_API_KEY) {
    return json(
      {
        error: "payment_not_configured",
        message: "NOWPayments API key is not configured for this Pages deployment.",
      },
      503,
    );
  }

  const origin = originFor(request);
  const orderId = orderIdFor(offerId);
  const invoiceBody = {
    price_amount: offer.priceUsd.toFixed(2),
    price_currency: "usd",
    order_id: orderId,
    order_description: offer.description,
    ipn_callback_url: `${origin}/api/nowpayments/ipn`,
    success_url: `${origin}/success.html?offer=${encodeURIComponent(offerId)}&order_id=${encodeURIComponent(orderId)}`,
    cancel_url: `${origin}/cancel.html?offer=${encodeURIComponent(offerId)}&order_id=${encodeURIComponent(orderId)}`,
    is_fixed_rate: false,
    is_fee_paid_by_user: false,
  };

  let providerResponse;
  let providerPayload;
  try {
    providerResponse = await fetch(NOWPAYMENTS_INVOICE_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": env.NOWPAYMENTS_API_KEY,
      },
      body: JSON.stringify(invoiceBody),
    });
    providerPayload = await providerResponse.json();
  } catch (error) {
    console.error("NOWPayments invoice request failed", { message: error.message });
    return json(
      {
        error: "provider_unreachable",
        message: "NOWPayments invoice service did not respond. Retry in a few minutes.",
      },
      502,
    );
  }

  if (!providerResponse.ok || !providerPayload || typeof providerPayload.invoice_url !== "string") {
    console.error("NOWPayments invoice create failed", {
      status: providerResponse.status,
      code: providerPayload && providerPayload.code,
    });
    return json(publicProviderError(providerResponse.status, providerPayload), 502);
  }

  return json({
    provider: "NOWPayments",
    order_id: orderId,
    invoice_id: providerPayload.id || providerPayload.invoice_id || null,
    invoice_url: providerPayload.invoice_url,
    offer: {
      id: offerId,
      name: offer.name,
      price_amount: offer.priceUsd.toFixed(2),
      price_currency: "usd",
    },
  });
}
