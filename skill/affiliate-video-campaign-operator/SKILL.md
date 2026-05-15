---
name: affiliate-video-campaign-operator
description: Build compliant AI affiliate-video campaigns from niche research to Claude/Higgsfield creative packs and supervised OpenClaw publishing handoffs. Use when users ask for affiliate UGC videos, Pinterest carousels, product research, Claude MCP/Higgsfield workflows, affiliate disclosure checks, monetization, or cross-posting to TikTok, Instagram, YouTube Shorts, or Pinterest.
license: MIT-0
metadata: {"openclaw":{"skillKey":"affiliate-video-campaign-operator","requires":{"anyBins":["python3","python"]},"relatedSkills":["agentic-video-production-publisher","openclaw-youtube-tiktok-publisher","chrome-extension-cws-shipper"]}}
---

# Affiliate Video Campaign Operator

## Goal

Run an AI-assisted affiliate campaign without losing disclosure, claim evidence, platform compliance, creative provenance, or publish evidence.

This skill is an original workflow for Claude, Codex, and OpenClaw. It may be inspired by public affiliate-video patterns, but it must not copy paid prompt packs, private playbooks, or third-party templates into public artifacts.

## Non-Negotiables

- Treat affiliate links, promo codes, gifted products, and paid placements as commercial content. Add clear disclosure close to the endorsement and in video/carousel creative when applicable.
- Do not create fake personal testimonials. If the operator has not used the product, avoid first-person result claims such as "I tried this" or "it fixed my sleep."
- Do not make medical, health, financial, legal, safety, or income claims without evidence that is recorded in the campaign ledger.
- For supplements, skincare, sleep aids, finance, weight loss, or other sensitive products, use conservative educational language and platform-specific gates before generating or publishing.
- Do not set paid-generation MCP tools to unrestricted background spending. Batch drafts can be automated; spend, health claims, and irreversible publishing need explicit operator review.
- Keep provenance for every asset: source image or link, generation provider/model, prompt file or prompt summary, rights note, selected export path, and rejected-take notes when useful.
- Use OpenClaw only for logged-in browser operations. Pause for CAPTCHA, 2FA, account recovery, billing, copyright disputes, or final publish confirmation when not pre-approved.

## Quick Start

1. Create a campaign ledger.

```bash
python3 {baseDir}/scripts/init_affiliate_campaign.py --out runs/campaign.json --title "Campaign title" --niche "home organization" --product-name "Cable organizer kit" --platform pinterest --platform youtube
```

2. Fill the ledger with:
   - offer: product, merchant, affiliate program, affiliate URL, commission note, product source, rights note
   - disclosure: short disclosure, Amazon Associate statement if relevant, platform label decisions
   - claims: claim text, evidence URL, allowed wording, risk level
   - creative: hooks, video/carousel variants, source assets, generated assets, provenance
   - posts: platform-native title, caption, hashtags, link, disclosure, publish status

3. Validate before generation, before publishing, and after analytics updates.

```bash
python3 {baseDir}/scripts/check_affiliate_campaign.py --campaign runs/campaign.json --repo-root . --out reports/campaign-qc.json
```

4. Render a readable plan for review.

```bash
python3 {baseDir}/scripts/render_affiliate_plan.py --campaign runs/campaign.json --out reports/campaign-plan.md
```

5. Export a supervised OpenClaw handoff for the target platform.

```bash
python3 {baseDir}/scripts/export_openclaw_handoff.py --campaign runs/campaign.json --platform pinterest --out runs/pinterest-openclaw-handoff.json --browser-profile pinterest-profile
```

## Workflow

### 1. Intake

Ask only for missing campaign-critical inputs:

- niche or product category
- target market/region
- product URL and affiliate program
- whether the operator personally used the product
- target platforms
- landing page preference: direct affiliate link, link-in-bio, owned landing page, or email capture
- generation stack: Claude/Higgsfield, Seedance, image model, editor, music source

If the user provides a PDF, video summary, prompt pack, or competitor workflow, extract reusable principles and risks. Do not copy long prompt text into the skill, repo, or public output unless the user owns it and explicitly requests private use.

### 2. Offer Gate

Score products before creative work:

- visual demonstration potential
- clear problem and non-deceptive benefit
- commission economics
- rights to use product imagery and brand names
- claim evidence burden
- platform restrictions
- audience trust risk
- refund or complaint risk

Prefer low-claim visual products for early tests: home tools, desk accessories, camera gear, bags, organizers, creator tools, kitchen workflow products, and software with clear demos.

Treat these as high-risk until manually reviewed: supplements, skincare with medicinal claims, sleep/anxiety claims, weight loss, finance, legal, medicine, baby products, safety equipment, gambling, crypto, and "make money" offers.

### 3. Creative Pack

Create two layers:

- `strategy`: hook angle, audience, promise boundary, evidence, disclosure, CTA, platform
- `generation`: shot list, aspect ratio, duration, reference assets, product visibility, on-screen disclosure, caption/disclosure, provenance fields

For Claude/Higgsfield:

- Use product references only when rights are clear.
- Ask for exact product text to be verified after generation; generated packaging text can hallucinate.
- Use natural demos and problem-solution storytelling without pretending the generated actor is the operator.
- Keep "AI-generated demonstration" notes in provenance when useful.

For carousels:

- Make slide 1 a problem or curiosity hook.
- Make slide 2 educational context.
- Make slide 3 the routine, demo, or comparison.
- Make slide 4 the CTA plus disclosure.
- Keep text readable on mobile and avoid medical certainty.

### 4. Publish Handoff

Before OpenClaw publishing:

- run `check_affiliate_campaign.py`
- confirm platform label requirements
- confirm caption includes disclosure before the link or call to action
- confirm generated asset path exists
- confirm affiliate URL belongs to an authorized site/account
- export the OpenClaw handoff bundle
- capture screenshots for upload, metadata review, final confirmation, and public view

Use `openclaw-youtube-tiktok-publisher` for YouTube/TikTok upload after the handoff exists. For Pinterest and Instagram, use this skill's handoff checklist until a dedicated publisher skill exists.

### 5. Analytics And Monetization

Track every post as an experiment:

- platform
- creative ID
- hook
- product
- published URL
- affiliate URL
- disclosure variant
- impressions
- saves
- clicks
- conversion count
- revenue
- cost of generation

Kill a campaign if it has no saves/clicks after a fair impression threshold, if compliance review blocks the product, or if generation costs exceed expected commission.

## References

Read `references/compliance-gates.md` before health, finance, supplement, skincare, or high-claim offers.

Read `references/platform-adapters.md` when packaging for Claude, Codex, OpenClaw, GitHub, or ClawHub.

Read `references/monetization.md` when turning the workflow into a paid offer, lead magnet, extension, template pack, or managed service.

## Bundled Scripts

- `scripts/init_affiliate_campaign.py`: create the campaign ledger skeleton.
- `scripts/check_affiliate_campaign.py`: validate disclosure, sensitive-category risk, claim evidence, fake testimonials, generated asset rights, and publish readiness.
- `scripts/render_affiliate_plan.py`: render a campaign plan and QC summary in markdown.
- `scripts/export_openclaw_handoff.py`: create a supervised browser-publishing handoff bundle for Pinterest, TikTok, YouTube, or Instagram.

## Done Criteria

The campaign is ready only when there is:

- a campaign ledger with offer, disclosure, claims, creative, posts, and provenance
- a QC report with no blocking errors
- creative assets with rights/provenance notes
- platform-specific captions and disclosures
- an OpenClaw handoff bundle if publishing is requested
- public URLs and screenshot evidence after publishing
