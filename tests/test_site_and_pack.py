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
            self.assertEqual(offer["price_usd"], 49)
            self.assertEqual(offer["status"], "nowpayments-invoice")
            self.assertEqual(offer["payment_provider"], "NOWPayments")
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

        self.assertIn("env.NOWPAYMENTS_IPN_SECRET", ipn)
        self.assertIn("x-nowpayments-sig", ipn)
        self.assertIn('hash: "SHA-512"', ipn)
        self.assertIn("sortObject", ipn)

        self.assertIn('checkout_type: "hosted_invoice"', offers)
        self.assertIn('fiat_price_currency: "usd"', offers)


if __name__ == "__main__":
    unittest.main()
