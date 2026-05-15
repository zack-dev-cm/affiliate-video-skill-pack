export const FREE_PACK = {
  id: "free-launch-pack",
  name: "Affiliate Video Launch Pack",
  priceAmount: "0.00",
  priceCurrency: "usd",
  checkoutType: "public_download",
  description:
    "Free public templates for affiliate campaign intake, disclosures, claims, captions, and 30-day experiments.",
  downloadUrl:
    "https://github.com/zack-dev-cm/affiliate-video-skill-pack/releases/latest/download/affiliate-video-pro-pack.zip",
};

export const PAID_OFFERS = {
  "setup-review": {
    id: "setup-review",
    name: "Affiliate Video Setup Review",
    priceUsd: 299,
    checkoutType: "nowpayments_invoice",
    description:
      "One sanitized campaign ledger reviewed for disclosure, claims, asset provenance, and publish handoff readiness.",
  },
  "managed-launch": {
    id: "managed-launch",
    name: "Affiliate Video Managed Launch",
    priceUsd: 999,
    checkoutType: "nowpayments_invoice",
    description:
      "One scoped affiliate campaign setup with creative planning, QC report, and OpenClaw handoff.",
  },
};

export function paidOfferFor(offerId) {
  return PAID_OFFERS[offerId] || null;
}

export function publicOffers() {
  return [
    {
      id: FREE_PACK.id,
      name: FREE_PACK.name,
      price_amount: FREE_PACK.priceAmount,
      price_currency: FREE_PACK.priceCurrency,
      checkout_type: FREE_PACK.checkoutType,
      description: FREE_PACK.description,
      download_url: FREE_PACK.downloadUrl,
    },
    ...Object.values(PAID_OFFERS).map((offer) => ({
      id: offer.id,
      name: offer.name,
      price_amount: offer.priceUsd.toFixed(2),
      price_currency: "usd",
      checkout_type: offer.checkoutType,
      description: offer.description,
    })),
  ];
}
