"""Small helpers for drawing book diagrams with matplotlib (no Graphviz needed).

Three diagram kinds are used throughout the book:
  * architecture / block diagrams  -> new_canvas(), box(), arrow()
  * flowcharts                     -> box(), diamond(), arrow()
  * sequence diagrams              -> sequence_diagram()

Coordinates are in "canvas units": x runs 0..100 left to right, y runs 0..height
bottom to top, so layouts stay readable in the figure scripts.
"""
from __future__ import annotations

from dataclasses import dataclass

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon

from common.bookstyle import DIAGRAM, FIG_WIDTH_IN, PALETTE, apply_style


@dataclass
class Node:
    """A drawn box; keeps its geometry so arrows can attach to its sides."""
    x: float
    y: float
    w: float
    h: float

    @property
    def cx(self) -> float:
        return self.x + self.w / 2

    @property
    def cy(self) -> float:
        return self.y + self.h / 2

    def side(self, where: str) -> tuple[float, float]:
        """Anchor point on a side: 'top', 'bottom', 'left', 'right' (or 'top:0.25' for a fraction)."""
        name, _, frac = where.partition(":")
        f = float(frac) if frac else 0.5
        if name == "top":
            return (self.x + self.w * f, self.y + self.h)
        if name == "bottom":
            return (self.x + self.w * f, self.y)
        if name == "left":
            return (self.x, self.y + self.h * f)
        if name == "right":
            return (self.x + self.w, self.y + self.h * f)
        raise ValueError(where)


def new_canvas(height_units: float = 60, width_in: float = FIG_WIDTH_IN):
    """Blank canvas, 100 units wide. Height in inches scales with height_units."""
    apply_style()
    fig, ax = plt.subplots(figsize=(width_in, width_in * height_units / 100))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, height_units)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.subplots_adjust(0, 0, 1, 1)
    return fig, ax


def box(ax, x, y, w, h, title, sub=None, fill=None, title_size=9, sub_size=7.5, bold=True,
        dashed=False, radius=1.2) -> Node:
    """Rounded box with a bold title and an optional smaller sub-line (use '\n' to wrap)."""
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        linewidth=0.9,
        edgecolor=DIAGRAM["edge"],
        facecolor=fill or "white",
        linestyle=(0, (3, 2)) if dashed else "-",
        zorder=2,
    )
    ax.add_patch(patch)
    if sub:
        ax.text(x + w / 2, y + h * 0.64, title, ha="center", va="center", fontsize=title_size,
                fontweight="bold" if bold else "normal", color=PALETTE["ink"], zorder=3)
        ax.text(x + w / 2, y + h * 0.30, sub, ha="center", va="center", fontsize=sub_size,
                color=PALETTE["ink2"], zorder=3, linespacing=1.15)
    else:
        ax.text(x + w / 2, y + h / 2, title, ha="center", va="center", fontsize=title_size,
                fontweight="bold" if bold else "normal", color=PALETTE["ink"], zorder=3,
                linespacing=1.15)
    return Node(x, y, w, h)


def group(ax, x, y, w, h, label, fill="none", label_side="left"):
    """Large dashed container that groups several boxes (for example 'Your VPS')."""
    patch = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.5",
                           linewidth=0.8, edgecolor=PALETTE["muted"], facecolor=fill,
                           linestyle=(0, (4, 3)), zorder=1)
    ax.add_patch(patch)
    lx = x + 1.2 if label_side == "left" else x + w - 1.2
    ax.text(lx, y + h - 1.0, label, ha=label_side, va="top", fontsize=7.5,
            color=PALETTE["ink2"], fontweight="bold", zorder=3)
    return Node(x, y, w, h)


def diamond(ax, cx, cy, w, h, text, fill="white", size=8) -> Node:
    """Decision diamond for flowcharts."""
    pts = [(cx, cy + h / 2), (cx + w / 2, cy), (cx, cy - h / 2), (cx - w / 2, cy)]
    ax.add_patch(Polygon(pts, closed=True, facecolor=fill, edgecolor=DIAGRAM["edge"],
                         linewidth=0.9, zorder=2))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=size, color=PALETTE["ink"],
            zorder=3, linespacing=1.1)
    return Node(cx - w / 2, cy - h / 2, w, h)


def arrow(ax, start, end, label=None, dashed=False, color=None, label_pos=0.5,
          label_offset=(0, 1.2), size=7.2, both=False, rad=0.0):
    """Arrow from start to end (x, y). Optional small label near the middle."""
    style = "<|-|>" if both else "-|>"
    a = FancyArrowPatch(start, end, arrowstyle=style, mutation_scale=9,
                        linewidth=0.9, color=color or DIAGRAM["edge"],
                        linestyle=(0, (3, 2)) if dashed else "-",
                        connectionstyle=f"arc3,rad={rad}", zorder=1.5,
                        shrinkA=0, shrinkB=0)
    ax.add_patch(a)
    if label:
        lx = start[0] + (end[0] - start[0]) * label_pos + label_offset[0]
        ly = start[1] + (end[1] - start[1]) * label_pos + label_offset[1]
        ax.text(lx, ly, label, ha="center", va="center", fontsize=size, color=PALETTE["ink2"],
                zorder=4, bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"))


def step_badge(ax, x, y, n, size=7):
    """Small numbered circle used to mark the order of steps on a diagram."""
    ax.text(x, y, str(n), ha="center", va="center", fontsize=size, color="white",
            fontweight="bold", zorder=5,
            bbox=dict(boxstyle="circle,pad=0.25", fc=PALETTE["ink2"], ec="none"))


def sequence_diagram(actors: list[str], messages: list[tuple], fills: list[str] | None = None,
                     row_gap: float = 5.0, top_pad: float = 10.0):
    """Draw a UML-style sequence diagram.

    actors   : column titles, left to right
    messages : tuples (from_index, to_index, text) or (from, to, text, 'dashed') for replies,
               or ('note', index, text) for a note on one lifeline.
    Returns (fig, ax).
    """
    n = len(actors)
    height = top_pad + row_gap * (len(messages) + 1) + 4
    fig, ax = new_canvas(height)
    xs = [100 * (i + 0.5) / n for i in range(n)]
    fills = fills or ["white"] * n
    head_h = 6
    top = height - 2
    for i, (x, name) in enumerate(zip(xs, actors)):
        box(ax, x - 9.5, top - head_h, 19, head_h, name, fill=fills[i], title_size=8)
        ax.plot([x, x], [2, top - head_h], color=PALETTE["axis"], lw=0.8, ls=(0, (3, 3)), zorder=1)
    y = top - head_h - row_gap
    for k, msg in enumerate(messages, start=1):
        if msg[0] == "note":
            _, i, text = msg
            ax.text(xs[i] + 1.2, y, text, ha="left", va="center", fontsize=7, color=PALETTE["ink2"],
                    style="italic", bbox=dict(boxstyle="round,pad=0.3", fc=PALETTE["neutral"], ec="none"))
        else:
            src, dst, text = msg[:3]
            dashed = len(msg) > 3 and msg[3] == "dashed"
            if src == dst:  # self-call: small loop on the right of the lifeline
                ax.add_patch(FancyArrowPatch((xs[src], y + 1), (xs[src], y - 1.2),
                                             connectionstyle="arc3,rad=-1.6", arrowstyle="-|>",
                                             mutation_scale=8, lw=0.9, color=DIAGRAM["edge"]))
                ax.text(xs[src] + 3.6, y, f"{k}. {text}", ha="left", va="center", fontsize=7,
                        color=PALETTE["ink"])
            else:
                arrow(ax, (xs[src], y), (xs[dst], y), dashed=dashed)
                ax.text((xs[src] + xs[dst]) / 2, y + 1.3, f"{k}. {text}", ha="center", va="center",
                        fontsize=7, color=PALETTE["ink"],
                        bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none"))
        y -= row_gap
    return fig, ax
