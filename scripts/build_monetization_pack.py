#!/usr/bin/env python3
"""Validate and package the Affiliate Video Launch Pack."""

from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACK_DIR = ROOT / "monetization" / "affiliate-video-pro-pack"
REQUIRED_FILES = [
    "offer.json",
    "templates/campaign-intake.md",
    "templates/offer-scorecard.md",
    "templates/claim-evidence-worksheet.md",
    "templates/platform-caption-matrix.md",
    "templates/openclaw-publish-checklist.md",
    "templates/experiment-tracker.csv",
    "examples/creator-desk-gear-example.json",
]


def validate_pack() -> dict[str, object]:
    missing = [item for item in REQUIRED_FILES if not (PACK_DIR / item).exists()]
    if missing:
        raise SystemExit(f"missing required pack files: {', '.join(missing)}")

    offer = json.loads((PACK_DIR / "offer.json").read_text(encoding="utf-8"))
    example = json.loads((PACK_DIR / "examples" / "creator-desk-gear-example.json").read_text(encoding="utf-8"))
    if offer.get("price_usd") != 0:
        raise SystemExit("offer.json price_usd must be 0 because this package is a public launch asset")
    if offer.get("status") != "free-public-pack":
        raise SystemExit("offer.json status must be free-public-pack")
    if "revenue" not in offer.get("positioning", {}).get("not_promised", []):
        raise SystemExit("offer.json must explicitly avoid revenue promises")
    if example.get("offer", {}).get("product_category") != "home office accessory":
        raise SystemExit("example campaign should remain low-risk creator desk gear")
    return offer


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(ROOT / "dist" / "affiliate-video-pro-pack.zip"), help="Output zip path.")
    args = parser.parse_args()

    offer = validate_pack()
    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if out_path.exists():
        out_path.unlink()

    with zipfile.ZipFile(out_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for item in REQUIRED_FILES:
            archive.write(PACK_DIR / item, arcname=f"affiliate-video-pro-pack/{item}")

    print(json.dumps({"out": str(out_path), "name": offer["name"], "files": len(REQUIRED_FILES)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
