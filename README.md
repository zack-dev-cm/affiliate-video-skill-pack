# Affiliate Video Skill Pack

Original skill for compliant AI affiliate-video campaign review across Claude,
Codex, OpenClaw, Grok, and generic agent runtimes.

It adapts the useful pattern from Claude + Higgsfield affiliate workflows into a safer production system:
research the offer, prove the claims, plan videos/carousels, keep provenance,
disclose commercial relationships, and prepare a human publishing checklist.

## Skill

- `skill/affiliate-video-campaign-operator`

## What It Does

- Reviews a product or niche campaign plan with offer, disclosure, claims,
  creative notes, posts, and analytics fields.
- Validates affiliate disclosures, Amazon Associate language, TikTok health/supplement risks, fake-testimonial language, product claims, and missing asset rights notes.
- Produces Claude/Higgsfield creative prompts as operator guidance without copying third-party prompt packs.
- Keeps final Pinterest, TikTok, YouTube Shorts, and Instagram Reels publishing
  as a human decision after review.
- The repo still includes `export_openclaw_handoff.py` for legacy local
  experiments, but that helper is excluded from the ClawHub package.

## Quick Start

```bash
python3 skill/affiliate-video-campaign-operator/scripts/init_affiliate_campaign.py \
  --out runs/campaign.json \
  --title "Creator Desk Cable Reset" \
  --owner "zack-dev-cm" \
  --niche "creator desk gear" \
  --product-name "Cable organizer kit" \
  --product-category "home office accessory" \
  --merchant "Example Merchant" \
  --product-url "https://example.com/product" \
  --affiliate-url "https://example.com/product?aff=example" \
  --affiliate-program "example-affiliate" \
  --short-disclosure "Paid link." \
  --platform pinterest \
  --platform youtube
```

```bash
python3 skill/affiliate-video-campaign-operator/scripts/add_affiliate_claim.py \
  --campaign runs/campaign.json \
  --claim "Designed to organize loose desk cables" \
  --risk low \
  --evidence-url "https://example.com/product"
```

```bash
mkdir -p assets
: > assets/pin-001.png
python3 skill/affiliate-video-campaign-operator/scripts/add_affiliate_asset.py \
  --campaign runs/campaign.json \
  --kind generated \
  --asset-id pin-001 \
  --path assets/pin-001.png \
  --provider "example-generator" \
  --rights-note "Generated for this campaign from operator-approved product reference."
```

```bash
python3 skill/affiliate-video-campaign-operator/scripts/set_affiliate_post.py \
  --campaign runs/campaign.json \
  --platform pinterest \
  --title "Desk cable reset" \
  --caption "Paid link. Simple desk setup idea." \
  --asset-path assets/pin-001.png \
  --status ready
```

```bash
python3 skill/affiliate-video-campaign-operator/scripts/check_affiliate_campaign.py \
  --campaign runs/campaign.json \
  --repo-root . \
  --out reports/campaign-qc.json
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

## Use In Agent Runtimes

All runtimes use the same source folder:

```text
skill/affiliate-video-campaign-operator
```

Common operator flow:

1. Create or edit `runs/campaign.json`.
2. Run `check_affiliate_campaign.py` before generation and publishing.
3. Render `reports/campaign-plan.md` for human review.
4. Prepare a human publishing checklist only after disclosures, claims, rights
   notes, and asset paths are filled.

### Claude

Package the skill folder as a zip and upload it through Claude's Skills UI:

```bash
mkdir -p dist
cd skill
zip -r ../dist/affiliate-video-campaign-operator-claude.zip affiliate-video-campaign-operator
```

In Claude, start with:

```text
Use the Affiliate Video Campaign Operator skill. Create a campaign ledger for this product, ask only for missing campaign-critical fields, then prepare conservative creative notes and tell me which local validation command to run before generation.
```

If Claude has local file/code execution, it can run the bundled scripts. Otherwise it should produce JSON edits, review notes, and exact local commands for the operator. Use Higgsfield or other MCP video tools only after the campaign ledger has offer, disclosure, claim, and rights fields filled.

### Codex

Install locally:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skill/affiliate-video-campaign-operator "${CODEX_HOME:-$HOME/.codex}/skills/"
```

In Codex, ask:

```text
Use the affiliate-video-campaign-operator skill to review a campaign ledger and
prepare a human publishing checklist for Pinterest.
```

Codex should run the bundled Python scripts instead of rewriting the workflow by hand.

### OpenClaw

OpenClaw-specific experiments should stay outside the ClawHub package. The
legacy local helper remains in this repo for maintainers who need to inspect old
run formats:

```bash
python3 skill/affiliate-video-campaign-operator/scripts/export_openclaw_handoff.py --help
```

Supported review platforms are `pinterest`, `tiktok`, `youtube`, and
`instagram`. Other platforms can be tracked manually in
`campaign.target_platforms`.

### Grok And Other Chat Agents

This repo does not assume Grok has a native skill installer. Use the skill as a plain-text operating guide:

1. Attach or paste `skill/affiliate-video-campaign-operator/SKILL.md`.
2. Attach `references/compliance-gates.md` and `references/platform-adapters.md` when platform or policy decisions matter.
3. Ask Grok to produce JSON edits, captions, claim wording, or review notes.
4. Run the Python scripts locally in the repo to validate and render final artifacts.

Starter prompt:

```text
Use the attached Affiliate Video Campaign Operator instructions. Do not invent product claims or fake personal experience. Ask for missing campaign fields, draft conservative creative notes, and tell me which local script command to run next.
```

## Landing Page And Monetization Pack

The static landing page lives in `site/` and is ready for Cloudflare Pages or any static host.

```bash
python3 -m http.server 8787 --directory site
```

The free launch template bundle lives in `monetization/affiliate-video-pro-pack`.

```bash
python3 scripts/build_monetization_pack.py \
  --out dist/affiliate-video-pro-pack.zip
```

The checkout page creates server-side NOWPayments hosted invoices for paid setup services through Cloudflare Pages
Functions. Prices are denominated in USD with `price_currency=usd`; the hosted invoice lets buyers choose supported
crypto or fiat rails available for the NOWPayments account.

For deployment and custom-domain setup, see `docs/deployment-checklist.md`.

```bash
python3 scripts/deploy_cloudflare_pages.py \
  --project-name affiliate-video-skill-pack \
  --custom-domain affiliate-video.getgeofix.xyz
```

## ClawHub Publish

Publish the skill folder, not the repo root:

```bash
clawhub publish "$PWD/skill/affiliate-video-campaign-operator" \
  --slug affiliate-video-campaign-operator \
  --name "Affiliate Video Campaign Operator" \
  --version 0.1.6 \
  --tags "affiliate,video,openclaw,claude,higgsfield,pinterest,tiktok,youtube,compliance" \
  --changelog "Add clear Claude, Codex, OpenClaw, Grok, and generic-agent usage instructions."
```

## Safety

Do not commit private affiliate IDs, cookies, account sessions, brand-provided confidential briefs, generated paid media that you cannot redistribute, or copied third-party prompt packs.
