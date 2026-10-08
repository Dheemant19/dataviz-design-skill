#!/usr/bin/env python3
"""Automated layout and encoding checks for matplotlib figures.

A palette checker can only judge colours. Most of what goes wrong in an agent's
chart is layout and encoding: labels that collide, text cut off at the edge,
bars that do not start at zero, a dozen coloured lines, series squashed into a
thin band, more words than data. These are measurable once the figure is drawn,
so this script measures them.

Two ways to use it
------------------
1. Run a plotting script through it. Every figure the script saves or shows is
   checked first. Nothing in the script needs to change.

       python chartlint.py make_chart.py [script args...]

2. Import it and check a figure directly.

       import sys; sys.path.insert(0, "<skill>/scripts")
       from chartlint import lint_figure, format_report
       print(format_report(lint_figure(fig)))

Each finding has a level:
  FAIL  something a reader will misread, or text they cannot read
  WARN  very likely a problem. Fix it or have a reason
  NOTE  worth a look, no action needed if it is intended

The thresholds are heuristics. Always look at the rendered image as well.
Exit status of the command-line mode: 1 if any FAIL, otherwise 0.
"""

import math
import os
import runpy
import sys
from itertools import combinations

try:
    import matplotlib
except ImportError:  # pragma: no cover
    print("chartlint needs matplotlib installed.", file=sys.stderr)
    raise

from matplotlib.container import BarContainer
from matplotlib.patches import Rectangle, Wedge
from matplotlib.text import Annotation, Text

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    import check_palette as _pal
except Exception:  # pragma: no cover - palette checks are skipped if unavailable
    _pal = None

# --- thresholds (heuristics) ---------------------------------------------------

MIN_FONT_PT = 7.0            # smaller text is hard to read at almost any size
MIN_TICK_FONT_PT = 8.0       # tick and axis labels carry the scale
MAX_LEGEND_ENTRIES = 6       # beyond this, readers lose track
MAX_LINE_COLOURS = 5         # distinct colours among data lines in one panel
MAX_PIE_WEDGES = 5
MAX_FIGURE_TEXT_CHARS = 360  # titles, subtitles, notes and panel titles together
MAX_TITLE_CHARS = 90
MAX_CALLOUTS = 3             # annotations with a leader line or arrow, per panel
SQUASH_BAND = 0.15           # share of the axis height counted as "squashed"
SQUASH_MIN_SERIES = 3
OVERLAP_TOLERANCE_PX = 1.5

RAINBOW_MAPS = {"jet", "rainbow", "hsv", "gist_rainbow", "nipy_spectral",
                "gist_ncar", "turbo", "spectral", "prism", "flag"}
DIVERGING_MAPS = {"rdbu", "rdbu_r", "bwr", "bwr_r", "seismic", "seismic_r", "coolwarm",
                  "coolwarm_r", "puor", "puor_r", "brbg", "brbg_r", "piyg", "piyg_r",
                  "prgn", "prgn_r", "rdgy", "rdgy_r", "rdylbu", "rdylbu_r", "rdylgn",
                  "rdylgn_r", "spectral_r", "vlag", "icefire"}


def _add(findings, level, check, message, where=""):
    findings.append({"level": level, "check": check, "message": message, "where": where})


def _short(text, n=28):
    text = str(text).replace("$\\mathdefault{", "").replace("}$", "").replace("$", "")
    text = " ".join(text.split())
    return text if len(text) <= n else text[: n - 1] + "…"


def _panel_name(ax, index):
    title = ax.get_title() or ax.get_title(loc="left") or ax.get_ylabel()
    return "panel %d%s" % (index + 1, (" (%s)" % _short(title, 24)) if title else "")


# --- text inventory ------------------------------------------------------------

def _visible_texts(fig, renderer):
    """Every visible, non-empty text artist with its role and window extent."""
    found = []

    def take(artist, role, ax_index=None):
        try:
            if artist is None or not artist.get_visible():
                return
            text = artist.get_text()
            if not text or not str(text).strip():
                return
            # For annotations, measure the text only, not the leader line.
            box = Text.get_window_extent(artist, renderer)
            if box.width <= 0 or box.height <= 0:
                return
            found.append({"artist": artist, "role": role, "text": text, "box": box,
                          "ax": ax_index})
        except Exception:
            return

    for t in fig.texts:
        take(t, "figure")
    if getattr(fig, "_suptitle", None) is not None:
        take(fig._suptitle, "figure")
    for i, ax in enumerate(fig.axes):
        if not ax.get_visible():
            continue
        for title in _ax_title_artists(ax):
            take(title, "panel_title", i)
        take(ax.xaxis.label, "axis_label", i)
        take(ax.yaxis.label, "axis_label", i)
        for tick in _drawn_tick_labels(ax):
            take(tick, "tick", i)
        for child in ax.texts:
            take(child, "annotation" if isinstance(child, Annotation) else "text", i)
        legend = ax.get_legend()
        if legend is not None:
            take(legend.get_title(), "legend", i)
            for t in legend.get_texts():
                take(t, "legend", i)
    for legend in getattr(fig, "legends", []):
        for t in legend.get_texts():
            take(t, "legend")
    return found


def _drawn_tick_labels(ax):
    """Tick labels that are actually drawn (inside the view limits)."""
    out = []
    for axis in (ax.xaxis, ax.yaxis):
        try:
            low, high = sorted(axis.get_view_interval())
        except Exception:
            continue
        eps = 1e-9 * max(abs(high - low), 1e-12)
        for tick in list(axis.get_major_ticks()) + list(axis.get_minor_ticks()):
            try:
                loc = tick.get_loc()
            except Exception:
                continue
            if loc is None or not (low - eps <= loc <= high + eps):
                continue
            for label in (tick.label1, tick.label2):
                if label.get_visible() and label.get_text():
                    out.append(label)
    return out


def _ax_title_artists(ax):
    out = []
    for name in ("title", "_left_title", "_right_title"):
        t = getattr(ax, name, None)
        if t is not None and t.get_text():
            out.append(t)
    return out


# --- checks --------------------------------------------------------------------

def check_text(fig, renderer, findings):
    texts = _visible_texts(fig, renderer)
    fig_box = fig.bbox

    # Overlapping text.
    tick_groups = {}
    other_pairs = []
    for a, b in combinations(texts, 2):
        if a["artist"] is b["artist"]:
            continue
        ba, bb = a["box"], b["box"]
        overlap_w = min(ba.x1, bb.x1) - max(ba.x0, bb.x0)
        overlap_h = min(ba.y1, bb.y1) - max(ba.y0, bb.y0)
        if overlap_w <= OVERLAP_TOLERANCE_PX or overlap_h <= OVERLAP_TOLERANCE_PX:
            continue
        same_place = (a["text"] == b["text"] and abs(ba.x0 - bb.x0) < 2 and abs(ba.y0 - bb.y0) < 2)
        if same_place:
            continue  # the same tick drawn twice, e.g. by a twin axis
        if a["role"] == "tick" and b["role"] == "tick" and a["ax"] == b["ax"]:
            tick_groups.setdefault(a["ax"], set()).update([a["text"], b["text"]])
        else:
            other_pairs.append((a, b))
    for ax_index, labels in tick_groups.items():
        sample = ", ".join("'%s'" % _short(t, 16) for t in sorted(labels)[:3])
        _add(findings, "FAIL", "text-overlap",
             "%d tick labels collide (%s ...). Show fewer ticks, shorten the labels, or use "
             "horizontal bars for long category names." % (len(labels), sample),
             _panel_name(fig.axes[ax_index], ax_index))
    for a, b in other_pairs[:8]:
        _add(findings, "FAIL", "text-overlap",
             "%s '%s' overlaps %s '%s'. Move one, shorten it, or give the panel more room." % (
                 a["role"].replace("_", " "), _short(a["text"]),
                 b["role"].replace("_", " "), _short(b["text"])))
    if len(other_pairs) > 8:
        _add(findings, "FAIL", "text-overlap",
             "%d more overlapping text pairs." % (len(other_pairs) - 8))

    # Text cut off at the figure edge.
    for t in texts:
        box = t["box"]
        if (box.x0 < fig_box.x0 - 1 or box.x1 > fig_box.x1 + 1 or
                box.y0 < fig_box.y0 - 1 or box.y1 > fig_box.y1 + 1):
            _add(findings, "FAIL", "text-clipped",
                 "%s '%s' runs past the edge of the figure and will be cut off."
                 % (t["role"].replace("_", " "), _short(t["text"])))

    # Font sizes.
    small = {}
    for t in texts:
        size = t["artist"].get_fontsize()
        limit = MIN_TICK_FONT_PT if t["role"] in ("tick", "axis_label") else MIN_FONT_PT
        if size < limit - 0.05:
            small.setdefault((t["role"], round(size, 1)), []).append(t["text"])
    for (role, size), items in small.items():
        _add(findings, "WARN", "font-size",
             "%d %s text(s) at %.1f pt, below %.0f pt (e.g. '%s'). Check them at the size "
             "the chart will be shown." % (len(items), role.replace("_", " "), size,
                                            MIN_TICK_FONT_PT if role in ("tick", "axis_label")
                                            else MIN_FONT_PT, _short(items[0])))

    # Text budget: titles, subtitles, notes and panel titles.
    heavy = [t for t in texts if t["role"] in ("figure", "panel_title")]
    chars = sum(len(" ".join(str(t["text"]).split())) for t in heavy)
    if chars > MAX_FIGURE_TEXT_CHARS:
        _add(findings, "WARN", "text-budget",
             "%d characters of title, subtitle, note and panel-title text (budget about %d). "
             "Keep one finding in the title and one line of scope in the subtitle. Move other "
             "caveats into the message that goes with the chart." % (chars, MAX_FIGURE_TEXT_CHARS))
    figure_texts = [t for t in texts if t["role"] == "figure"]
    if figure_texts:
        largest = max(figure_texts, key=lambda t: t["artist"].get_fontsize())
        title = " ".join(str(largest["text"]).split())
        if len(title) > MAX_TITLE_CHARS:
            _add(findings, "WARN", "title-length",
                 "The title is %d characters. Aim for one line that states the finding."
                 % len(title))
        if len(str(largest["text"]).strip().splitlines()) > 2:
            _add(findings, "WARN", "title-length", "The title wraps onto three or more lines.")
    return texts


def check_bars(ax, index, findings):
    name = _panel_name(ax, index)
    for container in ax.containers:
        if not isinstance(container, BarContainer):
            continue
        patches = [p for p in container.patches if p.get_visible()]
        if not patches:
            continue
        horizontal = getattr(container, "orientation", None) == "horizontal"
        if horizontal:
            sizes = [p.get_height() for p in patches]
            bases = [p.get_x() for p in patches]
            ends = [p.get_x() + p.get_width() for p in patches]
            low, high = sorted(ax.get_xlim())
            scale = ax.get_xscale()
        else:
            sizes = [p.get_width() for p in patches]
            bases = [p.get_y() for p in patches]
            ends = [p.get_y() + p.get_height() for p in patches]
            low, high = sorted(ax.get_ylim())
            scale = ax.get_yscale()

        if scale == "log":
            _add(findings, "WARN", "bar-log-scale",
                 "Bars on a log axis have no meaningful zero, so their lengths mislead. "
                 "Use dots or lines on a log scale.", name)
        else:
            base_min = min(bases)
            values = [e - b for e, b in zip(ends, bases)]
            positive = all(v >= 0 for v in values)
            negative = all(v <= 0 for v in values)
            if positive and base_min >= 0 and low > 1e-12 * max(1.0, abs(high)):
                _add(findings, "FAIL", "bar-baseline",
                     "The value axis starts at %.4g, not zero, so bar lengths exaggerate "
                     "differences. Start at zero or switch to dots." % low, name)
            elif negative and high < -1e-12:
                _add(findings, "FAIL", "bar-baseline",
                     "The value axis stops at %.4g, not zero, so bar lengths exaggerate "
                     "differences." % high, name)
        if len(sizes) > 1:
            spread = (max(sizes) - min(sizes)) / max(abs(max(sizes)), 1e-12)
            if spread > 0.02:
                _add(findings, "WARN", "bar-width",
                     "Bars in one series have different thicknesses. Unequal widths add an "
                     "area cue nobody asked for.", name)


def check_lines(ax, index, findings):
    name = _panel_name(ax, index)
    data_lines = []
    for line in ax.get_lines():
        if not line.get_visible():
            continue
        try:
            xs = [float(v) for v in line.get_xdata(orig=False)]
            ys = [float(v) for v in line.get_ydata(orig=False)]
        except (TypeError, ValueError):
            continue
        pts = [(x, y) for x, y in zip(xs, ys) if math.isfinite(x) and math.isfinite(y)]
        if len(pts) < 3:
            continue  # reference lines, markers, axhline/axvline
        if line.get_linestyle() in ("None", "none", " ", ""):
            continue  # scatter drawn with plot()
        data_lines.append((line, [p[1] for p in pts]))
    if not data_lines:
        return

    colours = {}
    for line, _ in data_lines:
        try:
            rgba = matplotlib.colors.to_rgba(line.get_color())
        except ValueError:
            continue
        key = tuple(round(c, 2) for c in rgba[:3])
        colours.setdefault(key, 0)
        colours[key] += 1
    chromatic = [c for c in colours if _chroma(c) > 0.03]
    if len(chromatic) > MAX_LINE_COLOURS:
        _add(findings, "WARN", "too-many-colours",
             "%d differently coloured lines. Readers cannot match that many colours. Show the "
             "series that matter in colour and the rest in grey, or use small multiples."
             % len(chromatic), name)

    # Series squashed into a thin band of the axis.
    low, high = ax.get_ylim()
    span = high - low
    if ax.get_yscale() == "linear" and span > 0 and len(data_lines) >= SQUASH_MIN_SERIES + 1:
        top_values = []
        for line, ys in data_lines:
            ordered = sorted(ys)
            top = ordered[int(0.95 * (len(ordered) - 1))]
            bottom = ordered[int(0.05 * (len(ordered) - 1))]
            top_values.append(((top - low) / span, (bottom - low) / span))
        squashed_low = [t for t in top_values if t[0] < SQUASH_BAND]
        tall = [t for t in top_values if t[0] > 0.5]
        if len(squashed_low) >= SQUASH_MIN_SERIES and tall:
            _add(findings, "WARN", "squashed-series",
                 "%d of %d lines sit in the bottom %d%% of the axis, so they cannot be read or "
                 "compared. If the message is about change, index each series to a start value "
                 "or show percent change. If the values span orders of magnitude, use a log "
                 "scale. Otherwise use small multiples or a second panel."
                 % (len(squashed_low), len(top_values), round(SQUASH_BAND * 100)), name)


def check_legend(ax, index, findings):
    legend = ax.get_legend()
    if legend is None or not legend.get_visible():
        return
    entries = [t for t in legend.get_texts() if t.get_text()]
    if len(entries) > MAX_LEGEND_ENTRIES:
        _add(findings, "WARN", "legend-size",
             "The legend has %d entries. Label series directly, highlight the few that "
             "matter, or split into small multiples." % len(entries), _panel_name(ax, index))


def check_pie(ax, index, findings):
    wedges = [p for p in ax.patches if isinstance(p, Wedge) and p.get_visible()]
    if not wedges:
        return
    name = _panel_name(ax, index)
    if len(wedges) > MAX_PIE_WEDGES:
        _add(findings, "WARN", "pie-slices",
             "A pie with %d slices. Angles are hard to compare. Use sorted horizontal bars."
             % len(wedges), name)
    centres = {(round(w.center[0], 3), round(w.center[1], 3)) for w in wedges}
    if len(centres) > 1 and len(wedges) < 40:
        _add(findings, "WARN", "pie-exploded",
             "Some slices are pulled out of the pie. Emphasise with colour or a label instead.",
             name)


def check_colour_maps(ax, index, findings):
    name = _panel_name(ax, index)
    mappables = list(ax.images) + [c for c in ax.collections if hasattr(c, "get_cmap")]
    for m in mappables:
        try:
            if m.get_array() is None:
                continue
            cmap = m.get_cmap()
        except Exception:
            continue
        cname = (getattr(cmap, "name", "") or "").lower()
        base = cname[:-2] if cname.endswith("_r") else cname
        if base in RAINBOW_MAPS:
            _add(findings, "FAIL", "rainbow-colormap",
                 "The '%s' colour map changes lightness unevenly and creates false bands. Use "
                 "a sequential map (viridis, cividis, Blues) for amounts or a diverging map "
                 "for values around a midpoint." % cname, name)
        if cname in DIVERGING_MAPS or base in DIVERGING_MAPS:
            norm = m.norm
            cls = type(norm).__name__
            if cls in ("TwoSlopeNorm", "CenteredNorm"):
                continue
            vmin, vmax = norm.vmin, norm.vmax
            if vmin is None or vmax is None:
                continue
            if vmin < 0 < vmax and abs(vmin + vmax) > 0.05 * (vmax - vmin):
                _add(findings, "WARN", "diverging-centre",
                     "A diverging colour map runs from %.3g to %.3g, so its neutral colour is "
                     "not at zero. Use symmetric limits or TwoSlopeNorm(vcenter=0)."
                     % (vmin, vmax), name)
            elif vmin >= 0 or vmax <= 0:
                _add(findings, "WARN", "diverging-centre",
                     "A diverging colour map is used for values on one side of zero only. "
                     "Use a sequential map unless there is a meaningful midpoint.", name)


def check_axes_structure(fig, findings):
    axes = [a for a in fig.axes if a.get_visible()]
    for i, ax in enumerate(axes):
        if getattr(ax, "name", "") == "3d":
            _add(findings, "WARN", "3d",
                 "A 3D panel. Perspective hides and distorts values. Use a flat chart, a "
                 "heatmap or a contour plot.", _panel_name(ax, i))
    for (i, a), (j, b) in combinations(enumerate(axes), 2):
        try:
            same_box = all(abs(u - v) < 1e-6 for u, v in
                           zip(a.get_position().bounds, b.get_position().bounds))
            shared_x = a.get_shared_x_axes().joined(a, b)
        except Exception:
            continue
        if same_box and shared_x and getattr(a, "name", "") != "3d":
            _add(findings, "WARN", "dual-axis",
                 "Two y-axes share one panel. Their scales can be set to show any relationship. "
                 "Use two aligned panels, or index both series to a common base.",
                 _panel_name(a, i))


def check_scales(ax, index, texts, findings):
    name = _panel_name(ax, index)
    words = " ".join(str(t["text"]).lower() for t in texts)
    for axis_name, scale in (("y", ax.get_yscale()), ("x", ax.get_xscale())):
        if scale in ("log", "symlog") and "log" not in words:
            _add(findings, "NOTE", "log-scale",
                 "The %s-axis is logarithmic but no text says so. Readers will assume a "
                 "linear scale." % axis_name, name)


def check_callouts(ax, index, findings):
    callouts = [t for t in ax.texts if isinstance(t, Annotation) and t.arrow_patch is not None
                and t.get_visible() and not getattr(t, "_chartkit_role", None)]
    if len(callouts) > MAX_CALLOUTS:
        _add(findings, "WARN", "callouts",
             "%d annotations with leader lines in one panel. Keep the one or two the reader "
             "must not miss." % len(callouts), _panel_name(ax, index))


def check_units(fig, findings):
    missing = []
    for index, ax in enumerate(fig.axes):
        if not ax.get_visible() or getattr(ax, "name", "") == "3d":
            continue
        if hasattr(ax, "_colorbar") or ax.images:
            continue
        if not (ax.get_lines() or ax.patches or ax.collections):
            continue
        yticks = [t for t in ax.get_yticklabels() if t.get_text()]
        numeric = sum(1 for t in yticks if any(ch.isdigit() for ch in t.get_text()))
        if numeric >= 2 and not ax.get_ylabel() and not _ax_title_artists(ax):
            missing.append(_panel_name(ax, index))
    if missing:
        _add(findings, "NOTE", "units",
             "Numeric y-axis with no axis label or panel title in %s. Make sure the unit is "
             "stated where the reader will see it, for example in the subtitle."
             % ", ".join(missing))


def _chroma(rgb):
    if _pal is None:
        r, g, b = rgb
        return max(rgb) - min(rgb)
    lab = _pal.oklab(_pal.linear_rgb(rgb))
    return (lab[1] ** 2 + lab[2] ** 2) ** 0.5


def _data_colours(ax):
    colours = set()
    for line in ax.get_lines():
        if line.get_visible() and len(line.get_xdata()) >= 2:
            colours.add(matplotlib.colors.to_hex(line.get_color()))
    for p in ax.patches:
        if isinstance(p, (Rectangle, Wedge)) and p.get_visible() and p.get_fill():
            fc = p.get_facecolor()
            if fc[3] > 0.2:
                colours.add(matplotlib.colors.to_hex(fc[:3]))
    for c in ax.collections:
        try:
            if c.get_array() is not None:
                continue
            for fc in c.get_facecolors()[:50]:
                if fc[3] > 0.2:
                    colours.add(matplotlib.colors.to_hex(fc[:3]))
        except Exception:
            continue
    return colours


def check_colours(fig, findings):
    if _pal is None:
        return
    seen_pairs = set()
    confusable = []
    for i, ax in enumerate(fig.axes):
        if not ax.get_visible():
            continue
        name = _panel_name(ax, i)
        background = matplotlib.colors.to_hex(ax.get_facecolor()[:3])
        if ax.get_facecolor()[3] < 0.05:
            background = matplotlib.colors.to_hex(fig.get_facecolor()[:3])
        bg_lin = _pal.linear_rgb(_pal.parse_hex(background))
        colours = sorted(_data_colours(ax))
        chromatic = []
        for hexcode in colours:
            rgb = _pal.parse_hex(hexcode)
            lin = _pal.linear_rgb(rgb)
            if _chroma(rgb) > 0.03:
                chromatic.append(hexcode)
                ratio = _pal.contrast_ratio(lin, bg_lin)
                if ratio < 1.6:
                    _add(findings, "WARN", "mark-contrast",
                         "Data colour %s is barely visible on the background %s (%.2f:1)."
                         % (hexcode, background, ratio), name)
        if 2 <= len(chromatic) <= 12:
            rows = _pal.pairwise_report([c.upper() for c in chromatic],
                                        [_pal.linear_rgb(_pal.parse_hex(c)) for c in chromatic])
            for row in rows:
                key = tuple(sorted(row["pair"]))
                if row["worst_distance"] < _pal.PAIR_FAIL and key not in seen_pairs:
                    seen_pairs.add(key)
                    confusable.append("%s/%s (%s)" % (row["pair"][0], row["pair"][1],
                                                      row["worst_view"]))
    if confusable:
        shown = ", ".join(confusable[:4]) + (" and %d more" % (len(confusable) - 4)
                                             if len(confusable) > 4 else "")
        _add(findings, "WARN", "colour-confusable",
             "Colour pairs that look nearly the same with colour-vision deficiency: %s. If "
             "these colours carry meaning, add direct labels, shapes or line styles, or "
             "change the palette." % shown)


def lint_figure(fig):
    """Draw the figure and return a list of findings (dicts with level, check, message)."""
    findings = []
    try:
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()
    except Exception as error:  # pragma: no cover
        _add(findings, "WARN", "draw", "Could not draw the figure to check it: %s" % error)
        return findings

    def guard(fn, *args):
        try:
            fn(*args)
        except Exception as error:  # never let a check break the user's run
            _add(findings, "NOTE", "internal", "Check %s skipped (%s)." % (fn.__name__, error))

    texts = []
    try:
        texts = check_text(fig, renderer, findings)
    except Exception as error:
        _add(findings, "NOTE", "internal", "Text checks skipped (%s)." % error)
    guard(check_axes_structure, fig, findings)
    for i, ax in enumerate(fig.axes):
        if not ax.get_visible():
            continue
        guard(check_bars, ax, i, findings)
        guard(check_lines, ax, i, findings)
        guard(check_legend, ax, i, findings)
        guard(check_pie, ax, i, findings)
        guard(check_colour_maps, ax, i, findings)
        guard(check_scales, ax, i, texts, findings)
        guard(check_callouts, ax, i, findings)
    guard(check_units, fig, findings)
    guard(check_colours, fig, findings)
    order = {"FAIL": 0, "WARN": 1, "NOTE": 2}
    findings.sort(key=lambda f: order.get(f["level"], 3))
    return findings


def safe_print(text):
    """Print without crashing on consoles that cannot show some characters (Windows pipes)."""
    text = str(text).replace("\u2212", "-").replace("\u2026", "...")
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("ascii", "replace").decode("ascii"))


def format_report(findings, label="figure"):
    lines = ["chartlint: %s" % label]
    if not findings:
        lines.append("  PASS: no layout or encoding problems found. Still look at the image.")
        return "\n".join(lines)
    for f in findings:
        where = (" [%s]" % f["where"]) if f.get("where") else ""
        lines.append("  %s %s%s: %s" % (f["level"], f["check"], where, f["message"]))
    fails = sum(f["level"] == "FAIL" for f in findings)
    warns = sum(f["level"] == "WARN" for f in findings)
    lines.append("  Result: %s (%d fail, %d warn)" % ("FAIL" if fails else ("WARN" if warns else "PASS"),
                                                       fails, warns))
    return "\n".join(lines)


# --- command-line mode -----------------------------------------------------------

def _run_script(path, args):
    matplotlib.use("Agg", force=True)
    import matplotlib.pyplot as plt
    from matplotlib.figure import Figure

    results = []
    seen = set()
    original_savefig = Figure.savefig

    def checked_savefig(self, fname, *a, **kw):
        if id(self) not in seen:
            seen.add(id(self))
            findings = lint_figure(self)
            results.append(findings)
            safe_print(format_report(findings, str(fname)))
        return original_savefig(self, fname, *a, **kw)

    def checked_show(*a, **kw):
        for num in plt.get_fignums():
            fig = plt.figure(num)
            if id(fig) not in seen:
                seen.add(id(fig))
                findings = lint_figure(fig)
                results.append(findings)
                safe_print(format_report(findings, "figure %d (shown)" % num))

    Figure.savefig = checked_savefig
    plt.show = checked_show
    sys.argv = [path] + list(args)
    script_dir = os.path.dirname(os.path.abspath(path))
    sys.path.insert(0, script_dir)
    try:
        runpy.run_path(path, run_name="__main__")
    finally:
        Figure.savefig = original_savefig
    for num in plt.get_fignums():
        fig = plt.figure(num)
        if id(fig) not in seen:
            seen.add(id(fig))
            findings = lint_figure(fig)
            results.append(findings)
            safe_print(format_report(findings, "figure %d (not saved)" % num))
    if not results:
        print("chartlint: the script created no figures.")
    return 1 if any(f["level"] == "FAIL" for r in results for f in r) else 0


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    return _run_script(argv[0], argv[1:])


if __name__ == "__main__":
    sys.exit(main())
