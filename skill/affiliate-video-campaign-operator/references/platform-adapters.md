# Platform Adapters

## Claude

Package the skill folder as a zip whose top-level directory contains `SKILL.md`:

```bash
cd skill
zip -r ../dist/affiliate-video-campaign-operator-claude.zip affiliate-video-campaign-operator
```

Claude can use the workflow directly. If it has a Higgsfield MCP connector, use it for creative drafts only after the campaign ledger has offer, disclosure, claim, and rights fields filled. Avoid "always allow" for paid generation unless the operator has set a spend limit and reviewed sensitive-claim gates.

## Codex

Install by copying the skill folder into the Codex skills directory:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skill/affiliate-video-campaign-operator "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Codex should run the bundled Python scripts for campaign creation, validation, report rendering, and handoff export. Keep affiliate IDs, private generated media, and account screenshots out of public repos.

## OpenClaw

Use OpenClaw for logged-in UI operations only:

- Pinterest pin creation and paid partnership label checks
- YouTube Studio Shorts upload with paid promotion checkbox
- TikTok upload with commercial content disclosure
- Instagram mobile/web publishing steps where available
- screenshot evidence capture

Rules:

- Require a named browser profile already logged into the target account.
- Pause on CAPTCHA, 2FA, account recovery, unexpected policy warnings, billing, copyright disputes, or final publish confirmation when not pre-approved.
- Never store cookies, passwords, passkeys, or account sessions in the campaign bundle.
- Record public URLs and screenshots back into the campaign ledger after publishing.

## GitHub

Public repo shape:

- `README.md`
- `LICENSE`
- `skill/affiliate-video-campaign-operator/SKILL.md`
- `skill/affiliate-video-campaign-operator/agents/openai.yaml`
- bundled scripts and references
- tests

Do not publish private prompts, copied third-party prompt packs, raw product scraping dumps, browser profiles, tokens, affiliate IDs, or private generated assets.

## ClawHub

Publish the skill folder:

```bash
clawhub publish "$PWD/skill/affiliate-video-campaign-operator" \
  --slug affiliate-video-campaign-operator \
  --name "Affiliate Video Campaign Operator" \
  --version 0.1.1 \
  --tags "affiliate,video,openclaw,claude,higgsfield,pinterest,tiktok,youtube,compliance" \
  --changelog "Add campaign mutation scripts, stricter disclosure checks, and published-post receipt validation."
```

After publish, inspect the entry and moderation state before calling the release complete.

## Skill Combination

Use this skill first for affiliate strategy and compliance. Then:

- `agentic-video-production-publisher`: consistent characters, shot ledgers, music beat maps, video provenance.
- `openclaw-youtube-tiktok-publisher`: supervised YouTube/TikTok upload after this skill exports a handoff.
- `chrome-extension-cws-shipper`: build a browser extension that captures product pages, affiliate disclosures, and publish receipts.
- `design-md-ui-designer`: build landing pages, policy pages, and conversion visuals for owned funnels.
