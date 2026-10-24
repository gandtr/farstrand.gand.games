"""Checks for the static site. Run: python3 -m unittest discover -s tests -v

Needs only the standard library; Pillow (palette check) and fontTools (glyph check, system python3)
are used when importable and the test is skipped otherwise.
"""
import datetime as dt
import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = [ROOT / "index.html", ROOT / "privacy/index.html"]
# Referenced on purpose before the file exists (the lead drops them in; see PROJECT.md).
PENDING = {"press-kit/"}


class Collect(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs, self.shots, self.ld, self._ld, self.classes = [], [], [], None, []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "script" and a.get("type") == "application/ld+json":
            self._ld = []
        for k in ("src", "href", "poster"):
            if a.get(k):
                self.refs.append((k, a[k]))
        if a.get("data-shot"):
            self.shots.append(a["data-shot"])
        self.classes.append(a.get("class", ""))

    def handle_data(self, data):
        if self._ld is not None:
            self._ld.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self._ld is not None:
            self.ld.append(json.loads("".join(self._ld)))
            self._ld = None


def parse(path: Path) -> Collect:
    c = Collect()
    c.feed(path.read_text())
    return c


def local(page: Path, ref: str):
    """Repo-relative path of a local reference, or None for external, anchors, mailto, data: URIs."""
    if re.match(r"^(https?:|mailto:|data:|#|\s*$)", ref):
        return None
    rel = (page.parent / ref.split("#")[0].split("?")[0]).resolve().relative_to(ROOT)
    return str(rel) + ("/" if ref.endswith("/") else "")


class SiteTests(unittest.TestCase):
    def test_references_resolve(self):
        for page in PAGES:
            text = page.read_text()
            refs = [r for _, r in parse(page).refs] + re.findall(r"url\(\s*['\"]?([^)'\"]+)", text)
            for ref in refs:
                path = local(page, ref)
                if path is None or path in PENDING:
                    continue
                with self.subTest(page=page.name, ref=ref):
                    target = ROOT / path
                    self.assertTrue(target.exists() or (path.endswith("/") and (target / "index.html").exists()), path)

    def test_every_gallery_shot_has_both_files(self):
        shots = parse(ROOT / "index.html").shots
        self.assertGreaterEqual(len(shots), 1)
        for slug in shots:
            with self.subTest(slug=slug):
                self.assertTrue((ROOT / f"public/shots/{slug}.png").exists())
                self.assertTrue((ROOT / f"public/shots/1x/{slug}.png").exists())

    def test_json_ld_video_game(self):
        docs = parse(ROOT / "index.html").ld
        self.assertEqual(len(docs), 1)
        d = docs[0]
        self.assertEqual((d["@type"], d["name"]), ("VideoGame", "FARSTRAND"))
        self.assertEqual(d["inLanguage"], ["en", "ja", "tr"])
        self.assertLessEqual(len(d["description"]), 155)

    def test_trailer_video_object(self):
        """The VideoObject names the real files. Its uploadDate is left out until the trailer is published
        (the lead sets it, see the TODO above the JSON-LD); when present it must carry a timezone and be past."""
        def videos(v):
            if isinstance(v, dict):
                if v.get("@type") == "VideoObject":
                    yield v
                for c in v.values():
                    yield from videos(c)
            elif isinstance(v, list):
                for c in v:
                    yield from videos(c)
        found = [v for doc in parse(ROOT / "index.html").ld for v in videos(doc)]
        self.assertEqual(len(found), 1)
        v = found[0]
        for key in ("thumbnailUrl", "contentUrl"):
            self.assertTrue((ROOT / v[key].replace("https://farstrand.gand.games/", "")).exists(), v[key])
        if "uploadDate" in v:
            self.assertRegex(v["uploadDate"], r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(Z|[+-]\d\d:\d\d)$")
            self.assertLess(dt.datetime.fromisoformat(v["uploadDate"].replace("Z", "+00:00")), dt.datetime.now(dt.timezone.utc))
        else:
            print("  (trailer VideoObject: uploadDate not set yet, see the TODO in index.html)")

    def test_three_languages_side_by_side(self):
        classes = parse(ROOT / "index.html").classes
        count = lambda c: sum(1 for x in classes if re.search(rf"(^|\s){c}(\s|$)", x))
        en, ja, tr = count("l-en"), count("l-ja"), count("l-tr")
        self.assertEqual((en, ja, tr), (en, en, en), "every EN element has its JA and TR twin")

    def test_steam_switch_is_on_and_carries_the_tags(self):
        s = (ROOT / "index.html").read_text()
        self.assertIn("var STEAM_LIVE = true;", s)   # the store page is public (Coming Soon, 2026-10-24)
        self.assertIn("var DEMO_LIVE = false;", s)   # the demo's page is not public yet
        self.assertIn("store.steampowered.com/app/5461390/Farstrand/?utm_source=farstrand.gand.games&utm_medium=web&utm_campaign=site&utm_content=farstrand", s)
        self.assertIn("store.steampowered.com/app/5461420/", s)

    def test_public_text_rules(self):
        banned = re.compile(r"chatgpt|claude|anthropic|openai|midjourney|stable diffusion|qwen|comfyui|elevenlabs|gemini|copilot|\bAI\b", re.I)
        for page in PAGES:
            text = page.read_text()
            body = re.sub(r"<style.*?</style>|<script.*?</script>", "", text, flags=re.S)
            with self.subTest(page=page.name):
                self.assertNotIn("\u2014", text, "em dash")
                self.assertIsNone(banned.search(body), banned.search(body))

    def test_art_uses_only_the_game_palette(self):
        try:
            from PIL import Image
        except ImportError:
            self.skipTest("Pillow not installed")
        pal = {tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) for h in (ROOT / "tools/palette.hex").read_text().split()}
        self.assertEqual(len(pal), 32)
        files = [p for p in (ROOT / "public/art").rglob("*.png")] + [ROOT / "public/favicon-64.png", ROOT / "public/apple-touch-icon.png", ROOT / "public/og-farstrand.png"]
        for f in files:
            im = Image.open(f).convert("RGBA")
            colours = {c[:3] for n, c in im.getcolors(maxcolors=1 << 24) if c[3] > 0}
            with self.subTest(file=str(f.relative_to(ROOT))):
                self.assertEqual(colours - pal, set())

    def test_fonts_cover_every_character_on_the_pages(self):
        try:
            from fontTools.ttLib import TTFont
        except ImportError:
            self.skipTest("fontTools not importable (use /usr/bin/python3)")
        cm = lambda name: set(TTFont(ROOT / f"public/fonts/{name}.woff2").getBestCmap())
        latin = cm("PublicPixel") & cm("FiraSansCondensed-Regular")
        ja = cm("PixelMplus12-ja")
        for page in PAGES:
            body = re.sub(r"<style.*?</style>|<!--.*?-->|/\*.*?\*/", "", page.read_text(), flags=re.S)
            for ch in sorted(set(body)):
                if ch in "\n\r\t" or ord(ch) < 0x20:
                    continue
                with self.subTest(page=str(page.relative_to(ROOT)), char=ch):
                    if ord(ch) > 0x2FFF:
                        self.assertIn(ord(ch), ja)
                    elif page == PAGES[0]:  # the site: pixel text and body text both need the glyph
                        self.assertIn(ord(ch), cm("FiraSansCondensed-Regular"))
                        self.assertIn(ord(ch), cm("PublicPixel"))
                    else:
                        self.assertIn(ord(ch), cm("FiraSansCondensed-Regular") | cm("PublicPixel"))

    def test_list_the_todos(self):
        """Not a failure: prints every TODO still in the pages so the lead can clear them."""
        for page in PAGES:
            for n, line in enumerate(page.read_text().splitlines(), 1):
                if "TODO" in line:
                    print(f"  {page.relative_to(ROOT)}:{n}: {line.strip()[:110]}")


if __name__ == "__main__":
    unittest.main()
