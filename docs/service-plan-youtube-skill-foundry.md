# YouTube Skill Foundry Service Plan

Date: 2026-05-15

## One-Sentence Product

YouTube Skill Foundry tracks high-value public YouTube videos, turns operator-approved transcripts into concise summaries, extracts reusable workflow patterns, and packages original open-source Claude/Codex/OpenClaw skills plus paid implementation packs.

## Verdict

`Ship Free`, but only with a strict transcript/provenance boundary.

Do not build a transcript scraper. Start with official YouTube metadata and user-provided or creator-authorized transcripts. The first paid product should be a reviewed skill pack, not a SaaS dashboard.

## Target User

Primary user:

- AI operator who watches tutorials and wants reusable skills instead of notes.

Secondary users:

- creator who wants their own videos converted into downloadable skills,
- agency building internal playbooks from public tutorials,
- open-source maintainer packaging repeatable workflows from video research.

## Job To Be Done

When a valuable tutorial appears, the user wants:

- a short summary,
- a workflow extraction,
- a public-safe skill draft,
- a provenance record,
- a decision on whether to open-source, monetize, or discard it.

## What Counts As A High-Value Video

Score from 0 to 100:

- `topic_fit` 0-20: agent workflows, automation, AI video, affiliate ops, Chrome extensions, OpenClaw, Codex, Claude, Figma/Open Design, publishing, monetization.
- `execution_density` 0-20: video appears to include concrete steps, tools, prompts, or setup flows.
- `freshness` 0-15: new enough that timing matters.
- `traction_velocity` 0-15: views/comments relative to channel size and video age.
- `monetization_signal` 0-10: affiliate, template, service, course, extension, or productized workflow potential.
- `skillability` 0-15: can become a reusable agent workflow without copying proprietary content.
- `rights_safety` 0-5: public video, usable metadata, clear source attribution, no private/paywalled content.

Minimum thresholds:

- `watchlist`: 65+
- `manual transcript request`: 75+
- `skill draft`: 80+ and transcript/provenance available
- `monetization candidate`: 85+ and share trigger exists

## Compliance Boundary

Allowed:

- use YouTube Data API for public metadata and search,
- store video ID, title, channel, URL, publish date, thumbnail URL, view/comment statistics if available,
- summarize user-provided transcripts or creator-owned captions,
- quote only short excerpts when needed,
- create original skills that encode reusable procedures, not copied prompt packs.

Not allowed:

- scraping captions as the default ingestion path,
- downloading video/audio,
- reproducing full transcripts,
- publishing copied prompts, paid-course content, private community content, or creator assets,
- claiming endorsement by YouTube, a creator, or a brand.

Transcript modes:

1. `manual`: user pastes transcript or notes.
2. `creator-owned`: OAuth-authorized captions for the operator's own channel or client channel.
3. `licensed`: a vendor or creator permission explicitly allows transcript use.
4. `metadata-only`: no transcript; produce only a watchlist card and do not draft a skill.

## MVP Workflow

1. Track candidates.
   - Input: channel IDs, search queries, keyword watchlists, RSS feeds, or manual URLs.
   - Output: ranked watchlist JSON.

2. Gate for source safety.
   - Check public URL, source type, transcript mode, creator attribution, and no paywalled/private source.
   - Output: source receipt.

3. Summarize.
   - Create concise summary: promise, tools, setup steps, workflow, risks, monetization idea, missing evidence.
   - Output: `summary.md`.

4. Extract workflow.
   - Convert video into steps, inputs, outputs, decisions, tools, failure modes, and done criteria.
   - Output: `workflow.yaml`.

5. Draft skill.
   - Create original `SKILL.md` with concise metadata and workflow instructions.
   - Include scripts only when deterministic validation is useful.
   - Output: `skill/<skill-name>/SKILL.md`.

6. Review.
   - Product-share gate: first traffic source, trust reason, share moment, free MVP, kill criteria.
   - Skill QA: no copied transcript, no copied prompts, no unsupported claims, no private data.
   - Output: `review.json`.

7. Publish.
   - Free: GitHub + ClawHub skill.
   - Paid: implementation pack, checklist, template, or setup service.

## Proposed Skill Suite

### 1. youtube-skill-intelligence

Purpose:

- Track candidate YouTube videos and rank them for skill-conversion value.

Scripts:

- `track_youtube_candidates.py`
- `score_youtube_candidate.py`
- `render_watchlist.py`

Outputs:

- `watchlist.json`
- `watchlist.md`
- `source-receipts/*.json`

### 2. video-workflow-extractor

Purpose:

- Convert user-provided transcripts or notes into workflow specs.

Scripts:

- `init_video_source_bundle.py`
- `check_source_rights.py`
- `render_summary.py`
- `extract_workflow_yaml.py`

Outputs:

- `summary.md`
- `workflow.yaml`
- `source-receipt.json`

### 3. workflow-to-skill-packager

Purpose:

- Convert workflow specs into Claude/Codex/OpenClaw skill folders and release artifacts.

Scripts:

- `draft_skill_from_workflow.py`
- `check_skill_public_safety.py`
- `package_claude_skill.py`
- `render_clawhub_publish_command.py`

Outputs:

- `skill/<name>/SKILL.md`
- `dist/<name>-claude.zip`
- `review/public-safety.json`

## Architecture

```text
Watchlist sources
  -> YouTube metadata collector
  -> high-value scorer
  -> source rights gate
  -> transcript/notes intake
  -> summary generator
  -> workflow extractor
  -> skill packager
  -> public-safety review
  -> GitHub/ClawHub release
  -> monetization pack or setup service
```

Storage:

- SQLite for local MVP.
- JSON bundles for shareable artifacts.
- No raw full transcripts in public repos.
- Store provenance and short summaries; keep full transcript private unless rights allow sharing.

## Data Model

`video_candidate`:

- `video_id`
- `url`
- `title`
- `channel_id`
- `channel_title`
- `published_at`
- `collected_at`
- `topic_tags`
- `view_count`
- `comment_count`
- `duration`
- `source_mode`
- `high_value_score`
- `decision`

`source_receipt`:

- `video_id`
- `transcript_mode`
- `rights_note`
- `allowed_use`
- `forbidden_use`
- `attribution`
- `source_url`
- `operator_decision`

`skill_candidate`:

- `name`
- `description`
- `source_video_id`
- `workflow_summary`
- `public_safety_status`
- `monetization_status`
- `publish_targets`

## Product-Share Gate

| Gate | Score | Reason |
| --- | ---: | --- |
| First traffic source | 2 | Existing audience around Codex/OpenClaw/AI-video skills, GitHub/ClawHub release flow, and YouTube tutorial operators. |
| Trust reason | 2 | Open-source receipts, source-safety gates, no transcript scraping default, public skill QA. |
| Share moment | 2 | User gets a generated skill folder and can share the repo/release. |
| Free MVP plan | 2 | Free watchlist + one manual transcript-to-skill conversion. |
| Kill criteria | 2 | Concrete 7/30/60-day install and conversion targets. |

Verdict:

- `Ship Free`

Share trigger:

- User feels: they turned a 40-minute video into a reusable operator workflow.
- User has: a summary, workflow YAML, and installable skill.
- User shares with: another AI operator or creator.
- User says: "This turns useful YouTube tutorials into skills instead of another notes graveyard."
- User gains: credibility and a reusable workflow artifact.

## Monetization Ladder

Free:

- public watchlist schema,
- one manual transcript-to-skill example,
- source-safety checker,
- skill packaging scripts.

Paid pack, $49:

- high-value scoring templates,
- channel watchlist templates,
- workflow extraction checklist,
- skill QA checklist,
- ClawHub/GitHub release templates.

Setup review, $299:

- convert one operator-supplied video transcript into a reviewed skill draft.

Creator package, $799:

- convert 3 creator-owned videos into skill pack + landing page + release assets.

Monthly intelligence, $500-$2,500:

- weekly watchlist, summaries, skill candidates, and monetization recommendations.

Avoid:

- selling copied transcripts,
- promising virality, revenue, or ranking,
- selling skills derived from paid/private videos without explicit rights.

## Chrome Extension Variant

Later extension:

- Adds "Send to Skill Foundry" button on YouTube watch pages.
- Captures URL, title, channel, timestamped notes, and operator-selected transcript text.
- Exports source receipt JSON.
- Does not bypass YouTube caption restrictions.

This extension can become the paid acquisition channel because the share moment is visible while the user is watching a video.

## 30/60-Day Plan

Days 1-7:

- Create repo `youtube-skill-foundry`.
- Implement local JSON bundle schema and manual URL intake.
- Convert 3 public videos using manual notes/transcripts.
- Publish 1 open-source skill from a low-risk video.

Days 8-30:

- Add YouTube Data API metadata collector.
- Add high-value scoring and source receipts.
- Publish 3 skills and 3 summaries.
- Launch landing page with free MVP and paid setup review waitlist.

Days 31-60:

- Add Chrome extension prototype for source receipt capture.
- Publish Pro Pack.
- Offer 5 setup reviews manually.
- Decide whether to build dashboard based on demand.

Kill criteria:

- Day 7: no one cares about the demo skill or summary artifact.
- Day 30: fewer than 5 users/stars/installs and no setup requests.
- Day 60: no repeat use, no creator interest, and no paid setup intent.

## Smallest Next Experiment

Build a single command:

```bash
python3 scripts/init_video_to_skill_bundle.py \
  --url "https://youtube.com/watch?v=..." \
  --transcript-file private/transcript.txt \
  --out runs/source-bundle.json
```

Then produce:

- `summary.md`
- `workflow.yaml`
- `skill/<draft>/SKILL.md`
- `review/public-safety.json`

Do this for one video where the transcript is operator-provided. If the result is useful enough to install as a skill, then build the YouTube metadata tracker.

## Open Questions

- Which first category wins: AI video generation, affiliate marketing, Chrome extensions, or OpenClaw publishing?
- Should the first public skill be created under this repo or a new `youtube-skill-foundry` repo?
- Which checkout provider will handle the paid pack?
- Does the operator have YouTube API credentials available for metadata collection?
