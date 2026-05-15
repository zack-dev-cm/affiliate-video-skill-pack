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

function sortObject(value) {
  if (Array.isArray(value)) {
    return value.map((item) => sortObject(item));
  }
  if (value && typeof value === "object") {
    return Object.keys(value)
      .sort()
      .reduce((result, key) => {
        result[key] = sortObject(value[key]);
        return result;
      }, {});
  }
  return value;
}

function toHex(buffer) {
  return Array.from(new Uint8Array(buffer))
    .map((byte) => byte.toString(16).padStart(2, "0"))
    .join("");
}

function constantTimeEqual(a, b) {
  if (typeof a !== "string" || typeof b !== "string" || a.length !== b.length) {
    return false;
  }
  let diff = 0;
  for (let index = 0; index < a.length; index += 1) {
    diff |= a.charCodeAt(index) ^ b.charCodeAt(index);
  }
  return diff === 0;
}

async function hmacSha512(secret, message) {
  const encoder = new TextEncoder();
  const key = await crypto.subtle.importKey(
    "raw",
    encoder.encode(secret),
    { name: "HMAC", hash: "SHA-512" },
    false,
    ["sign"],
  );
  const signature = await crypto.subtle.sign("HMAC", key, encoder.encode(message));
  return toHex(signature);
}

export async function onRequestOptions() {
  return new Response(null, {
    status: 204,
    headers: JSON_HEADERS,
  });
}

export async function onRequestPost({ request, env }) {
  if (!env.NOWPAYMENTS_IPN_SECRET) {
    return json({ error: "ipn_not_configured" }, 503);
  }

  const incomingSignature = (request.headers.get("x-nowpayments-sig") || "").trim().toLowerCase();
  if (!incomingSignature) {
    return json({ error: "missing_signature" }, 401);
  }

  let payload;
  try {
    payload = await request.json();
  } catch (error) {
    return json({ error: "invalid_json" }, 400);
  }

  const sortedJson = JSON.stringify(sortObject(payload));
  const expectedSignature = await hmacSha512(env.NOWPAYMENTS_IPN_SECRET, sortedJson);
  if (!constantTimeEqual(incomingSignature, expectedSignature)) {
    return json({ error: "invalid_signature" }, 401);
  }

  console.log("NOWPayments IPN verified", {
    order_id: payload.order_id || null,
    invoice_id: payload.invoice_id || null,
    payment_id: payload.payment_id || null,
    payment_status: payload.payment_status || null,
  });

  return json({ ok: true });
}
