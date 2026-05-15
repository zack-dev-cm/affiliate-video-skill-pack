# Critical Review: YouTube Skill Foundry

Date: 2026-05-15

## Blunt Verdict

The idea is promising, but the current plan is still too broad. The strongest product is not "tracking high-value YouTube videos." The strongest product is:

> Convert one operator-approved video transcript or note set into a public-safe, installable skill with a source receipt.

Tracking should come after the conversion artifact proves useful.

## What Was Good In The Previous Plan

- It correctly blocks transcript scraping as the default ingestion path.
- It names concrete outputs: `summary.md`, `workflow.yaml`, `SKILL.md`, and `public-safety.json`.
- It treats copied prompts, full transcripts, private videos, and paywalled content as unsafe.
- It has a real share moment: a long tutorial becomes an installable workflow.
- It creates a natural monetization ladder: free converter, paid pack, setup review, creator package.

## What Was Weak Or Under-Specified

### 1. "High-value video tracking" Is Too Vague

The scoring model is plausible, but not yet calibrated. Without a dataset of 20-50 reviewed videos, a score like `85/100` is just an opinion.

Fix:

- Start with a small labeled corpus:
  - 10 videos that clearly should become skills,
  - 10 videos that should only become summaries,
  - 10 videos that should be ignored.
- Tune the score after comparing against real conversion quality.

### 2. Transcript Acquisition Is The Real Constraint

The plan correctly says not to scrape captions, but the UX still needs to make this constraint unavoidable.

Fix:

- Every source bundle must declare one of:
  - `manual_notes`,
  - `manual_transcript`,
  - `creator_owned_oauth_caption`,
  - `licensed_transcript`,
  - `metadata_only`.
- The skill-drafting script must block when `metadata_only` is used.

### 3. The First MVP Should Not Use The YouTube API Yet

YouTube metadata collection is useful later, but it adds API keys, quota, retries, and policy surface before the core artifact is proven.

Fix:

- MVP command should accept manual metadata:

```bash
python3 scripts/init_video_to_skill_bundle.py \
  --url "https://youtube.com/watch?v=..." \
  --title "Video title" \
  --channel "Channel name" \
  --transcript-file private/transcript.txt \
  --out runs/source-bundle.json
```

Add YouTube Data API collection only after the first 3 manual conversions produce useful skills.

### 4. "Skill Suite" Is Premature

Three skills sound clean, but they fragment the workflow too early.

Fix:

Build one skill first:

- `youtube-skill-foundry`

It should include:

- source intake,
- source safety checks,
- summary rendering,
- workflow extraction,
- skill draft generation,
- public-safety review.

Split into separate skills only after repeated use exposes separate operator roles.

### 5. Monetization Needs A Stronger Trust Artifact

A $49 pack is plausible, but not before there are public examples.

Fix:

Before selling:

- publish 3 example conversions,
- include before/after artifacts,
- show the source receipt,
- show the generated `SKILL.md`,
- show the public-safety review.

### 6. The Plan Needs A Better "No Copying" Test

"Do not copy prompts" is a policy statement, not a test.

Fix:

Add a checker that flags:

- long verbatim chunks from transcript,
- phrases like "exact prompt from the video",
- copied paid-template language,
- missing attribution,
- missing source mode,
- skill with no original workflow abstraction.

## Recommended MVP

Build this first:

```text
youtube-skill-foundry/
  skill/youtube-skill-foundry/SKILL.md
  scripts/init_video_to_skill_bundle.py
  scripts/check_source_safety.py
  scripts/render_video_summary.py
  scripts/draft_workflow_yaml.py
  scripts/draft_skill_readme.py
  scripts/check_public_safety.py
  tests/
```

MVP input:

- YouTube URL,
- video title,
- channel name,
- transcript or notes file,
- source mode,
- rights note,
- target agent: Claude, Codex, OpenClaw.

MVP output:

- `runs/source-bundle.json`,
- `reports/summary.md`,
- `reports/workflow.yaml`,
- `skill/<draft-name>/SKILL.md`,
- `reports/public-safety.json`.

## Extension Candidates

### 1. YouTube Skill Receipt

Priority: highest.

Browser-native reason:

- It captures current YouTube page context, timestamped notes, selected text, and source receipt fields while the operator is watching.

MVP:

- active tab only,
- button: `Create Source Receipt`,
- fields: URL, title, channel, current timestamp, operator notes, source mode, rights note,
- export JSON to local file or clipboard.

Do not:

- scrape captions,
- download video/audio,
- claim endorsement by YouTube or creators,
- auto-publish skills.

Best landing:

- `youtube-skill-receipt.getgeofix.xyz`
- Headline: `Turn a YouTube tutorial into a source-safe skill receipt.`
- CTA: `Install free extension`

Monetization:

- free extension,
- $49 Skill Foundry Pack,
- $299 video-to-skill setup review.

### 2. Transcript-To-Skill Clipboard

Priority: second.

Browser-native reason:

- Captures selected transcript text or notes from any page and wraps it in a source-safety receipt.

MVP:

- selection capture,
- source mode picker,
- attribution fields,
- export bundle.

Why it may beat YouTube-specific:

- lower platform risk,
- works with creator-owned docs, blog posts, docs, and transcripts,
- easier CWS review.

Best landing:

- `transcript-to-skill.getgeofix.xyz`
- Headline: `Package allowed transcripts into agent skills without losing attribution.`

### 3. Skill Draft Reviewer

Priority: third.

Browser-native reason:

- Reviews a local or pasted `SKILL.md` against public-safety gates.

MVP:

- paste skill text,
- flag copied-transcript risk,
- flag missing source receipt,
- export review JSON.

This could also be a web tool, so extension priority is lower unless it integrates with GitHub pages or local files.

Best landing:

- `skill-draft-reviewer.getgeofix.xyz`

### 4. Video Watchlist Radar

Priority: low until conversion works.

This is more of a backend/web app than a Chrome extension. Tracking videos through an extension is weak because users do not need browser state for scheduled metadata collection.

Build only after:

- 5 useful conversions,
- at least 2 users ask for watchlists,
- YouTube API quota/key path is stable.

Best landing:

- `skill-radar.getgeofix.xyz`

## Landing Page Portfolio

### Main Product Landing

`youtube-skill-foundry.getgeofix.xyz`

Purpose:

- service overview,
- free MVP,
- examples,
- paid setup path.

Required sections:

- hero with real source receipt and skill output,
- 3-step workflow,
- source safety boundary,
- example gallery,
- pricing,
- FAQ,
- no-affiliation note.

### Extension Landing

`youtube-skill-receipt.getgeofix.xyz`

Purpose:

- Chrome Web Store reviewer and user landing.

Required pages:

- `/`
- `/privacy`
- `/support`
- `/reviewer`
- `/source-safety`

### Example Gallery

`youtube-skill-foundry.getgeofix.xyz/examples`

Purpose:

- prove the service creates useful artifacts.

Each example should show:

- video title and URL,
- rights/source mode,
- summary,
- workflow YAML excerpt,
- generated skill link,
- public-safety status.

### Paid Pack Landing

`youtube-skill-foundry.getgeofix.xyz/pro`

Purpose:

- sell templates after proof exists.

Offer:

- $49 Skill Foundry Pack,
- $299 setup review,
- $799 creator package.

Do not make this primary until examples exist.

## Recommended Build Order

1. Create `youtube-skill-foundry` repo.
2. Build manual transcript-to-skill pipeline.
3. Convert one safe video into a skill.
4. Publish landing with one example.
5. Build `YouTube Skill Receipt` extension.
6. Publish Chrome extension as free receipt capture tool.
7. Add Pro Pack only after 3 public examples.
8. Add YouTube API watchlist only after conversion proves valuable.

## CWS Extension MVP Spec: YouTube Skill Receipt

Permissions:

- `activeTab`
- `storage`
- `downloads` only if direct JSON file export is required; otherwise use clipboard/copy first.

Host permissions:

- Prefer none for MVP.
- Use active tab and user click to read current tab URL/title.

UI:

- Popup or side panel.
- Fields:
  - video URL,
  - title,
  - channel,
  - timestamp,
  - source mode,
  - rights note,
  - operator notes,
  - selected text, optional.
- Buttons:
  - `Copy receipt JSON`,
  - `Copy Codex command`,
  - `Clear`.

Output:

```json
{
  "source_type": "youtube_video",
  "source_mode": "manual_notes",
  "url": "",
  "title": "",
  "channel": "",
  "timestamp": "",
  "rights_note": "",
  "operator_notes": "",
  "allowed_use": "summarize and convert into original workflow",
  "forbidden_use": "do not republish transcript or copied prompts"
}
```

## Key Risks

1. It becomes a transcript-scraping tool.
   - Mitigation: do not build caption scraping; require operator source mode.

2. It produces shallow skills.
   - Mitigation: public-safety and workflow-depth checker.

3. It monetizes before proof.
   - Mitigation: examples first, checkout second.

4. CWS reviewers see it as a YouTube automation/downloader.
   - Mitigation: no download/video permissions, no caption scraping, no media claims, reviewer page explains receipt-only behavior.

5. Watchlist becomes noisy.
   - Mitigation: manual-first, then small curated channel list, then API scoring.

## What To Improve In The Existing Affiliate Video Skill Pack

- Add a link from the current landing to the future YouTube Skill Foundry as an "upstream idea source" only after a first demo exists.
- Do not blend affiliate-video compliance with YouTube-skill extraction in the same skill; keep them separate products.
- Reuse the checkout/terms/refund/deployment template from the current repo.
- Reuse the product-share gate and public-safety checker pattern.
- Keep the first YouTube Skill Foundry landing simpler than the affiliate-video landing: one artifact, one source receipt, one generated skill.

## Sources Checked

- YouTube API Services Terms: https://developers.google.com/youtube/terms/api-services-terms-of-service
- YouTube API Developer Policies: https://developers.google.com/youtube/terms/developer-policies
- YouTube Data API `search.list`: https://developers.google.com/youtube/v3/docs/search/list
- YouTube Data API `captions.download`: https://developers.google.com/youtube/v3/docs/captions/download
- Chrome Web Store Program Policies: https://developer.chrome.com/docs/webstore/program-policies
- Chrome Extensions `activeTab`: https://developer.chrome.com/docs/extensions/develop/concepts/activeTab
- Chrome Side Panel API: https://developer.chrome.com/docs/extensions/reference/api/sidePanel
