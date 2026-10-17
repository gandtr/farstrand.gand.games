#!/bin/sh
# Re-subset the page fonts from the game's own font sources (a snapshot of the game at 2e08e64).
#   tools/subset_fonts.sh <snapshot>
# Public Pixel (CC0): ASCII, Latin-1 and the Turkish letters (İ ı Ş ş Ğ ğ), plus the arrows.
# PixelMplus12 (M+ licence): only the glyphs index.html uses above U+2FFF, plus ASCII and the kana punctuation.
# Fira Sans Condensed (OFL) is copied unchanged from heliobane.gand.games/public/fonts.
set -eu
SNAP="$1"
cd "$(dirname "$0")/.."
pyftsubset "$SNAP/art/src/fonts/PublicPixel.ttf" \
  --unicodes="U+0020-007E,U+00A0-00FF,U+011E,U+011F,U+0130,U+0131,U+015E,U+015F,U+2013,U+2018,U+2019,U+201C,U+201D,U+2022,U+2026,U+2190-2193" \
  --flavor=woff2 --output-file=public/fonts/PublicPixel.woff2
TXT="$(mktemp)"
python3 -c "
s = open('index.html').read()
print(''.join(sorted(set(c for c in s if ord(c) > 0x2FFF))) + '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz .,:;!?()-/&+・·、。「」（）！？：　〜×％%')
" > "$TXT"
pyftsubset "$SNAP/art/src/fonts/ja/PixelMplus12-Regular.ttf" --text-file="$TXT" --flavor=woff2 \
  --output-file=public/fonts/PixelMplus12-ja.woff2
rm -f "$TXT"
ls -l public/fonts/*.woff2
