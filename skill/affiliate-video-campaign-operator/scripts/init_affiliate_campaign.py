#!/usr/bin/env python3
"""Create an affiliate video campaign ledger."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def require_text(value: str, label: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise SystemExit(f"{label} must not be empty")
    return normalized


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, help="Output JSON campaign ledger.")
    parser.add_argument("--title", required=True, help="Campaign title.")
    parser.add_argument("--owner", default="", help="Owner or publisher handle.")
    parser.add_argument("--niche", default="", help="Campaign niche or category.")
    parser.add_argument("--region", default="US", help="Target region.")
    parser.add_argument("--product-name", default="", help="Product name.")
    parser.add_argument("--product-category", default="", help="Product category.")
    parser.add_argument("--merchant", default="", help="Merchant or affiliate network.")
    parser.add_argument("--product-url", default="", help="Public product URL.")
    parser.add_argument("--affiliate-url", default="", help="Affiliate URL or placeholder.")
    parser.add_argument("--affiliate-program", default="", help="Affiliate program name.")
    parser.add_argument("--commission-note", default="", help="Commission note or expected payout.")
    parser.add_argument("--landing-page-url", default="", help="Owned landing page URL, if any.")
    parser.add_argument("--platform", action="append", default=[], help="Repeatable target platform.")
    parser.add_argument("--personal-use", action="store_true", help="Operator has personally used the product.")
    parser.add_argument("--short-disclosure", default="", help="Short disclosure shown near links.")
    parser.add_argument("--amazon-associate-statement", default="", help="Amazon Associate identity statement.")
    args = parser.parse_args()

    platforms = args.platform or ["pinterest"]
    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "schema_version": "1.0",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "campaign": {
            "title": require_text(args.title, "title"),
            "owner": args.owner.strip(),
            "niche": args.niche.strip(),
            "region": args.region.strip() or "US",
            "target_platforms": platforms,
            "landing_page_url": args.landing_page_url.strip(),
            "thesis": "",
            "kill_criteria": {
                "min_impressions": 1000,
                "min_clicks": 10,
                "max_generation_cost_usd": 25.0,
            },
        },
        "offer": {
            "product_name": args.product_name.strip(),
            "product_category": args.product_category.strip(),
            "merchant": args.merchant.strip(),
            "product_url": args.product_url.strip(),
            "affiliate_url": args.affiliate_url.strip(),
            "affiliate_program": args.affiliate_program.strip(),
            "commission_note": args.commission_note.strip(),
            "rights_note": "",
            "personal_use": bool(args.personal_use),
            "source_snapshots": [],
        },
        "disclosure": {
            "short": args.short_disclosure.strip(),
            "long": "",
            "amazon_associate_statement": args.amazon_associate_statement.strip(),
            "video_overlay_required": True,
            "platform_labels": {
                "pinterest_paid_partnership": False,
                "tiktok_commercial_content": False,
                "youtube_paid_promotion": False,
                "instagram_paid_partnership": False,
            },
        },
        "claims": [],
        "creative": {
            "strategy": {
                "audience": "",
                "promise_boundary": "",
                "cta": "",
                "voice": "helpful",
            },
            "hooks": [],
            "variants": [],
            "source_assets": [],
            "generated_assets": [],
            "music": {
                "source": "",
                "rights_note": "",
            },
        },
        "posts": {
            platform: {
                "platform": platform,
                "title": "",
                "caption": "",
                "hashtags": [],
                "affiliate_url": args.affiliate_url.strip(),
                "disclosure": args.short_disclosure.strip(),
                "asset_path": "",
                "status": "planned",
                "published_url": "",
                "evidence_screenshot": "",
            }
            for platform in platforms
        },
        "analytics": {
            "experiments": [],
            "totals": {
                "impressions": 0,
                "clicks": 0,
                "conversions": 0,
                "revenue_usd": 0.0,
                "generation_cost_usd": 0.0,
            },
        },
        "qc": {
            "status": "planned",
            "findings": [],
            "operator_decisions": [],
        },
    }

    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
