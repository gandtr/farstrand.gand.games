# FARSTRAND: press kit

A sci-fi metroidvania set seven years after HELIOBANE: map six worlds on frozen star roads with an arm that moves heat. FARSTRAND is made by **Gand**.
Everything in this kit may be used for coverage, previews, reviews and storefronts. Credit line:
**"FARSTRAND, a game by Gand (https://farstrand.gand.games)"**. Press contact: contact@gand.games.

The press page is `doc.html` (English, 日本語 and Türkçe in one file). The whole kit is also one archive:
`farstrand-press-kit_2026-10-17.zip`.

## Folders

| Folder | What |
|---|---|
| `doc.html` | the press page: fact sheet, features, trailer, history, screenshots, art and logos, contact (EN / 日本語 / TÜRKÇE) |
| `factsheet.md`, `factsheet.ja.md`, `factsheet.tr.md` | the same facts as plain text, in three languages |
| `key-art/` | `key_art.png` 1920×1080 and `key_art_4k.png` 3840×2160 (Hesper, with the logo and lockup), `key_art_no_logo.png`, `key_art_vertical.png` 1200×1800 (and `_no_logo`), `key_art_road*.png` (the *Plumbline* on a strand), `key_art_mott*.png` (Old Mott's stall) |
| `logo/` | the logo, transparent PNG at ×1 to ×8; `farstrand_lockup_*` with the line A HELIOBANE METROIDVANIA; on dark |
| `screenshots/` | 22 in-game frames at 1920×1080 (the twelve on the Steam page and ten more); `native/` has the 320×180 originals, `native/demo/` the demo's |
| `steam-screenshots/` | the twelve Steam screenshots in store order, 1920×1080; `demo/` for the demo's eight |
| `steam/` | Steam capsules, library images, icons and event images; `steam/demo/` for the demo. Sizes in `steam/ASSETS.md` |
| `icons/` | app icon 32–512 px, native 16 to 48 px, `.ico`, 184 px community icon |
| `social/` | `og_1200x630.png` link card, `card_1200x675.png` |
| `video/` | the trailer (87 s, 1920×1080, 60 fps, H.264), English captions (`.srt`, `.vtt`), poster, thumbnail |
| `fonts/` | Public Pixel (CC0), the game's pixel font; Fira Sans Condensed (OFL) and PixelMplus12 (M+ licence), used by `doc.html` |

## About the images

Screenshots are real in-game frames: the game draws at 320×180 and they are scaled by exactly 6 (1920×1080), which is
how it looks full-screen on a 1080p display. `native/` has the unscaled 320×180 frames.

The logo is the game's own. The key art and capsules are painted with an image generator, then run through the game's
palette pipeline: scaled to a small pixel canvas, dithered to the game's 32 colours and enlarged by a whole number.
They show the game's own characters, colours and fonts.

All pixel art is scaled by whole numbers with nearest-neighbour. If you resize it, please do the same, or start from
the ×1 files in `logo/` and `screenshots/native/`.
