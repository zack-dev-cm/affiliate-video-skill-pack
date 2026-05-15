# Affiliate Video Skill Pack

Original skill for compliant AI affiliate-video campaigns across Claude, Codex, and OpenClaw.

It adapts the useful pattern from Claude + Higgsfield affiliate workflows into a safer production system:
research the offer, prove the claims, generate videos/carousels, keep provenance, disclose commercial relationships, and hand off publishing to supervised browser automation.

## Skill

- `skill/affiliate-video-campaign-operator`

## What It Does

- Turns a product or niche into a campaign ledger with offer, disclosure, claims, creative assets, posts, and analytics.
- Validates affiliate disclosures, Amazon Associate language, TikTok health/supplement risks, fake-testimonial language, product claims, and missing asset rights notes.
- Produces Claude/Higgsfield creative prompts as operator guidance without copying third-party prompt packs.
- Exports OpenClaw handoff bundles for supervised Pinterest, TikTok, YouTube Shorts, and Instagram Reels publishing.
- Combines with `agentic-video-production-publisher` for character/music/shot ledgers and with `openclaw-youtube-tiktok-publisher` for logged-in publishing.

## Quick Start

```bash
python3 skill/affiliate-video-campaign-operator/scripts/init_affiliate_campaign.py \
  --out runs/campaign.json \
  --title "Sleep Routine Magnesium Test" \
  --owner "zack-dev-cm" \
  --niche "sleep wellness" \
  --product-name "Magnesium glycinate supplement" \
  --merchant "Amazon" \
  --affiliate-program "amazon-associates" \
  --platform pinterest \
  --platform youtube
```

```bash
python3 skill/affiliate-video-campaign-operator/scripts/check_affiliate_campaign.py \
  --campaign runs/campaign.json \
  --repo-root . \
  --out reports/campaign-qc.json
```

```bash
python3 skill/affiliate-video-campaign-operator/scripts/add_affiliate_claim.py \
  --campaign runs/campaign.json \
  --claim "Designed to organize loose desk cables" \
  --risk low \
  --evidence-url "https://example.com/product"
```

```bash
python3 skill/affiliate-video-campaign-operator/scripts/set_affiliate_post.py \
  --campaign runs/campaign.json \
  --platform pinterest \
  --title "Desk cable reset" \
  --caption "Paid link. Simple desk setup idea." \
  --status ready
```

```bash
python3 skill/affiliate-video-campaign-operator/scripts/render_affiliate_plan.py \
  --campaign runs/campaign.json \
  --out reports/campaign-plan.md
```

```bash
python3 skill/affiliate-video-campaign-operator/scripts/export_openclaw_handoff.py \
  --campaign runs/campaign.json \
  --platform pinterest \
  --out runs/pinterest-openclaw-handoff.json \
  --browser-profile pinterest-profile
```

## Claude Package

```bash
mkdir -p dist
cd skill
zip -r ../dist/affiliate-video-campaign-operator-claude.zip affiliate-video-campaign-operator
```

Upload the zip in Claude through Settings -> Capabilities -> Skills -> Upload skill.

## Codex Install

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skill/affiliate-video-campaign-operator "${CODEX_HOME:-$HOME/.codex}/skills/"
```

## Tests

```bash
python3 -m unittest discover -s tests -v
```

## Landing Page And Monetization Pack

The static landing page lives in `site/` and is ready for Cloudflare Pages or any static host.

```bash
python3 -m http.server 8787 --directory site
```

The paid template bundle lives in `monetization/affiliate-video-pro-pack`.

```bash
python3 scripts/build_monetization_pack.py \
  --out dist/affiliate-video-pro-pack.zip
```

The checkout page is intentionally a placeholder until a Stripe, Gumroad, Lemon Squeezy, Polar, or other provider URL is connected.

## ClawHub Publish

Publish the skill folder, not the repo root:

```bash
clawhub publish "$PWD/skill/affiliate-video-campaign-operator" \
  --slug affiliate-video-campaign-operator \
  --name "Affiliate Video Campaign Operator" \
  --version 0.1.2 \
  --tags "affiliate,video,openclaw,claude,higgsfield,pinterest,tiktok,youtube,compliance" \
  --changelog "Add static landing page, checkout placeholder, and Pro Pack monetization bundle."
```

## Safety

Do not commit private affiliate IDs, cookies, account sessions, brand-provided confidential briefs, generated paid media that you cannot redistribute, or copied third-party prompt packs.
