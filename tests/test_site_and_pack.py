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
            self.assertIn("revenue", offer["positioning"]["not_promised"])


if __name__ == "__main__":
    unittest.main()
