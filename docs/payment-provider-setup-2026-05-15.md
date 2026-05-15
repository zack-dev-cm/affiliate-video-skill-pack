# Payment Provider Setup 2026-05-15

## Goal

Accept setup-service payments through:

- NOWPayments hosted invoices as the active primary rail.
- Lava.top as a card-friendly digital-product rail after email/profile/product moderation.
- Boosty as a creator-support rail after creator-page creation.

## Current Status

| Provider | Status | Blocker |
| --- | --- | --- |
| NOWPayments | API key, IPN secret, invoice creation, and IPN verification are already wired through Cloudflare Pages Functions. | Fiat on-ramp activation requires provider KYC/KYB and a dashboard activation request. |
| Lava.top | Account session is present in Chrome. Creator dashboard opens. | Email confirmation code must be entered by explicit approval. Profile details and product publication are required before product links can be used. |
| Boosty | Account session is present in Chrome. Creator-account modal opens. | Public creator URL and final account creation require explicit approval before submission. |

## NOWPayments Fiat

Dashboard path:

```text
Settings -> Payments -> Fiat operations
```

The account shows on-ramp providers with activation buttons:

- Guardarian: card, Google Pay, Apple Pay, SEPA; dashboard notes 140+ countries except the US and Canada; KYC and KYB required.
- Banxa: card, Google Pay, Apple Pay, SEPA, PIX; dashboard notes 200+ countries including some US states; KYC and KYB required.

Do not click `Activate` without action-time approval. Activation can start a provider request and may require transmitting business, identity, payout, and compliance data to NOWPayments or the fiat provider.

Recommendation: use Banxa first if US buyer coverage matters. Use Guardarian as a second rail if its country coverage fits the buyer base.

## Lava.top Product Setup

Official Lava docs describe the product flow as:

1. Create -> Digital product.
2. Fill `Card`: name, short description, price, tariffs, availability, and purchase-button text.
3. Fill `Landing page`: public pre-purchase description and cover.
4. Fill `After payment`: paid content, links, files, or instructions.
5. Publish. Lava sends products to moderation before they appear publicly.

Recommended products:

### Affiliate Video Setup Review

Price: `299 USD`

Short description:

```text
One sanitized affiliate-video campaign ledger reviewed for disclosures, claims, asset provenance, and handoff readiness. No revenue, ranking, platform approval, or legal-compliance guarantee.
```

After-payment instructions:

```text
Open support at https://github.com/zack-dev-cm/affiliate-video-skill-pack/issues/new with the offer name and a sanitized campaign brief. Do not include credentials, cookies, affiliate IDs, payment IDs, wallet addresses, or account screenshots.
```

### Affiliate Video Managed Launch

Price: `999 USD`

Short description:

```text
One scoped affiliate-video campaign setup with creative planning, QC report, and supervised OpenClaw handoff. Scope must be agreed before work starts. No revenue, ranking, platform approval, or legal-compliance guarantee.
```

After-payment instructions:

```text
Open support at https://github.com/zack-dev-cm/affiliate-video-skill-pack/issues/new with the offer name, target platforms, and a sanitized campaign brief. Do not include credentials, cookies, affiliate IDs, payment IDs, wallet addresses, or account screenshots.
```

After each Lava product is approved, add its public product URL to `site/checkout-config.json`:

```json
{
  "setup_review_lava_checkout_url": "https://app.lava.top/...",
  "managed_launch_lava_checkout_url": "https://app.lava.top/..."
}
```

## Boosty Creator Setup

Boosty currently opens the `Become a creator` modal. Suggested public URL:

```text
boosty.to/affiliate-video-operator
```

Do not submit the modal without action-time approval. Submitting creates a public creator account and accepts platform terms. After the creator page exists, create either:

- A paid post for `Affiliate Video Setup Review`.
- A paid post or goal for `Affiliate Video Managed Launch`.

Recommended copy should match the Lava descriptions above. After each Boosty payment link exists, add it to `site/checkout-config.json`:

```json
{
  "setup_review_boosty_checkout_url": "https://boosty.to/...",
  "managed_launch_boosty_checkout_url": "https://boosty.to/..."
}
```

## Checkout Behavior

The live checkout uses `/api/nowpayments/create-invoice` by default. `checkout-config.json` can add external links without disabling NOWPayments.

Supported optional keys:

```json
{
  "setup_review_checkout_url": "https://...",
  "managed_launch_checkout_url": "https://...",
  "setup_review_lava_checkout_url": "https://...",
  "managed_launch_lava_checkout_url": "https://...",
  "setup_review_boosty_checkout_url": "https://...",
  "managed_launch_boosty_checkout_url": "https://..."
}
```

Only `https://` links are accepted by the front-end script. Placeholder values stay hidden.

## References

- NOWPayments integration guide: `https://nowpayments.zendesk.com/hc/en-us/articles/21341613323421-NOWPayments-Integration-Guide`
- NOWPayments Guardarian fiat article: `https://nowpayments.zendesk.com/hc/en-us/articles/30614003290781-Fiat-payments-with-Guardarian`
- Lava.top creating a product: `https://en.faq.lava.top/article/61207`
- Lava.top moderation and verification: `https://en.faq.lava.top/article/61205`
- Boosty support and creator landing: `https://boosty.to/app/support?locale=en_US`
