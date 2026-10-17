# FARSTRAND: Steam graphical assets

Full game AppID **5461390**, free demo AppID **5461420**.
Sizes are Steamworks' current ones (Store Assets / Library Assets pages, 2026).

## Full game (5461390)

| File | Steamworks slot | Size |
|---|---|---|
| `steam/header_capsule.png` | Store Assets → Header Capsule | 920×430 |
| `steam/small_capsule.png` | Store Assets → Small Capsule | 462×174 |
| `steam/main_capsule.png` | Store Assets → Main Capsule | 1232×706 |
| `steam/vertical_capsule.png` | Store Assets → Vertical Capsule | 748×896 |
| `steam/page_background.png` | Store Assets → Page Background | 1438×810 |
| `steam/library_capsule.png` | Library Assets → Library Capsule | 600×900 |
| `steam/library_header.png` | Library Assets → Library Header | 920×430 |
| `steam/library_hero.png` | Library Assets → Library Hero (no text, no logo) | 3840×1240 |
| `steam/library_logo.png` | Library Assets → Library Logo (transparent PNG) | 1280×720 |
| `steam/community_icon.jpg` | Installation → Client Images → Community Icon | 184×184 |
| `steam/client_icon.ico` | Installation → Client Images → Client Icon | 16 + 32 (.ico) |
| `steam/client_image_16.tga` | Installation → Client Images → Client Image (if asked) | 16×16 |
| `steam/linux_icons.zip` | Installation → Client Images → Linux Client Icons | 16, 24, 32, 48, 64, 96, 128, 256 |
| `steam/client_icon_32.png` | the client icon as PNG, for reference | 32×32 |
| `steam/app-icon/farstrand_{16…256}.png`, `farstrand.ico` | the app/shortcut icon at every size, and as one .ico | 16 to 256 |
| `steam/event_cover.png` | Events & Announcements → Cover image | 800×450 |
| `steam/event_header.png` | Events & Announcements → Header image | 1920×622 |
| `steam-screenshots/` | Store Assets → Screenshots (see that folder) | 1920×1080 each |

The capsules carry the logo only. The line "A HELIOBANE METROIDVANIA" is on the key art and the logo lockup
files, not on the capsules, so the logo stays readable at the small capsule's 231×87 display size.

Library logo placement: the logo is the in-game logo at ×5 (1200×200), centred on the transparent 1280×720. In the
library logo editor put it bottom left, over the frozen plain left of Hesper (the hero's lower left is quiet ice and
a row of dark trees). The hero keeps Hesper and the red sun in the centre third, so they survive every crop
Steam makes.

## Demo (5461420)

Same slots, with **DEMO** in the game's gold title font in the corner of the capsules and the library capsule and
header. The hero, page background and icons are the full game's (Steam forbids text on the hero). The demo's
library logo reads FARSTRAND with DEMO under its right end, outlined so it holds over any hero.

| File | Steamworks slot | Size |
|---|---|---|
| `steam/demo/header_capsule.png` | Header Capsule | 920×430 |
| `steam/demo/small_capsule.png` | Small Capsule | 462×174 |
| `steam/demo/main_capsule.png` | Main Capsule | 1232×706 |
| `steam/demo/vertical_capsule.png` | Vertical Capsule | 748×896 |
| `steam/demo/library_capsule.png` | Library Capsule | 600×900 |
| `steam/demo/library_header.png` | Library Header | 920×430 |
| `steam/demo/library_hero.png` | Library Hero (same as the full game's) | 3840×1240 |
| `steam/demo/library_logo.png` | Library Logo (FARSTRAND, DEMO under it) | 1280×720 |
| page background, icons | reuse the full game's files | |

## What is on them

- Header, main, event cover: Hesper Lind on a ridge of black glass, the Graft (her glass left arm, veined with dull
  gold) against the red dwarf, Bob at her shoulder, the strand rising into the dark.
- Small capsule: the logo fills the width (460 of 462 px, which Steam asks the uploader to confirm) along the bottom,
  and Hesper stands above it with her legs behind the logo, the Graft held out against the red dwarf. The demo's has
  DEMO in the top left corner.
- Event header, library hero: the same scene cut wide (Hesper right of centre on the event header, dead centre on the
  library hero).
- Vertical and library capsule: the same scene tall, the strand climbing to the logo.

## Checks done

- Sizes: every file matches the tables (`tools/check.py`, which also fails on a missing file).
- Palette: every PNG uses only the game's 32 colours (0 off-palette pixels on all of them).
- Pixel scaling: integer nearest-neighbour only. Capsules use ×2 (small, library capsule), ×3 (header, library
  header, vertical, event cover), ×4 (main), ×5 (page background, library logo), ×6 (event header) or ×8 (library
  hero) of a native canvas; the icons are ×4 of 46 px (community) and ×1 to ×8 of the 32 px icon.
- Legibility: the small capsule was checked at 462×174 and at 231×87 (its 1× display size): the logo reads, and
  Hesper, the cyan visor slit and the gold on the Graft read. Its logo's ink is 230 of 231 native pixels wide (460 of 462),
  the width Steam asks for; the demo's DEMO is legible in its corner.
