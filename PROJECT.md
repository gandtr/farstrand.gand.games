# PROJECT.md — FARSTRAND.GAND.GAMES

The official page for **FARSTRAND**, a sci-fi metroidvania set seven years after
HELIOBANE, made by Gand and published as Gand (self-published) on Steam
(full game app 5461390, free demo app 5461420). Ported from
[heliobane.gand.games](https://heliobane.gand.games/): same build, FARSTRAND's colours and words.

- Address: `https://farstrand.gand.games/` (`CNAME`)
- Hosting: GitHub Pages, `main` branch, repository root, like the other Gand game sites. `.nojekyll` is present.
- DNS: CNAME `farstrand` → `gandtr.github.io` (not set up; the site owner manages DNS).
- No framework, build step, external fonts or third-party scripts. One `index.html`: markup, one `<style>`,
  one vanilla-JS IIFE.

## Structure

```
index.html                  The whole site (EN / 日本語 / TÜRKÇE side by side)
privacy/index.html          Privacy policy, English only (the store pages link here)
CNAME, robots.txt, sitemap.xml, .nojekyll, .gitignore
.htmlvalidate.json          html-validate:recommended (run: npx --yes html-validate@9 index.html privacy/index.html)
.claude/launch.json         local preview on :8151
tests/test_site.py          references resolve, JSON-LD, three languages in step, Steam switch, public-text rules,
                            palette of the art, font coverage (python3 -m unittest discover -s tests)
tools/
  build_media.py            public/ art and screenshots from a snapshot of the game
  build_extras.py           vein bars, favicons, temporary social card
  subset_fonts.sh           Public Pixel (Latin + Turkish) and PixelMplus12 (Japanese) subsets
  shots.json                gallery order: slug -> file name in the screenshots folder
  palette.hex               the game's 32 colours, for the palette test
public/
  og-farstrand.png          1200x630 social card, TEMPORARY (title backdrop x4, logo, lockup)
  favicon.ico, favicon-64.png, apple-touch-icon.png   a hand-drawn 16x16 icon at x1/x2/x3/x4/x11, TEMPORARY
  trailer-poster.jpg        1920x1080 poster, TEMPORARY (the title backdrop crop at x6)
  (trailer.mp4, trailer.en.vtt are not there yet: the page copes, see Trailer)
  shots/<slug>.png          1920x1080 frames (exact x6 of 320x180), indexed PNG
  shots/1x/<slug>.png       320x180, the centre of every 6x6 block; shown at x1 and as the viewer's x2..x5
  art/                      game art copied unchanged (logo, bg_title, portraits, Bob, Hesper, fx, glyphs, six
                            strand-end views in worlds/) and built here (see Art)
  fonts/                    Public Pixel (CC0), Fira Sans Condensed (OFL), PixelMplus12 subset (M+ licence)
```

## Design notes

- **Colour**: only the game's 32-colour master palette (`assets/palette.hex` at game commit `2e08e64`, byte for byte the
  one HELIOBANE uses), as CSS variables at the top of the stylesheet. Cold blues and glass (void, night, the steel
  ramp, ice) carry the page; the red dwarf's reds are the hero, the Kindle button and the Halm card; the Graft's
  dull gold (umber3, amber) is links, small headings and the vein under every section heading. Cyan is only the
  focus ring, as in the game it belongs to Hesper's things.
- **The bar**: HELIOBANE's copper bars are FARSTRAND's *frost-vein* bars: a dark-light-dark glass band
  (`vein-frost.png`, `vein-ember.png`, 160x11 native, shown x2) with a dull-gold vein wandering through it,
  drawn by `tools/build_extras.py`. The world cards keep stepped colour ramps, one per world.
- **Type**: Public Pixel on its 8 px grid (16/24/32 px) for display and labels, 8 px for captions. It is the game's
  own face: the game's bitmap fonts (`hud8`, `title16`) are Public Pixel rendered at 8 px. Fira Sans Condensed for body
  text. PixelMplus12 (12/24/36 px) for Japanese display, system Japanese sans for Japanese body.
  Public Pixel carries `İ ı Ş ş Ğ ğ Ç ç Ö ö Ü ü`, but the copy HELIOBANE's site shipped was a subset without
  `İ ı Ş ş Ğ ğ`; this site subsets the full TTF (`tools/subset_fonts.sh`) with them. The font stack falls back to
  Fira Sans Condensed per glyph, never to tofu. The capital `İ`, `Ş` and `Ğ` are squeezed under their marks (the
  game's own bitmap fonts do the same), so `İ` reads like a small `i` in all caps.
- **Pixel art is shown only at whole-number scales** with `image-rendering: pixelated`: hero backdrop and logo at
  x3 (x4 on a tall desktop, x5 on a very large one, x2 on phones; the logo x1 below 560 px), trailer still x3/x2/x1,
  screenshots x1 in the gallery and x1..x5 in the viewer (x6 file at x6), world views and portraits x1/x2, the
  toy stage x2/x3/x4. A scripted check measures every `img.px` at 14 widths from 320 to 1920: all whole numbers
  from 360 px up; a 320 px screen is narrower than a x1 picture, so it shows them pixelated at a fraction.
- **Hero**: the title backdrop (320x208) is TEMPORARY hero art until the key art exists. The logo and tagline sit in
  its calm sky (rows 0 to 84, which the game keeps clear for the logo), the Steam card over its dark ground. The
  edges fade out in eight steps, as HELIOBANE's hero does. To change the art, edit `.hero-art` and `--iw/--ih`.
- **Motion** (all off under `prefers-reduced-motion`): the logo drops in and shines once, one glint travels along the
  vein bars every 11 s, and the heat ladder's enemy patrols, Hesper breathes, pips flash and the fx play. The
  toy loop runs only while the toy is on screen and the tab visible.

## The heat ladder (#graft)

One flesh enemy (the Halm thornling), Hesper (idle and Graft-reach frames), her three HUD heat pips, a lamp-heart,
QUENCH and KINDLE buttons and the keys `Q` and `K` (only while the toy is on screen and the viewer is closed). The rules are
`sim/heat_ladder.gd`'s and `game/player/graft.gd`'s, at game commit `2e08e64`:

| | Quench (+1 pip) | Kindle (-1 pip) |
|---|---|---|
| sunfed | flesh | burst, and a new flesh enemy appears after a beat |
| flesh | glass | sunfed |
| glass | nothing | flesh |

The arm holds 3 pips and **starts empty**, so the first Quench visibly fills one. A Quench at 3 still changes the
enemy but the heat is lost ("The arm is full. That heat is lost"); Kindle at 0 does nothing and blinks the pips red
("No heat. Quench something first"). There are no thaw timers: the small print says what the game does, and the
toy waits for you.

Heat is conserved by the ladder alone (Quench trades a rung for a pip, Kindle a pip for a rung), so from an empty
arm one enemy can only loop between 0 and 1 pips: sunfed, the burst and a full arm would be unreachable. The toy
therefore has the game's own heat source, a **lamp-heart** (`prop_lamp_heart`, `game/world/props/props_lamp.gd`).
The Graft takes the enemy first (`graft.gd`); when the enemy has nothing to give (glass, or gone in a burst) it
reaches for the lamp-heart: +1 pip, and the heart is dim for 3 s (`dim_ticks` 180), as in the game. To remove it,
delete `#lamp`, `.lamp`, `drain()` and the lamp lines in `render()`. The captions are the game's
(`nudge.frozen`, `nudge.arm_full`, `nudge.no_heat` without its button glyph) and the two site-only ones from the
copy.

The enemy's states are `public/art/thornling_states.png`: the game has no separate glass or sunfed frames for the
thornling, it tints one strip in `game/enemies/material_tint.gdshader` (brightness picks a step of a four-colour
ramp, plus a 1-px rim). `tools/build_media.py` applies exactly that ramp per pixel at build time. The one
departure: the sunfed rim's 50 per cent blend is a palette amber on the dim half of the pulse. The pip sheet (empty,
full, flash, red) is the game's `ui_heat_pip` with the flash and the red modulate mapped to palette colours; the
stage is Halm's backdrop with the frost-capped rock floor from `tile_halm_rock` (autotile frames 14 and 15).

## Languages

English, Japanese and Turkish live side by side in the markup (`.l-en` / `.l-ja` / `.l-tr`); the
`EN / 日本語 / TÜRKÇE` switch sets `html[data-lang]`, `lang`, the title and every image's alt text
(`data-alt-ja`, `data-alt-tr`). The choice is stored in `localStorage` (`fs-lang`); `?lang=ja|tr|en` forces one; a
`ja` or `tr` browser language picks it by default. The page is one URL (no hreflang). The lockup, the product
names, the platform line and the Heliobane-shaped names that the game keeps in Latin stay English; the text has
`lang="en"` where a Turkish or Japanese page would otherwise change its case or font (Turkish capitals would turn
`Windows` into `WİNDOWS`).

**After editing any Japanese text, re-subset the pixel font** (it only contains the glyphs the page uses):

```sh
tools/subset_fonts.sh <snapshot>      # snapshot: see Rebuilding
python3 -m unittest discover -s tests  # the font test fails if a glyph is missing
```

## Content sources (do not invent)

- Words: `farstrand-press-kit/copy/{en,ja,tr}.md`, the "website" sections by section id, as of press-kit commit
  `2621b61` (lockup `A HELIOBANE METROIDVANIA` and tagline 1 approved by Arda on 2026-10-17).
- Facts and art: the game at commit `2e08e64`, from a `git archive` snapshot, never its working tree. No patch was
  needed, and no Godot was run: the build only reads PNG, JSON and the palette. The toy's rules are
  `sim/heat_ladder.gd`, `game/player/graft.gd`, `sim/material_state.gd`, `game/world/burst.gd`; its captions are
  `i18n/{en,ja,tr}.json` (`nudge.*`); the privacy facts are `steam/README.md`, `game/core/steam_service.gd`,
  `game/ui/end_card.gd` and a search of `game/` and `sim/` for any network code (there is none beyond Steam).
- Written here, not in the copy (alt texts, captions of the ten screenshots, nav labels, the skip link, the
  `Language / 言語 / Dil` group name, the page titles and the privacy page): functional text in the game's own
  terms (`i18n` names for worlds, Heralds and the Hollow Bell; the in-game nudges for two captions). Review the
  Japanese and Turkish of these first.

Spoilers are out of every piece (the list in the launch kit's `common.md`): no Hespers twist, no Hesper who said
yes, no Kell worn or his fight, no Taproot, no Marrow, no coda, no ending. The prologue, Halm, the Knot, Verrin,
Carcanet, Sunder, Ninth Light, their Heralds and Old Mott are named as the copy names them.

## Steam

The store page is not public, so the hero button is a non-interactive
`<span class="btn soon" aria-disabled="true">` ("Coming to Steam"). **To switch it on, set `STEAM_LIVE = true`
in the script**: the live `a[data-steam]` links (hero button, the Store and Demo rows of the fact sheet, the Links row)
appear and the `soon` ones go. The two URLs, both with the Steamworks UTM tags, are in the `STEAM` object right
above it: `https://store.steampowered.com/app/5461390/Farstrand/?utm_source=farstrand.gand.games&utm_medium=web&utm_campaign=site&utm_content=farstrand`
and the demo's `.../app/5461420/?...`. "Free demo coming to Steam" under the button is plain text until the demo
page is public. JSON-LD `sameAs` already names the Steam page.

## Trailer

Source (when it exists): `../farstrand-trailer/` (`output/` master and captions, `review/` poster). The site copies
are re-encoded for the web the way HELIOBANE's are:

```sh
T=../farstrand-trailer
ffmpeg -i $T/output/farstrand-trailer.mp4 -map 0:v -map 0:a -c:v libx264 -profile:v high \
  -pix_fmt yuv420p -preset slow -crf 20 -tune animation -c:a aac -b:a 160k \
  -movflags +faststart public/trailer.mp4
ffmpeg -i $T/review/poster.jpg -q:v 4 public/trailer-poster.jpg
ffmpeg -i $T/output/farstrand-trailer.srt public/trailer.en.vtt
```

The `<video>` in `#trailer` has `preload="none"`, native controls, the poster and an English captions `<track>`. The
script sends a `HEAD` for `trailer.mp4` and falls back to a still with a "Trailer coming" label when it is missing or
not served as `video/*` (checked: missing, and present with a temporary 2 s clip that was deleted again). Then
add the `trailer` VideoObject to the JSON-LD (the note above it says how; `tests/test_site.py` checks that any
VideoObject has a dated, timezone-carrying `uploadDate`).

## Rebuilding

```sh
SNAP=<empty dir>
git -C ~/projects/games/farstrand/farstrand archive 2e08e64 | tar -x -C $SNAP
python3 tools/build_media.py --game $SNAP        # art, shots, toy sprites; prints exact-x6 and palette checks
python3 tools/build_extras.py --game $SNAP       # veins, icons, social card
tools/subset_fonts.sh $SNAP                      # fonts
```

Screenshots: the ten frames of `marketing/steam/screenshots/` (1920x1080, each an exact x6 of 320x180: the script
refuses a frame that is not). When `farstrand-press-kit/press-kit/screenshots/` fills up, edit `tools/shots.json`
(slugs stay, file names change) and run with `--shots-dir <that folder>`; the markup needs only a caption and
alt text per new slug.

## Social preview

`public/og-farstrand.png` is a temporary 1200x630 card: the title backdrop at x4 (a 300x158 window, one pixel row cut
top and bottom), the logo and `A HELIOBANE METROIDVANIA` in Public Pixel at x4, all palette colours. When the key
art and `press-kit/social/` exist, replace it and, if the file name changes, the `og:image` and `twitter:image`
URLs and the VideoGame `image` (HELIOBANE versioned the name to bust caches). Open Graph carries the real size and
type, Twitter explicit title, description and alt text, all absolute HTTPS URLs.

## Validation done

`html-validate@9` clean on `index.html` and `privacy/index.html`; `tests/test_site.py` green (a skip of the font test
only under a Python without fontTools); every `public/` reference resolves (the trailer files and `press-kit/` are
the declared exceptions); a headless Chrome (155, no window, software rendering) at 1920, 1440, 1280, 1024, 800,
768, 720, 640, 560, 420, 390, 375, 360 and 320 px in EN, JA and TR for horizontal overflow (none from 360 up, at any
language), every pixel image's scale (whole numbers from 360 up), the toy with mouse and the `Q` and `K` keys (every
rung of the ladder and every caption, and that keys do nothing off screen), the viewer with mouse, arrows and Escape
(focus returns to the current thumbnail; x4, x5, x3, x1 and the x6 file at 1440, 1920, 1280, 390 and 2560 px), the
trailer missing and present, and `prefers-reduced-motion` (no animation, the toy holds still). Full-page screenshots
were read at 1440 in all three languages and at 360 and 390.

## Press kit

`press-kit/` is linked from the fact sheet and the Links row but does not exist yet. It comes from
`../farstrand-press-kit/press-kit/` once the lead has built it (rsync it in, run that repo's tool-name grep first;
public text never names AI tools, models or vendors). Add it to `sitemap.xml` then.
