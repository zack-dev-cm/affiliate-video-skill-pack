import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skill" / "affiliate-video-campaign-operator" / "scripts"


def run_script(name, *args):
    return subprocess.run(
        [sys.executable, str(SCRIPTS / name), *args],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )


class AffiliateCampaignScriptsTest(unittest.TestCase):
    def test_checker_blocks_tiktok_supplement_claim_without_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            campaign = root / "campaign.json"
            report = root / "qc.json"

            run_script(
                "init_affiliate_campaign.py",
                "--out",
                str(campaign),
                "--title",
                "Magnesium Test",
                "--niche",
                "sleep wellness",
                "--product-name",
                "Magnesium supplement",
                "--affiliate-url",
                "https://example.com/?tag=test",
                "--short-disclosure",
                "I may earn a commission.",
                "--platform",
                "tiktok",
            )
            payload = json.loads(campaign.read_text())
            payload["claims"].append({"claim": "This helps you sleep better."})
            campaign.write_text(json.dumps(payload, indent=2) + "\n")

            run_script("check_affiliate_campaign.py", "--campaign", str(campaign), "--repo-root", str(root), "--out", str(report))

            qc = json.loads(report.read_text())
            messages = "\n".join(item["message"] for item in qc["errors"])
            self.assertEqual(qc["status"], "BLOCK")
            self.assertIn("TikTok branded content is high-risk", messages)
            self.assertIn("Sensitive claim needs evidence", messages)

    def test_checker_requires_amazon_associate_statement(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            campaign = root / "campaign.json"
            report = root / "qc.json"

            run_script(
                "init_affiliate_campaign.py",
                "--out",
                str(campaign),
                "--title",
                "Organizer Test",
                "--product-name",
                "Desk organizer",
                "--merchant",
                "Amazon",
                "--affiliate-program",
                "amazon-associates",
                "--affiliate-url",
                "https://amazon.com/dp/example?tag=test",
                "--short-disclosure",
                "Paid link.",
            )
            run_script("check_affiliate_campaign.py", "--campaign", str(campaign), "--repo-root", str(root), "--out", str(report))

            qc = json.loads(report.read_text())
            self.assertEqual(qc["status"], "BLOCK")
            self.assertTrue(any("Amazon campaigns need" in item["message"] for item in qc["errors"]))

    def test_handoff_prepends_disclosure_and_keeps_campaign_reference(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            asset = root / "pin.png"
            asset.write_bytes(b"test")
            campaign = root / "campaign.json"
            handoff = root / "handoff.json"

            run_script(
                "init_affiliate_campaign.py",
                "--out",
                str(campaign),
                "--title",
                "Creator Desk Gear",
                "--product-name",
                "Cable organizer",
                "--affiliate-url",
                "https://example.com/product",
                "--short-disclosure",
                "Paid link.",
                "--platform",
                "pinterest",
            )
            payload = json.loads(campaign.read_text())
            payload["posts"]["pinterest"]["caption"] = "Clean up your desk in 5 minutes."
            payload["posts"]["pinterest"]["asset_path"] = str(asset)
            campaign.write_text(json.dumps(payload, indent=2) + "\n")

            run_script(
                "export_openclaw_handoff.py",
                "--campaign",
                str(campaign),
                "--platform",
                "pinterest",
                "--out",
                str(handoff),
                "--browser-profile",
                "pin-profile",
            )

            payload = json.loads(handoff.read_text())
            self.assertEqual(payload["platform"], "pinterest")
            self.assertEqual(payload["run"]["browser_profile"], "pin-profile")
            self.assertEqual(payload["source_campaign_bundle"], "campaign.json")
            self.assertTrue(payload["content"]["caption"].startswith("Paid link."))
            self.assertEqual(payload["assets"]["extra_files"], ["campaign.json"])

    def test_mutation_scripts_add_claim_asset_and_post(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            asset = root / "pin.png"
            asset.write_bytes(b"test")
            campaign = root / "campaign.json"
            report = root / "qc.json"

            run_script(
                "init_affiliate_campaign.py",
                "--out",
                str(campaign),
                "--title",
                "Desk Accessory Test",
                "--product-name",
                "Cable organizer",
                "--affiliate-url",
                "https://example.com/product",
                "--short-disclosure",
                "Paid link.",
                "--platform",
                "pinterest",
            )
            run_script(
                "add_affiliate_claim.py",
                "--campaign",
                str(campaign),
                "--claim",
                "Designed to organize loose desk cables.",
                "--risk",
                "low",
                "--evidence-url",
                "https://example.com/product",
            )
            run_script(
                "add_affiliate_asset.py",
                "--campaign",
                str(campaign),
                "--kind",
                "generated",
                "--asset-id",
                "pin-001",
                "--path",
                str(asset),
                "--provider",
                "Higgsfield",
                "--rights-note",
                "Generated from operator-owned prompt.",
            )
            run_script(
                "set_affiliate_post.py",
                "--campaign",
                str(campaign),
                "--platform",
                "pinterest",
                "--title",
                "Desk cable reset",
                "--caption",
                "Paid link. Simple setup idea.",
                "--asset-path",
                str(asset),
                "--status",
                "ready",
                "--hashtag",
                "desksetup,organization",
            )
            run_script("check_affiliate_campaign.py", "--campaign", str(campaign), "--repo-root", str(root), "--out", str(report))

            payload = json.loads(campaign.read_text())
            qc = json.loads(report.read_text())
            self.assertEqual(payload["claims"][0]["risk"], "low")
            self.assertEqual(payload["creative"]["generated_assets"][0]["asset_id"], "pin-001")
            self.assertEqual(payload["posts"]["pinterest"]["hashtags"], ["#desksetup", "#organization"])
            self.assertNotEqual(qc["status"], "BLOCK")

    def test_affiliate_link_alone_is_not_accepted_as_clear_disclosure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            campaign = root / "campaign.json"
            report = root / "qc.json"

            run_script(
                "init_affiliate_campaign.py",
                "--out",
                str(campaign),
                "--title",
                "Weak Disclosure",
                "--product-name",
                "Desk mat",
                "--affiliate-url",
                "https://example.com/product",
                "--short-disclosure",
                "Affiliate link.",
            )
            run_script("check_affiliate_campaign.py", "--campaign", str(campaign), "--repo-root", str(root), "--out", str(report))

            qc = json.loads(report.read_text())
            self.assertEqual(qc["status"], "BLOCK")
            self.assertTrue(any("clear disclosure" in item["message"] for item in qc["errors"]))

    def test_published_post_requires_url(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            asset = root / "pin.png"
            asset.write_bytes(b"test")
            campaign = root / "campaign.json"
            report = root / "qc.json"

            run_script(
                "init_affiliate_campaign.py",
                "--out",
                str(campaign),
                "--title",
                "Published Receipt Gap",
                "--product-name",
                "Desk mat",
                "--affiliate-url",
                "https://example.com/product",
                "--short-disclosure",
                "Paid link.",
                "--platform",
                "pinterest",
            )
            run_script(
                "set_affiliate_post.py",
                "--campaign",
                str(campaign),
                "--platform",
                "pinterest",
                "--asset-path",
                str(asset),
                "--status",
                "published",
            )
            run_script("check_affiliate_campaign.py", "--campaign", str(campaign), "--repo-root", str(root), "--out", str(report))

            qc = json.loads(report.read_text())
            self.assertEqual(qc["status"], "BLOCK")
            self.assertTrue(any("published_url" in item["kind"] for item in qc["errors"]))


if __name__ == "__main__":
    unittest.main()
