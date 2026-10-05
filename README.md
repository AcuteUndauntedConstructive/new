# Trading Crypto Futures with AI Agents

*TradingView MCP, Binance MCP and Your Own Bot* — a practical book written chapter by chapter
for one reader (Subodh), built as Word documents with real graphs and diagrams.

Education only, not financial advice.

## Project layout

```
book/                 Markdown sources: preface, outline, chapters, glossary
  00_preface.md
  00_outline.md
  glossary.md
figures/              Generated PNG figures (front/, ch01/ ... ch12/)
code/
  common/             Shared chart style (bookstyle.py) and diagram helpers (diagrams.py)
  front/              Scripts for the preface figures
  ch01/ ... ch12/     Runnable code for each chapter (Python, Pine Script v6, SQL)
build/
  build_docx.py       Markdown -> .docx builder (python-docx), optional PDF export
  setup_build_env.sh  Installs fonts and LibreOffice Writer for PDF export
  output/             Built .docx and .pdf files
STYLE_GUIDE.md        Fonts, headings, chart palette, prompt-box style, chapter template
PROGRESS.md           Done chapters, open questions, facts not yet verified
.env.example          Names of the environment variables the code reads (no values)
```

## Build

```bash
pip install -r requirements.txt
bash build/setup_build_env.sh             # fonts + LibreOffice Writer (only needed for PDF)
python code/front/make_front_figures.py   # regenerate the preface figures
python build/build_docx.py book/00_preface.md book/00_outline.md \
       -o build/output/00_preface_and_outline.docx --pdf
```

Chapters are built the same way, for example
`python build/build_docx.py book/ch03.md -o build/output/ch03.docx --pdf`.
The Markdown features the builder understands (prompt boxes, code includes, callouts, numbered
figures and tables) are listed at the top of `build/build_docx.py` and in `STYLE_GUIDE.md`.

## Safety

- Never put API keys or secrets in any file. Copy `.env.example` to `.env` and fill it in
  locally; `.env` is ignored by git.
- All exercises run on the Binance testnet or at minimum order size first.
