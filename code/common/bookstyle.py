"""Shared matplotlib style for every chart in the book.

Import this module in every figure script so all charts look like one system:

    from common.bookstyle import apply_style, PALETTE, save_figure, source_note

Palette: the validated categorical order from STYLE_GUIDE.md (light mode, because
the book is printed / read on white pages). Use slots in fixed order; never cycle.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless rendering, no display needed
import matplotlib.pyplot as plt
from matplotlib import font_manager

# ---------------------------------------------------------------------------
# Colour tokens (see STYLE_GUIDE.md section 5)
# ---------------------------------------------------------------------------
SERIES = [
    "#2a78d6",  # 1 blue
    "#eb6834",  # 2 orange
    "#1baf7a",  # 3 aqua
    "#eda100",  # 4 yellow
    "#e87ba4",  # 5 magenta
    "#008300",  # 6 green
    "#4a3aa7",  # 7 violet
    "#e34948",  # 8 red
]

PALETTE = {
    "surface": "#fcfcfb",
    "ink": "#0b0b0b",
    "ink2": "#52514e",       # secondary text
    "muted": "#898781",      # axis labels, notes
    "grid": "#e1e0d9",
    "axis": "#c3c2b7",
    # Diverging pair for gains / losses (polarity), neutral midpoint grey
    "gain": "#2a78d6",
    "loss": "#e34948",
    "neutral": "#f0efec",
    # Candles: up = aqua hollow, down = red filled (shape is the second cue)
    "candle_up": "#1baf7a",
    "candle_down": "#e34948",
    # Status colours: reserved for state, always paired with a text label
    "good": "#0ca30c",
    "warning": "#fab219",
    "serious": "#ec835a",
    "critical": "#d03b3b",
    # Sequential blue ramp, light -> dark
    "seq": ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"],
}

# Diagram fills (pale tints so black text always has strong contrast)
DIAGRAM = {
    "tradingview": "#dceafb",   # blue tint
    "binance": "#fde8d9",       # orange tint
    "bridge": "#f0efec",        # neutral grey
    "agent": "#e3e0f6",         # violet tint
    "data": "#dcf3e9",          # aqua tint
    "risk": "#fbe3e3",          # red tint
    "edge": "#52514e",          # arrows and outlines
}

FIG_WIDTH_IN = 6.3  # matches the 16 cm text width in the Word template
DPI = 200


def _pick_font() -> str:
    """Prefer Calibri (Windows/Word) or its metric twin Carlito; fall back to DejaVu Sans."""
    installed = {f.name for f in font_manager.fontManager.ttflist}
    for name in ("Calibri", "Carlito", "Liberation Sans", "DejaVu Sans"):
        if name in installed:
            return name
    return "sans-serif"


def apply_style() -> None:
    """Apply the book's rcParams. Call once at the top of each figure script."""
    font = _pick_font()
    plt.rcParams.update(
        {
            "font.family": font,
            "font.size": 9,
            "axes.titlesize": 11,
            "axes.titleweight": "bold",
            "axes.titlelocation": "left",
            "axes.labelsize": 9,
            "axes.labelcolor": PALETTE["ink2"],
            "axes.edgecolor": PALETTE["axis"],
            "axes.linewidth": 0.8,
            "axes.facecolor": PALETTE["surface"],
            "axes.prop_cycle": matplotlib.cycler(color=SERIES),
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "axes.axisbelow": True,
            "grid.color": PALETTE["grid"],
            "grid.linewidth": 0.6,
            "grid.linestyle": "-",
            "xtick.color": PALETTE["muted"],
            "ytick.color": PALETTE["muted"],
            "xtick.labelcolor": PALETTE["ink2"],
            "ytick.labelcolor": PALETTE["ink2"],
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "lines.linewidth": 1.6,
            "lines.solid_capstyle": "round",
            "lines.solid_joinstyle": "round",
            "legend.frameon": False,
            "legend.fontsize": 8,
            "figure.facecolor": "white",
            "figure.dpi": 100,
            "savefig.dpi": DPI,
            "savefig.facecolor": "white",
        }
    )


def source_note(fig, text: str) -> None:
    """Print the data source (or 'SIMULATED DATA') under the plot, bottom-left."""
    fig.text(0.01, 0.01, text, fontsize=7.5, color=PALETTE["muted"], ha="left", va="bottom")


def save_figure(fig, path: str | Path) -> Path:
    """Save a figure as PNG at book resolution and close it."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=DPI, bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)
    return path


def inr(amount: float, decimals: int = 0) -> str:
    """Format rupees with Indian digit grouping: 100000 -> 'Rs 1,00,000'."""
    negative = amount < 0
    amount = abs(amount)
    whole = int(round(amount, decimals)) if decimals == 0 else int(amount)
    frac = f"{amount:.{decimals}f}".split(".")[1] if decimals else ""
    s = str(whole)
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        groups = []
        while len(head) > 2:
            groups.insert(0, head[-2:])
            head = head[:-2]
        if head:
            groups.insert(0, head)
        s = ",".join(groups + [tail])
    out = f"Rs {s}" + (f".{frac}" if frac else "")
    return f"-{out}" if negative else out


if __name__ == "__main__":
    # Self-check for the rupee formatter
    assert inr(100000) == "Rs 1,00,000", inr(100000)
    assert inr(1234567) == "Rs 12,34,567", inr(1234567)
    assert inr(999) == "Rs 999"
    assert inr(-2500) == "-Rs 2,500"
    assert inr(1500.5, 2) == "Rs 1,500.50", inr(1500.5, 2)
    print("bookstyle self-check passed; chart font =", _pick_font())
