#!/usr/bin/env python3
"""Draw the site's own small art on a native grid, palette colours only, scaled by whole numbers:

  public/art/vein-frost.png, vein-ember.png  160x11 tiles for the section bars (shown x2)
  public/favicon.ico, favicon-64.png, apple-touch-icon.png   a 16x16 icon (sun, beam, Hesper, ledge)
  public/og-farstrand.png     1200x630 TEMPORARY social card: title backdrop x4 + logo + lockup
                              (replace with farstrand-press-kit/press-kit/social/ when it exists)

  python3 tools/build_extras.py --game <snapshot>        (Python 3, Pillow, NumPy)
"""
import argparse
import struct
from io import BytesIO
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
PUB = ROOT / "public"
H = lambda s: tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))
P = {k: H(v) for k, v in dict(
    black="000000", void="0b0b1a", night="1a1c2c", steel1="2b2f4a", steel2="3e4a6b", steel3="5b6ea0",
    steel4="8aa4d6", ice="cfe0ff", white="ffffff", umber2="6b3e12", umber3="a8641a", amber="e09a2a",
    gold="ffd24a", pale="fff3a8", blood0="3b0d14", blood1="7a1a1a", red="c8321e", fire="ff6a1a",
    flame="ff9e3d", cyan="20e0ff").items()}

FROST = [P[k] for k in "void steel1 steel2 steel3 steel4 ice steel4 steel3 steel2 steel1 void".split()]
EMBER = [P[k] for k in "black blood0 blood1 red fire flame fire red blood1 blood0 black".split()]


def vein_tile(ramp, vein, glint, seed) -> Image.Image:
    """A glass bar (dark-light-dark rows) with a dull-gold vein wandering through it."""
    rng = np.random.default_rng(seed)
    w = 160
    img = np.zeros((11, w, 3), np.uint8)
    for y in range(11):
        img[y, :] = ramp[y]
    for _ in range(16):  # frost glints
        img[rng.integers(3, 8), rng.integers(0, w)] = glint
    ys, y = [], 5
    for x in range(w):
        if x > w - 12:  # walk back to the start row so the tile repeats without a seam
            y += int(np.sign(5 - y))
        elif rng.random() < 0.3:
            y = int(np.clip(y + rng.choice([-1, 1]), 3, 7))
        ys.append(y)
    for x, y in enumerate(ys):
        img[y, x] = vein[0]
        if x % 7 == 3:
            img[y, x] = vein[1]
        if x % 29 == 11:
            img[y, x] = vein[2]
        if x + 1 < w and ys[x + 1] != y:
            img[ys[x + 1], x] = vein[0]
    for bx in (31, 77, 122):  # three short branches
        d = rng.choice([-1, 1])
        for k in range(1, 4):
            yy = ys[bx] + d * k
            if 0 < yy < 10:
                img[yy, bx + k] = P["umber2"]
    return Image.fromarray(img)


ICON = [  # 16x16, one character per palette colour (see KEY)
    "................",
    "............w...",
    "............i...",
    "............i...",
    ".....bbbb...i...",
    "...bbooOObb.i...",
    "..bboorrrrb.i...",
    "..booorrrrB.i...",
    "..boorrrrrBBi...",
    "..brrrrrrrBBi...",
    "..bBrrrrrBB.i...",
    "...bBBrrBB..i...",
    "SSSSSSSSSSSSwSSS",
    "tttttttttttttttt",
    "nnnnnnnnnnnnnnnn",
    "kkkkkkkkkkkkkkkk",
]
KEY = {".": "void", "w": "white", "i": "ice", "b": "blood0", "B": "blood1", "r": "red", "o": "fire", "O": "flame",
       "S": "steel4", "t": "steel2", "n": "steel1", "k": "black"}


def icon16() -> Image.Image:
    a = np.zeros((16, 16, 3), np.uint8)
    for y, row in enumerate(ICON):
        for x, ch in enumerate(row):
            a[y, x] = P[KEY[ch]]
    for (x, y), c in {(3, 8): "steel3", (4, 8): "cyan", (3, 9): "steel2", (4, 9): "steel3", (3, 10): "steel2",
                      (4, 10): "steel2", (3, 11): "steel1", (4, 11): "steel1"}.items():
        a[y, x] = P[c]  # Hesper on the ledge
    return Image.fromarray(a)


def ico(path: Path, img16: Image.Image) -> None:
    """favicon.ico with whole-number scales of the 16x16 icon: 16, 32, 48, 64 (PNG entries)."""
    sizes, blobs = (16, 32, 48, 64), []
    for s in sizes:
        b = BytesIO()
        img16.resize((s, s), Image.NEAREST).save(b, "PNG")
        blobs.append(b.getvalue())
    out = struct.pack("<HHH", 0, 1, len(sizes))
    off = 6 + 16 * len(sizes)
    for s, b in zip(sizes, blobs):
        out += struct.pack("<BBBBHHII", s, s, 0, 0, 1, 32, len(b), off)
        off += len(b)
    path.write_bytes(out + b"".join(blobs))


def og(game: Path) -> None:
    """Title backdrop at x4 (native 300x158 window, 1 px cut top and bottom) with the logo and lockup."""
    bg = Image.open(game / "assets/backgrounds/bg_title.png").convert("RGBA")
    win = bg.crop((10, 6, 310, 164))
    logo = Image.open(game / "assets/ui/logo.png").convert("RGBA")
    win.alpha_composite(logo, (30, 8))
    d = ImageDraw.Draw(win)
    d.fontmode = "1"
    font = ImageFont.truetype(str(game / "art/src/fonts/PublicPixel.ttf"), 8)
    text = "A HELIOBANE METROIDVANIA"
    x = (300 - 8 * len(text)) // 2
    d.text((x + 1, 55), text, font=font, fill=P["void"])
    d.text((x, 54), text, font=font, fill=P["ice"])
    big = win.convert("RGB").resize((1200, 632), Image.NEAREST).crop((0, 1, 1200, 631))
    big.save(PUB / "og-farstrand.png", optimize=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True, type=Path)
    game = ap.parse_args().game.resolve()
    vein_tile(FROST, (P["umber3"], P["amber"], P["gold"]), P["white"], 7).save(PUB / "art/vein-frost.png")
    vein_tile(EMBER, (P["pale"], P["white"], P["gold"]), P["pale"], 11).save(PUB / "art/vein-ember.png")
    ic = icon16()
    ico(PUB / "favicon.ico", ic)
    ic.resize((64, 64), Image.NEAREST).save(PUB / "favicon-64.png", optimize=True)
    touch = Image.new("RGB", (180, 180), P["void"])  # 16 x 11 = 176, a 2 px palette border
    touch.paste(ic.resize((176, 176), Image.NEAREST), (2, 2))
    touch.save(PUB / "apple-touch-icon.png", optimize=True)
    og(game)
    print("wrote veins, favicon.ico, favicon-64.png, apple-touch-icon.png, og-farstrand.png")


if __name__ == "__main__":
    main()
