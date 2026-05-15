---
version: "alpha"
name: Affiliate Video Campaign Operator Landing System
description: Public conversion page for a compliance-first affiliate video skill and monetization pack.
colors:
  ink: "#151311"
  paper: "#FAF8F3"
  panel: "#FFFFFF"
  line: "#D8D0C3"
  muted: "#645E55"
  forest: "#1F5D50"
  amber: "#C47A2C"
  blue: "#315C93"
  red: "#A23D35"
typography:
  body:
    fontFamily: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif
    fontSize: 16px
    lineHeight: 1.55
    letterSpacing: 0
  h1:
    fontFamily: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif
    fontSize: 56px
    fontWeight: 790
    lineHeight: 1.02
    letterSpacing: 0
rounded:
  sm: 4px
  md: 8px
  lg: 12px
spacing:
  page: 24px
  section: 72px
components:
  button-primary:
    backgroundColor: "{colors.forest}"
    textColor: "#FFFFFF"
    rounded: "{rounded.md}"
  button-secondary:
    backgroundColor: "#FFFFFF"
    textColor: "{colors.ink}"
    borderColor: "{colors.line}"
    rounded: "{rounded.md}"
---

## Overview

The landing page should feel like an operator workbench, not a generic AI product. The visual signature is receipts, ledgers, check statuses, and channel handoffs.

## Layout

- First viewport must show the product name, the concrete job, and a real-looking campaign receipt panel.
- Use full-width sections with constrained inner content.
- Use cards only for pricing tiers, included assets, and receipt examples.
- Avoid nested cards and generic gradient hero art.

## Copy Rules

- Do not promise revenue, virality, approval, rankings, compliance guarantee, or platform safety.
- Make the free path visible before paid offers.
- Paid offers are framed as templates and setup help, not guaranteed results.
- Every affiliate monetization statement must mention disclosure and claim evidence.

## Components

- Receipt panels use compact rows and pass/review/block status pills.
- Pricing cards use 8px radius and no decorative bloat.
- CTA buttons are explicit: `Download free skill`, `Buy Pro Pack`, `Book setup review`.
