#!/usr/bin/env python3
"""Build public/ media from a git-archive snapshot of the game (never its working tree).

  git -C ~/projects/games/farstrand/farstrand archive 2e08e64 | tar -x -C <snap>
  python3 tools/build_media.py --game <snap> [--shots-dir DIR]

Pixel art is copied unchanged or composed on its native grid; nothing is resampled.
Extras (frost-vein bars, favicons, social card): tools/build_extras.py. Python 3, Pillow, NumPy.
"""
import argparse
import json
import shutil
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PUB = ROOT / "public"
# the sister game's own art, for the "After HELIOBANE" tile (copied unchanged from its site)
HELIOBANE_ART = Path.home() / "projects/games/heliobane/heliobane.gand.games/public/art"

# the game's own copies of the art the site shows at whole-number scales
COPIES = {
    "assets/ui/logo.png": "art/logo.png",
    "assets/backgrounds/bg_title.png": "art/bg_title.png",
    "assets/ui/portrait_hesper.png": "art/portrait_hesper.png",
    "assets/ui/portrait_mott.png": "art/portrait_mott.png",
    "assets/ui/portrait_warden.png": "art/portrait_warden.png",
    "assets/sprites/bob.png": "art/bob.png",
    "assets/sprites/hesper_idle.png": "art/hesper_idle.png",
    "assets/sprites/hesper_graft.png": "art/hesper_graft.png",
    "assets/sprites/fx_frost.png": "art/fx_frost.png",
    "assets/sprites/fx_thaw.png": "art/fx_thaw.png",
    "assets/sprites/fx_explode_m.png": "art/fx_explode_m.png",
    "assets/sprites/ui_glyphs_deck.png": "art/glyphs_deck.png",
    "assets/sprites/prop_lamp_heart.png": "art/lamp_heart.png",
    "assets/backgrounds/bg_strand_end_halm.png": "art/worlds/halm.png",
    "assets/backgrounds/bg_strand_end_knot.png": "art/worlds/knot.png",
    "assets/backgrounds/bg_strand_end_verrin.png": "art/worlds/verrin.png",
    "assets/backgrounds/bg_strand_end_carcanet.png": "art/worlds/carcanet.png",
    "assets/backgrounds/bg_strand_end_sunder.png": "art/worlds/sunder.png",
    "assets/backgrounds/bg_strand_end_ninth_light.png": "art/worlds/ninth-light.png",
}

# assets/enemies/material_tint.gdshader: brightness picks a step of a four-colour ramp
GLASS = [(0x0B, 0x0B, 0x1A), (0x2A, 0x1A, 0x3A), (0x5A, 0x2E, 0x7A), (0xCF, 0xE0, 0xFF)]
SUNFED = [(0x6B, 0x3E, 0x12), (0xA8, 0x64, 0x1A), (0xE0, 0x9A, 0x2A), (0xFF, 0xD2, 0x4A)]
RIM_GLASS, RIM_SUNFED, RIM_SUNFED_DIM = (0xCF, 0xE0, 0xFF), (0xFF, 0xD2, 0x4A), (0xE0, 0x9A, 0x2A)


def hexes(path: Path) -> set:
    return {tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) for h in path.read_text().split()}


def off_palette(img: Image.Image, pal: set) -> int:
    a = np.array(img.convert("RGBA"))
    px = {tuple(int(v) for v in c[:3]) for c in a.reshape(-1, 4) if c[3] > 0}
    return len(px - pal)


def save_png(img: Image.Image, dst: Path) -> None:
    """Lossless; indexed when 256 colours or fewer are used (the exact colours, no quantising)."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    rgb = np.array(img.convert("RGB"))
    flat = (rgb[..., 0].astype(np.uint32) << 16) | (rgb[..., 1].astype(np.uint32) << 8) | rgb[..., 2]
    cols, inv = np.unique(flat, return_inverse=True)
    if len(cols) <= 256:
        out = Image.fromarray(inv.reshape(flat.shape).astype(np.uint8), "P")
        out.putpalette([c for v in cols for c in ((v >> 16) & 255, (v >> 8) & 255, v & 255)])
        out.save(dst, optimize=True)
    else:
        Image.fromarray(rgb).save(dst, optimize=True)


def build_shots(shots_dir: Path) -> None:
    entries = json.loads((ROOT / "tools/shots.json").read_text())["shots"]
    for slug, name in entries:
        a = np.array(Image.open(shots_dir / name).convert("RGB"))
        assert a.shape == (1080, 1920, 3), (name, a.shape)
        small = a[3::6, 3::6]  # the centre of every 6x6 block
        exact = np.array_equal(np.repeat(np.repeat(small, 6, 0), 6, 1), a)
        print(f"  shot {slug:16s} from {name}: exact x6 = {exact}")
        assert exact, f"{name} is not an exact x6 scale of 320x180"
        save_png(Image.fromarray(a), PUB / "shots" / f"{slug}.png")
        save_png(Image.fromarray(small), PUB / "shots/1x" / f"{slug}.png")


def thornling_states(game: Path) -> None:
    """The enemy in the material states the Graft gives it, 18x18 frames (a 1 px margin for the
    rim), rows: flesh (as drawn), glass, sunfed A, sunfed B (the pulse's two halves)."""
    sheet = np.array(Image.open(game / "assets/sprites/enemy_thornling.png").convert("RGBA"))
    out = np.zeros((4 * 18, 4 * 18, 4), np.uint8)
    for f in range(4):
        spr = np.zeros((18, 18, 4), np.uint8)
        spr[1:17, 1:17] = sheet[:, f * 16:(f + 1) * 16]
        solid = spr[..., 3] > 127
        nb = np.zeros_like(solid)
        nb[1:] |= solid[:-1]
        nb[:-1] |= solid[1:]
        nb[:, 1:] |= solid[:, :-1]
        nb[:, :-1] |= solid[:, 1:]
        rim = nb & ~solid
        luma = (spr[..., :3] / 255.0) @ np.array([0.3, 0.55, 0.15])
        step = np.clip((luma * 4).astype(int), 0, 3)
        for row, (ramp, bump, rim_col) in enumerate([(None, 0, None), (GLASS, 0, RIM_GLASS),
                                                      (SUNFED, 0, RIM_SUNFED_DIM), (SUNFED, 1, RIM_SUNFED)]):
            cell = out[row * 18:(row + 1) * 18, f * 18:(f + 1) * 18]
            if ramp is None:
                cell[:] = spr
                continue
            idx = np.clip(step + bump, 0, 3) if ramp is SUNFED else np.maximum(step, 1)
            for y, x in zip(*np.where(solid)):
                cell[y, x] = (*ramp[idx[y, x]], 255)
            for y, x in zip(*np.where(rim)):
                cell[y, x] = (*rim_col, 255)
    Image.fromarray(out).save(PUB / "art/thornling_states.png", optimize=True)


def pips(game: Path) -> None:
    """HUD heat pip (7x7), frames: empty, full, flash (the pip that just changed), red (no heat)."""
    pal = sorted(hexes(game / "assets/palette.hex"))
    src = np.array(Image.open(game / "assets/sprites/ui_heat_pip.png").convert("RGBA"))
    empty, full = src[:, :7].copy(), src[:, 7:].copy()
    flash, red = full.copy(), empty.copy()
    for y in range(7):
        for x in range(7):
            if flash[y, x, 3] and tuple(flash[y, x, :3]) != (0x0B, 0x0B, 0x1A):
                lum = int(flash[y, x, :3].astype(int) @ np.array([0.3, 0.55, 0.15]))
                flash[y, x, :3] = (255, 255, 255) if lum > 140 else (0xFF, 0xF3, 0xA8)
            if red[y, x, 3] and tuple(red[y, x, :3]) != (0x0B, 0x0B, 0x1A):
                c = red[y, x, :3].astype(int) * np.array([200, 50, 30]) // 255  # Pal.RED as the modulate
                red[y, x, :3] = min(pal, key=lambda p: sum((p[i] - c[i]) ** 2 for i in range(3)))
    Image.fromarray(np.concatenate([empty, full, flash, red], 1)).save(PUB / "art/pips.png", optimize=True)


def stage(game: Path) -> None:
    """The toy's 160x112 stage: Halm's red sky and glass trees over a frost-capped rock floor
    (autotile frames 14 and 15 of tile_halm_rock, the game's rule), floor top at y 80."""
    far = Image.open(game / "assets/backgrounds/bg_halm_far.png").convert("RGBA")
    mid = Image.open(game / "assets/backgrounds/bg_halm_mid.png").convert("RGBA")
    x0, y0 = 120, 34
    img = far.crop((x0, y0, x0 + 160, y0 + 112))
    img.alpha_composite(mid.crop((x0 + 6, y0 + 10, x0 + 166, y0 + 122)))
    tiles = Image.open(game / "assets/tiles/tile_halm_rock.png").convert("RGBA")
    for cx in range(10):
        img.alpha_composite(tiles.crop((14 * 16, 0, 15 * 16, 16)), (cx * 16, 80))
        h = ((cx * 73856093) ^ (1 * 19349663) ^ (cx * 83492791)) % 4
        fill = [15, 20, 21, 22][h]
        img.alpha_composite(tiles.crop((fill * 16, 0, fill * 16 + 16, 16)), (cx * 16, 96))
    img.convert("RGB").save(PUB / "art/stage.png", optimize=True)


def trailer_placeholder(game: Path) -> None:
    """Until the trailer exists: a 320x180 crop of the title backdrop (x6 for the poster)."""
    still = Image.open(game / "assets/backgrounds/bg_title.png").convert("RGB").crop((0, 14, 320, 194))
    still.save(PUB / "art/trailer-still.png", optimize=True)
    still.resize((1920, 1080), Image.NEAREST).save(PUB / "trailer-poster.jpg", quality=90, subsampling=0)
    icon = Image.open(game / "assets/sprites/hesper_idle.png").convert("RGBA").crop((0, 0, 16, 32))
    icon.save(PUB / "art/hesper-icon.png", optimize=True)
    for src, dst in (("logo.png", "heliobane-logo.png"), ("ship.png", "heliobane-ship.png")):
        if (HELIOBANE_ART / src).exists():
            shutil.copy(HELIOBANE_ART / src, PUB / "art" / dst)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True, type=Path, help="snapshot of the game (git archive 2e08e64)")
    ap.add_argument("--shots-dir", type=Path)
    a = ap.parse_args()
    game = a.game.resolve()
    pal = hexes(game / "assets/palette.hex")
    assert len(pal) == 32
    for src, dst in COPIES.items():
        (PUB / dst).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(game / src, PUB / dst)
        bad = off_palette(Image.open(PUB / dst), pal)
        print(f"  copy {dst}" + (f"  ({bad} off-palette colours)" if bad else ""))
    build_shots((a.shots_dir or game / "marketing/steam/screenshots").resolve())
    thornling_states(game)
    pips(game)
    stage(game)
    trailer_placeholder(game)
    for f in ("art/thornling_states.png", "art/pips.png", "art/stage.png"):
        print(f"  built {f}: off-palette colours {off_palette(Image.open(PUB / f), pal)}")


if __name__ == "__main__":
    main()
