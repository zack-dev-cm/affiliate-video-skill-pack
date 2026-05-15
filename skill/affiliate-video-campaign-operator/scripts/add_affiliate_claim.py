#!/usr/bin/env python3
"""Add a claim to an affiliate campaign ledger."""

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
    parser.add_argument("--claim", required=True, help="Claim text.")
    parser.add_argument("--evidence-url", default="", help="Evidence URL.")
    parser.add_argument("--evidence-note", default="", help="Evidence note when no URL exists.")
    parser.add_argument("--allowed-wording", default="", help="Safer approved wording.")
    parser.add_argument("--risk", default="medium", choices=["low", "medium", "high"], help="Claim risk level.")
    parser.add_argument("--replace", type=int, default=0, help="Replace 1-based claim index instead of appending.")
    args = parser.parse_args()

    path = Path(args.campaign).expanduser().resolve()
    payload = load_json(path)
    claims = payload.setdefault("claims", [])
    if not isinstance(claims, list):
        raise SystemExit("claims must be a list")

    claim = {
        "claim": require_text(args.claim, "claim"),
        "risk": args.risk,
        "evidence_url": args.evidence_url.strip(),
        "evidence_note": args.evidence_note.strip(),
        "allowed_wording": args.allowed_wording.strip(),
    }

    if args.replace:
        index = args.replace - 1
        if index < 0 or index >= len(claims):
            raise SystemExit(f"--replace index out of range: {args.replace}")
        claims[index] = claim
    else:
        claims.append(claim)

    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
