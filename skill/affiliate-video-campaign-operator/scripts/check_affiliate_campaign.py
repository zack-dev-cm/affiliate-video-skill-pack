#!/usr/bin/env python3
"""Validate an affiliate video campaign ledger for disclosure and publish readiness."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


PRIVATE_PATH_RE = re.compile(r"^(?:/Users/|/home/|[A-Za-z]:\\\\Users\\\\)")
DISCLOSURE_RE = re.compile(
    r"(#ad\b|paid link|paid partnership|commission|sponsored|i may earn|i earn|as an amazon associate|affiliate (commission|relationship))",
    re.IGNORECASE,
)
AMAZON_ASSOCIATE_RE = re.compile(r"as an amazon associate,?\s+i earn from qualifying purchases", re.IGNORECASE)
FAKE_TESTIMONIAL_RE = re.compile(
    r"\b(i tried|i used|my results|changed my life|fixed my|cured my|i finally|before i found)\b",
    re.IGNORECASE,
)
HEALTH_RE = re.compile(
    r"\b(supplement|vitamin|magnesium|sleep aid|anxiety|stress|weight loss|fat burner|detox|"
    r"healthcare|medicine|pharmaceutical|skincare|acne|wrinkle|hair growth|teeth whitening)\b",
    re.IGNORECASE,
)
MEDICAL_CLAIM_RE = re.compile(
    r"\b(cure|treat|diagnose|prevent|heal|fix|reduce anxiety|anxiety relief|sleep better|"
    r"lower blood pressure|burn fat|lose weight|clinical proof|doctor recommended)\b",
    re.IGNORECASE,
)
FINANCE_RE = re.compile(r"\b(invest|crypto|loan|credit|insurance|mortgage|trading|passive income|make money)\b", re.IGNORECASE)
SHORTENER_HOSTS = {
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "goo.gl",
    "ow.ly",
    "buff.ly",
    "cutt.ly",
    "rebrand.ly",
    "lnkd.in",
}


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit(f"expected JSON object in {path}")
    return payload


def add_issue(bucket: list[dict[str, str]], kind: str, message: str) -> None:
    bucket.append({"kind": kind, "message": message})


def text_blob(*values: Any) -> str:
    parts: list[str] = []
    for value in values:
        if isinstance(value, str):
            parts.append(value)
        elif isinstance(value, list):
            parts.extend(str(item) for item in value)
        elif isinstance(value, dict):
            parts.extend(text_blob(*value.values()).splitlines())
        elif value is not None:
            parts.append(str(value))
    return "\n".join(parts)


def exists_for_path(value: str, repo_root: Path) -> bool:
    if not value or re.match(r"^https?://", value):
        return True
    candidate = Path(value).expanduser()
    if candidate.is_absolute():
        return candidate.exists()
    return (repo_root / candidate).exists()


def is_shortener(url: str) -> bool:
    if not re.match(r"^https?://", url):
        return False
    host = urlparse(url).netloc.lower().split(":")[0]
    return host in SHORTENER_HOSTS


def claim_has_evidence(claim: dict[str, Any]) -> bool:
    return bool(str(claim.get("evidence_url") or "").strip() or str(claim.get("evidence_note") or "").strip())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--campaign", required=True, help="Campaign ledger JSON.")
    parser.add_argument("--repo-root", default=".", help="Root for relative path checks.")
    parser.add_argument("--out", required=True, help="Output JSON report.")
    args = parser.parse_args()

    campaign_path = Path(args.campaign).expanduser().resolve()
    repo_root = Path(args.repo_root).expanduser().resolve()
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

    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []

    title = str(campaign.get("title") or "").strip()
    if not title:
        add_issue(errors, "campaign.title", "Campaign title is required.")

    platforms = [str(item).lower() for item in campaign.get("target_platforms") or []]
    if not platforms:
        add_issue(warnings, "campaign.target_platforms", "No target platforms set.")

    product_name = str(offer.get("product_name") or "").strip()
    product_category = str(offer.get("product_category") or "").strip()
    affiliate_url = str(offer.get("affiliate_url") or "").strip()
    affiliate_program = str(offer.get("affiliate_program") or "").strip().lower()
    personal_use = bool(offer.get("personal_use"))
    offer_blob = text_blob(product_name, product_category, offer.get("merchant"), affiliate_program, campaign.get("niche"))
    campaign_blob = text_blob(payload)

    if not product_name:
        add_issue(warnings, "offer.product_name", "Product name is missing.")
    if affiliate_url and is_shortener(affiliate_url):
        add_issue(warnings, "offer.affiliate_url", "Affiliate URL uses a shortener; avoid surprise redirects on affiliate platforms.")
    if affiliate_url and not re.match(r"^https?://|\[", affiliate_url):
        add_issue(warnings, "offer.affiliate_url", "Affiliate URL should be an https URL or explicit placeholder.")

    short_disclosure = str(disclosure.get("short") or "").strip()
    long_disclosure = str(disclosure.get("long") or "").strip()
    amazon_statement = str(disclosure.get("amazon_associate_statement") or "").strip()
    disclosure_blob = text_blob(short_disclosure, long_disclosure, amazon_statement)
    if affiliate_url and not DISCLOSURE_RE.search(disclosure_blob):
        add_issue(errors, "disclosure", "Affiliate campaign needs a clear disclosure near the endorsement or link.")
    if ("amazon" in affiliate_program or "amazon" in str(offer.get("merchant") or "").lower()) and not AMAZON_ASSOCIATE_RE.search(amazon_statement):
        add_issue(errors, "disclosure.amazon", "Amazon campaigns need the Associate identity statement.")

    if not isinstance(claims, list):
        add_issue(errors, "claims", "claims must be a list.")
        claims = []
    for index, claim in enumerate(claims, start=1):
        if not isinstance(claim, dict):
            add_issue(errors, f"claim.{index}", "Each claim must be an object.")
            continue
        claim_text = str(claim.get("claim") or "").strip()
        if not claim_text:
            add_issue(warnings, f"claim.{index}", "Claim text is missing.")
        if (MEDICAL_CLAIM_RE.search(claim_text) or FINANCE_RE.search(claim_text)) and not claim_has_evidence(claim):
            add_issue(errors, f"claim.{index}", "Sensitive claim needs evidence_url or evidence_note.")
        if FAKE_TESTIMONIAL_RE.search(claim_text) and not personal_use:
            add_issue(errors, f"claim.{index}", "First-person testimonial claim requires personal_use=true or a rewrite.")

    sensitive_health = bool(HEALTH_RE.search(offer_blob) or HEALTH_RE.search(campaign_blob) or MEDICAL_CLAIM_RE.search(campaign_blob))
    sensitive_finance = bool(FINANCE_RE.search(offer_blob) or FINANCE_RE.search(campaign_blob))
    if sensitive_health:
        add_issue(warnings, "sensitive.health", "Health, supplement, skincare, sleep, or body-result language requires manual claim review.")
    if sensitive_finance:
        add_issue(warnings, "sensitive.finance", "Finance or income language requires manual claim review.")
    if "tiktok" in platforms and sensitive_health:
        add_issue(errors, "platform.tiktok", "TikTok branded content is high-risk for supplements, healthcare, weight loss, and health-benefit claims.")
    if "tiktok" in platforms and sensitive_finance:
        add_issue(warnings, "platform.tiktok", "TikTok financial branded content may be restricted or require approved brand workflows.")

    fake_text = text_blob(creative.get("hooks"), creative.get("variants"), posts)
    if FAKE_TESTIMONIAL_RE.search(fake_text) and not personal_use:
        add_issue(errors, "creative.testimonial", "Creative uses first-person testimonial language but offer.personal_use is false.")

    generated_assets = creative.get("generated_assets") or []
    if not isinstance(generated_assets, list):
        add_issue(errors, "creative.generated_assets", "generated_assets must be a list.")
        generated_assets = []
    for index, asset in enumerate(generated_assets, start=1):
        if not isinstance(asset, dict):
            add_issue(errors, f"asset.{index}", "Each generated asset must be an object.")
            continue
        asset_path = str(asset.get("path") or "").strip()
        if asset_path:
            if PRIVATE_PATH_RE.match(asset_path):
                add_issue(warnings, f"asset.{index}", f"Generated asset uses a private absolute path: {asset_path}")
            if not exists_for_path(asset_path, repo_root):
                add_issue(warnings, f"asset.{index}", f"Generated asset path does not exist locally: {asset_path}")
        if not str(asset.get("rights_note") or "").strip():
            add_issue(warnings, f"asset.{index}", "Generated asset rights_note is missing.")
        if not str(asset.get("provider") or "").strip():
            add_issue(warnings, f"asset.{index}", "Generated asset provider is missing.")

    music = creative.get("music") or {}
    if str(music.get("source") or "").strip() and not str(music.get("rights_note") or "").strip():
        add_issue(errors, "creative.music.rights_note", "Music source is set but rights_note is missing.")

    if not isinstance(posts, dict):
        add_issue(errors, "posts", "posts must be an object keyed by platform.")
        posts = {}
    for platform, post in posts.items():
        if not isinstance(post, dict):
            add_issue(errors, f"post.{platform}", "Each post must be an object.")
            continue
        post_disclosure = text_blob(post.get("disclosure"), post.get("caption"), post.get("title"))
        post_link = str(post.get("affiliate_url") or affiliate_url or "").strip()
        if post_link and not DISCLOSURE_RE.search(post_disclosure):
            add_issue(warnings, f"post.{platform}.disclosure", "Post with affiliate link should include clear disclosure in title/caption/disclosure field.")
        if post_link and is_shortener(post_link):
            add_issue(warnings, f"post.{platform}.affiliate_url", "Post uses URL shortener; platform may block or reduce trust.")
        if str(post.get("status") or "").lower() in {"ready", "scheduled", "published"}:
            asset_path = str(post.get("asset_path") or "").strip()
            if not asset_path:
                add_issue(errors, f"post.{platform}.asset_path", "Ready/scheduled/published post needs asset_path.")
            elif not exists_for_path(asset_path, repo_root):
                add_issue(errors, f"post.{platform}.asset_path", f"asset_path does not exist locally: {asset_path}")
        if str(post.get("status") or "").lower() == "published":
            if not str(post.get("published_url") or "").strip():
                add_issue(errors, f"post.{platform}.published_url", "Published post needs published_url.")
            if not str(post.get("evidence_screenshot") or "").strip():
                add_issue(warnings, f"post.{platform}.evidence_screenshot", "Published post should include evidence_screenshot.")

    platform_labels = disclosure.get("platform_labels") or {}
    if "youtube" in platforms and affiliate_url and not platform_labels.get("youtube_paid_promotion"):
        add_issue(warnings, "disclosure.youtube_paid_promotion", "Confirm whether YouTube paid promotion disclosure must be enabled.")
    if "tiktok" in platforms and affiliate_url and not platform_labels.get("tiktok_commercial_content"):
        add_issue(warnings, "disclosure.tiktok_commercial_content", "TikTok affiliate content generally needs commercial content disclosure.")
    if "instagram" in platforms and affiliate_url and not platform_labels.get("instagram_paid_partnership"):
        add_issue(warnings, "disclosure.instagram_paid_partnership", "Instagram affiliate-link posts generally need paid partnership labeling.")
    if "pinterest" in platforms and affiliate_url and not platform_labels.get("pinterest_paid_partnership"):
        add_issue(warnings, "disclosure.pinterest_paid_partnership", "Confirm Pinterest paid partnership label or clear disclosure before publishing.")

    totals = analytics.get("totals") or {}
    try:
        cost = float(totals.get("generation_cost_usd") or 0)
        revenue = float(totals.get("revenue_usd") or 0)
        if cost > 0 and revenue == 0:
            add_issue(warnings, "analytics.cost", "Generation spend is recorded but no revenue is recorded.")
    except (TypeError, ValueError):
        add_issue(warnings, "analytics.totals", "Analytics totals should be numeric.")

    status = "PASS" if not errors and not warnings else "REVIEW" if not errors else "BLOCK"
    report = {
        "schema_version": "1.0",
        "campaign_path": str(campaign_path),
        "repo_root": str(repo_root),
        "status": status,
        "errors": errors,
        "warnings": warnings,
        "counts": {
            "claims": len(claims),
            "generated_assets": len(generated_assets),
            "posts": len(posts),
            "errors": len(errors),
            "warnings": len(warnings),
        },
        "risk_flags": {
            "health_or_body_claims": sensitive_health,
            "finance_or_income_claims": sensitive_finance,
            "personal_use": personal_use,
        },
    }
    out_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
