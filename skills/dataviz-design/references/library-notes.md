# Library notes

Places where a plotting library's defaults or parameter meanings affect what the chart says. Read the section for the library you are using.

Defaults change between versions. The matplotlib, seaborn and pandas notes were checked against matplotlib 3.11, seaborn 0.13 and pandas 3.0. For the other libraries, confirm against the installed version before relying on a default. Whatever the library, look at the rendered output: a default you did not choose is still a design decision you are responsible for.

## Contents

- Patterns that apply everywhere
- pandas
- matplotlib
- seaborn
- statsmodels
- plotly
- ggplot2
- Vega-Lite and Altair
- D3
- Spreadsheets and BI tools

## Patterns that apply everywhere

- **Fix category colours in a mapping** (a dict or a named scale) so that filtering or reordering never reassigns them.
- **Set category order explicitly.** Defaults are alphabetical or order of appearance, and neither is usually right for ordinal data.
- **Check what the size argument means** (area, radius or diameter) and whether sizes are rescaled between a minimum and maximum.
- **Find out what a library aggregates silently.** Several draw the mean of repeated x values, with an interval, without being asked.
- **Find out how missing values are drawn.** Dropped, bridged, or shown as a gap.
- **Use straight line segments.** Turn off curve or spline interpolation.
- **Export at the final size and look at the file,** not the notebook preview.

## pandas

- `merge` defaults to an inner join, which silently drops unmatched rows. Pass `how=` deliberately. Use `validate="one_to_one"` or `"many_to_one"` to fail fast on unexpected duplicates, and `indicator=True` to count unmatched rows.
- `sum()` skips missing values, and the sum of an all-missing group is 0. Use `min_count=1` to keep it missing.
- `groupby` sorts keys alphabetically by default and drops rows whose key is missing (`dropna=True`).
- `pivot_table` aggregates duplicates with the mean by default. Pass `aggfunc` explicitly. `pivot` raises an error on duplicates, which is the safer check.
- `concat(axis=1)` aligns on the index, not on row position. Make sure the index is the real key.
- `rolling(7)` counts rows, and `rolling("7D")` counts time. They differ when dates are missing. With an integer window, `min_periods` defaults to the window size, so the first values are blank. With a time window it defaults to 1, so early values are averages of very few points. `center=False` is a trailing window.
- `interpolate()` is linear by row position. Use `method="time"` with a datetime index for uneven spacing, and interpolate within each group, not across groups.
- Dates stored as text sort as text. Convert with `pd.to_datetime` first.
- For ordered categories use `pd.Categorical(values, categories=[...], ordered=True)` so that every later step keeps the order.
- A line chart only shows a gap if the missing period exists as a row with a missing value. Reindex to the full date range first.

## matplotlib

The skill ships two helpers for matplotlib. Prefer them to hand-rolled layout code:

- `scripts/chartkit.py` sets the type scale and size for the destination, adds a left-aligned title block and footer, places direct labels without collisions, adds evenly spaced bar labels, and saves at the right size with alt text.
- `scripts/chartlint.py` checks a drawn figure for overlapping or clipped text, small fonts, bars not starting at zero, unequal bar widths, squashed series, too many colours, big legends, pies with many slices, dual axes, rainbow and off-centre colour maps, and colour pairs that fail colour-vision checks. Run any plotting script through it with `python scripts/chartlint.py make_chart.py`.

Notes for plain matplotlib:

- `scatter(s=...)` takes marker **area** in points squared. For proportional bubbles pass something proportional to the value:

```python
max_area = 900  # points^2 for the largest value
ax.scatter(x, y, s=values / values.max() * max_area, alpha=0.6, edgecolor="white")
```

- `plot` breaks the line at `NaN`, which is the behaviour you want for gaps.
- `boxplot` uses whiskers at 1.5 × IQR, ending at the last data point inside that limit. `whis=(5, 95)` switches to percentiles, and then the caption must say so.
- `bar` does not force a zero baseline once you call `set_ylim`. If you set limits on a bar chart, keep 0 in them.
- The default colormap is viridis, which is a sound sequential choice. Avoid `jet`, `rainbow` and `hsv` for ordered data. Use `RdBu`, `PuOr` or `BrBG` with `TwoSlopeNorm(vcenter=0)` or symmetric `vmin` and `vmax` for diverging data.
- Twin axes (`twinx`) create a dual-axis chart. See the alternatives in `comparison.md`.
- Direct labels at line ends:

```python
for name, s in series.items():
    ax.plot(s.index, s.values, color=colours[name])
    ax.annotate(name, (s.index[-1], s.values[-1]), xytext=(6, 0),
                textcoords="offset points", va="center", color=colours[name])
```

- Grey context with one accent:

```python
for name, s in series.items():
    focus = name == "North"
    ax.plot(s.index, s.values, color="#D55E00" if focus else "#BBBBBB",
            linewidth=2.5 if focus else 1, zorder=3 if focus else 2)
```

- Clean-up that is usually right: `ax.spines[["top", "right"]].set_visible(False)`, `ax.grid(axis="y", alpha=0.2)`, `ax.set_axisbelow(True)`.
- Save with `fig.savefig(path, dpi=200, bbox_inches="tight")` and open the file to check for clipped labels.

## seaborn

- `barplot`, `pointplot` and `lineplot` **aggregate**. With several rows per x value they draw the mean and a bootstrapped 95% confidence interval (`estimator="mean"`, `errorbar=("ci", 95)`). Decide whether that is what you want. Use `errorbar=None`, `errorbar="sd"`, or pre-aggregate yourself, and say in the caption what the bars and intervals are.
- `hue` with a numeric column produces a sequential ramp, not distinct hues. With a categorical column it produces a qualitative palette. Pass `palette={category: colour}` to fix the mapping, and `hue_order` and `order` to fix order.
- `scatterplot(size=...)` rescales values linearly between a smallest and largest marker area. Values 1, 2 and 10 come out with areas in the ratio 3 : 4 : 12, not 1 : 2 : 10. For true proportional area use `sizes=(0, max_area), size_norm=(0, values.max())`.
- `histplot`: `stat` defaults to `"count"`. With `hue` and a normalised `stat`, `common_norm=True` normalises across all groups together, so a smaller group looks smaller. Set `common_norm=False` to compare shapes. `common_bins=True` keeps bin edges shared, which you want. Use `discrete=True` for whole-number data.
- `kdeplot`: the curve extends 3 bandwidths past the data (`cut=3`). Use `cut=0` to stop at the data, or `clip=(low, high)` for hard limits, and remember this hides the spill without fixing the estimate near the edge. `bw_adjust` scales the bandwidth. Try 0.5 and 2 to test whether a peak is real. `common_norm=True` scales each group's curve by its size.
- `violinplot`: `density_norm="area"` by default, so every violin has the same area whatever its sample size. Options are `"count"` and `"width"`. `cut=2` extends past the data, so use `cut=0` to trim. `inner="box"` draws a small box plot inside. Older versions call the scaling parameter `scale`.
- `regplot` and `lmplot`: the shaded band is a bootstrapped 95% confidence interval for the fitted line (`ci=95`), not a range for the points. `order=2` fits a polynomial. `lowess=True` draws a LOWESS curve with no band and needs statsmodels.
- `heatmap`: missing cells are left blank automatically. Set `center=0` (or another reference) with a diverging `cmap` for signed data. `robust=True` sets colour limits from percentiles, which changes what the extremes mean, so mention it. Use `annot=True` only for small grids.
- Small multiples: `relplot`, `catplot` and `displot` with `col=` share axes by default. If you set `facet_kws={"sharey": False}`, say so on the chart.

## statsmodels

- `lowess(endog, exog, frac=...)` takes **y first, then x**. Swapping them runs without error and gives a wrong curve.
- `frac` is the share of points used in each local fit (default about two thirds), not a distance on the x-axis.
- `it` sets the number of robustness passes that down-weight outliers. It is separate from `frac`.
- The result is sorted by x by default, as two columns (x, fitted y). Rows with missing values are dropped by default, so the output can be shorter than the input.
- No confidence band is returned.

## plotly

- In `plotly.graph_objects`, `marker.size` is a **diameter** by default. Set `marker.sizemode="area"` and a `sizeref` for proportional bubbles. `plotly.express` with `size=` already uses area mode and maps zero to zero area.
- `line_shape="spline"` draws curves between points. Keep the default `"linear"`.
- `connectgaps` is off by default for line traces, so `None` or `NaN` leaves a gap. Leave it off.
- `px.bar` does not aggregate. Several rows with the same x are drawn as stacked segments, which often looks like a single bar with odd internal lines. Aggregate first.
- 3D chart types and the pie `pull` option (exploded slices) exist. Avoid them for the reasons in `comparison.md` and `composition.md`.
- Hover text does not survive a static export. Anything essential must be visible without hovering.
- Pass `color_discrete_map={category: colour}` to fix category colours and `category_orders={column: [...]}` to fix order.

## ggplot2

- `geom_bar()` counts rows. `geom_col()` plots the values you give it. Using the wrong one produces bars of height 1 or a count nobody asked for.
- `ylim()` and `scale_y_continuous(limits = ...)` **remove** data outside the limits before statistics are computed, which changes box plots, smooths and stacked bars. To zoom without dropping data use `coord_cartesian(ylim = ...)`.
- `scale_size()` maps values to area, with a nonzero minimum size. `scale_size_area()` maps zero to zero area, which is what proportional bubbles need. `scale_radius()` maps to radius and should be avoided for amounts.
- `geom_smooth()` picks a method by sample size (loess for smaller data) and draws a 95% confidence band for the fit by default. State the method in the caption, or set `method = "lm"` or `se = FALSE` deliberately.
- Character columns are ordered alphabetically. Use factors with explicit levels, or `reorder()` and `forcats::fct_reorder()` to sort by value.
- `geom_line()` connects points in x order within each group. Without the right `group` aesthetic it will join different entities into one zigzag line. `geom_path()` connects in data order.
- `geom_histogram()` defaults to 30 bins and tells you so. Set `binwidth` or `breaks` deliberately.
- `geom_violin()` uses equal areas by default (`scale = "area"`) and trims to the data range. `scale = "count"` ties width to sample size.
- `facet_wrap()` shares scales by default. If you set `scales = "free"`, label it.
- Use `scale_colour_manual(values = c(name = "#hex"))` to fix category colours. Viridis scales and ColorBrewer scales are built in (`scale_fill_viridis_c`, `scale_fill_distiller`, `scale_fill_brewer`).

## Vega-Lite and Altair

- The `size` channel of point marks is **area** in square pixels, so a linear scale with `zero: true` gives proportional bubbles.
- Bar charts include zero on the quantitative axis by default. If you set a custom `domain` or `zero: false` on a bar, you have cut the axis.
- Always give the type (`:Q`, `:O`, `:N`, `:T`). It decides the palette and axis: nominal gets distinct hues, ordinal and quantitative get a ramp. A year stored as a number and typed `:Q` gets a continuous axis with tick labels like "2,020".
- Sort explicitly: `sort="-x"` to sort bars by value, or `sort=[...]` for an ordinal order.
- State aggregation in the encoding (`mean(price)`, `count()`), so the chart documents itself.
- Fix category colours with `scale=alt.Scale(domain=[...], range=[...])`.

## D3

- Use `d3.scaleSqrt()` for circle radius, so area is proportional to the value. `d3.scaleLinear()` on radius is the classic bubble error.
- Bar scales need 0 in the domain: `d3.scaleLinear().domain([0, d3.max(data, d => d.value)])`.
- Curves: `d3.curveLinear` is the honest default. `curveBasis`, `curveCardinal` and `curveNatural` overshoot or miss the data points. If a smooth look is required, `curveMonotoneX` passes through the points without overshooting.
- Use `line.defined(d => d.value != null)` so that missing values break the line.
- `d3.scaleOrdinal(d3.schemeTableau10)` assigns colours in order of first appearance, so the mapping changes with the data order. Set `.domain([...])` explicitly.
- For ordered data use `d3.interpolateViridis`, `interpolateBlues` and similar. For diverging data use `interpolateRdBu` or `interpolatePuOr` with `d3.scaleDiverging` and an explicit centre. Avoid `interpolateRainbow` and `interpolateSinebow` for magnitudes.
- An SVG chart needs text alternatives: a `<title>`, labelled axes, and visible values for anything essential.

## Spreadsheets and BI tools

- Check the value axis minimum. Automatic axis ranges sometimes start above zero for bar charts.
- "Smoothed line" options draw curves between points. Turn them off.
- 3D column, 3D pie and exploded pie types are offered prominently. Use the flat versions.
- Look for the setting that controls empty cells in line charts (gap, zero, or connect). Choose gap.
- Bubble charts usually have a setting for whether size means area or width. Choose area.
- Default palettes assign a new colour per series and may reassign when a filter changes the series list. Pin colours to categories where the tool allows it.
- Dual-axis and "combo" charts are one click away. See the alternatives in `comparison.md`.
- Dashboards: state which filters apply to which charts, keep one colour meaning across all tiles, and make sure the default view shows the main point without interaction.
