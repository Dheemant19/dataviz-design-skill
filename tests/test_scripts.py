"""Smoke tests for the skill's scripts. Run with: python -m pytest tests, or python tests/test_scripts.py"""

import os
import subprocess
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

SCRIPTS = os.path.join(os.path.dirname(__file__), "..", "skills", "dataviz-design", "scripts")
sys.path.insert(0, os.path.abspath(SCRIPTS))

import chartkit as ck  # noqa: E402
from chartlint import lint_figure  # noqa: E402


def checks(findings, level=None):
    return {f["check"] for f in findings if level is None or f["level"] == level}


def test_linter_flags_common_problems():
    fig, (a, b, c) = plt.subplots(1, 3, figsize=(12, 4))
    years = np.arange(2000, 2021)
    for i in range(8):
        a.plot(years, (40 if i == 0 else 1.5) * np.linspace(1, 2, years.size), label=str(i))
    a.legend()
    b.bar(["x", "y"], [82, 85])
    b.set_ylim(80, 86)
    c.imshow(np.random.default_rng(0).random((4, 4)), cmap="jet")
    found = lint_figure(fig)
    assert "bar-baseline" in checks(found, "FAIL")
    assert "rainbow-colormap" in checks(found, "FAIL")
    assert "squashed-series" in checks(found)
    assert "legend-size" in checks(found)
    plt.close(fig)


def test_clean_chart_passes(tmp_path):
    ck.apply_style("web")
    fig, ax = ck.figure()
    years = np.arange(2010, 2021)
    for name, slope in (("North", 3), ("South", 1), ("East", 1.5)):
        ax.plot(years, 10 + slope * (years - 2010), label=name, **ck.emphasis(name, focus="North"))
    ck.label_lines(ax, focus="North")
    ck.tidy(ax)
    found = ck.finish(fig, str(tmp_path / "chart.png"), title="North grew fastest",
                      subtitle="Sales, thousand units", source="Source: test", alt="Line chart.")
    assert not checks(found, "FAIL")
    assert (tmp_path / "chart.png").exists()
    assert (tmp_path / "chart.alt.txt").exists()
    plt.close(fig)


def test_bar_labels_do_not_collide(tmp_path):
    ck.apply_style("web")
    fig, ax = ck.figure()
    ax.barh(["a", "b", "c"], [42.0, 31.5, 4.1])
    ck.bar_labels(ax, secondary=["$42k", "$31k", "$4k"])
    found = ck.finish(fig, str(tmp_path / "bars.png"), title="t", alt="x")
    assert "text-overlap" not in checks(found)
    plt.close(fig)


def test_fmt():
    assert ck.fmt(12289) == "12,289"
    assert ck.fmt(0.4123, percent=True) == "41%"
    assert ck.fmt(15805, compact=True) == "15.8k"
    assert ck.fmt(-4.2) == "−4.2"
    assert ck.fmt(3.0, sign=True) == "+3.0"


def test_palette_checker_cli():
    script = os.path.join(SCRIPTS, "check_palette.py")
    bad = subprocess.run([sys.executable, script, "#FF0000", "#00A000"], capture_output=True)
    good = subprocess.run([sys.executable, script, "#0072B2", "#D55E00"], capture_output=True)
    assert bad.returncode == 1
    assert good.returncode == 0


if __name__ == "__main__":  # also runs without pytest: python tests/test_scripts.py
    import pathlib
    import tempfile

    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            with tempfile.TemporaryDirectory() as tmp:
                if "tmp_path" in fn.__code__.co_varnames[:fn.__code__.co_argcount]:
                    fn(pathlib.Path(tmp))
                else:
                    fn()
            print("ok", name)
