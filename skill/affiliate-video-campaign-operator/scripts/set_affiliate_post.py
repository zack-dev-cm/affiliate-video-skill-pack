#!/usr/bin/env python3
"""Create or update platform post metadata in an affiliate campaign ledger."""

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


def split_tags(values: list[str]) -> list[str]:
    tags: list[str] = []
    for value in values:
        for item in value.split(","):
            normalized = item.strip()
            if not normalized:
                continue
            if not normalized.startswith("#"):
                normalized = f"#{normalized}"
            tags.append(normalized)
    return tags


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--campaign", required=True, help="Campaign ledger JSON.")
    parser.add_argument("--platform", required=True, choices=["pinterest", "tiktok", "youtube", "instagram"], help="Target platform.")
    parser.add_argument("--title", default=None, help="Platform post title.")
    parser.add_argument("--caption", default=None, help="Caption/description.")
    parser.add_argument("--hashtag", action="append", default=None, help="Repeatable hashtag or comma list.")
    parser.add_argument("--affiliate-url", default=None, help="Post destination URL.")
    parser.add_argument("--disclosure", default=None, help="Post-level disclosure.")
    parser.add_argument("--asset-path", default=None, help="Creative asset path.")
    parser.add_argument("--status", default=None, choices=["planned", "ready", "scheduled", "published"], help="Post status.")
    parser.add_argument("--published-url", default=None, help="Published post URL.")
    parser.add_argument("--evidence-screenshot", default=None, help="Publish evidence screenshot path.")
    args = parser.parse_args()

    path = Path(args.campaign).expanduser().resolve()
    payload = load_json(path)
    posts = payload.setdefault("posts", {})
    if not isinstance(posts, dict):
        raise SystemExit("posts must be an object")
    post = posts.setdefault(
        args.platform,
        {
            "platform": args.platform,
            "title": "",
            "caption": "",
            "hashtags": [],
            "affiliate_url": "",
            "disclosure": "",
            "asset_path": "",
            "status": "planned",
            "published_url": "",
            "evidence_screenshot": "",
        },
    )
    if not isinstance(post, dict):
        raise SystemExit(f"post for {args.platform} must be an object")

    updates = {
        "title": args.title,
        "caption": args.caption,
        "affiliate_url": args.affiliate_url,
        "disclosure": args.disclosure,
        "asset_path": args.asset_path,
        "status": args.status,
        "published_url": args.published_url,
        "evidence_screenshot": args.evidence_screenshot,
    }
    for key, value in updates.items():
        if value is not None:
            post[key] = value.strip()
    if args.hashtag is not None:
        post["hashtags"] = split_tags(args.hashtag)

    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
