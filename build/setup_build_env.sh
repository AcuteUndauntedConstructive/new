#!/usr/bin/env bash
# Prepare a fresh Linux machine to build the book's .docx and .pdf files.
# - Carlito and Caladea are metric twins of Calibri and Cambria, so PDF line breaks match Word.
# - LibreOffice Writer is needed for the PDF export (the core package alone cannot open .docx).
set -euo pipefail

mkdir -p "$HOME/.fonts" "$HOME/.config/fontconfig"
base="https://raw.githubusercontent.com/google/fonts/main/ofl"
for f in carlito/Carlito-Regular carlito/Carlito-Bold carlito/Carlito-Italic carlito/Carlito-BoldItalic \
         caladea/Caladea-Regular caladea/Caladea-Bold caladea/Caladea-Italic caladea/Caladea-BoldItalic; do
  out="$HOME/.fonts/$(basename "$f").ttf"
  [ -f "$out" ] || curl -sSfL "$base/$f.ttf" -o "$out"
done

cat > "$HOME/.config/fontconfig/fonts.conf" <<'XML'
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig>
  <dir>~/.fonts</dir>
  <alias binding="same"><family>Consolas</family><prefer><family>DejaVu Sans Mono</family></prefer></alias>
  <alias binding="same"><family>Calibri</family><prefer><family>Carlito</family></prefer></alias>
  <alias binding="same"><family>Cambria</family><prefer><family>Caladea</family></prefer></alias>
</fontconfig>
XML
fc-cache -f >/dev/null
rm -rf "$HOME/.cache/matplotlib"   # let matplotlib see the new fonts

if ! dpkg -s libreoffice-writer >/dev/null 2>&1; then
  apt-get install -y --no-install-recommends libreoffice-writer
fi
echo "Build environment ready."
