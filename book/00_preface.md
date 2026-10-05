---
label: DRAFT FOR REVIEW · OCTOBER 2026
title: Trading Crypto Futures with AI Agents
subtitle: TradingView MCP, Binance MCP and Your Own Bot
author: Preface and detailed outline · written for Subodh, Delhi
note: Education only, not financial advice. Leveraged crypto trading can lose more money than you expect, and most retail traders who use leverage lose money.
header: Trading Crypto Futures with AI Agents · Preface and Outline
---

# Preface

This book teaches you to trade crypto futures with AI tools in a careful, testable way. You will
use Claude to read charts through TradingView, to place and manage orders on Binance through the
official Binance MCP server, and finally to run your own small trading bot. At every step the goal
is the same: understand the mechanism, measure the risk, test on fake money or the smallest size,
and only then use real capital.

It is written for one reader. You are a third-year BMS (finance) student in Delhi. You work as a
mutual fund distributor, you are aiming for the CFA programme and a career in fund management,
and you already write Python, Pine Script, SQL and some Rust. You have Rs 1,00,000 of trading
capital and you trade crypto futures on Binance. Every example in the book is sized for that
account.

## What you will build

By the end of the book you will have a complete, working system. Figure P.1 shows all of it on
one page, and each chapter builds one part.

![Figure P.1. The complete system. Top: you analyse with TradingView through Claude and trade by prompt through the Binance MCP server, approving every action. Bottom: the automated path from a TradingView alert to a Binance order, guarded by a risk engine.](figures/front/figP-01-system.png)

The top half of Figure P.1 is **trading by prompt**. A **prompt** is the instruction you type to
an AI model. Claude talks to two **MCP servers**. MCP (Model Context Protocol) is an open standard
that lets an AI app connect to outside tools in one common way; an MCP server is the program that
offers those tools. One server controls TradingView Desktop on your own computer, so Claude can
read prices and indicators, draw levels and run Pine Script. The other is Binance's own MCP
server, so Claude can read your balances and place orders, but only inside a separately funded
**Agentic subaccount**: a Binance subaccount you fund yourself and assign to the AI, which
(according to Binance's launch material) cannot withdraw money to outside addresses.

The bottom half is **automation**. A Pine Script strategy on TradingView sends an alert as a
**webhook** (an HTTP message sent to your web address when an event happens). Your own Python
server receives it, checks a secret token, sizes the trade, passes it through a risk engine, and
only then sends orders to the Binance Futures API. A journal database records everything and
Telegram tells you what happened.

## How the book is organised

The book has 4 units and 12 chapters. Figure P.2 shows the order in which they build on each
other.

![Figure P.2. The roadmap: four units, twelve chapters. Risk control runs underneath all of them.](figures/front/figP-02-roadmap.png)

- **Unit I, The tools and your first trades (Chapters 1-3).** You connect Claude to Binance and
  to TradingView, and you learn the mechanics and maths of perpetual futures: funding, leverage,
  margin modes, liquidation and position sizing.
- **Unit II, Building and testing strategies (Chapters 4-6).** You write three Pine Script
  strategies with Claude's help, learn to backtest honestly, and build a research toolkit in
  Python and SQL.
- **Unit III, Automation (Chapters 7-9).** You build the bridge from a TradingView alert to a
  Binance order, engineer it to be reliable, and then add AI agents for research and monitoring,
  with a human approving every trade.
- **Unit IV, Growth and the road ahead (Chapters 10-12).** You separate real edge from hype in
  new tools, plan how to grow capital in stages, handle Indian tax and records, and finish with a
  capstone review and a career portfolio.

## How each chapter works

Every chapter follows the same pattern, so you always know where to look:

1. **Learning goals**: 3 to 5 things you will be able to do.
2. **Concepts from the basics**, with worked examples in rupees and USDT for a Rs 1,00,000
   account.
3. **Copy-paste prompts** in blue boxes. After each one: what the tool does, and what a good
   response looks like.
4. **Complete code** (Python, Pine Script v6, SQL) included from files that were run or
   compile-checked. Anything that could not be tested is marked UNTESTED.
5. **At least four figures**: graphs from real or clearly labelled simulated data, and diagrams.
6. **Common mistakes**, a **hands-on exercise** with a checklist, and a **5-question self-test**
   with answers.

## The honest maths of leveraged trading

Before any tool, one fact: **most retail traders who use leverage lose money.** The best large
study of retail derivatives traders in India is SEBI's study of individual traders in equity
futures and options. For the financial year 2024-25 it reported that more than 91% of individual
traders made net losses, with an average loss of about Rs 1.1 lakh per trader. That study covers
Indian equity derivatives, not crypto, but crypto futures have the same features that hurt retail
traders (leverage, fees, fast moves) and run 24 hours a day.

> [!UNVERIFIED] SEBI figures
> The SEBI numbers above are as reported by Business Standard (7 July 2025) and Value Research.
> The sebi.gov.in site could not be opened from the writing environment. Check the original
> study on sebi.gov.in under Reports and Statistics before quoting it.

Two simple pieces of maths explain much of why. The first is that losses hurt more than gains
help. If Rs 1,00,000 falls to Rs 50,000 (a 50% loss), you need a 100% gain just to get back to
where you started. Figure P.3 shows this curve.

![Figure P.3. The gain needed to recover from a loss grows faster than the loss itself.](figures/front/figP-03-recovery.png)

The second is that the amount you risk on each trade matters more than almost anything else.
Figure P.4 takes one simulated strategy that genuinely has an edge: it wins 45% of trades, wins
1.5 times what it risks, and so makes +0.125R per trade on average (**R** is the amount you risk
on one trade; risking Rs 1,000 and making Rs 1,500 is +1.5R). Only the risk per trade changes.

![Figure P.4. The same winning strategy, simulated 10,000 times over 200 trades. At 1% risk per trade the typical worst fall is about 12%; at 10% risk it is about 78%, and a 50% fall is almost certain.](figures/front/figP-04-risk-drawdown.png)

Read Figure P.4 slowly. At 1% risk per trade (Rs 1,000 on a Rs 1,00,000 account), the typical
largest fall from a peak is about 12%, and in the unlucky 5% of paths about 21%. At 5% risk the
typical fall is about half the account, and in nearly half the paths the account falls 50% or
more at some point. At 10% risk a 50% fall happens in about 99% of paths. The strategy did not
change; only the bet size did. Real strategies are usually weaker than this one, and real
markets have fat tails (rare, very large moves) that this simple simulation leaves out.

That is why this book puts risk control ahead of returns in every chapter, and why it never
promises profits, "financial freedom" or fast growth. Where returns are discussed (Chapter 11),
you will see realistic compounding maths together with the drawdowns that come with it.

## Safety rules used in this book

These rules apply in every chapter. They are not optional.

1. **Fake money or minimum size first.** Every exercise starts on the Binance Futures testnet
   (Binance's practice environment with fake funds) or at the smallest order size the exchange
   allows.
2. **The AI never trades without you.** Prompts that could change your account ask Claude to
   show a summary and wait for your explicit confirmation. You approve each order yourself.
3. **Separate, small pots of money.** The Agentic subaccount and the bot's subaccount hold only
   what you can afford to lose completely. Your main account is never connected to automation.
4. **No secrets in files.** API keys live in environment variables. The project ships an
   `.env.example` file with empty values; your real `.env` is never committed or shared.
5. **No withdrawal permission, ever.** API keys used by bots are created without withdrawal
   rights and, where possible, restricted to your server's IP address.
6. **Limits outside the AI.** Daily loss limits, maximum position size and a kill switch live in
   code and in account funding, not in a prompt the model might misread.
7. **The author never trades for you.** While writing this book, Claude does not place, modify
   or cancel any real order. All examples are illustrative or run on testnet.

## Conventions

Table P.1 lists the conventions used throughout the book.

Table P.1. Conventions used in this book.
| Item | Convention |
|---|---|
| Rupees | Indian grouping: Rs 1,00,000; Rs 12,500 |
| USDT | 1,000.00 USDT; Binance futures are priced in USDT |
| Exchange rate | **1 USDT = Rs 100** for easy maths. App quotes on 4-5 October 2026 were about Rs 96 to Rs 101. Always check the live rate. |
| Prices in examples | Labelled "illustrative" unless they come from a dated data source |
| Times | UTC for exchange data, IST for your daily routine; always labelled |
| Default risk | 1% of equity per trade (Rs 1,000 = 10 USDT) in worked examples |
| Code | Python 3.11+, Pine Script v6, SQLite. Files live in `code/chXX/` |
| Figures | Numbered per chapter (Figure 3.2); every chart says whether data is real or SIMULATED |

You will meet five kinds of boxes. A blue **prompt box** holds text to copy into Claude. A grey
**code box** holds a program. Coloured callouts mark a **Risk**, a **Note**, a **Tip**, a
**Checklist**, or a fact that is **Not verified**. Here is what a prompt box looks like:

```prompt Binance MCP (read-only)
List the MCP tools you can see from the Binance server, grouped by area
(market data, account, spot, futures, margin, convert). For each tool give its
exact name and say whether it only reads data or can change my account.
Do not call any tool that places, changes or cancels an order.
```

**What the tool does.** Nothing is called on Binance; Claude reads the tool list its MCP client
already received when it connected. **A good response looks like** a grouped table of exact tool
names with a clear "read" or "write" label. A red flag is any tool name Claude cannot show you
from the actual list, which means it is guessing.

## How facts were checked

Crypto tools change monthly. Every chapter is researched just before it is written, using
official sources first: the Binance developer documentation and announcements, the TradingView
Pine Script reference and Help Center, the Income Tax Department and CBDT, and Anthropic's
documentation for Claude. Each chapter ends with a "Sources and verification" list with the date
each source was checked.

When something could not be verified against an official source, the text says so in a
**Not verified** callout and tells you where to check. The project file `PROGRESS.md` keeps a
running list of these items. For this preface and outline, several official sites
(binance.com, developers.binance.com, tradingview.com and the income tax portal) could not be
opened from the writing environment, so facts about them were taken from search results and
public GitHub repositories and are marked for re-checking.

The tool names in the prompts come from your own installed MCP servers. Before Chapter 1 is
written, you will paste the exact tool lists from your TradingView MCP and Binance MCP servers,
and every prompt will be written against those names.

## What you need before Chapter 1

- [ ] A Binance account with KYC done and two-factor authentication (2FA) switched on.
- [ ] Access to Binance Agent OS and an Agentic subaccount (check availability for Indian users in the Binance app).
- [ ] Claude Code or Claude Desktop, signed in, able to add MCP servers.
- [ ] TradingView Desktop and a TradingView MCP server installed and connected to Claude.
- [ ] Python 3.11 or newer, Node.js, Git, and a code editor such as VS Code.
- [ ] A Binance Futures testnet (demo trading) account for the practice exercises.
- [ ] A TradingView Essential plan (or higher) by Unit III, for webhook alerts.

> [!RISK] Education, not financial advice
> This book is for education only. It is not financial, investment, legal or tax advice, and
> nothing in it is a recommendation to buy or sell any asset. Crypto futures are high-risk,
> leveraged products; you can lose all the money you put in. Indian tax treatment of crypto
> futures is not fully settled; consult a chartered accountant for your own situation. You are
> responsible for your own trades.
