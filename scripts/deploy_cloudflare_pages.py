#!/usr/bin/env python3
"""Deploy the static landing page to Cloudflare Pages and optionally attach a custom domain."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=ROOT, check=check, text=True, capture_output=True)


def wrangler_json(command: list[str]) -> dict:
    completed = run(command)
    return json.loads(completed.stdout)


def account_id() -> str:
    if os.environ.get("CLOUDFLARE_ACCOUNT_ID"):
        return os.environ["CLOUDFLARE_ACCOUNT_ID"]
    payload = wrangler_json(["npx", "-y", "wrangler", "whoami", "--json"])
    accounts = payload.get("accounts") or []
    if len(accounts) != 1:
        raise SystemExit("Set CLOUDFLARE_ACCOUNT_ID when wrangler has zero or multiple accounts.")
    return accounts[0]["id"]


def ensure_project(project_name: str) -> None:
    created = run(
        ["npx", "-y", "wrangler", "pages", "project", "create", project_name, "--production-branch", "main"],
        check=False,
    )
    combined = f"{created.stdout}\n{created.stderr}"
    if created.returncode == 0:
        return
    if "already exists" in combined.lower() or "project already exists" in combined.lower():
        return
    raise SystemExit(combined.strip())


def deploy(project_name: str, directory: str) -> str:
    completed = run(
        [
            "npx",
            "-y",
            "wrangler",
            "pages",
            "deploy",
            directory,
            "--project-name",
            project_name,
            "--branch",
            "main",
            "--commit-dirty=true",
        ]
    )
    return completed.stdout


def add_custom_domain(project_name: str, domain: str, account: str) -> dict:
    token = os.environ.get("CLOUDFLARE_API_TOKEN")
    if not token:
        raise SystemExit("CLOUDFLARE_API_TOKEN is required to add a Pages custom domain.")
    url = f"https://api.cloudflare.com/client/v4/accounts/{account}/pages/projects/{project_name}/domains"
    body = json.dumps({"name": domain}).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        payload = error.read().decode("utf-8", errors="replace")
        if error.code == 409 or "already" in payload.lower():
            return {"success": True, "already_exists": True, "response": payload}
        raise SystemExit(payload) from error


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-name", default="affiliate-video-skill-pack")
    parser.add_argument("--directory", default="site")
    parser.add_argument("--custom-domain", default="")
    parser.add_argument("--skip-domain", action="store_true")
    args = parser.parse_args()

    ensure_project(args.project_name)
    deploy_output = deploy(args.project_name, args.directory)
    result = {
        "project": args.project_name,
        "pages_url": f"https://{args.project_name}.pages.dev",
        "deploy_output_tail": deploy_output.strip().splitlines()[-8:],
    }
    if args.custom_domain and not args.skip_domain:
        result["custom_domain"] = add_custom_domain(args.project_name, args.custom_domain, account_id())
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
