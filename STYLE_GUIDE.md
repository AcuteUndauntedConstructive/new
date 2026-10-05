# Style Guide

Book: *Trading Crypto Futures with AI Agents: TradingView MCP, Binance MCP and Your Own Bot*

This guide fixes how every chapter looks and reads, so the 12 chapters feel like one book.
The Word builder (`build/build_docx.py`) and the chart module (`code/common/bookstyle.py`)
implement these rules in code. If you change a value here, change it there too.

---

## 1. Voice and language

- Write for one reader: Subodh, a 3rd-year BMS (finance) student in Delhi who knows Python,
  Pine Script, SQL and basic Rust, and trades crypto futures with Rs 1,00,000.
- Simple, clear English. Short sentences. One idea per paragraph.
- Start every topic from the basics, then go deep. Plain words first, jargon second.
- **Define every term the first time it appears**, in bold, followed by a one-line meaning.
  Add it to `book/glossary.md` with the chapter where it first appears.
- Use "you" for the reader. Use "we" only for steps we do together in an exercise.
- Avoid hype words: "guaranteed", "passive income", "financial freedom", "to the moon",
  "easy money". Never promise returns.
- Risk comes before reward in every section that discusses a trade or a strategy.
- Use commas and colons rather than long dashes. Keep sentences under about 25 words.
- Dates: "5 October 2026". Times: 24-hour with zone, for example "09:30 IST" or "04:00 UTC".
  Binance and TradingView data are in UTC; say so whenever a time appears.

## 2. Money, numbers and units

| Item | Rule | Example |
|---|---|---|
| Rupees | "Rs" + Indian digit grouping | Rs 1,00,000 · Rs 2,500 · Rs 12,34,567 |
| USDT | Western grouping, 2 decimals for money, symbol after | 1,000.00 USDT · 10.00 USDT |
| Exchange rate | Book-wide illustrative rate **1 USDT = Rs 100** (app quotes on 4-5 Oct 2026 were about Rs 96-101). Always tell the reader to check the live rate. | 1,000 USDT ≈ Rs 1,00,000 |
| Percentages | No space; 2 decimals only when needed | 1% · 0.05% · 0.0100% (funding) |
| Prices | Illustrative prices are labelled "illustrative" | "BTC at 60,000 USDT (illustrative)" |
| Crypto quantity | Respect step size in examples | 0.016 BTC, not 0.01613 BTC |

Worked examples always use an account of Rs 1,00,000 (1,000 USDT) unless the text says otherwise.
Default risk per trade in examples: **1% of equity (Rs 1,000 = 10 USDT)**. Never more than 2% in
any example.

## 3. Page layout (Word)

- Paper: A4 portrait. Margins: 2.5 cm left/right, 2.2 cm top/bottom. Text width 16 cm.
- Header: book short title, right aligned, 8 pt grey. Footer: page number, centred.
- Each chapter starts on a new page with a title page block (unit label, chapter title).

## 4. Fonts and heading styles

| Element | Font | Size | Colour | Notes |
|---|---|---|---|---|
| Body text | Cambria | 11 pt, line spacing 1.2 | ink `#0B0B0B` | 6 pt after |
| Heading 1 (chapter) | Calibri bold | 24 pt | navy `#14213D` | new page |
| Heading 2 (section, "3.4 ...") | Calibri bold | 15 pt | blue `#1C5CAB` | 16 pt before |
| Heading 3 (subsection) | Calibri bold | 12.5 pt | ink | 12 pt before |
| Heading 4 | Calibri bold | 11 pt | grey `#52514E` | |
| Code | Consolas | 8.5 pt | ink | grey box |
| Prompt text | Calibri | 10.5 pt | ink | blue box |
| Captions | Calibri | 9 pt | grey; "Figure 3.2." in bold ink | below figures, above tables |
| Table text | Calibri | 9.5 pt | ink | header row shaded `#DCE8F7` |

When the PDF is made on Linux, Carlito and Caladea (metric twins of Calibri and Cambria) are
used, so line breaks match Word.

Section numbering: H2 headings carry the chapter number, for example "3.4 Isolated vs cross
margin". Fixed end sections in every chapter: "Common mistakes", "Hands-on exercise",
"Self-test", "Answers".

## 5. Colour palette for charts

The categorical palette is a validated, colour-blind-safe order (checked with a palette
validator: adjacent-pair CVD ΔE ≥ 9.1, normal-vision ΔE ≥ 19.6). Use slots **in this fixed
order**; never cycle colours or invent a ninth.

| Slot | Name | Hex | Typical use |
|---|---|---|---|
| 1 | blue | `#2A78D6` | main series, strategy equity |
| 2 | orange | `#EB6834` | comparison series, benchmark |
| 3 | aqua | `#1BAF7A` | third series; up candles (hollow) |
| 4 | yellow | `#EDA100` | fourth series |
| 5 | magenta | `#E87BA4` | fifth series |
| 6 | green | `#008300` | sixth series |
| 7 | violet | `#4A3AA7` | seventh series |
| 8 | red | `#E34948` | eighth series; down candles (filled) |

- Slots 3, 4 and 5 are light on white: whenever they are used, add direct labels or a table.
- **Gains vs losses** (polarity): blue `#2A78D6` vs red `#E34948`, neutral grey `#F0EFEC`.
- **Candles**: up = aqua outline, hollow; down = red, filled. Shape is the second cue, so the
  chart still reads for colour-blind readers and in black-and-white print.
- **Status colours** (reserved, always paired with a text label): good `#0CA30C`,
  warning `#FAB219`, serious `#EC835A`, critical `#D03B3B`.
- Chrome: gridlines `#E1E0D9` hairline solid, axis `#C3C2B7`, axis text `#52514E`, notes `#898781`.
- Text is never drawn in a series colour. Values and labels use ink or grey.

Chart rules:
- One y-axis per chart. Never a dual-axis chart; use two stacked panels instead.
- Line width 1.6 pt; markers ≥ 6 pt with a white ring; bars with a small gap between them.
- A legend whenever there are 2 or more series; a single series has no legend box.
- Label selectively (end values, extremes), never every point.
- Title left-aligned, bold, states the finding ("Fees eat tight-stop strategies"), not just
  the variable names.
- **Every chart carries a source line** bottom-left: either the real data source and date range
  ("Source: Binance USDS-M BTCUSDT 1h klines, 1 Jan-30 Jun 2026, UTC") or
  **"SIMULATED DATA: ... Not market prices."** with the simulation settings.
- Size: 6.3 in (16 cm) wide, saved as PNG at 200 dpi.

## 6. Diagrams

Drawn with matplotlib (`code/common/diagrams.py`): rounded boxes, thin dark-grey arrows,
pale tinted fills so black text always has strong contrast.

| Layer | Fill |
|---|---|
| TradingView side | pale blue `#DCEAFB` |
| Binance side | pale orange `#FDE8D9` |
| Your code / bridge | pale grey `#F0EFEC` |
| AI agent / Claude | pale violet `#E3E0F6` |
| Data stores, logs, alerts | pale aqua `#DCF3E9` |
| Risk controls | pale red `#FBE3E3` |

Diagram kinds: architecture (boxes and arrows), flowcharts (boxes and decision diamonds),
sequence diagrams (lifelines with numbered messages), state machines.

## 7. Figures and tables

- Number figures per chapter: Figure 3.1, 3.2, ... Front matter uses Figure P.1, P.2, ...
- File names: `figures/chXX/figXX-NN-short-name.png` (front matter: `figures/front/figP-NN-...`).
- Each figure is produced by a script in `code/chXX/` (or `code/front/`) so it can be rebuilt.
- Every figure has a caption **and** is referenced in the text before it appears
  ("Figure 3.4 shows ..."). The builder warns if a figure is never referenced.
- At least 4 figures per chapter: a mix of data graphs and diagrams.
- Tables are numbered Table 3.1, 3.2, ... with the caption above the table.

## 8. Boxes: prompts, code and callouts

### Prompt box
Blue box, thick blue left edge, label line "PROMPT · <tool or server>".
- Written to be copied exactly. Plain ASCII quotes, no smart quotes.
- Placeholders in `{CURLY_CAPS}` (shown bold blue), for example `{SYMBOL}`, `{RISK_PCT}`.
- Every prompt that could change an account says so, and asks for a summary and a
  confirmation step before any write action.
- After every prompt box, two short parts follow:
  **What the tool does** (which MCP tools are called, read or write) and
  **A good response looks like** (the shape of a correct answer, and red flags).

### Code box
Grey box, Consolas 8.5 pt, label line "PYTHON · code/ch03/position_size.py".
- Code in the book is included from the tested file (`@include(...)`), never retyped.
- Each file starts with a header comment: purpose, how to run, and test status:
  `Tested: <date>, <environment>` or `UNTESTED: <reason>`.
- Pine Script is v6 (`//@version=6`). SQL is SQLite unless stated.
- No API keys or secrets in any file. Read them from environment variables; ship a
  `.env.example` with empty values.

### Callouts
| Callout | Edge colour | Used for |
|---|---|---|
| RISK | red | anything that can lose money or leak keys |
| NOTE | grey | background, side details |
| TIP | green | shortcuts, good habits |
| NOT VERIFIED | amber | a fact that could not be checked against an official source; says where to check |
| CHECKLIST | blue | step lists the reader ticks off |

Markdown source for these blocks (what the builder understands):

````text
```prompt Binance MCP
Show my USDS-M futures balance in the agentic subaccount. Do not place any order.
```

@include(code/ch03/position_size.py, python)

> [!RISK] Liquidation
> With 20x leverage a 5% move against you can wipe out the position margin.

![Figure 3.4. Liquidation distance shrinks as leverage rises.](figures/ch03/fig03-04-liq-distance.png)

- [ ] I placed the order on testnet, not live.
````

## 9. Fixed chapter template

1. Title block (unit, chapter number, title) and a 2-3 sentence "why this chapter matters".
2. **Learning goals** (3-5 bullets).
3. Concept sections N.1 ... N.k, basics first, each with worked numeric examples in Rs and USDT.
4. Prompts (boxed) with "What the tool does" and "A good response looks like".
5. Code (included from tested files) with how to run it and expected output.
6. At least 4 figures, each referenced in the text.
7. **Common mistakes** (table: mistake, why it hurts, fix).
8. **Hands-on exercise** (testnet or minimum size first) with a tick-box checklist.
9. **Self-test**: 5 questions, then **Answers** with short explanations.
10. **Sources and verification**: official pages used, date checked, and anything not verified.

## 10. Accuracy rules (summary)

- Check official documentation before writing (Binance developer docs, TradingView Pine
  Script docs and Help Center, Indian tax law and CBDT material). Note the date checked.
- Never invent tool names, endpoints, parameters, prices or tax rates. If not verified,
  use a NOT VERIFIED callout and say where to check. Log it in `PROGRESS.md`.
- MCP prompts use the exact tool names from the reader's own installed servers.
- Run every Python script; compile-check every Pine script where possible; anything not
  run is marked UNTESTED.
- The author (Claude) never places, modifies or cancels a real order.
