const OFFERS = [
  {
    id: "pro-pack",
    name: "Affiliate Video Pro Pack",
    price_amount: "49.00",
    price_currency: "usd",
    description:
      "Editable templates for affiliate campaign intake, disclosures, claims, captions, and 30-day experiments.",
  },
  {
    id: "setup-review",
    name: "Affiliate Video Setup Review",
    price_amount: "299.00",
    price_currency: "usd",
    description:
      "One sanitized campaign ledger reviewed for disclosure, claims, asset provenance, and publish handoff readiness.",
  },
  {
    id: "managed-launch",
    name: "Affiliate Video Managed Launch",
    price_amount: "999.00",
    price_currency: "usd",
    description: "One scoped affiliate campaign setup with creative planning, QC report, and OpenClaw handoff.",
  },
];

export async function onRequestGet() {
  return new Response(
    JSON.stringify({
      provider: "NOWPayments",
      checkout_type: "hosted_invoice",
      fiat_price_currency: "usd",
      offers: OFFERS,
    }),
    {
      headers: {
        "Content-Type": "application/json; charset=utf-8",
        "Cache-Control": "no-store",
      },
    },
  );
}
