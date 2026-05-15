# Agent Runtime Usage Audit 2026-05-15

Auditor: GPT-5.5 xhigh subagent.

## Verdict

The usage instructions are now explicit enough for Claude, Codex, OpenClaw, Grok, and generic chat agents.

## Issues Fixed

- README quick start now uses a low-risk desk-gear campaign instead of a supplement/Amazon example that would block QC.
- README quick start now creates a placeholder asset and sets `--asset-path` before marking a post `ready`.
- Claude instructions now distinguish between setups with local file/code execution and chat-only setups.
- Grok and generic-agent usage is documented as a plain-text workflow, without claiming a native installer.
- Supported post and handoff platforms are documented next to the commands: `pinterest`, `tiktok`, `youtube`, and `instagram`.
- Related publishing/video/design skills are described as optional, with manual handoff fallback.
- ClawHub publish commands and agent metadata now use version `0.1.6`.

## Regression Tests Added

- Runtime documentation must mention Claude, Codex, OpenClaw, Grok, generic agents, and the Grok/generic no-native-installer caveat.
- README happy-path commands are executed in a temp directory and must not produce a `BLOCK` QC status.
- Claude zip packaging is rebuilt in test and must contain current `SKILL.md`, `agents/openai.yaml`, and `references/platform-adapters.md`.
