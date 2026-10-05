# PROGRESS

Book: *Trading Crypto Futures with AI Agents: TradingView MCP, Binance MCP and Your Own Bot*
Last updated: 5 October 2026

## Status

| Step | Item | Status | Output |
|---|---|---|---|
| 1 | Project structure, style guide, glossary, build pipeline | Done | `STYLE_GUIDE.md`, `book/glossary.md`, `build/build_docx.py`, `code/common/` |
| 2 | Preface and detailed outline | **Done, waiting for your approval** | `book/00_preface.md`, `book/00_outline.md`, `build/output/00_preface_and_outline.docx` (+ `.pdf`) |
| 3 | Chapter 1. Binance MCP: trading by prompt | Not started (needs your tool list) | |
| 3 | Chapter 2. TradingView MCP: analysing the market by prompt | Not started (needs your tool list) | |
| 3 | Chapter 3. Futures mechanics and risk maths | Not started | |
| 3 | Chapter 4. Pine Script strategies with AI | Not started | |
| 3 | Chapter 5. Backtesting honestly | Not started | |
| 3 | Chapter 6. Research with Python and SQL | Not started | |
| 3 | Chapter 7. The bridge: TradingView signal to Binance order | Not started | |
| 3 | Chapter 8. Engineering a reliable bot | Not started | |
| 3 | Chapter 9. Launching an AI agent | Not started | |
| 3 | Chapter 10. The new technology landscape | Not started | |
| 3 | Chapter 11. Growing Rs 1,00,000 responsibly | Not started | |
| 3 | Chapter 12. Capstone and career | Not started | |
| 5 | Combined book (.docx with cover, TOC, glossary, prompt index) and PDF | Not started | |

## Open questions for Subodh

1. **MCP tool lists (needed before Chapters 1 and 2).** No TradingView or Binance MCP tools are
   connected to the session that writes this book, so the real tool names must come from you.
   In Claude Code, run `/mcp`, pick each server and open its tool list, or paste the read-only
   prompt from the Preface into Claude and copy the answer. Please also say which TradingView
   MCP project you installed (GitHub link and version), because several community projects exist
   with different tool names.
2. **Which Claude app** do you use with the MCP servers: Claude Code (terminal) or Claude Desktop?
   Windows or macOS? Setup steps and screenshots differ.
3. **Network access for research and real data.** The writing environment currently blocks
   binance.com, developers.binance.com, tradingview.com, the income tax portals, sebi.gov.in and
   all market-data APIs. Search and GitHub work. If you can, add these to the environment's
   allowed domains (cloud environment settings > Network access):
   `developers.binance.com`, `www.binance.com`, `data.binance.vision`, `fapi.binance.com`,
   `demo-fapi.binance.com`, `www.tradingview.com`, `www.incometax.gov.in`,
   `incometaxindia.gov.in`, `www.sebi.gov.in`, `core.telegram.org`, `fastapi.tiangolo.com`.
   Without them, charts use clearly labelled SIMULATED data and facts stay marked "Not verified".
   (Binance's live API may still refuse requests from some server locations; the bulk-data site
   data.binance.vision is the most likely to work.)
4. **Pine Script compile checks.** TradingView cannot be reached from the writing environment, so
   Chapter 4's Pine files will be marked "compile pending" until you run one compile prompt through
   your TradingView MCP and paste the result. Is that OK?
5. **Outline approval.** Any chapters to add, drop, merge or re-order? Are the page targets right?

## Facts not yet verified against an official source

Each item will be re-checked when its chapter is written. "Source used" is what the current text
relies on.

| # | Fact | Used in | Source used | Where to verify |
|---|---|---|---|---|
| 1 | Binance Agent OS and the Binance MCP Server launched 20 August 2026; parts: APIs, Wallet Agentic Hub, x402, Skill Hub, MCP | Preface, Ch1 | Press release text via search results (PR Newswire, AAP) | binance.com announcements; developers.binance.com Agent-native section |
| 2 | MCP endpoint `https://agent.binance.com/mcp/agentic`; OAuth login on Binance's page | Ch1 | Search results; a community GitHub repo | developers.binance.com/en/docs/agent-native/mcp-server/agentic |
| 3 | Agentic subaccount: no external withdrawals; agent cannot move money from the main account; can trade spot, margin, convert, USDS-M and COIN-M futures and move funds between wallets inside the subaccount | Preface, Ch1 | crypto.news and Binance press text via search results | Binance MCP docs and FAQ |
| 4 | Write actions (orders, transfers) need confirmation on the Binance side | Ch1 | Secondary sources and a community repo | Binance MCP docs |
| 5 | Binance MCP tool names (a community repo shows names like `futures_usds.newOrder`) | Ch1 | Community GitHub repo only | Your own `/mcp` tool list |
| 6 | Agent OS availability for Indian accounts | Ch1 | Not found | Binance app / support |
| 7 | TradingView webhooks need a paid plan (Essential or higher) and 2FA; only ports 80 and 443 | Preface, Ch7 | TradingView Help Center text via search results | tradingview.com/support (webhook article) |
| 8 | TradingView Essential alert limits | Ch2, Ch7 | Third-party blogs | tradingview.com/pricing |
| 9 | Binance USDS-M futures testnet REST base `https://demo-fapi.binance.com` | Ch8 | Binance official SDK listing on PyPI via search results | developers.binance.com (USDS-M Futures, General Info) |
| 10 | Futures conditional orders (stop, take-profit) moved to a separate algo-order API in late 2025 | Ch1, Ch7, Ch8 | Author's memory, not confirmed | Binance USDS-M change log |
| 11 | India: 30% VDA tax + 4% cess; 1% TDS; under the Income-tax Act 2025 (from 1 April 2026) the sections are reported as 194 (tax) and 393 (TDS) | Ch11 | Tax websites via search results | incometax.gov.in; CBDT; the Act text |
| 12 | No CBDT clarification yet on crypto futures; conservative practice treats them as VDA income | Ch11 | Tax websites via search results | CBDT circulars; a chartered accountant |
| 13 | 18% GST on exchange trading fees | Ch11 | Third-party blogs | CBIC / exchange fee pages |
| 14 | SEBI FY2024-25: over 91% of individual equity F&O traders made losses; average loss about Rs 1.1 lakh | Preface | Business Standard (7 July 2025), Value Research | sebi.gov.in study |
| 15 | USDT/INR about Rs 96-101 on 4-5 October 2026 (book uses Rs 100) | Preface | App/aggregator quotes via search results | Live rate on your exchange |
| 16 | Binance registered with FIU-IND in 2024 | Ch10, Ch11 | TechCrunch, FXStreet via search results | fiuindia.gov.in |

Verified from primary sources so far:
- Binance Skills Hub is at `github.com/binance/binance-skills-hub`, installs with
  `npx skills add https://github.com/binance/binance-skills-hub`, and needs Node.js 22+ (read on
  GitHub, 5 Oct 2026).
- The `tradesdontlie/tradingview-mcp` project controls TradingView Desktop through the Chrome
  DevTools Protocol on port 9222, is MIT-licensed, is not affiliated with TradingView, and lists
  tools such as `chart_set_symbol`, `data_get_ohlcv`, `pine_smart_compile`, `replay_start`,
  `alert_create` and `capture_screenshot` (read on GitHub, 5 Oct 2026). Your installed project may
  differ.

## Decisions log

| Date | Decision |
|---|---|
| 5 Oct 2026 | Book sources are Markdown in `book/`; Word files are built with python-docx by `build/build_docx.py`; PDFs via LibreOffice. |
| 5 Oct 2026 | A4 pages; Cambria body, Calibri headings, Consolas code (Caladea/Carlito used for PDF rendering on Linux). |
| 5 Oct 2026 | Illustrative exchange rate 1 USDT = Rs 100; default example risk 1% (Rs 1,000). |
| 5 Oct 2026 | Chart palette: validated colour-blind-safe categorical order (see `STYLE_GUIDE.md` section 5). |
| 5 Oct 2026 | All code in the book is included from tested files; untested code is labelled UNTESTED. |
