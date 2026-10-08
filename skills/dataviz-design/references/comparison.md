# Comparison charts

Bars, dots, lines and time series, plus the axis decisions that apply to every chart.

## Contents

- Bar or line?
- Bar charts
- Grouped bars
- Dot plots, slope charts and bullet charts
- Line charts and time series
- Axes: baseline, range, direction, labels
- Dual axes
- Aspect ratio
- Log scales
- Smoothing and rolling averages
- Small multiples
- 3D
- Special forms: radar, pyramids, variable-width bars

## Bar or line?

- **Bars** make individual amounts easy to compare. Use them for separate categories or for totals per period.
- **Lines** make the shape of change easy to follow. Use them when the x-axis has a real order and the trend is the point.

"Discrete data gets bars, continuous data gets lines" is too simple. What matters is the x variable. Daily counts are discrete and still make a valid line. Average salary by department is continuous and must not be joined by a line, because there is no path from one department to the next.

If readers need many exact values, add a table or labels to the trend chart instead of forcing the chart to do lookup.

## Bar charts

- **Start at zero.** The bar's length is the value. If the axis starts at 80, a bar for 85 is 2.5 times as tall as a bar for 82, when the real difference is under 4%.
- **Equal widths.** A wider bar has more area and looks more important.
- **Horizontal when labels are long** or when showing a ranking. Do not rotate labels to vertical if turning the chart solves it.
- **Sort by value** for nominal categories. Keep natural order for time and ordinal categories.
- **One colour** for all bars of one series. Use a second colour only to highlight.
- **Plain ends.** No pictures, rounded caps, shadows or perspective on the bar ends, since the end is where the value is read.
- A bar that stands for an average says nothing about the values behind it. Add an interval, or show the distribution, when the spread matters.
- If a few values dwarf the rest, do not break the axis or clip the bars. Use a second panel for the small values, a log-scaled dot plot, or direct labels.

## Grouped bars

Grouped bars compare subcategories inside each main category. The inner grouping is what is easy to compare, so choose it by the question:

- regions within each year: "which region led in each year?"
- years within each region: "how did each region change?"

Keep gaps inside a group smaller than gaps between groups. Use a small, fixed set of colours for the inner categories, in the same order every time.

With more than three or four inner categories, the bars get thin and the legend gets heavy. Switch to small multiples, a line chart if the inner variable is time, or a heatmap.

Grouped bars beat stacked bars when individual components must be compared precisely, because every bar sits on the same baseline.

## Dot plots, slope charts and bullet charts

- **Dot plot.** A dot at the value instead of a bar. It encodes position, not length, so it does not need a zero baseline. Use it for small differences around a large value, for interval data, and for log scales.
- **Paired dots (dumbbell).** Two dots per category joined by a line, for before and after or two groups. The connector must join the same entity.
- **Slope chart.** Two time points on x, one line per entity. Good for showing which entities rose or fell and which one moved against the rest.
- **Bullet chart.** A bar for the measure, a tick for the target, and shaded bands for qualitative ranges (Few, 2006). It replaces dial gauges, which use angle and a lot of space for one number. Label what the bands mean. A performance band is not a statistical interval.
- **Single number.** If the task is "what is the current value", a large number with a comparison (versus last period, versus target) is often the best display.

## Line charts and time series

- Use a real time axis so that uneven gaps between observations look uneven.
- Sort by time within each series before drawing. A line must never jump from where one series ends to where the next begins.
- Show markers when observations are sparse or irregular. A line between two yearly values is a connector, not a record of what happened in between.
- Break the line where data is missing. Do not bridge long gaps.
- Limit the number of lines. With more than about five, highlight one or two and grey the rest, or use small multiples.
- When one series is ten or more times larger than the rest, the small ones collapse into a band at the bottom. Index them to a common start, use a log scale, use small multiples, or add a second panel. Choose by the question, as set out in `claims-and-evidence.md`.
- Label lines at their right-hand end instead of using a legend.
- Draw forecasts and estimates in a different style (dashed, lighter) and say so.
- Filling the area under a line adds emphasis on magnitude and makes the baseline matter. If the chart is about variation in a narrow range, leave the area unfilled.
- Use straight segments between points. Curved "smooth line" options draw peaks and dips between observations that nobody measured.

## Axes: baseline, range, direction, labels

- **Bars and filled areas:** zero baseline. For values on both sides of zero, a clearly marked zero line with bars going both ways.
- **Lines and dots:** the range can be narrower than zero-to-max when the variation is the story. State the range clearly, and do not describe a small wiggle on a zoomed axis as a dramatic change.
- **Direction:** up means more and time runs left to right. Reverse an axis only for a strong reason (rank 1 at the top) and make it obvious. An inverted axis under a filled area can make a rise look like a fall.
- **Labels:** every axis needs the unit and any transformation. A tick that says "10" could be dollars, thousands, people or percent.
- **Ticks:** use round values at a sensible spacing. Avoid more precision than the data has.
- **Panels:** shared scales for comparing size across panels. Independent scales only for comparing shape, and then say so on the chart.

## Dual axes

Two different y-scales on one chart can be stretched so that the lines cross, overlap or diverge wherever the designer likes. The crossing point means nothing. Avoid them by default.

Alternatives:

- two panels stacked vertically with a shared x-axis,
- both series indexed to 100 at a common start date,
- a scatterplot of one variable against the other if the relationship is the point.

If a dual axis is unavoidable (the user insists, or it is a domain convention), colour each axis to match its series, label both clearly, and do not draw conclusions from where the lines meet.

## Aspect ratio

The steepness the reader sees depends on the chart's shape as well as the data. The same series looks dramatic in a tall narrow chart and flat in a wide short one.

- Choose a shape where the typical slope of the line is moderate, somewhere near 45 degrees, so that changes in slope are easy to see (Cleveland, McGill and McGill, 1988). This is a guideline, not a rule.
- Keep the same shape and scales for panels that will be compared.
- After resizing for a slide or a phone, look again. The impression may have changed.

## Log scales

A linear axis gives equal space to equal differences. A log axis gives equal space to equal ratios, so 1 to 10 takes the same space as 10 to 100.

Use a log scale when:

- values span several orders of magnitude,
- the question is about growth rates or relative change,
- the relationship is multiplicative.

Do not use one when the reader cares about absolute differences (budget gaps, profit shortfalls), because it compresses them.

Rules:

- Label the axis as logarithmic and use readable ticks (1, 10, 100, or 1, 2, 5, 10).
- Zero and negative values cannot be shown. Dropping them or adding a constant changes the data and must be stated.
- Use points or lines, not bars. A bar on a log axis has no meaningful zero to start from.

## Smoothing and rolling averages

Smoothing removes short-term noise to show the broader trend. It is a transformation of the data, not a styling choice, and the amount of smoothing changes what the reader sees.

Three different things get called "smoothing":

| Operation | What it does | Caution |
|---|---|---|
| Rolling average | Replaces each value with the average of nearby values | Window size and alignment move and flatten peaks |
| Statistical smoother (LOWESS, spline fit) | Estimates a local trend | The span setting changes the shape. See `relationships.md` |
| Curved connector | Draws a curve through the same points | Purely cosmetic and can invent overshoots. Avoid |

For a rolling average, decide and state:

- **Window.** For example 7 days to cancel a weekly cycle. A longer window gives a calmer line that hides short peaks and reacts late to turning points.
- **Alignment.** A trailing window uses only past values and lags behind. A centred window lines up with the data but uses future values, so it cannot describe "the latest" point.
- **Edges.** A full window leaves blanks at the start (and at the end if centred). Partial windows fill them with less reliable values.
- **Missing values.** How many real observations a window needs before it reports a value.
- **Points versus time.** Seven rows are seven days only if there is one row per day.

Show the raw series faintly behind the smoothed line when short-term variation matters. Say "7-day average" in the title or legend. Do not compare the volatility of a smoothed series with an unsmoothed one.

## Small multiples

The same chart repeated for each group, in a grid, with the same axes. They replace a tangle of lines or a long colour legend with position.

- Share the y-scale when sizes should be compared across panels. Use free scales only to compare shapes, and label that clearly.
- Order panels meaningfully: by time, by size, or by a known sequence.
- Keep units, colours and category order identical across panels.
- Put each panel's title close to it. Repeat axis labels only on the outer edges.
- Too many tiny panels are unreadable. Check at final size.
- A faint copy of all series in grey behind each panel's highlighted series helps comparison.

A dashboard is a set of coordinated views. Give it a reading order, with the most important view largest and first. Make it clear which filters apply to which views.

## 3D

Decorative 3D (bars with depth, tilted pies) adds perspective, hidden surfaces and foreshortening, and no data. Things at the front look bigger, things at the back are hard to read. Draw it flat.

A 3D surface can be justified when the data really is a value over two coordinates. Even then a heatmap or contour plot usually shows the same structure without hiding anything.

## Special forms: radar, pyramids, variable-width bars

- **Radar or spider charts.** The shape and area of the polygon depend on the order of the axes, which is usually arbitrary. Different axes often have different units. Prefer small-multiple bars or a dot plot per measure. Radial layouts are defensible for truly cyclic data (hour of day, month of year), with the caveat that radial distance is harder to compare than height.
- **Polar area charts.** If sector area carries the value, the radius must follow the square root of the value, as with bubbles.
- **Population pyramids.** Two groups on opposite sides of a shared age axis. State whether bars are counts or shares, use the same scale on both sides, and label the axis with positive numbers on both sides.
- **Variable-width bars (Marimekko, mosaic).** Width and height both carry data, so area is their product. Only use them when both variables are defined and explained. Never vary bar width in an ordinary bar chart.
- **Candlesticks and other domain forms.** Fine for audiences who use them daily. Explain the parts or choose a simpler form for general readers.
