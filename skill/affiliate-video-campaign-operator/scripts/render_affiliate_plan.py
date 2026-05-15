#!/usr/bin/env python3
"""Render a readable affiliate campaign plan."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit(f"expected JSON object in {path}")
    return payload


def as_list(values: Any) -> list[str]:
    if not isinstance(values, list):
        return []
    return [str(value).strip() for value in values if str(value).strip()]


def line(label: str, value: Any) -> str:
    text = "" if value is None else str(value).strip()
    return f"- **{label}:** {text or 'TBD'}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--campaign", required=True, help="Campaign ledger JSON.")
    parser.add_argument("--qc", default="", help="Optional QC report JSON.")
    parser.add_argument("--out", required=True, help="Output markdown plan.")
    args = parser.parse_args()

    campaign_path = Path(args.campaign).expanduser().resolve()
    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = load_json(campaign_path)

    campaign = payload.get("campaign") or {}
    offer = payload.get("offer") or {}
    disclosure = payload.get("disclosure") or {}
    claims = payload.get("claims") or []
    creative = payload.get("creative") or {}
    posts = payload.get("posts") or {}
    analytics = payload.get("analytics") or {}

    qc_payload: dict[str, Any] | None = None
    if args.qc:
        qc_payload = load_json(Path(args.qc).expanduser().resolve())

    lines: list[str] = []
    lines.append(f"# {campaign.get('title') or 'Affiliate Campaign'}")
    lines.append("")
    lines.append("## Campaign")
    lines.append(line("Owner", campaign.get("owner")))
    lines.append(line("Niche", campaign.get("niche")))
    lines.append(line("Region", campaign.get("region")))
    lines.append(line("Platforms", ", ".join(as_list(campaign.get("target_platforms")))))
    lines.append(line("Landing page", campaign.get("landing_page_url")))
    lines.append("")

    lines.append("## Offer")
    lines.append(line("Product", offer.get("product_name")))
    lines.append(line("Category", offer.get("product_category")))
    lines.append(line("Merchant", offer.get("merchant")))
    lines.append(line("Affiliate program", offer.get("affiliate_program")))
    lines.append(line("Commission", offer.get("commission_note")))
    lines.append(line("Personal use", offer.get("personal_use")))
    lines.append(line("Rights note", offer.get("rights_note")))
    lines.append("")

    lines.append("## Disclosure")
    lines.append(line("Short", disclosure.get("short")))
    lines.append(line("Long", disclosure.get("long")))
    lines.append(line("Amazon Associate", disclosure.get("amazon_associate_statement")))
    lines.append("")

    lines.append("## Claims")
    if claims:
        for index, claim in enumerate(claims, start=1):
            if not isinstance(claim, dict):
                continue
            lines.append(f"{index}. {claim.get('claim') or 'TBD'}")
            lines.append(f"   Evidence: {claim.get('evidence_url') or claim.get('evidence_note') or 'TBD'}")
            if claim.get("allowed_wording"):
                lines.append(f"   Allowed wording: {claim.get('allowed_wording')}")
    else:
        lines.append("- TBD")
    lines.append("")

    strategy = creative.get("strategy") or {}
    lines.append("## Creative")
    lines.append(line("Audience", strategy.get("audience")))
    lines.append(line("Promise boundary", strategy.get("promise_boundary")))
    lines.append(line("CTA", strategy.get("cta")))
    hooks = as_list(creative.get("hooks"))
    lines.append(line("Hooks", "; ".join(hooks[:5])))
    lines.append(line("Generated assets", len(creative.get("generated_assets") or [])))
    lines.append("")

    lines.append("## Posts")
    if posts:
        for platform, post in posts.items():
            if not isinstance(post, dict):
                continue
            lines.append(f"### {platform}")
            lines.append(line("Title", post.get("title")))
            lines.append(line("Status", post.get("status")))
            lines.append(line("Disclosure", post.get("disclosure")))
            lines.append(line("Published URL", post.get("published_url")))
            lines.append("")
    else:
        lines.append("- TBD")
        lines.append("")

    totals = analytics.get("totals") or {}
    lines.append("## Analytics")
    lines.append(line("Impressions", totals.get("impressions")))
    lines.append(line("Clicks", totals.get("clicks")))
    lines.append(line("Conversions", totals.get("conversions")))
    lines.append(line("Revenue USD", totals.get("revenue_usd")))
    lines.append(line("Generation cost USD", totals.get("generation_cost_usd")))
    lines.append("")

    if qc_payload:
        lines.append("## QC")
        lines.append(line("Status", qc_payload.get("status")))
        for bucket_name in ("errors", "warnings"):
            bucket = qc_payload.get(bucket_name) or []
            if bucket:
                lines.append(f"### {bucket_name.title()}")
                for item in bucket:
                    lines.append(f"- {item.get('kind')}: {item.get('message')}")
        lines.append("")

    out_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
