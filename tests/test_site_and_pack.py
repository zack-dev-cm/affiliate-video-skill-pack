import json
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"


class SiteAndPackTest(unittest.TestCase):
    def test_static_pages_parse_and_local_assets_exist(self):
        parser = HTMLParser()
        for path in sorted(SITE.glob("*.html")):
            html = path.read_text(encoding="utf-8")
            parser.feed(html)
            for target in re.findall(r'(?:href|src)="([^"]+)"', html):
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                if target == "/":
                    self.assertTrue((SITE / "index.html").exists())
                    continue
                candidate = SITE / target.lstrip("/")
                if not candidate.exists() and not candidate.suffix:
                    candidate = candidate.with_suffix(".html")
                self.assertTrue(candidate.exists(), f"{path.name} links missing local target {target}")

    def test_monetization_pack_builds_expected_zip(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "pack.zip"
            subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "build_monetization_pack.py"), "--out", str(out)],
                cwd=ROOT,
                check=True,
                text=True,
                capture_output=True,
            )
            with zipfile.ZipFile(out) as archive:
                names = set(archive.namelist())
                self.assertIn("affiliate-video-pro-pack/offer.json", names)
                self.assertIn("affiliate-video-pro-pack/templates/campaign-intake.md", names)
                offer = json.loads(archive.read("affiliate-video-pro-pack/offer.json"))
            self.assertEqual(offer["price_usd"], 0)
            self.assertEqual(offer["status"], "free-public-pack")
            self.assertEqual(offer["payment_provider"], "none")
            self.assertIn("revenue", offer["positioning"]["not_promised"])

    def test_nowpayments_checkout_is_server_side_and_fiat_priced(self):
        checkout_js = (SITE / "checkout.js").read_text(encoding="utf-8")
        create_invoice = (ROOT / "functions" / "api" / "nowpayments" / "create-invoice.js").read_text(
            encoding="utf-8"
        )
        ipn = (ROOT / "functions" / "api" / "nowpayments" / "ipn.js").read_text(encoding="utf-8")
        offers = (ROOT / "functions" / "api" / "nowpayments" / "offers.js").read_text(encoding="utf-8")

        self.assertIn("/api/nowpayments/create-invoice", checkout_js)
        self.assertIn("env.NOWPAYMENTS_API_KEY", create_invoice)
        self.assertIn('"x-api-key": env.NOWPAYMENTS_API_KEY', create_invoice)
        self.assertIn('price_currency: "usd"', create_invoice)
        self.assertNotIn("pay_currency", create_invoice)
        self.assertIn("invoice_url", create_invoice)
        self.assertNotIn('"pro-pack"', create_invoice)
        self.assertIn("setup-review", create_invoice)

        self.assertIn("env.NOWPAYMENTS_IPN_SECRET", ipn)
        self.assertIn("x-nowpayments-sig", ipn)
        self.assertIn('hash: "SHA-512"', ipn)
        self.assertIn("sortObject", ipn)

        self.assertIn('checkout_type: "hosted_invoice_for_paid_services"', offers)
        self.assertIn('fiat_price_currency: "usd"', offers)
        self.assertIn("publicOffers", offers)

    def test_agent_runtime_usage_instructions_are_explicit(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        skill = (ROOT / "skill" / "affiliate-video-campaign-operator" / "SKILL.md").read_text(encoding="utf-8")
        adapters = (
            ROOT / "skill" / "affiliate-video-campaign-operator" / "references" / "platform-adapters.md"
        ).read_text(encoding="utf-8")

        for runtime in ("Claude", "Codex", "OpenClaw", "Grok"):
            self.assertIn(runtime, readme)
            self.assertIn(runtime, adapters)

        self.assertIn("generic chat-agent", skill)
        self.assertIn("Generic agents", adapters)
        self.assertIn("Claude's Skills UI", readme)
        self.assertIn("cp -R skill/affiliate-video-campaign-operator", readme)
        self.assertIn("export_openclaw_handoff.py", readme)
        self.assertIn("does not assume Grok has a native skill installer", readme)
        self.assertIn("Do not assume Grok or another chat agent has a native skill installer", adapters)
        for platform in ("pinterest", "tiktok", "youtube", "instagram"):
            self.assertIn(platform, readme)
            self.assertIn(platform, adapters)

    def test_readme_happy_path_is_not_blocked(self):
        scripts = ROOT / "skill" / "affiliate-video-campaign-operator" / "scripts"
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            campaign = work / "runs" / "campaign.json"
            asset = work / "assets" / "pin-001.png"
            asset.parent.mkdir(parents=True)
            asset.write_bytes(b"placeholder")
            def run_step(args: list[str]) -> None:
                subprocess.run(args, cwd=work, check=True, text=True, capture_output=True)

            run_step(
                [
                    sys.executable,
                    str(scripts / "init_affiliate_campaign.py"),
                    "--out",
                    str(campaign),
                    "--title",
                    "Creator Desk Cable Reset",
                    "--owner",
                    "zack-dev-cm",
                    "--niche",
                    "creator desk gear",
                    "--product-name",
                    "Cable organizer kit",
                    "--product-category",
                    "home office accessory",
                    "--merchant",
                    "Example Merchant",
                    "--product-url",
                    "https://example.com/product",
                    "--affiliate-url",
                    "https://example.com/product?aff=example",
                    "--affiliate-program",
                    "example-affiliate",
                    "--short-disclosure",
                    "Paid link.",
                    "--platform",
                    "pinterest",
                    "--platform",
                    "youtube",
                ]
            )
            run_step(
                [
                    sys.executable,
                    str(scripts / "add_affiliate_claim.py"),
                    "--campaign",
                    str(campaign),
                    "--claim",
                    "Designed to organize loose desk cables",
                    "--risk",
                    "low",
                    "--evidence-url",
                    "https://example.com/product",
                ]
            )
            run_step(
                [
                    sys.executable,
                    str(scripts / "add_affiliate_asset.py"),
                    "--campaign",
                    str(campaign),
                    "--kind",
                    "generated",
                    "--asset-id",
                    "pin-001",
                    "--path",
                    "assets/pin-001.png",
                    "--provider",
                    "example-generator",
                    "--rights-note",
                    "Generated for this campaign from operator-approved product reference.",
                ]
            )
            run_step(
                [
                    sys.executable,
                    str(scripts / "set_affiliate_post.py"),
                    "--campaign",
                    str(campaign),
                    "--platform",
                    "pinterest",
                    "--title",
                    "Desk cable reset",
                    "--caption",
                    "Paid link. Simple desk setup idea.",
                    "--asset-path",
                    "assets/pin-001.png",
                    "--status",
                    "ready",
                ]
            )
            report = work / "reports" / "campaign-qc.json"
            run_step(
                [
                    sys.executable,
                    str(scripts / "check_affiliate_campaign.py"),
                    "--campaign",
                    str(campaign),
                    "--repo-root",
                    str(work),
                    "--out",
                    str(report),
                ]
            )
            qc = json.loads(report.read_text(encoding="utf-8"))
            self.assertNotEqual(qc["status"], "BLOCK", qc)

    def test_claude_zip_packaging_source_is_current(self):
        source_skill = (ROOT / "skill" / "affiliate-video-campaign-operator" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        source_agent = (
            ROOT / "skill" / "affiliate-video-campaign-operator" / "agents" / "openai.yaml"
        ).read_text(encoding="utf-8")
        source_adapters = (
            ROOT / "skill" / "affiliate-video-campaign-operator" / "references" / "platform-adapters.md"
        ).read_text(encoding="utf-8")

        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "claude.zip"
            subprocess.run(
                [
                    "zip",
                    "-qr",
                    str(out),
                    "affiliate-video-campaign-operator",
                    "-x",
                    "*/__pycache__/*",
                    "*.pyc",
                ],
                cwd=ROOT / "skill",
                check=True,
                text=True,
                capture_output=True,
            )
            with zipfile.ZipFile(out) as archive:
                self.assertEqual(
                    archive.read("affiliate-video-campaign-operator/SKILL.md").decode("utf-8"),
                    source_skill,
                )
                self.assertEqual(
                    archive.read("affiliate-video-campaign-operator/agents/openai.yaml").decode("utf-8"),
                    source_agent,
                )
                self.assertEqual(
                    archive.read("affiliate-video-campaign-operator/references/platform-adapters.md").decode("utf-8"),
                    source_adapters,
                )


if __name__ == "__main__":
    unittest.main()
