# New Skill Proposals

## Implemented First: affiliate-video-campaign-operator

Audience: Claude, Codex, OpenClaw.

Reason: all agents need the same source of truth for offer, claims, disclosures, creative assets, posts, and analytics. Splitting too early would make compliance drift likely.

Claude role:

- use as campaign strategist and Higgsfield creative director
- produce claim-safe creative packs
- maintain the ledger when local scripts are unavailable
- stop before spend-heavy generation or sensitive claims

Codex role:

- run deterministic scripts
- validate campaigns
- render reports
- export OpenClaw handoffs
- package GitHub/ClawHub/Claude zip artifacts

OpenClaw role:

- operate logged-in browser UIs
- apply platform labels
- upload assets
- capture screenshots and public URLs
- pause on account, policy, billing, or final-publish gates

## Next Skill 1: affiliate-receipt-extension-operator

Purpose: build and operate the Chrome extension that captures product evidence and publishing receipts.

Inputs:

- product page URL
- affiliate URL
- post URL
- generated asset path
- caption/disclosure text

Outputs:

- campaign JSON patch
- product-page screenshot
- link/disclosure receipt
- publish receipt
- policy-risk flags

Combine with:

- `chrome-extension-cws-shipper`
- `affiliate-video-campaign-operator`
- `product-share-trigger-reviewer`

## Next Skill 2: pinterest-affiliate-openclaw-publisher

Purpose: dedicated OpenClaw publisher for Pinterest pins and carousels with disclosure and affiliate-link checks.

Inputs:

- OpenClaw handoff JSON
- browser profile
- board name
- pin title, description, asset path, destination URL

Outputs:

- draft/published pin URL
- screenshot evidence
- label/disclosure confirmation
- campaign JSON update

Combine with:

- `affiliate-video-campaign-operator`
- `openclaw-youtube-tiktok-publisher`

## Next Skill 3: affiliate-landing-page-conversion-builder

Purpose: owned landing page and buy-button workflow for affiliate/video products.

Inputs:

- campaign ledger
- offer tier
- testimonials or public proof
- policy URLs
- Stripe/Lemon Squeezy/Gumroad/Polar choice

Outputs:

- landing page copy
- visual direction
- checkout button config
- analytics events
- privacy/affiliate disclosure pages

Combine with:

- `design-md-ui-designer`
- `product-share-trigger-reviewer`
- `affiliate-video-campaign-operator`

## Decision

Ship the base campaign skill first, then build the receipt extension second. Do not make the supplement tutorial the flagship demo. Use a lower-risk physical product or creator-tool affiliate first, prove demand, then expand to sensitive niches only with stronger review gates.
