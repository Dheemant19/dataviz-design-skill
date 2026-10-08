#!/usr/bin/env python3
"""chartkit: small matplotlib helpers for clean, finished static charts.

The design rules live in the skill's reference files. This module does the
fiddly parts that agents otherwise hand-roll and get slightly wrong every time:
a consistent type scale, a left-aligned title block, direct labels that do not
collide, value labels with even spacing, a layout that keeps everything inside
the canvas, and a final check before saving.

Typical use
-----------
    import sys; sys.path.insert(0, "<skill>/scripts")
    import chartkit as ck

    ck.apply_style("slide")                      # once, before plotting
    fig, ax = ck.figure()                        # sized for the preset
    for name, s in series.items():
        ax.plot(s.index, s.values, label=name,
                **ck.emphasis(name, focus="North"))
    ck.label_lines(ax, focus="North", values=True)
    ck.finish(fig, "chart.png",
              title="North overtook every other region in 2024",
              subtitle="Monthly revenue, thousand dollars, Jan 2022 to Dec 2024",
              source="Source: Sales ledger export, 3 Jan 2025",
              alt="Line chart of monthly revenue for nine regions ...")

`finish` lays the figure out, runs chartlint, prints the findings, saves the
image at the preset's size and resolution, and writes the alt text next to it.

Requires matplotlib 3.7 or later.
"""

import math
import os
import sys
import textwrap

import matplotlib
from matplotlib import pyplot as plt
from matplotlib.container import BarContainer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# --- presets and tokens --------------------------------------------------------

PRESETS = {
    # name: figure size in inches, export dpi, base font size in points
    "slide": {"size": (13.33, 7.5), "dpi": 150, "base": 13.0},   # 16:9, 2000 x 1125 px
    "report": {"size": (6.5, 4.2), "dpi": 220, "base": 9.5},     # one column of an A4/Letter page
    "web": {"size": (9.0, 5.6), "dpi": 200, "base": 11.0},       # article or README body width
    "social": {"size": (12.0, 6.75), "dpi": 150, "base": 15.0},  # 1800 x 1013 px, read on phones
    "square": {"size": (8.0, 8.0), "dpi": 180, "base": 12.0},
}

SCALE = {  # multipliers of the base size
    "title": 1.55, "subtitle": 1.0, "panel": 1.0, "label": 0.9, "tick": 0.85,
    "annotation": 0.9, "source": 0.78,
}

INK = "#1A1A1A"        # titles, focus labels, values
INK_2 = "#4A4A4A"      # subtitles, axis labels, ticks
MUTED = "#6E6E6E"      # notes, source, context labels (4.9:1 on white)
CONTEXT = "#BDBDBD"    # context marks drawn behind the focus
REFERENCE = "#8A8A8A"  # zero lines, targets, averages
ACCENT = "#0072B2"     # the focus
ACCENT_2 = "#D55E00"   # a second focus, used sparingly
CATEGORICAL = ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#E69F00", "#56B4E9"]
OTHER = "#9E9E9E"      # an "Other" group
FONT_STACK = ["Inter", "Source Sans 3", "Source Sans Pro", "IBM Plex Sans", "Segoe UI",
              "Helvetica Neue", "Helvetica", "Arial", "Liberation Sans", "DejaVu Sans"]

_STATE = {"preset": "slide"}


def _preset(name=None):
    name = name or _STATE["preset"]
    if name not in PRESETS:
        raise ValueError("unknown preset %r, choose from %s" % (name, ", ".join(PRESETS)))
    return name, PRESETS[name]


def size(role, preset=None):
    """Font size in points for a text role ('title', 'subtitle', 'tick', ...)."""
    return round(_preset(preset)[1]["base"] * SCALE[role], 1)


def apply_style(preset="slide", font=None):
    """Set matplotlib defaults for the chosen output size. Call before plotting."""
    name, p = _preset(preset)
    _STATE["preset"] = name
    base = p["base"]
    families = ([font] if font else []) + FONT_STACK
    matplotlib.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": families,
        "font.size": base,
        "axes.titlesize": base * SCALE["panel"],
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.titlepad": base * 0.9,
        "axes.titlecolor": INK,
        "axes.labelsize": base * SCALE["label"],
        "axes.labelcolor": INK_2,
        "axes.labelpad": base * 0.5,
        "axes.edgecolor": "#9A9A9A",
        "axes.linewidth": 0.8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.grid.axis": "y",
        "axes.axisbelow": True,
        "axes.facecolor": "white",
        "axes.prop_cycle": matplotlib.cycler(color=CATEGORICAL),
        "axes.formatter.limits": (-6, 9),
        "axes.formatter.use_locale": False,
        "grid.color": "#000000",
        "grid.alpha": 0.10,
        "grid.linewidth": 0.8,
        "xtick.labelsize": base * SCALE["tick"],
        "ytick.labelsize": base * SCALE["tick"],
        "xtick.color": INK_2,
        "ytick.color": INK_2,
        "xtick.major.size": 3.5,
        "xtick.major.width": 0.8,
        "ytick.major.size": 0,
        "ytick.minor.size": 0,
        "xtick.minor.size": 0,
        "ytick.major.pad": 6,
        "lines.linewidth": 2.0,
        "lines.solid_capstyle": "round",
        "lines.markersize": 6,
        "patch.linewidth": 0,
        "legend.frameon": False,
        "legend.fontsize": base * SCALE["tick"],
        "legend.title_fontsize": base * SCALE["tick"],
        "figure.facecolor": "white",
        "figure.constrained_layout.use": True,
        "savefig.facecolor": "white",
        "figure.dpi": 100,
        "savefig.dpi": p["dpi"],
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
    })
    return name


def figure(preset=None, nrows=1, ncols=1, **subplots_kw):
    """plt.subplots sized for a preset. Extra keywords go to plt.subplots."""
    name, p = _preset(preset)
    if name != _STATE["preset"]:
        apply_style(name)
    fig, axes = plt.subplots(nrows, ncols, figsize=p["size"], **subplots_kw)
    fig._chartkit_preset = name
    return fig, axes


def grid(n, ncols=None, preset=None, sharex=True, sharey=True):
    """Small multiples: n panels in a grid with shared axes. Returns (fig, list_of_axes).

    Unused cells are removed. Shared axes are the default because small multiples are
    for comparing like with like. If you set sharey=False, say so on the chart.
    """
    ncols = ncols or min(n, 4 if n > 6 else 3)
    nrows = int(math.ceil(n / ncols))
    fig, axes = figure(preset, nrows, ncols, sharex=sharex, sharey=sharey, squeeze=False)
    flat = list(axes.ravel())
    for ax in flat[n:]:
        ax.remove()
    return fig, flat[:n]


# --- colour helpers --------------------------------------------------------------

def emphasis(name, focus, accent=ACCENT, context=CONTEXT, focus_width=3.0, context_width=1.4):
    """Plot keywords that draw the focus series strongly and everything else as context.

        ax.plot(x, y, label=name, **ck.emphasis(name, focus=["North", "South"]))
    """
    focus = [focus] if isinstance(focus, str) else list(focus or [])
    if name in focus:
        colour = accent if len(focus) == 1 else CATEGORICAL[focus.index(name) % len(CATEGORICAL)]
        return {"color": colour, "linewidth": focus_width, "zorder": 3}
    return {"color": context, "linewidth": context_width, "zorder": 2}


def colours_for(names, focus=None, palette=None):
    """A fixed name -> colour mapping. With focus: focus in colour, the rest grey."""
    names = list(names)
    if focus is not None:
        focus = [focus] if isinstance(focus, str) else list(focus)
        return {n: (ACCENT if len(focus) == 1 else CATEGORICAL[focus.index(n) % len(CATEGORICAL)])
                if n in focus else CONTEXT for n in names}
    palette = palette or CATEGORICAL
    if len(names) > len(palette):
        raise ValueError("%d categories but only %d colours. Group the smallest into 'Other', "
                         "highlight a few, or use small multiples." % (len(names), len(palette)))
    return dict(zip(names, palette))


def _contrast_ok(colour, background="white", minimum=3.0):
    try:
        import check_palette as pal
        a = pal.linear_rgb(pal.parse_hex(matplotlib.colors.to_hex(colour)))
        b = pal.linear_rgb(pal.parse_hex(matplotlib.colors.to_hex(background)))
        return pal.contrast_ratio(a, b) >= minimum
    except Exception:
        return True


def _is_grey(colour):
    r, g, b = matplotlib.colors.to_rgb(colour)
    return max(r, g, b) - min(r, g, b) < 0.06


# --- number formatting -------------------------------------------------------------

def fmt(value, decimals=None, unit="", compact=False, sign=False, percent=False):
    """Format a number for a label.

    fmt(12289)                 -> '12,289'
    fmt(0.4123, percent=True)  -> '41%'
    fmt(15805, compact=True)   -> '15.8k'
    fmt(-4.2, sign=True)       -> '−4.2'  (true minus sign)
    fmt(3.2, unit=" t")        -> '3.2 t'
    """
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "n/a"
    v = value * 100 if percent else value
    suffix = ""
    if compact:
        for limit, s in ((1e12, "tn"), (1e9, "bn"), (1e6, "M"), (1e3, "k")):
            if abs(v) >= limit:
                v, suffix = v / limit, s
                break
    if decimals is None:
        a = abs(v)
        decimals = 0 if a >= 100 or a == 0 else (1 if a >= 10 else (1 if a >= 1 else 2))
        if percent and a >= 10:
            decimals = 0
    text = "{:,.{d}f}".format(abs(v), d=decimals)
    if v < 0:
        text = "−" + text
    elif sign and v > 0:
        text = "+" + text
    return text + suffix + ("%" if percent else "") + unit


# --- labels --------------------------------------------------------------------------

def _spread(desired, gap, low, high):
    """Place 1-D label positions near `desired` with at least `gap` between them."""
    order = sorted(range(len(desired)), key=lambda i: desired[i])
    clusters = [[i] for i in order]

    def centre(cluster):
        mean = sum(desired[i] for i in cluster) / len(cluster)
        start = mean - gap * (len(cluster) - 1) / 2.0
        start = max(low, min(start, high - gap * (len(cluster) - 1)))
        return start

    merged = True
    while merged:
        merged = False
        for k in range(len(clusters) - 1):
            a, b = clusters[k], clusters[k + 1]
            top_a = centre(a) + gap * (len(a) - 1)
            if top_a + gap > centre(b) + 1e-9:
                clusters[k:k + 2] = [a + b]
                merged = True
                break
    placed = [0.0] * len(desired)
    for cluster in clusters:
        start = centre(cluster)
        for j, i in enumerate(sorted(cluster, key=lambda i: desired[i])):
            placed[i] = start + j * gap
    return placed


def label_lines(ax, focus=None, values=False, value_fmt=None, lines=None, pad=6,
                fontsize=None, min_gap=1.4):
    """Label each line at its last point, nudging labels apart so none collide.

    focus     name or list of names drawn bold in their line colour
    values    also print the last value, formatted with value_fmt (default ck.fmt)
    lines     restrict to these Line2D objects (default: lines with a label)
    Call after all plotting and after setting axis limits.
    """
    fig = ax.figure
    focus = [focus] if isinstance(focus, str) else list(focus or [])
    value_fmt = value_fmt or fmt
    fontsize = fontsize or size("annotation", getattr(fig, "_chartkit_preset", None))
    if lines is None:
        lines = [l for l in ax.get_lines()
                 if not str(l.get_label()).startswith("_") and len(l.get_xdata()) >= 2]
    items = []
    for line in lines:
        xs, ys = line.get_xdata(), line.get_ydata()
        last = None
        for x, y in zip(xs, ys):
            try:
                if y is not None and math.isfinite(float(y)):
                    last = (x, float(y))
            except (TypeError, ValueError):
                continue
        if last is None:
            continue
        items.append((line, last))
    if not items:
        return []
    texts = []
    for line, (x, y) in items:
        name = str(line.get_label())
        colour = line.get_color()
        is_focus = name in focus
        if is_focus or (not focus and not _is_grey(colour)):
            text_colour = colour if _contrast_ok(colour, ax.get_facecolor(), 3.0) else INK
        else:
            text_colour = MUTED
        text = "%s  %s" % (name, value_fmt(y)) if values else name
        t = ax.annotate(text, xy=(x, y), xycoords="data", xytext=(pad, 0),
                        textcoords="offset points", va="center", ha="left",
                        fontsize=fontsize, color=text_colour,
                        fontweight="bold" if is_focus else "normal", annotation_clip=False,
                        arrowprops=dict(arrowstyle="-", color=CONTEXT, lw=0.8, shrinkA=1,
                                        shrinkB=2))
        t._chartkit_role = "line-label"
        t.arrow_patch.set_visible(False)
        texts.append(t)
    group = {"ax": ax, "texts": texts, "pad": pad, "gap_pt": fontsize * min_gap,
             "fontsize": fontsize}
    if not hasattr(fig, "_chartkit_label_groups"):
        fig._chartkit_label_groups = []
    fig._chartkit_label_groups.append(group)
    _place_line_labels(group)
    return texts


def _place_line_labels(group):
    """(Re)compute label offsets from the current layout so labels never collide."""
    ax, texts = group["ax"], group["texts"]
    if not texts:
        return
    fig = ax.figure
    fig.canvas.draw()
    to_px = ax.transData.transform
    desired = []
    for t in texts:
        x, y = t.xy
        desired.append(to_px((ax.convert_xunits(x), y))[1])
    gap = group["gap_pt"] * fig.dpi / 72.0
    box = ax.get_window_extent()
    placed = _spread(desired, gap, box.y0 + gap * 0.3, box.y1 + gap * 0.5)
    shifts = [(got - want) * 72.0 / fig.dpi for want, got in zip(desired, placed)]
    any_moved = any(abs(d) > group["fontsize"] * 0.35 for d in shifts)
    x_offset = group["pad"] * (2.5 if any_moved else 1.0)  # one column for every label
    for t, dy_pt in zip(texts, shifts):
        t.xyann = (x_offset, dy_pt)
        t.arrow_patch.set_visible(any_moved)


def bar_labels(ax, value_fmt=None, secondary=None, container=None, pad=4, fontsize=None,
               weight="bold", colour=INK, secondary_colour=MUTED, make_room=True):
    """Value labels at the end of each bar, with an optional second, quieter label.

    value_fmt  function value -> text (default ck.fmt)
    secondary  list of strings, or function (value, index) -> text, placed after the
               main label with an even gap, e.g. the absolute amount next to a share
    make_room  widen the value axis so labels stay inside the panel
    """
    fig = ax.figure
    value_fmt = value_fmt or fmt
    fontsize = fontsize or size("annotation", getattr(fig, "_chartkit_preset", None))
    containers = [container] if container is not None else \
        [c for c in ax.containers if isinstance(c, BarContainer)]
    made = []
    for c in containers:
        values = list(c.datavalues)
        horizontal = getattr(c, "orientation", "vertical") == "horizontal"
        formatter = value_fmt
        if formatter is fmt:  # one precision for the whole set, chosen from the largest value
            top = max([abs(v) for v in values] + [0])
            shared = 0 if top >= 100 else (1 if top >= 1 else 2)
            formatter = lambda v, d=shared: fmt(v, decimals=d)
        texts = ax.bar_label(c, labels=[formatter(v) for v in values], padding=pad,
                             fontsize=fontsize, color=colour, fontweight=weight)
        for t in texts:
            t._chartkit_role = "bar-label"
        made.extend(texts)
        if secondary is None:
            continue
        for i, (t, v) in enumerate(zip(texts, values)):
            extra = secondary(v, i) if callable(secondary) else secondary[i]
            if not extra:
                continue
            if horizontal:
                xy, offset, ha, va = ((1, 0.5), (pad + 2, 0), "left", "center") if v >= 0 else \
                    ((0, 0.5), (-(pad + 2), 0), "right", "center")
            else:
                xy, offset, ha, va = ((0.5, 1), (0, 1), "center", "bottom") if v >= 0 else \
                    ((0.5, 0), (0, -1), "center", "top")
            second = ax.annotate(extra, xy=xy, xycoords=t, xytext=offset,
                                 textcoords="offset points", ha=ha, va=va,
                                 fontsize=fontsize, color=secondary_colour,
                                 annotation_clip=False)
            second._chartkit_role = "bar-label"
            made.append(second)
    if make_room and made:
        _make_room(ax, made, horizontal=any(getattr(c, "orientation", "") == "horizontal"
                                            for c in containers))
    return made


def _make_room(ax, texts, horizontal):
    fig = ax.figure
    for _ in range(3):
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()
        box = ax.get_window_extent(renderer)
        low, high = ax.get_xlim() if horizontal else ax.get_ylim()
        span_px = box.width if horizontal else box.height
        over_hi = max([0.0] + [((t.get_window_extent(renderer).x1 - box.x1) if horizontal else
                                (t.get_window_extent(renderer).y1 - box.y1)) for t in texts])
        over_lo = max([0.0] + [((box.x0 - t.get_window_extent(renderer).x0) if horizontal else
                                (box.y0 - t.get_window_extent(renderer).y0)) for t in texts])
        if over_hi <= 1 and over_lo <= 1:
            return
        per_px = (high - low) / span_px
        new_high = high + (over_hi + 6) * per_px * 1.05 if over_hi > 1 else high
        new_low = low - (over_lo + 6) * per_px * 1.05 if over_lo > 1 else low
        if horizontal:
            ax.set_xlim(new_low, new_high)
        else:
            ax.set_ylim(new_low, new_high)


def callout(ax, text, xy, offset=(30, 30), colour=INK_2, fontsize=None, ha="left", **kw):
    """A short annotation with a thin leader line. Keep to one or two per chart."""
    fontsize = fontsize or size("annotation", getattr(ax.figure, "_chartkit_preset", None))
    return ax.annotate(text, xy=xy, xytext=offset, textcoords="offset points", ha=ha,
                       va="center", fontsize=fontsize, color=colour, annotation_clip=False,
                       arrowprops=dict(arrowstyle="-", color=REFERENCE, lw=0.8, shrinkA=2,
                                       shrinkB=3), **kw)


def reference_line(ax, value, label=None, axis="y", colour=REFERENCE, style="--"):
    """A labelled zero line, target or average, drawn behind the data."""
    fontsize = size("annotation", getattr(ax.figure, "_chartkit_preset", None)) * 0.95
    if axis == "y":
        ax.axhline(value, color=colour, lw=1.0, ls=style, zorder=1.5)
        if label:
            ax.annotate(label, xy=(1, value), xycoords=("axes fraction", "data"),
                        xytext=(-2, 3), textcoords="offset points", ha="right", va="bottom",
                        fontsize=fontsize, color=MUTED)
    else:
        ax.axvline(value, color=colour, lw=1.0, ls=style, zorder=1.5)
        if label:
            ax.annotate(label, xy=(value, 1), xycoords=("data", "axes fraction"),
                        xytext=(3, -2), textcoords="offset points", ha="left", va="top",
                        fontsize=fontsize, color=MUTED)


def tidy(ax, grid_axis="y", hide_y_axis_line=True):
    """Common clean-up: quiet grid on one axis, no y-axis line, whole-number year ticks."""
    from matplotlib.ticker import MaxNLocator
    ax.grid(False)
    if grid_axis:
        ax.grid(axis=grid_axis)
    if hide_y_axis_line:
        ax.spines["left"].set_visible(False)
    ax.set_axisbelow(True)
    xs = []
    for line in ax.get_lines():
        try:
            xs.extend(float(v) for v in line.get_xdata())
        except (TypeError, ValueError):
            xs = []
            break
    if xs and ax.get_xscale() == "linear" and all(v == int(v) and 1000 <= v <= 3000 for v in xs):
        ax.xaxis.set_major_locator(MaxNLocator(integer=True, nbins="auto", steps=[1, 2, 5, 10]))
    return ax


def plain_log_ticks(ax, axis="y", values=None):
    """Label a log axis with ordinary numbers (50, 100, 200) instead of powers of ten."""
    from matplotlib.ticker import FixedLocator, FuncFormatter, NullFormatter
    target = ax.yaxis if axis == "y" else ax.xaxis
    if values is not None:
        target.set_major_locator(FixedLocator(values))
    target.set_major_formatter(FuncFormatter(lambda v, _: fmt(v)))
    target.set_minor_formatter(NullFormatter())
    return ax


# --- layout and saving -----------------------------------------------------------------

def _wrap(fig, text, fontsize, weight, width_in):
    if not text:
        return text
    renderer = fig.canvas.get_renderer()
    out = []
    for paragraph in str(text).split("\n"):
        probe = fig.text(0, 0, paragraph, fontsize=fontsize, fontweight=weight)
        width = probe.get_window_extent(renderer).width / fig.dpi
        probe.remove()
        if width <= width_in or len(paragraph) < 12:
            out.append(paragraph)
            continue
        chars = max(12, int(len(paragraph) * width_in / width * 0.96))
        out.extend(textwrap.wrap(paragraph, chars))
    return "\n".join(out)


def _manual_layout(fig, rect, rounds=3):
    """Fit all axes and their decorations inside rect (figure fraction) with subplots_adjust."""
    left0, bottom0, width0, height0 = rect
    right0, top0 = left0 + width0, bottom0 + height0
    for _ in range(rounds):
        fig.canvas.draw()
        for group in getattr(fig, "_chartkit_label_groups", []):
            _place_line_labels(group)
        renderer = fig.canvas.get_renderer()
        axes = [a for a in fig.axes if a.get_visible()]
        if not axes:
            return
        inv = fig.transFigure.inverted()
        tight = [inv.transform_bbox(a.get_tightbbox(renderer)) for a in axes]
        pos = [a.get_position() for a in axes]
        extra_left = min(p.x0 for p in pos) - min(t.x0 for t in tight)
        extra_right = max(t.x1 for t in tight) - max(p.x1 for p in pos)
        extra_bottom = min(p.y0 for p in pos) - min(t.y0 for t in tight)
        extra_top = max(t.y1 for t in tight) - max(p.y1 for p in pos)
        new = dict(left=left0 + extra_left, right=right0 - extra_right,
                   bottom=bottom0 + extra_bottom, top=top0 - extra_top)
        if new["right"] - new["left"] < 0.2 or new["top"] - new["bottom"] < 0.2:
            return
        grids = []
        for a in axes:
            spec = a.get_subplotspec() if hasattr(a, "get_subplotspec") else None
            if spec is not None:
                grid = spec.get_topmost_subplotspec().get_gridspec()
                if grid not in grids:
                    grids.append(grid)
        if not grids:
            return
        current = grids[0].get_subplot_params(fig)
        if all(abs(getattr(current, k) - v) < 1e-3 for k, v in new.items()):
            return
        for grid in grids:
            grid.update(**new)


def finish(fig, path=None, title=None, subtitle=None, source=None, note=None, alt=None,
           preset=None, lint=True, margin=0.32, save_kwargs=None):
    """Add the title block and footer, lay out, check, save, and write alt text.

    title     the finding, one line
    subtitle  what is plotted: measure, unit, scope, period
    note      a short note that changes the reading (definitions, exclusions)
    source    'Source: ...'
    alt       alt text; written to <image>.alt.txt
    Returns the chartlint findings.
    """
    name, p = _preset(preset or getattr(fig, "_chartkit_preset", None))
    base = p["base"]
    width_in, height_in = fig.get_size_inches()
    mx = margin / width_in
    my = margin / height_in
    usable = width_in - 2 * margin
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()

    header = []
    y = 1 - my
    for text, role, colour, weight in ((title, "title", INK, "bold"),
                                       (subtitle, "subtitle", INK_2, "normal")):
        if not text:
            continue
        fs = base * SCALE[role]
        wrapped = _wrap(fig, text, fs, weight, usable)
        t = fig.text(mx, y, wrapped, ha="left", va="top", fontsize=fs, color=colour,
                     fontweight=weight, linespacing=1.25)
        header.append(t)
        box = t.get_window_extent(renderer)
        y = box.y0 / fig.bbox.height - (base * 0.45) / 72.0 / height_in
    header_bottom = y if header else 1 - my

    footer_text = "\n".join([s for s in (note, source) if s])
    footer_top = my
    if footer_text:
        fs = base * SCALE["source"]
        wrapped = _wrap(fig, footer_text, fs, "normal", usable)
        t = fig.text(mx, my, wrapped, ha="left", va="bottom", fontsize=fs, color=MUTED,
                     linespacing=1.3)
        box = t.get_window_extent(renderer)
        footer_top = box.y1 / fig.bbox.height + (base * 0.9) / 72.0 / height_in

    gap_top = (base * 0.6) / 72.0 / height_in
    pad = 2.0 / 72.0
    rect = (mx - pad / width_in, footer_top, 1 - 2 * mx + 2 * pad / width_in,
            max(0.2, header_bottom - gap_top - footer_top))
    params = dict(rect=rect, w_pad=pad, h_pad=pad, wspace=0.04, hspace=0.06)
    try:
        from matplotlib.layout_engine import ConstrainedLayoutEngine
        engine = fig.get_layout_engine()
        if isinstance(engine, ConstrainedLayoutEngine):
            engine.set(**params)
        else:
            fig.set_layout_engine("constrained", **params)
        for _ in range(2):  # labels depend on the layout and the layout on the labels
            fig.canvas.draw()
            for group in getattr(fig, "_chartkit_label_groups", []):
                _place_line_labels(group)
        fig.canvas.draw()
    except Exception:
        # Figures built without constrained layout (for example with a colour bar added
        # first) cannot switch to it. Lay them out by measuring instead.
        fig.set_layout_engine("none")
        _manual_layout(fig, rect)
    fig.set_layout_engine("none")  # freeze the layout so the label positions stay valid
    for group in getattr(fig, "_chartkit_label_groups", []):
        _place_line_labels(group)
    fig.canvas.draw()

    findings = []
    if lint:
        try:
            from chartlint import lint_figure, format_report, safe_print
            findings = lint_figure(fig)
            safe_print(format_report(findings, path or "figure"))
        except Exception as error:  # pragma: no cover
            print("chartkit: lint skipped (%s)" % error)
    if path:
        fig.savefig(path, dpi=p["dpi"], **(save_kwargs or {}))
        if alt:
            alt_path = os.path.splitext(str(path))[0] + ".alt.txt"
            with open(alt_path, "w", encoding="utf-8") as handle:
                handle.write(alt.strip() + "\n")
        else:
            print("chartkit: no alt text given. Write one: chart type, what is plotted, "
                  "the main finding with its key number.")
    return findings
