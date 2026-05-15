import { publicOffers } from "../../_shared/monetization-offers.js";

export async function onRequestGet() {
  return new Response(
    JSON.stringify({
      provider: "NOWPayments",
      checkout_type: "hosted_invoice_for_paid_services",
      fiat_price_currency: "usd",
      offers: publicOffers(),
    }),
    {
      headers: {
        "Content-Type": "application/json; charset=utf-8",
        "Cache-Control": "no-store",
      },
    },
  );
}
