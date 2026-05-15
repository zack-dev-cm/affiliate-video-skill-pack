# Platform Adapters

## Claude

Package the skill folder as a zip whose top-level directory contains `SKILL.md`:

```bash
cd skill
zip -r ../dist/affiliate-video-campaign-operator-claude.zip affiliate-video-campaign-operator
```

Claude can use the workflow as an uploaded skill. If Claude has local file/code execution, it can run the bundled scripts. Otherwise, ask it to produce JSON edits, review notes, and exact local commands for the operator to run. If it has a Higgsfield MCP connector, use it for creative drafts only after the campaign ledger has offer, disclosure, claim, and rights fields filled. Avoid "always allow" for paid generation unless the operator has set a spend limit and reviewed sensitive-claim gates.

Starter prompt:

```text
Use the Affiliate Video Campaign Operator skill. Create a campaign ledger for this product, ask only for missing campaign-critical fields, then prepare conservative creative notes and tell me which local validation command to run before generation.
```

## Codex

Install by copying the skill folder into the Codex skills directory:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skill/affiliate-video-campaign-operator "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Codex should run the bundled Python scripts for campaign creation, validation, report rendering, and handoff export. Keep affiliate IDs, private generated media, and account screenshots out of public repos.

Starter prompt:

```text
Use the affiliate-video-campaign-operator skill to create and validate a campaign ledger, then export an OpenClaw handoff for Pinterest.
```

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

Handoff command:

```bash
python3 skill/affiliate-video-campaign-operator/scripts/export_openclaw_handoff.py \
  --campaign runs/campaign.json \
  --platform youtube \
  --out runs/youtube-openclaw-handoff.json \
  --browser-profile youtube-profile
```

Give OpenClaw the exported JSON and a named logged-in browser profile. Do not ask OpenClaw to infer missing claims, disclosures, or affiliate URLs from browser state.

Supported post and handoff platforms are `pinterest`, `tiktok`, `youtube`, and `instagram`. Other platforms can be tracked manually in `campaign.target_platforms`, but these scripts cannot export OpenClaw handoffs for them.

## Grok And Generic Chat Agents

Do not assume Grok or another chat agent has a native skill installer. Treat this skill as a plain-text operating guide:

1. Attach or paste `SKILL.md`.
2. Attach `references/compliance-gates.md` and this file when platform or policy decisions matter.
3. Ask the agent for JSON edits, conservative caption options, claim wording, or review notes.
4. Run the Python scripts locally in this repo to validate and render final artifacts.

Starter prompt:

```text
Use the attached Affiliate Video Campaign Operator instructions. Do not invent product claims or fake personal experience. Ask for missing campaign fields, draft conservative creative notes, and tell me which local script command to run next.
```

Generic agents should not claim platform-native publishing, MCP access, or browser control unless that runtime actually provides those tools.

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
  --version 0.1.6 \
  --tags "affiliate,video,openclaw,claude,higgsfield,pinterest,tiktok,youtube,compliance" \
  --changelog "Add clear Claude, Codex, OpenClaw, Grok, and generic-agent usage instructions."
```

After publish, inspect the entry and moderation state before calling the release complete.

## Skill Combination

Use this skill first for affiliate strategy and compliance. Then:

- `agentic-video-production-publisher`: consistent characters, shot ledgers, music beat maps, video provenance.
- `openclaw-youtube-tiktok-publisher`: supervised YouTube/TikTok upload after this skill exports a handoff.
- `chrome-extension-cws-shipper`: build a browser extension that captures product pages, affiliate disclosures, and publish receipts.
- `design-md-ui-designer`: build landing pages, policy pages, and conversion visuals for owned funnels.
