# farstrand.gand.games

The FARSTRAND site: one static `index.html` (EN / 日本語 / TÜRKÇE), a privacy page, no build step, no third-party
scripts or fonts, GitHub Pages from `main` (`CNAME`, `.nojekyll`). A port of
[heliobane.gand.games](https://heliobane.gand.games/) in FARSTRAND's colours and words. **`PROJECT.md` is the full
description** (structure, design, the toy's rules, content sources, how every file was made, what was checked); this
file is the short version and the open list.

Nothing here is committed, pushed or deployed; DNS is untouched.

## What is where

| Path | What |
|---|---|
| `index.html` | the whole site: markup, one `<style>`, one JS IIFE. Sections `#top #trailer #after #pillars #graft #worlds #heralds #people #screens #facts`, footer, screenshot viewer |
| `privacy/index.html` | privacy policy, English, adapted from HELIOBANE's (Steam only, no accounts of its own) |
| `public/` | art, screenshots, fonts, icons, social card (`PROJECT.md` lists each) |
| `tools/` | `build_media.py`, `build_extras.py`, `subset_fonts.sh`, `shots.json`, `palette.hex` |
| `tests/test_site.py` | `python3 -m unittest discover -s tests -v` (use `/usr/bin/python3` for the font test) |
| `PROJECT.md` | the project notes, HELIOBANE-style |
| `.htmlvalidate.json`, `.claude/launch.json` | validator config; preview on :8151 (`python3 -m http.server 8151`) |

## How it was made, how to rebuild

Everything is made from a snapshot of the game at commit `2e08e64` (`git archive`, never the working tree; no Godot
was run), the press kit's key art, screenshots and icons (`farstrand-press-kit/press-kit/`), the trailer
(`farstrand-trailer`, encode lines in `PROJECT.md`) and the lead's copy (`farstrand-press-kit/copy/`):

```sh
SNAP=<empty dir>
git -C ~/projects/games/farstrand/farstrand archive 2e08e64 | tar -x -C $SNAP
python3 tools/build_media.py --game $SNAP     # art, key art and shots (x6 -> native), icons, toy sprites, stage
python3 tools/build_extras.py --game $SNAP    # frost-vein bars, temporary social card
tools/subset_fonts.sh $SNAP                   # Public Pixel with Turkish, PixelMplus12 for the Japanese in index.html
npx --yes html-validate@9 index.html privacy/index.html
python3 -m unittest discover -s tests
```

Every pixel is one of the game's 32 colours (`tools/palette.hex`, the test checks every file in `public/art/`), shown
only at whole-number scales (measured at 22 widths).

## What was checked

html-validate@9 clean on both pages; the unit tests green; every `public/` reference resolves (declared exception:
`press-kit/`); headless Chrome 155 (no window, no GPU) at 1920, 1440, 1280, 1024,
800, 768, 720, 640, 560, 420, 390, 375, 360 and 320 px in EN, JA and TR: no horizontal scroll from 360 up (320: no
overflow either, but pictures show at a fraction), every pixel image at a whole-number scale from 360 up; the heat
ladder with mouse and with `Q`/`K` (all rungs, all captions); the viewer with mouse, arrows and Escape; the trailer
present (130 s, captions load) and missing (the fallback); `prefers-reduced-motion`; the Steam switch flipped on a
copy. Not checked: Safari and Firefox (Chrome only), a real touch device, a screen reader, any network but loopback.

## TODOs left in the pages

Visible (privacy page, dashed boxes): Steam Cloud wording to confirm; other storefronts if any. In `index.html`, as HTML
comments (nothing visible): the trailer's `uploadDate` (left out on purpose); the demo link under the Steam button; `press-kit/`.
`python3 -m unittest discover -s tests -v` prints them all.

## Open for the lead

1. **Steam**: set `STEAM_LIVE = true` in the script when the store page is public (one line; the UTM URLs are in the
   `STEAM` object above it). The demo line under the button stays plain text until you link it.
2. **Trailer** is in (`public/trailer.mp4` 50 MB, v3.2, `trailer-poster.jpg`, `trailer.en.vtt`; encode lines in `PROJECT.md`). The
   JSON-LD `VideoObject` has **no `uploadDate`** yet; add the real publication instant with its timezone when the
   trailer is published (the test accepts it missing and checks it once present). The page names only an English
   caption track; if the trailer gets Japanese or Turkish captions, give me the files.
3. **Key art, icons, screenshots** are the press kit's now (hero: `key_art_no_logo` at x3 to x6, the tall one on
   phones; `key_art_road` in `#after`; the twelve store screenshots, plus `halm_map` and `the_six` from the spares; icons
   from `icons/`). **Social card, expected path: `press-kit/social/og_1200x630.png`**, which I copy over
   `public/og-farstrand.png` (the temporary card keeps that name, so no meta tag changes; tell me if it ships under
   another name). The card's alt text in the head describes the old one: reread it.
4. **To refresh the media** run `build_media.py` (it refuses any picture that is not an exact x6 or x5 scale); a new
   screenshot slug needs a caption and alt text in the markup (`tools/shots.json`).
5. **Text I wrote, not in the copy** (review the Japanese and Turkish first): the twelve screenshot captions and alt
   texts, every other alt text (portraits, trailer still, road art, pillar art, viewer), nav labels (Graft, Worlds, Heralds,
   Screens, Facts and their JA/TR forms), the skip link, `Language / 言語 / Dil`, the three page titles, the
   Open Graph text, and the whole privacy page. Four captions are the game's own strings (`Kindle it, quench it, climb on`,
   `Halm, the glass forest`, `overfeed one on the plating`, `The network`); the rest use its world, room and Herald
   names. The alt texts avoid the cocoons and the earlier Hespers.
6. **Copy gaps**: the fact sheets are level in all three languages now (Engine, Players, the fuller Platforms row).
   The privacy page is English only, as HELIOBANE's. No `#pillars` heading in the copy: each pillar's title is a
   heading.
7. **Privacy**: facts come from `steam/README.md`, `steam_service.gd` and `end_card.gd`; a search of `game/` and
   `sim/` found no HTTP, socket or telemetry code. Confirm Steam Cloud and the effective date (17 October 2026).
   The contact is `contact@gand.games` (Arda's call, as HELIOBANE's site). The "Children" paragraph is HELIOBANE's.
8. **`press-kit/`** is linked (fact sheet, Links row) and 404s until you sync it in; add it to `sitemap.xml` then.
   JSON-LD `sameAs` already names the Steam page (dead until it is public).
9. **The toy** starts with an empty arm (Quench fills a pip). The ladder alone conserves heat, so from empty it can
   only loop between 0 and 1 pips and never reach sunfed, the burst or a full arm. I added the game's own heat
   source, a lamp-heart (Quench on a frozen enemy takes a pip from it; dim for 3 s). No thaw timers. Delete the
   lamp (see `PROJECT.md`) if you would rather not have it.
10. **Turkish in the pixel font**: Public Pixel squeezes `İ Ş Ğ` under their marks (the game's own fonts do the same),
    so a capital `İ` reads like a small `i`. If Arda dislikes it in headings, one CSS rule sets `.pix:lang(tr)` in the
    body font.
11. The nav has six links (Trailer, Graft, Worlds, Heralds, Screens, Facts). "After HELIOBANE" and "Who's out there" are
    not in it, to keep one row in Turkish at 1241 px; both are one scroll away.
