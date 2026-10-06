#!/usr/bin/env python3
"""Draw the before and after figures used in the README.

All data is invented. Each figure shows one rule from the skill:
the left panel breaks it and the right panel follows it.

Requires matplotlib and numpy.
Usage: python examples/make_examples.py [output_dir]
"""

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "docs" / "images"

INK = "#222222"
MUTED = "#8A8A8A"
GREY = "#C4C4C4"
ACCENT = "#D55E00"
BLUE = "#0072B2"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.edgecolor": "#666666",
    "axes.labelcolor": INK,
    "xtick.color": INK,
    "ytick.color": INK,
    "axes.titlesize": 11,
    "axes.titleweight": "bold",
    "axes.titlelocation": "left",
})


def two_panels(width=11.0, height=4.4, right_edge=0.97):
    fig, (left, right) = plt.subplots(1, 2, figsize=(width, height))
    fig.subplots_adjust(left=0.07, right=right_edge, top=0.76, bottom=0.14, wspace=0.28)
    for ax, tag, colour in ((left, "BEFORE", "#B00020"), (right, "AFTER", "#00695C")):
        ax.panel_x0 = ax.get_position().x0
        fig.text(ax.panel_x0, 0.93, tag, fontsize=10, fontweight="bold", color=colour)
    return fig, left, right


def caption(fig, ax, text):
    fig.text(ax.panel_x0, 0.865, text, fontsize=9.5, color=MUTED)


def clean(ax, grid_axis=None):
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_axisbelow(True)
    if grid_axis:
        ax.grid(axis=grid_axis, color="#000000", alpha=0.12, linewidth=0.8)


def save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    fig.savefig(path, dpi=160, facecolor="white")
    plt.close(fig)
    print("wrote", path)


def truncated_axis():
    products = ["Product A", "Product B"]
    scores = [82, 85]
    fig, left, right = two_panels()

    left.bar(products, scores, color=["#4C72B0", "#55A868"], width=0.6)
    left.set_ylim(80, 86)
    left.set_title("Satisfaction score")
    caption(fig, left, "Axis starts at 80, so B looks 2.5 times as tall as A")

    right.bar(products, scores, color=[GREY, BLUE], width=0.6)
    right.set_ylim(0, 100)
    for i, value in enumerate(scores):
        right.text(i, value + 2, str(value), ha="center", va="bottom", fontweight="bold", color=INK)
    right.set_ylabel("Score out of 100")
    right.set_title("B scores 3 points higher than A")
    clean(right, "y")
    caption(fig, right, "Bars from zero. The true difference is under 4%")
    save(fig, "01-zero-baseline.png")


def too_many_lines():
    rng = np.random.default_rng(7)
    months = np.arange(1, 25)
    names = ["North", "South", "East", "West", "Central", "Coastal", "Highland"]
    series = {}
    for i, name in enumerate(names):
        if name == "North":
            series[name] = 34 + 1.25 * months + rng.normal(0, 1.2, months.size)
        else:
            series[name] = 38 + i * 2.2 + np.cumsum(rng.normal(0.05, 1.6, months.size))
    fig, left, right = two_panels()

    rainbow = plt.cm.tab10(np.linspace(0, 0.65, len(names)))
    for colour, (name, values) in zip(rainbow, series.items()):
        left.plot(months, values, color=colour, linewidth=1.6, label=name)
    left.legend(fontsize=8, ncol=2, frameon=True, loc="upper left")
    left.set_title("Revenue by region")
    left.grid(True, color="#000000", alpha=0.25)
    caption(fig, left, "Seven colours, a legend to decode, no clear point")

    for name, values in series.items():
        if name != "North":
            right.plot(months, values, color=GREY, linewidth=1.1, zorder=2)
    right.plot(months, series["North"], color=ACCENT, linewidth=2.6, zorder=3)
    right.annotate("North", (months[-1], series["North"][-1]), xytext=(6, 0),
                   textcoords="offset points", va="center", color=ACCENT, fontweight="bold")
    lowest = min((n for n in names if n != "North"), key=lambda n: series[n][-1])
    right.annotate("Other\nregions", (months[-1], series[lowest][-1]), xytext=(6, 0),
                   textcoords="offset points", va="center", color=MUTED, fontsize=9)
    right.set_xlim(1, 28.5)
    right.set_xticks([1, 6, 12, 18, 24])
    right.set_xlabel("Month")
    right.set_ylabel("Revenue (thousands)")
    right.set_title("North rose from last place to first in two years")
    clean(right, "y")
    caption(fig, right, "Grey for context, one accent, labels on the lines")
    save(fig, "02-highlight-one-series.png")


def pie_to_bars():
    labels = ["Billing", "Delivery", "Login", "Pricing", "Quality", "Returns", "Setup", "Other"]
    values = [17, 14, 9, 12, 16, 13, 11, 8]
    fig, left, right = two_panels()

    left.pie(values, labels=None, colors=plt.cm.Set3(np.linspace(0, 1, len(values))),
             startangle=40, wedgeprops={"edgecolor": "white"})
    left.legend(labels, fontsize=8, loc="center left", bbox_to_anchor=(0.98, 0.5), frameon=False)
    fig.text(left.panel_x0, 0.785, "Complaints by topic", fontsize=11, fontweight="bold")
    caption(fig, left, "Which topic is third largest? Compare eight angles to find out")

    order = np.argsort(values)
    sorted_labels = [labels[i] for i in order]
    sorted_values = [values[i] for i in order]
    colours = [GREY] * len(values)
    colours[-3] = ACCENT
    right.barh(sorted_labels, sorted_values, color=colours, height=0.68)
    for y, value in enumerate(sorted_values):
        right.text(value + 0.3, y, "%d%%" % value, va="center", fontsize=9,
                   color=INK, fontweight="bold" if y == len(values) - 3 else "normal")
    right.set_xlim(0, 20)
    right.set_xticks([0, 5, 10, 15, 20])
    right.set_xlabel("Share of complaints (%)")
    right.set_title("Delivery is the third most common complaint")
    right.tick_params(axis="y", length=0)
    clean(right)
    right.spines["left"].set_visible(False)
    caption(fig, right, "Sorted bars on one scale. The answer is the third bar")
    save(fig, "03-sorted-bars-not-pie.png")


def rainbow_to_sequential():
    rng = np.random.default_rng(3)
    hours = np.arange(24)
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    daily = np.exp(-0.5 * ((hours - 13) / 4.0) ** 2)
    weekday = np.array([1.0, 1.05, 1.1, 1.08, 1.2, 0.75, 0.6])
    orders = np.outer(weekday, daily) * 120 + rng.normal(0, 4, (7, 24))
    evening = np.exp(-0.5 * ((hours - 20) / 1.5) ** 2) * 70
    orders[4] += evening
    orders[5] += evening * 1.2
    orders = np.clip(orders, 0, None)
    fig, left, right = two_panels(right_edge=0.93)

    for ax, cmap in ((left, "jet"), (right, LinearSegmentedColormap.from_list(
            "blues", ["#f7fbff", "#c6dbef", "#6baed6", "#2171b5", "#08306b"]))):
        image = ax.imshow(orders, aspect="auto", cmap=cmap, vmin=0)
        ax.set_yticks(range(7))
        ax.set_yticklabels(days)
        ax.set_xticks([0, 6, 12, 18, 23])
        ax.set_xticklabels(["00:00", "06:00", "12:00", "18:00", "23:00"])
        bar = fig.colorbar(image, ax=ax, fraction=0.046, pad=0.03)
        bar.outline.set_visible(False)
        if ax is right:
            bar.set_label("Orders per hour")
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.tick_params(length=0)
    left.set_title("Orders by hour and weekday")
    caption(fig, left, "Rainbow scale: bright bands look like edges that are not in the data")
    right.set_title("Midday peak, plus a Fri and Sat evening rush")
    caption(fig, right, "One ramp, darker means more. The pattern is easy to see")
    save(fig, "04-sequential-not-rainbow.png")


def survey_distribution():
    teams = ["Team X", "Team Y", "Team Z"]
    answers = ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"]
    shares = np.array([
        [3, 7, 10, 50, 30],
        [12, 4, 4, 18, 62],
        [5, 25, 42, 22, 6],
    ], dtype=float)
    palette = ["#a6611a", "#dfc27d", "#d9d9d9", "#80cdc1", "#018571"]
    fig, left, right = two_panels()

    favourable = shares[:, 3] + shares[:, 4]
    left.bar(teams, favourable, color="#4C72B0", width=0.6)
    for i, value in enumerate(favourable):
        left.text(i, value + 2, "%d%%" % value, ha="center")
    left.set_ylim(0, 100)
    left.set_title("% favourable")
    caption(fig, left, "X and Y look identical at 80%")

    for row, team in enumerate(teams):
        start = -(shares[row, 0] + shares[row, 1] + shares[row, 2] / 2)
        for col in range(5):
            width = shares[row, col]
            right.barh(team, width, left=start, color=palette[col], height=0.62,
                       edgecolor="white", linewidth=0.8)
            if width >= 8:
                right.text(start + width / 2, row, "%d" % width, ha="center", va="center",
                           fontsize=8.5, color="white" if col in (0, 4) else INK)
            start += width
    right.axvline(0, color="#444444", linewidth=0.9, zorder=0)
    right.set_xlim(-65, 95)
    right.set_xticks([-50, 0, 50])
    right.set_xticklabels(["50%", "Neutral midpoint", "50%"])
    right.invert_yaxis()
    right.tick_params(axis="y", length=0)
    clean(right)
    right.spines["left"].set_visible(False)
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in palette]
    right.legend(handles, answers, ncol=5, fontsize=7.5, frameon=False, loc="upper center",
                 bbox_to_anchor=(0.5, -0.13), handlelength=1, columnspacing=1, handletextpad=0.4)
    right.set_title("Team Y is split. Team X is broadly content")
    caption(fig, right, "Whole distribution: Y has 4 times X's strong disagreement")
    fig.subplots_adjust(bottom=0.2)
    save(fig, "05-show-the-distribution.png")


def bubble_area():
    cities = ["Avon", "Brook", "Calder", "Dale"]
    population = np.array([1.0, 2.0, 4.0, 8.0])
    x = np.array([1.0, 2.1, 3.3, 4.7])
    y = np.array([1.0, 1.0, 1.0, 1.0])
    fig, left, right = two_panels(height=4.0)
    unit = 170.0

    for ax, areas in ((left, unit * population ** 2), (right, unit * population)):
        ax.scatter(x, y, s=areas, color=BLUE, alpha=0.55, edgecolor="white", linewidth=1.5)
        for cx, name, pop in zip(x, cities, population):
            ax.text(cx, 0.08, "%s\n%dM" % (name, pop), ha="center", va="top", fontsize=9, color=INK)
        ax.set_xlim(0.2, 6.6)
        ax.set_ylim(-0.35, 2.0)
        ax.axis("off")
    left.set_title("Population mapped to radius", loc="left")
    caption(fig, left, "Dale has 8 times Avon's population and 64 times its area")
    right.set_title("Population mapped to area", loc="left")
    caption(fig, right, "Radius follows the square root, so area matches the value")
    save(fig, "06-bubble-area.png")


if __name__ == "__main__":
    truncated_axis()
    too_many_lines()
    pie_to_bars()
    rainbow_to_sequential()
    survey_distribution()
    bubble_area()
