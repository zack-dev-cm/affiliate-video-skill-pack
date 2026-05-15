#!/usr/bin/env python3
"""Export a supervised OpenClaw publishing handoff bundle."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit(f"expected JSON object in {path}")
    return payload


def rel_or_name(path_text: str, root: Path) -> str:
    if not path_text:
        return ""
    path = Path(path_text).expanduser()
    if path.is_absolute():
        try:
            return str(path.relative_to(root))
        except ValueError:
            return path.name
    return path_text


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--campaign", required=True, help="Campaign ledger JSON.")
    parser.add_argument("--platform", required=True, choices=["pinterest", "tiktok", "youtube", "instagram"], help="Target platform.")
    parser.add_argument("--out", required=True, help="Output handoff JSON.")
    parser.add_argument("--browser-profile", required=True, help="Logged-in OpenClaw browser profile.")
    parser.add_argument("--asset-path", default="", help="Override asset path.")
    parser.add_argument("--publish-mode", default="draft", choices=["draft", "schedule", "publish"], help="Requested publish mode.")
    args = parser.parse_args()

    campaign_path = Path(args.campaign).expanduser().resolve()
    root = campaign_path.parent
    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    payload = load_json(campaign_path)
    campaign = payload.get("campaign") or {}
    offer = payload.get("offer") or {}
    disclosure = payload.get("disclosure") or {}
    posts = payload.get("posts") or {}
    post = posts.get(args.platform) or {}
    if not isinstance(post, dict):
        raise SystemExit(f"post for {args.platform} must be an object")

    asset_path = args.asset_path.strip() or str(post.get("asset_path") or "").strip()
    affiliate_url = str(post.get("affiliate_url") or offer.get("affiliate_url") or "").strip()
    short_disclosure = str(post.get("disclosure") or disclosure.get("short") or "").strip()
    caption = str(post.get("caption") or "").strip()
    if short_disclosure and short_disclosure.lower() not in caption.lower():
        caption = f"{short_disclosure}\n\n{caption}".strip()

    handoff = {
        "schema_version": "1.0",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "platform": args.platform,
        "source_campaign_bundle": campaign_path.name,
        "run": {
            "browser_profile": args.browser_profile,
            "publish_mode": args.publish_mode,
            "requires_supervision": True,
            "pause_on": [
                "captcha",
                "2fa",
                "account_recovery",
                "policy_warning",
                "billing",
                "copyright_dispute",
                "final_publish_confirmation",
            ],
        },
        "campaign": {
            "title": campaign.get("title") or "",
            "owner": campaign.get("owner") or "",
            "region": campaign.get("region") or "",
            "niche": campaign.get("niche") or "",
        },
        "offer": {
            "product_name": offer.get("product_name") or "",
            "merchant": offer.get("merchant") or "",
            "affiliate_program": offer.get("affiliate_program") or "",
            "affiliate_url": affiliate_url,
        },
        "content": {
            "title": post.get("title") or campaign.get("title") or "",
            "caption": caption,
            "hashtags": post.get("hashtags") or [],
            "disclosure": short_disclosure,
            "asset_path": rel_or_name(asset_path, root),
            "landing_page_url": campaign.get("landing_page_url") or "",
        },
        "platform_labels": disclosure.get("platform_labels") or {},
        "evidence_to_capture": [
            "upload screen",
            "metadata/disclosure review",
            "affiliate link or destination preview",
            "final confirmation screen",
            "published public URL or draft URL",
        ],
        "operator_notes": [
            "Run the campaign QC checker before publishing.",
            "Use native commercial-content or paid-partnership labels when required.",
            "Do not publish if platform shows a policy warning that is not understood.",
            "Record screenshots and final URL back into the campaign ledger.",
        ],
        "assets": {
            "extra_files": [campaign_path.name],
        },
    }

    out_path.write_text(json.dumps(handoff, indent=2) + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
