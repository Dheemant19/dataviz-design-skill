#!/usr/bin/env python3
"""Check a chart colour palette for visibility, distinctness and ordering.

Standard library only. Works with Python 3.8 or later.

Checks
------
All palette types:
  * Contrast of every colour against the background (WCAG 2.1 contrast ratio).

Qualitative (default):
  * Every pair of colours stays distinct for normal vision, for simulated
    protanopia, deuteranopia and tritanopia, and in greyscale.

Sequential:
  * Perceived lightness changes steadily in one direction.
  * Neighbouring steps differ enough to tell apart.

Diverging:
  * The centre colour is the lightest (or the darkest) in the ramp.
  * Each arm changes lightness steadily away from the centre.
  * The two ends have similar lightness, so neither side dominates.
  * The two ends stay distinct under simulated colour-vision deficiency.

Colour differences are Euclidean distances in the Oklab colour space
(Ottosson, 2020). Colour-vision deficiency is simulated with the matrices of
Machado, Oliveira and Fernandes (2009) at full severity. The thresholds are
heuristics. A warning means "look at the rendered chart", not "this is wrong".
A note is information only and does not change the result.

Examples
--------
  python check_palette.py "#0072B2" "#E69F00" "#009E73"
  python check_palette.py "#eff3ff" "#6baed6" "#08519c" --type sequential
  python check_palette.py "#ca0020" "#f7f7f7" "#0571b0" --type diverging --json
  python check_palette.py "#4477AA" "#EE6677" --background "#111111"

Exit status: 0 if no check failed, 1 if any check failed, 2 on bad input.
"""

import argparse
import json
import sys

# --- thresholds (heuristics, see module docstring) ---------------------------

CONTRAST_FAIL = 1.25  # below this a mark is close to invisible on the background
CONTRAST_WARN = 3.0   # WCAG 2.1 SC 1.4.11 minimum for graphical objects
PAIR_FAIL = 0.05      # Oklab distance: pair is close to indistinguishable
PAIR_WARN = 0.07      # Oklab distance: pair is hard to tell apart in small marks
GREY_WARN = 0.06      # Oklab lightness gap needed to survive greyscale
STEP_WARN = 0.04      # minimum lightness step between neighbours in a ramp
ARM_BALANCE_WARN = 0.12  # allowed lightness gap between the two ends of a diverging ramp

# Machado, Oliveira & Fernandes (2009), severity 1.0, applied to linear RGB.
CVD_MATRICES = {
    "protanopia": (
        (0.152286, 1.052583, -0.204868),
        (0.114503, 0.786281, 0.099216),
        (-0.003882, -0.048116, 1.051998),
    ),
    "deuteranopia": (
        (0.367322, 0.860646, -0.227968),
        (0.280085, 0.672501, 0.047413),
        (-0.011820, 0.042940, 0.968881),
    ),
    "tritanopia": (
        (1.255528, -0.076749, -0.178779),
        (-0.078411, 0.930809, 0.147602),
        (0.004733, 0.691367, 0.303900),
    ),
}


# --- colour maths -----------------------------------------------------------

def parse_hex(text):
    """Return (r, g, b) in 0..1 from '#rgb' or '#rrggbb'."""
    raw = text.strip().lstrip("#")
    if len(raw) == 3:
        raw = "".join(ch * 2 for ch in raw)
    if len(raw) != 6:
        raise ValueError("not a hex colour: %r" % text)
    try:
        return tuple(int(raw[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
    except ValueError:
        raise ValueError("not a hex colour: %r" % text)


def to_linear(channel):
    if channel <= 0.04045:
        return channel / 12.92
    return ((channel + 0.055) / 1.055) ** 2.4


def linear_rgb(rgb):
    return tuple(to_linear(c) for c in rgb)


def relative_luminance(lin):
    r, g, b = lin
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(lin_a, lin_b):
    la, lb = relative_luminance(lin_a), relative_luminance(lin_b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def oklab(lin):
    """Linear sRGB to Oklab (L, a, b)."""
    r, g, b = lin
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = (max(v, 0.0) ** (1.0 / 3.0) for v in (l, m, s))
    return (
        0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
        1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
        0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_,
    )


def distance(lab_a, lab_b):
    return sum((x - y) ** 2 for x, y in zip(lab_a, lab_b)) ** 0.5


def simulate(lin, matrix):
    out = []
    for row in matrix:
        value = sum(coef * chan for coef, chan in zip(row, lin))
        out.append(min(1.0, max(0.0, value)))
    return tuple(out)


# --- checks -----------------------------------------------------------------

def add(findings, level, check, message):
    findings.append({"level": level, "check": check, "message": message})


def check_contrast(names, lins, background_name, background_lin, findings, is_ramp):
    """Qualitative colours are judged one by one. A ramp is expected to have a pale
    (or dark) end near the background, so it gets a single note instead."""
    ratios = [contrast_ratio(lin, background_lin) for lin in lins]
    if is_ramp:
        low = [name for name, ratio in zip(names, ratios) if ratio < CONTRAST_WARN]
        if low:
            add(findings, "note", "contrast",
                "Contrast below 3:1 on %s for %d of %d colours (%s). That is normal for the "
                "pale part of a ramp in filled cells. For points or lines, use stronger "
                "colours throughout." % (background_name, len(low), len(names), ", ".join(low)))
        return
    for name, ratio in zip(names, ratios):
        if ratio < CONTRAST_FAIL:
            add(findings, "fail", "contrast",
                "%s is nearly invisible on %s (contrast %.2f:1)." % (name, background_name, ratio))
        elif ratio < CONTRAST_WARN:
            add(findings, "warn", "contrast",
                "%s has low contrast on %s (%.2f:1, below 3:1). Fine for large filled areas, "
                "weak for lines, points and text." % (name, background_name, ratio))


def pairwise_report(names, lins):
    """Smallest Oklab distance for each pair across normal vision and the three simulations."""
    views = {"normal vision": [oklab(lin) for lin in lins]}
    for label, matrix in CVD_MATRICES.items():
        views[label] = [oklab(simulate(lin, matrix)) for lin in lins]
    rows = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            per_view = {label: distance(labs[i], labs[j]) for label, labs in views.items()}
            worst = min(per_view, key=per_view.get)
            lightness_gap = abs(views["normal vision"][i][0] - views["normal vision"][j][0])
            rows.append({
                "pair": [names[i], names[j]],
                "distances": {k: round(v, 3) for k, v in per_view.items()},
                "worst_view": worst,
                "worst_distance": round(per_view[worst], 3),
                "lightness_gap": round(lightness_gap, 3),
            })
    return rows


def check_qualitative(names, lins, findings):
    rows = pairwise_report(names, lins)
    grey_pairs = []
    for row in rows:
        a, b = row["pair"]
        worst, dist = row["worst_view"], row["worst_distance"]
        if dist < PAIR_FAIL:
            add(findings, "fail", "distinct",
                "%s and %s are nearly identical under %s (distance %.3f)." % (a, b, worst, dist))
        elif dist < PAIR_WARN:
            add(findings, "warn", "distinct",
                "%s and %s are hard to tell apart under %s (distance %.3f). "
                "Add labels, shapes or dash styles, or change one colour." % (a, b, worst, dist))
        if row["lightness_gap"] < GREY_WARN:
            grey_pairs.append("%s/%s" % (a, b))
    if grey_pairs:
        shown = ", ".join(grey_pairs[:3]) + (" and others" if len(grey_pairs) > 3 else "")
        add(findings, "note", "greyscale",
            "%d pair(s) have almost the same lightness and will merge in greyscale print (%s). "
            "Balanced lightness is normal for category colours. Add labels, shapes or dash "
            "styles if the chart may be printed without colour." % (len(grey_pairs), shown))
    if len(names) > 8:
        add(findings, "warn", "count",
            "%d categorical colours is a lot to match against a legend. Consider direct labels, "
            "small multiples, or highlighting a few and greying the rest." % len(names))
    return rows


def monotonic_direction(values):
    """Return 1 if strictly rising, -1 if strictly falling, 0 otherwise."""
    diffs = [b - a for a, b in zip(values, values[1:])]
    if all(d > 0 for d in diffs):
        return 1
    if all(d < 0 for d in diffs):
        return -1
    return 0


def check_steps(names, lightness, findings, label):
    for (name_a, l_a), (name_b, l_b) in zip(zip(names, lightness), zip(names[1:], lightness[1:])):
        if abs(l_b - l_a) < STEP_WARN:
            add(findings, "warn", "steps",
                "%s: %s and %s differ very little in lightness (%.3f). Neighbouring classes "
                "may look the same." % (label, name_a, name_b, abs(l_b - l_a)))


def check_sequential(names, lins, findings):
    lightness = [oklab(lin)[0] for lin in lins]
    if len(names) < 2:
        add(findings, "fail", "order", "A sequential ramp needs at least two colours.")
        return lightness
    if monotonic_direction(lightness) == 0:
        add(findings, "fail", "order",
            "Lightness does not change steadily along the ramp (%s). Readers will not see a "
            "clear low-to-high order." % ", ".join("%.2f" % v for v in lightness))
    else:
        check_steps(names, lightness, findings, "Ramp")
    return lightness


def check_diverging(names, lins, findings):
    lightness = [oklab(lin)[0] for lin in lins]
    count = len(names)
    if count < 3 or count % 2 == 0:
        add(findings, "fail", "centre",
            "A diverging ramp needs an odd number of colours (3 or more) so that it has a "
            "centre colour. Got %d." % count)
        return lightness
    mid = count // 2
    centre = lightness[mid]
    if not (centre >= max(lightness) - 1e-9 or centre <= min(lightness) + 1e-9):
        add(findings, "fail", "centre",
            "The centre colour %s is neither the lightest nor the darkest (lightness %.2f). "
            "The midpoint will not read as neutral." % (names[mid], centre))
    left, right = lightness[:mid + 1], lightness[mid:]
    if monotonic_direction(left) == 0 or monotonic_direction(right) == 0:
        add(findings, "fail", "order",
            "Lightness does not change steadily from the centre to each end (%s)."
            % ", ".join("%.2f" % v for v in lightness))
    else:
        check_steps(names[:mid + 1], left, findings, "Left arm")
        check_steps(names[mid:], right, findings, "Right arm")
    gap = abs(lightness[0] - lightness[-1])
    if gap > ARM_BALANCE_WARN:
        add(findings, "warn", "balance",
            "The two ends differ in lightness by %.2f, so one side will look stronger than "
            "the other for equal distances from the centre." % gap)
    ends = pairwise_report([names[0], names[-1]], [lins[0], lins[-1]])[0]
    if ends["worst_distance"] < PAIR_WARN:
        level = "fail" if ends["worst_distance"] < PAIR_FAIL else "warn"
        add(findings, level, "distinct",
            "The two ends %s and %s are hard to tell apart under %s (distance %.3f). The two "
            "directions may be confused." % (names[0], names[-1], ends["worst_view"],
                                             ends["worst_distance"]))
    return lightness


# --- command line -----------------------------------------------------------

def run(colours, palette_type, background):
    names = [("#" + c.strip().lstrip("#")).upper() for c in colours]
    lins = [linear_rgb(parse_hex(c)) for c in colours]
    background_name = ("#" + background.strip().lstrip("#")).upper()
    background_lin = linear_rgb(parse_hex(background))

    findings = []
    result = {"type": palette_type, "background": background_name, "colours": names}

    check_contrast(names, lins, background_name, background_lin, findings,
                   is_ramp=palette_type != "qualitative")
    result["contrast"] = {
        name: round(contrast_ratio(lin, background_lin), 2) for name, lin in zip(names, lins)
    }

    if palette_type == "qualitative":
        result["pairs"] = check_qualitative(names, lins, findings)
    elif palette_type == "sequential":
        result["lightness"] = [round(v, 3) for v in check_sequential(names, lins, findings)]
    else:
        result["lightness"] = [round(v, 3) for v in check_diverging(names, lins, findings)]

    result["findings"] = findings
    if any(f["level"] == "fail" for f in findings):
        result["status"] = "fail"
    elif any(f["level"] == "warn" for f in findings):
        result["status"] = "warn"
    else:
        result["status"] = "pass"
    return result


def print_report(result):
    print("Palette type: %s    Background: %s" % (result["type"], result["background"]))
    print("")
    print("Contrast against background (3:1 or more recommended for lines and points)")
    for name, ratio in result["contrast"].items():
        print("  %s  %5.2f:1" % (name, ratio))
    if "lightness" in result:
        print("")
        print("Perceived lightness along the ramp (0 = black, 1 = white)")
        print("  " + "  ".join("%.2f" % v for v in result["lightness"]))
    if "pairs" in result and result["pairs"]:
        closest = min(result["pairs"], key=lambda row: row["worst_distance"])
        print("")
        print("Closest pair: %s and %s, distance %.3f under %s"
              % (closest["pair"][0], closest["pair"][1], closest["worst_distance"],
                 closest["worst_view"]))
        print("  (below %.2f is hard to tell apart, below %.2f is nearly identical)"
              % (PAIR_WARN, PAIR_FAIL))
    print("")
    for finding in result["findings"]:
        print("%s [%s] %s" % (finding["level"].upper(), finding["check"], finding["message"]))
    if result["findings"]:
        print("")
    print("Result: %s" % result["status"].upper())
    print("")
    print("Thresholds are heuristics. Always check the rendered chart at its final size.")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Check a chart colour palette for contrast, distinctness under "
                    "colour-vision deficiency, and lightness ordering.")
    parser.add_argument("colours", nargs="+", help="hex colours in palette order, e.g. '#0072B2'")
    parser.add_argument("--type", choices=["qualitative", "sequential", "diverging"],
                        default="qualitative", dest="palette_type",
                        help="how the palette will be used (default: qualitative)")
    parser.add_argument("--background", default="#FFFFFF",
                        help="chart background colour (default: #FFFFFF)")
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON")
    args = parser.parse_args(argv)

    try:
        result = run(args.colours, args.palette_type, args.background)
    except ValueError as error:
        print("error: %s" % error, file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_report(result)
    return 1 if result["status"] == "fail" else 0


if __name__ == "__main__":
    sys.exit(main())
