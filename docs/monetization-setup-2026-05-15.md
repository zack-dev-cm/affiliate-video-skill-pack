# Monetization Setup 2026-05-15

## Decision

The public templates are a free launch pack. Do not sell the zip as private content while the source and release asset are public.

Paid checkout is reserved for services:

- Setup Review: $299
- Managed Launch: $999

## Live Surfaces

- Landing: `https://affiliate-video.getgeofix.xyz/`
- Public example: `https://affiliate-video.getgeofix.xyz/examples`
- Checkout: `https://affiliate-video.getgeofix.xyz/checkout`
- GitHub release: `https://github.com/zack-dev-cm/affiliate-video-skill-pack/releases/latest`
- ClawHub slug: `affiliate-video-campaign-operator`

## Payment Configuration

Provider: NOWPayments hosted invoices.

Cloudflare Pages production secrets:

- `NOWPAYMENTS_API_KEY`
- `NOWPAYMENTS_IPN_SECRET`

The invoice function sends `price_currency=usd` and does not force a `pay_currency`. Fiat/card availability is controlled by NOWPayments account settings, buyer location, provider support, and account approval.

Additional payment rails are tracked in `docs/payment-provider-setup-2026-05-15.md`.

- NOWPayments fiat activation is visible in the dashboard through Guardarian and Banxa, but both require KYC/KYB and an activation request.
- Lava.top product links can be exposed after email confirmation, profile setup, product publication, and moderation.
- Boosty links can be exposed after the public creator page and paid posts or goals are created.

The checkout page reads optional Lava.top and Boosty URLs from `site/checkout-config.json`. If those URLs are absent, only NOWPayments appears.

## Fulfillment

Free launch pack:

- Download from the latest GitHub release asset.

Setup Review:

1. Buyer completes a NOWPayments invoice.
2. Buyer opens a sanitized support issue with the offer name and campaign blocker.
3. Operator verifies invoice completion in NOWPayments dashboard.
4. Operator reviews one sanitized campaign ledger and returns disclosure, claim, provenance, and handoff notes.

Managed Launch:

1. Buyer completes a NOWPayments invoice only after scope is clear.
2. Buyer opens a sanitized support issue with offer name and desired target platforms.
3. Operator verifies invoice completion in NOWPayments dashboard.
4. Operator prepares one campaign setup with creative plan, QC report, and OpenClaw handoff.

Do not ask buyers to post payment IDs, wallet addresses, account screenshots, cookies, affiliate IDs, or credentials in public support.

## Next Monetization Upgrade

Before selling a private digital pack, add one of:

- Cloudflare D1/KV order storage plus signed private download links.
- Gumroad/Lemon Squeezy/Polar checkout for digital delivery.
- Email-based fulfillment with a verified support inbox and privacy terms.

Do not add a SaaS dashboard until there is demand for one of:

- 10 users asking for paid templates or setup.
- 3 creators submitting real campaigns for review.
- 100 weekly active users in the receipt extension.
