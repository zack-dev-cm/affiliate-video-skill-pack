# Monetization Strategy

## Product Ladder

1. Free public skill pack
   - GitHub and ClawHub distribution.
   - Gives campaign ledger, compliance checker, and OpenClaw handoff.
   - Goal: trust, stars, installs, examples, inbound demand.

2. Free launch template pack
   - Public release asset.
   - Niche scorecards, compliant hook banks, carousel structures, caption/disclosure variants, and landing-page templates.
   - Avoid selling copied prompts from third-party PDFs or videos.

3. Chrome extension
   - Freemium.
   - Free: capture product page, affiliate URL, disclosure text, source screenshots, post receipts.
   - Pro: policy checks, campaign analytics import, team review, export to Claude/Codex/OpenClaw bundles.

4. Managed setup
   - $299 to $999 one-time.
   - Configure Claude/Higgsfield, install Codex skill, set up landing page, connect analytics, create first compliant campaign.

5. Monthly operator
   - $500 to $2,500 per month plus generation spend.
   - Weekly campaign research, creative batching, OpenClaw publishing handoff, analytics review, and kill/scale decisions.

6. Performance upside
   - Use only when attribution is clean and account ownership is clear.
   - Avoid vague revenue share if the operator cannot verify clicks, refunds, chargebacks, and policy compliance.

## Best First Market

Avoid starting with health supplements despite high tutorial appeal. The trust and policy burden is high.

Better first verticals:

- creator desk gear
- camera/mobile accessories
- home organization
- kitchen workflow tools
- travel organization
- productivity software with affiliate programs
- AI creator tools where claims are demonstrable

## Landing Page Positioning

Primary promise:

`Launch AI affiliate videos with receipts: claims, disclosures, provenance, and publish handoffs in one workflow.`

Trust proof:

- open-source skill
- current policy-aware gates
- no copied prompt packs
- no fake testimonial defaults
- sample campaign ledger
- screenshot receipt workflow

CTA offers:

- `Free Launch Pack`
- `Setup Review`
- `Managed Launch`

Use NOWPayments hosted invoices for setup services in the current deployment. Keep the free skill and launch pack usable without payment.

Repo implementation:

- Static page: `site/index.html`
- Setup-service checkout: `site/checkout.html`
- Privacy/support pages: `site/privacy.html`, `site/support.html`
- Launch Pack source: `monetization/affiliate-video-pro-pack`
- Launch Pack build command: `python3 scripts/build_monetization_pack.py --out dist/affiliate-video-pro-pack.zip`

Do not charge for a private digital pack until the operator has:

- refund/support terms,
- a working delivery path for the zip,
- a provider account URL,
- privacy text updated for the provider,
- at least one public demo campaign or explicit buyer request.

## Kill Gates

Do not build a heavy SaaS until one of these happens:

- 10 users ask for paid setup or private template delivery.
- 3 creators submit real campaigns for review.
- The extension has 100 weekly active users.
- A landing page converts above 2 percent from targeted traffic.

Stop a niche campaign if:

- no saves or clicks after 1,000 relevant impressions
- cost per click exceeds expected commission economics
- platform policy blocks the product category
- content depends on unsupported health or income claims
