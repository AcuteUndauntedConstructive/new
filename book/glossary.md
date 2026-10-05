# Glossary

Plain-English meanings of the terms used in this book. "Ch" is the chapter where the term is
first explained. This file grows as each chapter is written; entries marked † will be
re-checked against official documentation when their chapter is written.

| Term | Meaning | Ch |
|---|---|---|
| ADL (auto-deleveraging) | When the insurance fund cannot cover a bankrupt position, the exchange closes some profitable opposite positions automatically. Rare, but possible in violent moves. | 3 |
| Agent (AI agent) | A program in which an AI model chooses and calls tools in a loop to reach a goal, keeping some memory between steps. | 9 |
| Agent OS (Binance) † | Binance's set of tools for AI agents, launched 20 August 2026: its APIs, Wallet Agentic Hub, x402 payments, Skill Hub and an MCP server. | 1 |
| Agentic subaccount † | A Binance subaccount that you fund yourself and assign to an AI agent. Reported rules: it cannot withdraw externally and the agent cannot pull money from your main account. | 1 |
| Alert (TradingView) | A rule on TradingView that fires a notification when a condition is met, for example price crossing a level or a strategy filling an order. | 2 |
| API (application programming interface) | A defined way for one program to ask another for data or actions, for example "give me my open orders". | 1 |
| API key / secret | A pair of long strings that identify your program to an exchange. The secret signs requests; anyone holding both can act within the key's permissions. | 8 |
| ATR (average true range) | The average size of a candle's full range, including gaps, over N bars. Used to set stops that match current volatility. | 2 |
| Backtest | Running a strategy's rules on past prices to see how it would have performed. A backtest is evidence, not proof. | 4 |
| Basis | The gap between a futures price and the spot (index) price. | 3 |
| Bollinger Bands | A moving average with bands placed a set number of standard deviations above and below it. | 4 |
| Candle (OHLCV) | One bar of price data: Open, High, Low, Close and Volume for a time period such as 1 hour. | 2 |
| CDP (Chrome DevTools Protocol) | A debugging interface built into Chromium-based apps. Community TradingView MCP servers use it to control TradingView Desktop locally. | 2 |
| Claude Agent SDK † | Anthropic's library for building your own agents with Claude, the same agent loop that powers Claude Code. | 9 |
| Claude Code | Anthropic's command-line coding agent. It can connect to MCP servers and run tools with your permission. | 1 |
| COIN-M futures | Futures margined and settled in the coin itself (for example BTC), not in USDT. This book uses USDS-M. | 3 |
| Cross margin | One margin pool shared by all positions; a losing position can use the whole futures balance before liquidation. | 3 |
| Drawdown (max drawdown) | The fall from a previous equity peak to a later low, in %. Max drawdown is the largest such fall. | 5 |
| EMA (exponential moving average) | An average of recent prices that gives more weight to newer prices. | 2 |
| Expectancy | Average profit or loss per trade, often in R. Expectancy = win rate x average win - loss rate x average loss. | 5 |
| Funding rate | A periodic payment between long and short holders of a perpetual contract that keeps its price close to the index price. Positive: longs pay shorts. | 3 |
| GTC / IOC / FOK | Time-in-force settings. GTC stays until cancelled; IOC fills what it can now and cancels the rest; FOK fills fully now or cancels completely. | 1 |
| Hedge mode / one-way mode | Position modes on Binance Futures. One-way: one net position per symbol. Hedge: separate long and short positions at the same time. | 1 |
| HTTPS / TLS | Encrypted HTTP. TLS is the encryption layer. Webhook endpoints must use HTTPS. | 7 |
| Index price | A price built from several spot exchanges. Binance uses it to compute the mark price and funding. | 3 |
| Initial margin | The money locked when you open a futures position: notional value / leverage. | 3 |
| In-sample / out-of-sample | Data used to design a strategy (in-sample) versus fresh data kept aside to test it (out-of-sample). | 5 |
| Insurance fund | An exchange fund that absorbs losses when positions are liquidated below their bankruptcy price. | 3 |
| Isolated margin | Margin assigned to one position only; if it is liquidated, only that margin is lost. | 3 |
| JSON | A text format for structured data, for example {"side": "buy", "qty": 0.01}. Used in webhook messages and APIs. | 7 |
| Kill switch | A control that immediately stops a bot, cancels its orders and (optionally) closes positions. | 8 |
| Leverage | Trading a position larger than your margin. 5x leverage means 1,000 USDT notional uses 200 USDT margin. | 3 |
| Limit order | An order to buy or sell at a set price or better. It may not fill. | 1 |
| Liquidation | Forced closing of a position by the exchange when margin falls below the maintenance margin. | 3 |
| Liquidation price | The mark price at which the exchange will liquidate your position. | 3 |
| listenKey † | A token used to open the Binance user-data WebSocket stream that reports your orders and balances. | 8 |
| Lookahead bias | A testing error where the strategy uses information that would not have been known at that time. | 5 |
| Maintenance margin | The minimum margin a position must keep; below it, liquidation starts. | 3 |
| Maker / taker | A maker order adds liquidity to the order book (usually a resting limit order); a taker order removes it (a market order). Taker fees are higher. | 3 |
| Mark price | A fair price Binance uses for unrealised profit and loss and for liquidation, so one odd trade cannot trigger liquidations. | 3 |
| Market order | An order to buy or sell immediately at the best available prices. | 1 |
| MCP (Model Context Protocol) | An open standard that lets AI apps (clients) connect to external tools and data (servers) in one common way. | 1 |
| MCP client / host | The AI app side of MCP, for example Claude Code or Claude Desktop. | 1 |
| MCP server | A program that offers tools (actions) and resources (data) to an MCP client. | 1 |
| MCP tool | One named action an MCP server exposes, with defined inputs, for example "get open orders". | 1 |
| Min notional † | The smallest order value an exchange accepts for a symbol, in USDT. | 3 |
| Monte Carlo simulation | Re-running many random versions of a process (for example shuffled trade sequences) to see the range of possible outcomes. | 6 |
| Notional value | Full size of a position: quantity x price. 0.016 BTC at 60,000 USDT = 960 USDT notional. | 3 |
| OAuth | A login standard that lets you grant an app limited access to an account without giving it your password. | 1 |
| Open interest (OI) | The total number of futures contracts open at a time. | 6 |
| Overfitting | Tuning a strategy so closely to past data that it captures noise and fails on new data. | 5 |
| Perpetual futures (perp) | A futures contract with no expiry date. Funding payments keep its price near the index. | 3 |
| Pine Script | TradingView's programming language for indicators and strategies. This book uses version 6. | 4 |
| Position sizing | Choosing how much to buy or sell so that a stop-loss hit loses only a planned amount. | 3 |
| Post-only | A limit order that is cancelled instead of filling as a taker, so you always pay the maker fee. | 1 |
| Profit factor | Gross profit / gross loss. Above 1 means profits exceeded losses before other costs. | 5 |
| Prompt | The instruction you type to an AI model. | 1 |
| R (R-multiple) | Profit or loss measured in units of the amount you risked. Risk 10 USDT, make 15 USDT = +1.5R. | 3 |
| Rate limit | The maximum number of API requests or orders allowed per time window. | 8 |
| Reconciliation | Regularly comparing what your bot believes (orders, positions) with what the exchange reports, and fixing differences. | 8 |
| Reduce-only | An order flag that only allows the order to shrink or close a position, never to open or increase one. | 1 |
| Regime (market regime) | A period with a typical behaviour: trending, ranging, calm or volatile. | 5 |
| Repainting | When an indicator or strategy shows past signals that differ from what it showed in real time. | 5 |
| Replay mode | A TradingView feature that hides future bars so you can practise bar by bar on past data. | 2 |
| RSI (relative strength index) | A 0-100 oscillator comparing recent gains with recent losses. | 2 |
| Sharpe ratio | Average excess return divided by the volatility of returns. Higher means more return per unit of ups and downs. | 6 |
| Slippage | The difference between the price you expected and the price you got. | 3 |
| Stop-loss | An order that closes a position at a set price to cap the loss. | 1 |
| Strategy Tester | TradingView's panel that backtests Pine Script strategies and shows results and trade lists. | 4 |
| Subaccount | A separate account under your main Binance account, with its own balances. | 1 |
| Take-profit | An order that closes a position at a target price to lock in profit. | 1 |
| TDS (tax deducted at source) † | Tax deducted on a payment before you receive it. India applies 1% TDS on many transfers of crypto (VDAs). | 11 |
| Testnet / demo trading † | Binance's practice environment with fake money and a separate API address. | 8 |
| Tick size / step size | The smallest allowed price change (tick) and quantity change (step) for a symbol. | 3 |
| Timeframe | The period one candle covers: 15m, 1h, 4h, 1D. | 2 |
| USDS-M futures | Binance futures margined and settled in stablecoins such as USDT. Binance writes it "USDⓈ-M". | 3 |
| USDT (Tether) | A stablecoin designed to track 1 US dollar. | 3 |
| VDA (virtual digital asset) † | The Indian tax law term for crypto assets and similar tokens. | 11 |
| VPS (virtual private server) | A rented always-on computer in a data centre where your bot runs. | 8 |
| Walk-forward analysis | Testing by repeatedly optimising on one window of past data and testing on the next unseen window. | 5 |
| Webhook | An HTTP request one system sends to your URL when an event happens, for example a TradingView alert. | 7 |
| WebSocket | A connection that stays open so a server can push live updates (prices, order fills) to you. | 8 |
| x402 † | An open payments standard built on the HTTP 402 "Payment Required" status, used for machine-to-machine (agent) payments. | 10 |
