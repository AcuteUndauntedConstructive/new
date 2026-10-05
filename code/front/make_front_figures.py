"""Figures for the Preface (Figures P.1 - P.4).

Run from the repository root:
    python code/front/make_front_figures.py

Outputs PNG files into figures/front/. Figure P.4 uses SIMULATED trades (clearly
labelled); Figure P.3 is pure arithmetic. No market data is used here.
Tested: 2026-10-05, Python 3.11, matplotlib 3.11, numpy 2.4.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # make 'common' importable

import matplotlib.pyplot as plt  # noqa: E402

from common.bookstyle import (DIAGRAM, FIG_WIDTH_IN, PALETTE, SERIES, apply_style,  # noqa: E402
                              save_figure, source_note)
from common.diagrams import arrow, box, group, new_canvas  # noqa: E402

OUT = Path(__file__).resolve().parents[2] / "figures" / "front"


def fig_p1_system() -> Path:
    """Figure P.1: the complete system the book builds, by unit."""
    fig, ax = new_canvas(66)
    group(ax, 0.5, 35, 99, 30.5, "UNITS I-II  ·  analyse and trade by prompt (you approve every action)")
    group(ax, 0.5, 1, 99, 32, "UNIT III  ·  automation on your own server (testnet first)", label_side="right")

    you = box(ax, 42, 56.5, 17, 5.5, "You", "read · decide · approve", fill="white", title_size=8.5, sub_size=7)
    tv = box(ax, 1.5, 39, 17, 13, "TradingView\nDesktop", "charts · Pine Script\nstrategy tester", fill=DIAGRAM["tradingview"])
    tvm = box(ax, 22, 39, 17, 13, "TradingView\nMCP server", "runs on your PC\n(local debug port)", fill=DIAGRAM["tradingview"])
    cl = box(ax, 42, 39, 17, 13, "Claude", "Claude Code or\nClaude Desktop", fill=DIAGRAM["agent"])
    bm = box(ax, 62, 39, 17, 13, "Binance\nMCP server", "agent.binance.com\nOAuth login", fill=DIAGRAM["binance"])
    sub = box(ax, 82, 39, 17, 13, "Agentic\nsubaccount", "separately funded\nno external withdrawal", fill=DIAGRAM["binance"])

    arrow(ax, tv.side("right"), tvm.side("left"), both=True)
    arrow(ax, tvm.side("right"), cl.side("left"), both=True, label="tools", label_offset=(0, 1.6))
    arrow(ax, cl.side("right"), bm.side("left"), both=True, label="tools", label_offset=(0, 1.6))
    arrow(ax, bm.side("right"), sub.side("left"), both=True)
    arrow(ax, you.side("bottom"), cl.side("top"), both=True)

    rx = box(ax, 22, 15, 17, 12, "Webhook\nreceiver", "FastAPI · HTTPS\nsecret token check", fill=DIAGRAM["bridge"])
    rk = box(ax, 42, 15, 17, 12, "Risk engine", "size · daily loss limit\nkill switch", fill=DIAGRAM["risk"])
    ex = box(ax, 62, 15, 17, 12, "Order\nexecutor", "entry · stop · target\nreconciliation", fill=DIAGRAM["bridge"])
    fut = box(ax, 82, 15, 17, 12, "Binance\nFutures API", "own API key\nno withdrawal rights", fill=DIAGRAM["binance"])
    jr = box(ax, 42, 3, 17, 8, "Trade journal", "SQLite", fill=DIAGRAM["data"], title_size=8.5)
    tg = box(ax, 62, 3, 17, 8, "Telegram alerts", "fills · errors · limits", fill=DIAGRAM["data"], title_size=8.5)

    # TradingView alert drops down to the receiver
    ax.plot([10, 10], [39, 21], color=DIAGRAM["edge"], lw=0.9, zorder=1)
    arrow(ax, (10, 21), rx.side("left"))
    ax.text(11, 15.5, "alert webhook\n(JSON over HTTPS)", fontsize=7.2, color=PALETTE["ink2"], ha="center",
            va="center", bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"), zorder=4)
    arrow(ax, rx.side("right"), rk.side("left"))
    arrow(ax, rk.side("right"), ex.side("left"))
    arrow(ax, ex.side("right"), fut.side("left"), both=True)
    arrow(ax, rk.side("bottom"), jr.side("top"))
    arrow(ax, ex.side("bottom"), tg.side("top"))
    return save_figure(fig, OUT / "figP-01-system.png")


def fig_p2_roadmap() -> Path:
    """Figure P.2: the 12 chapters in 4 units, read left to right."""
    fig, ax = new_canvas(52)
    units = [
        ("Unit I", "Tools and first trades", DIAGRAM["tradingview"],
         ["1  Binance MCP:\ntrading by prompt", "2  TradingView MCP:\nanalysis by prompt", "3  Futures mechanics\nand risk maths"]),
        ("Unit II", "Building and testing", DIAGRAM["data"],
         ["4  Pine Script\nstrategies with AI", "5  Backtesting\nhonestly", "6  Research with\nPython and SQL"]),
        ("Unit III", "Automation", DIAGRAM["bridge"],
         ["7  Signal-to-order\nbridge (webhooks)", "8  Engineering a\nreliable bot", "9  Launching an\nAI agent"]),
        ("Unit IV", "Growth and the road ahead", DIAGRAM["agent"],
         ["10  The new tech\nlandscape", "11  Growing Rs 1,00,000\nresponsibly", "12  Capstone\nand career"]),
    ]
    col_w, gap = 22, 3.33
    for u, (name, sub, fill, chapters) in enumerate(units):
        x = 1 + u * (col_w + gap)
        ax.text(x + col_w / 2, 49.5, name, ha="center", va="center", fontsize=10, fontweight="bold",
                color=PALETTE["ink"])
        ax.text(x + col_w / 2, 46.3, sub, ha="center", va="center", fontsize=7.8, color=PALETTE["ink2"])
        prev = None
        for k, ch in enumerate(chapters):
            y = 33 - k * 12.5
            node = box(ax, x, y, col_w, 10, ch, fill=fill, title_size=8.3)
            if prev is not None:
                arrow(ax, prev.side("bottom"), node.side("top"))
            prev = node
        if u < 3:
            arrow(ax, (x + col_w + 0.3, 24), (x + col_w + gap - 0.3, 24))
    # the risk thread under everything
    ax.add_patch(plt.Rectangle((1, 0.8), 98, 5.2, facecolor=DIAGRAM["risk"], edgecolor=DIAGRAM["edge"],
                               linewidth=0.8, zorder=2))
    ax.text(50, 3.4, "Risk control first in every chapter:  testnet  →  minimum size  →  staged capital (Chapter 11)",
            ha="center", va="center", fontsize=8.3, fontweight="bold", color=PALETTE["ink"], zorder=3)
    return save_figure(fig, OUT / "figP-02-roadmap.png")


def simulate_drawdowns(risk_levels, n_paths=10_000, n_trades=200, win_rate=0.45, win_r=1.5, loss_r=1.0,
                       seed=42):
    """Monte Carlo: each trade wins +win_r R or loses -loss_r R; risk is a % of current equity."""
    rng = np.random.default_rng(seed)
    rows = []
    for f in risk_levels:
        outcome_r = np.where(rng.random((n_paths, n_trades)) < win_rate, win_r, -loss_r)
        equity = np.cumprod(1 + f * outcome_r, axis=1)
        equity = np.hstack([np.ones((n_paths, 1)), equity])
        peak = np.maximum.accumulate(equity, axis=1)
        max_dd = (1 - equity / peak).max(axis=1)
        rows.append({
            "risk": f,
            "median_dd": float(np.median(max_dd)),
            "p95_dd": float(np.percentile(max_dd, 95)),
            "p_dd50": float((max_dd >= 0.5).mean()),
            "median_final": float(np.median(equity[:, -1])),
        })
    return rows


def fig_p4_drawdown() -> Path:
    """Figure P.4: bigger risk per trade -> much deeper drawdowns, even with an edge."""
    apply_style()
    levels = [0.005, 0.01, 0.02, 0.05, 0.10]
    rows = simulate_drawdowns(levels)
    x = np.arange(len(levels))
    w = 0.36
    fig, ax = plt.subplots(figsize=(FIG_WIDTH_IN, 3.4))
    med = [r["median_dd"] * 100 for r in rows]
    bad = [r["p95_dd"] * 100 for r in rows]
    b1 = ax.bar(x - w / 2 - 0.01, med, w, color=SERIES[0], label="Typical luck (median path)")
    b2 = ax.bar(x + w / 2 + 0.01, bad, w, color=SERIES[1], label="Bad luck (worst 5% of paths)")
    for bars in (b1, b2):
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1.2, f"{bar.get_height():.0f}%",
                    ha="center", va="bottom", fontsize=7.5, color=PALETTE["ink"])
    ax.set_xticks(x, [f"{f*100:g}% risk\nper trade" for f in levels])
    ax.set_ylabel("Largest fall from a peak (max drawdown)")
    ax.set_ylim(0, 105)
    ax.yaxis.set_major_formatter(lambda v, _: f"{v:.0f}%")
    ax.grid(axis="x", visible=False)
    ax.set_title("Same strategy, same edge: only the risk per trade changes", pad=10)
    ax.legend(loc="upper left")
    for k, r in enumerate(rows):
        if r["p_dd50"] >= 0.01:
            ax.text(x[k], -21, f"{r['p_dd50']*100:.0f}% chance\nof a 50%+ fall", ha="center", va="top",
                    fontsize=7, color=PALETTE["ink2"])
    fig.subplots_adjust(bottom=0.30)
    source_note(fig, "SIMULATED DATA: 10,000 paths x 200 trades; win rate 45%, wins +1.5R, losses -1R "
                     "(expectancy +0.125R per trade). Not market prices.")
    return save_figure(fig, OUT / "figP-04-risk-drawdown.png")


def fig_p3_recovery() -> Path:
    """Figure P.3: the gain needed to get back to break-even after a loss."""
    apply_style()
    loss = np.linspace(0, 0.80, 400)
    need = loss / (1 - loss)
    fig, ax = plt.subplots(figsize=(FIG_WIDTH_IN, 3.0))
    ax.plot(loss * 100, need * 100, color=SERIES[0])
    # (loss, label offset in points, alignment): labels sit below-right, the last one left
    for l, off, ha in ((0.10, (-2, 18), "left"), (0.25, (-2, 34), "left"), (0.50, (8, -12), "left"),
                       (0.75, (-10, 0), "right")):
        g = l / (1 - l)
        ax.plot(l * 100, g * 100, "o", ms=6, color=SERIES[0], mec="white", mew=1.5, zorder=3)
        ax.annotate(f"lose {l*100:.0f}% → need +{g*100:.0f}%", (l * 100, g * 100), xytext=off,
                    textcoords="offset points", ha=ha, va="center", fontsize=8, color=PALETTE["ink"],
                    arrowprops=dict(arrowstyle="-", color=PALETTE["muted"], lw=0.6, shrinkA=2, shrinkB=4)
                    if off[1] > 15 else None)
    ax.set_xlabel("Loss from your starting capital")
    ax.set_ylabel("Gain needed to get back to start")
    ax.xaxis.set_major_formatter(lambda v, _: f"{v:.0f}%")
    ax.yaxis.set_major_formatter(lambda v, _: f"{v:.0f}%")
    ax.set_xlim(0, 82)
    ax.set_ylim(0, 420)
    ax.set_title("Losses hurt more than gains help", pad=8)
    source_note(fig, "Pure arithmetic: gain needed = loss / (1 - loss). Example: Rs 1,00,000 → Rs 50,000 needs +100% to return.")
    fig.subplots_adjust(bottom=0.2)
    return save_figure(fig, OUT / "figP-03-recovery.png")


if __name__ == "__main__":
    for fn in (fig_p1_system, fig_p2_roadmap, fig_p3_recovery, fig_p4_drawdown):
        print("wrote", fn())
    for r in simulate_drawdowns([0.005, 0.01, 0.02, 0.05, 0.10]):
        print({k: round(v, 3) for k, v in r.items()})
