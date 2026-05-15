#!/usr/bin/env python3
"""Add a source or generated asset to an affiliate campaign ledger."""

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


def require_text(value: str, label: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise SystemExit(f"{label} must not be empty")
    return normalized


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--campaign", required=True, help="Campaign ledger JSON.")
    parser.add_argument("--kind", required=True, choices=["source", "generated"], help="Asset bucket.")
    parser.add_argument("--asset-id", required=True, help="Stable asset ID.")
    parser.add_argument("--path", required=True, help="Local path or URL.")
    parser.add_argument("--provider", default="", help="Generation/source provider.")
    parser.add_argument("--model", default="", help="Generation model.")
    parser.add_argument("--prompt-file", default="", help="Prompt file used to create this asset.")
    parser.add_argument("--rights-note", default="", help="Rights or license note.")
    parser.add_argument("--notes", default="", help="Review notes.")
    args = parser.parse_args()

    path = Path(args.campaign).expanduser().resolve()
    payload = load_json(path)
    creative = payload.setdefault("creative", {})
    if not isinstance(creative, dict):
        raise SystemExit("creative must be an object")
    bucket_name = "source_assets" if args.kind == "source" else "generated_assets"
    bucket = creative.setdefault(bucket_name, [])
    if not isinstance(bucket, list):
        raise SystemExit(f"{bucket_name} must be a list")

    asset_id = require_text(args.asset_id, "asset-id")
    asset = {
        "asset_id": asset_id,
        "path": require_text(args.path, "path"),
        "provider": args.provider.strip(),
        "model": args.model.strip(),
        "prompt_file": args.prompt_file.strip(),
        "rights_note": args.rights_note.strip(),
        "notes": args.notes.strip(),
    }

    for index, existing in enumerate(bucket):
        if isinstance(existing, dict) and str(existing.get("asset_id") or "") == asset_id:
            bucket[index] = asset
            break
    else:
        bucket.append(asset)

    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
