---
name: dataviz-design
description: "Design rules, chart selection and review checklists for charts, graphs, plots and dashboards. Use this skill whenever you are about to create, choose, critique or fix a data visualisation (visualization) in any tool, including matplotlib, seaborn, plotly, ggplot2, D3, Vega-Lite, Recharts, Excel, Tableau and Power BI. It covers picking a chart type, colours and palettes, axes and baselines, stacked charts, pies, bubbles, heatmaps, histograms, box and violin plots, trend lines and smoothing, titles and annotations, accessibility, and checking whether a chart is misleading. Also use it when a user says a chart looks wrong, confusing, cluttered or ugly, or asks which chart to use, even if they do not ask for design advice."
license: MIT
metadata:
  author: Dheemant Rastogi
  version: "1.0.0"
---

# Data visualisation design

This skill helps you decide what to draw and check that it is honest and readable. It is about design decisions, not about a particular plotting library. Use it with whatever tool the task needs.

The one rule everything else follows from: pick the representation that lets this reader answer this question accurately, with the context they need and the least effort. A chart that looks good but makes the comparison hard, or that leaves a false impression, has failed.

Rules here have different strengths. Some are arithmetic (bubble area must be proportional to the value). Some are strong defaults (bars start at zero). Some are heuristics (keep categorical colours few). When you break a default, have a reason you could say out loud to the reader.

## Workflow

Work through these steps in order. They are quick for a simple chart. Go back a step when something does not fit. A legend that is hard to read often means too many categories. A total that looks impossible often means a bad join.

### 1. Write the brief

Finish this sentence before choosing a chart:

> For [reader], this chart should make it easy to see [comparison or pattern], so that they can [decision or understanding].

"Visualise the dataset" is not a brief. If the user has not said what the chart is for, infer the most likely question from the data and say which question you chose. Also note where the chart will be seen (slide, report, dashboard, phone, print), because that limits label count, detail and interaction.

Decide whether the chart is exploratory (you are looking for what is there, so show distributions and exceptions) or explanatory (the reader should get one supported finding, so edit hard and label directly).

### 2. Check what the data means

A chart cannot fix a wrong number. Before plotting, confirm:

- **Grain.** What does one row represent? What will one mark represent?
- **Scale type of each variable.** Nominal (labels), ordinal (ranked labels), interval (differences meaningful, zero arbitrary) or ratio (true zero). A numeric ID is still a label. This decides which channels, palettes and baselines are valid.
- **Aggregation.** Is each plotted value a count, sum, mean, share or rate? Do not let the library pick the aggregation silently.
- **Denominator.** For every percentage or rate, a share of what?
- **Missing values.** Missing is not zero. Decide how gaps are shown.
- **Order.** Dates sorted as dates. Ordinal levels in their real order, not alphabetical.

Read `references/data-and-preparation.md` when the task involves joins, reshaping, missing data, outliers, percentages, or data with time, map, hierarchy or network structure.

### 3. Choose the form from the task

Identify the main task, then use the chooser table below. Most questions fall into four families:

| Task | The reader asks | Usual starting points |
|---|---|---|
| Comparison | Which is bigger? How did it change? | Bars, dots, lines, small multiples |
| Composition | What is the whole made of? | Stacked bar, 100% bar, pie for a few parts, treemap |
| Relationship | How do two things vary together? | Scatterplot, bubble, heatmap |
| Distribution | What values occur and how often? | Histogram, box plot, violin, ECDF, raw points |

If the reader needs exact values, a table may beat any chart. A single number with context can beat a gauge.

### 4. Encode the key comparison with the strongest channel

People judge some visual properties much more accurately than others. From most to least precise for quantities:

1. Position on a common scale
2. Position on separate but identical scales (small multiples)
3. Length
4. Angle and slope
5. Area
6. Volume, colour lightness and colour saturation

Put the most important quantitative comparison on position or length. Use hue and shape for categories, never for amounts. Use area and colour intensity for patterns where rough reading is enough. Read `references/encoding-and-perception.md` when a mapping is not obvious, when there are more than three variables, or when layout and grouping matter.

### 5. Choose colour by meaning

- Unordered categories: distinct hues (qualitative palette).
- Ordered or numeric low to high: one ramp that gets steadily lighter or darker (sequential palette).
- Two directions around a meaningful midpoint: two ramps meeting at a neutral centre (diverging palette).
- One thing matters: grey for context and one accent colour for the focus.

Keep the same colour for the same category in every chart. Never let colour be the only cue for something essential. Read `references/colour.md` for palette choice, accessibility and legends, and run `scripts/check_palette.py` on any custom palette.

### 6. Explain

- Title: state the finding or the question, not just the variable names.
- Subtitle or note: population, period, unit, and any transformation (log scale, 7-day average, per 100,000).
- Label lines and bars directly when there are about five series or fewer. Use a legend only when direct labels would collide.
- Annotate the one or two things the reader must not miss.
- Match wording to evidence. "Rose after" is not "rose because of".

Read `references/explanation-and-honesty.md` when writing titles and annotations, when emphasising something, or when the chart supports a claim someone will act on.

### 7. Render it, look at it, review it

Always produce the actual image and inspect it at the size it will be used. Code that runs is not proof the chart reads well. Check for overlapping labels, clipped text, invisible pale marks, and a legend order that does not match the chart. Then run the final review in `references/review-checklist.md`.

## Chart chooser

Use this to get candidates, then read the named reference for the pitfalls of the form you pick. The files in the last column are in `references/`. "Few" and "many" are judgments, not thresholds.

| The reader needs to | Start with | Watch for | Reference |
|---|---|---|---|
| Compare one value across categories | Bars or dots, sorted by value | Zero baseline for bars, long labels (go horizontal) | `comparison.md` |
| Compare many categories | Horizontal sorted bars, or small multiples | Do not give every bar its own colour | `comparison.md` |
| Compare several values within each category | Grouped bars, or small multiples | Which grouping is primary changes what is easy to compare | `comparison.md` |
| See change over a few periods | Bars per period, or a slope chart | Keep periods in time order | `comparison.md` |
| See change over many periods | Line | Real time spacing, gaps for missing data, no line across unrelated groups | `comparison.md` |
| Compare many series over time | Lines with one highlighted, or small multiples | A tangle of coloured lines with a long legend | `comparison.md` |
| Compare against a target | Bullet chart, or bar with a target line | Gauges waste space and use angle | `comparison.md` |
| Show shares of one whole | Sorted bar, 100% bar, or a pie with up to about five slices | Parts must be disjoint and sum to the whole | `composition.md` |
| Show shares across groups or periods | 100% stacked bars | Hides group size, so add totals | `composition.md` |
| Show amounts and shares together | Stacked bars or stacked area | Only the bottom segment sits on a common baseline | `composition.md` |
| Show how a total was built up or reduced | Waterfall | Distinguish totals from changes | `composition.md` |
| Show stages of a process | Funnel as plain bars | Stages are nested, not parts of a whole | `composition.md` |
| Show hierarchy with sizes | Treemap | Area is imprecise, tiny cells are unreadable | `composition.md` |
| Relate two numeric variables | Scatterplot | Overplotting, outliers, fitting a line too early | `relationships.md` |
| Add a third numeric variable | Bubble chart | Scale area, not radius | `relationships.md` |
| Show a value for every row and column pair | Heatmap | Palette type, missing cells, row or column normalisation | `relationships.md` |
| Show pairwise links between entities | Matrix, or node-link diagram for small sparse networks | Dense node-link diagrams become unreadable | `relationships.md` |
| Show one distribution | Histogram, or ECDF | Bin width changes the story | `distributions.md` |
| Compare distributions across groups | Box plots, violins, small-multiple histograms, or raw points | Group sizes, shared bins and scales | `distributions.md` |
| Show values across places | Choropleth for rates, proportional symbols for counts | Raw counts on a choropleth mostly show population | `data-and-preparation.md` |

## Defaults that prevent most bad charts

Each of these exists because breaking it changes what the reader believes.

1. **Bars start at zero.** Bar length is the value. Cutting the axis makes small differences look like large ratios. If small differences matter, use dots or a line, which encode position and can use a narrower range.
2. **Bars in one chart have equal width.** Otherwise area becomes a second, unintended encoding.
3. **Size means area.** For circles, radius must scale with the square root of the value. Doubling the radius shows four times the amount.
4. **No decorative 3D.** Perspective and occlusion change apparent sizes and add no data.
5. **Avoid dual y-axes.** The two scales can be tuned to show any relationship you like. Use two aligned panels or index both series to a common base.
6. **Stack only disjoint parts of one whole.** Never stack a total with its own subsets, or metrics with different meanings.
7. **Sort categories by value** unless they have a natural order (time, rank, age bands). Never sort a time axis or a histogram by height.
8. **Connect points with a line only when the order between them is real** and they belong to the same series.
9. **Palette type follows data type.** No rainbow for numeric data. No ramp for unordered categories.
10. **Colour is never the only cue** for anything essential. Add labels, shapes, line styles or position.
11. **Say what was done to the data.** Smoothing, binning, log scales, exclusions, imputation and normalisation all change the reading.
12. **Show estimated values differently from observed ones.** Forecasts, fits and imputed points need their own style and a label.
13. **Plot the raw data before trusting a summary.** Very different datasets can share the same mean, spread and correlation.
14. **Remove what does not help reading**, such as heavy frames, background fills, shadows and redundant legends. Keep axes, units, reference lines and uncertainty when they carry meaning.
15. **Ask two questions before finishing.** Are the numbers right? What will a reasonable reader conclude at a glance? Both answers must be defensible.

## Critiquing or fixing an existing chart

Read the chart as an encoding before judging its style:

1. What question is it trying to answer, and for whom?
2. What does one mark represent?
3. Which variable is on which channel, and does the channel suit the variable's scale type?
4. What was aggregated, filtered, sorted or normalised?
5. Which comparison is easy? Which one needs angle, area, colour or memory?
6. What draws the eye first, and is that the most important thing?
7. What impression does it leave, and does the data support it?

Then name the specific problem and the specific repair. Common symptoms, with the file in `references/` to read:

| Symptom | Likely cause | Read |
|---|---|---|
| Small difference looks huge | Truncated bar axis, or a tall narrow aspect ratio | `comparison.md` |
| Totals look too large after combining tables | Join multiplied rows | `data-and-preparation.md` |
| A gap in the data shows as a dip to zero | Missing values filled with zero | `data-and-preparation.md` |
| Cannot compare the middle segments of a stack | Floating baselines | `composition.md` |
| Two groups with the same share look equally important | Normalisation hid the group sizes | `composition.md` |
| Big bubbles look far too big | Value mapped to radius | `relationships.md` |
| Legend has many colours that are hard to match | Too many categories on hue | `colour.md` |
| Colours change when the data is filtered | Colour mapping not fixed to category | `colour.md` |
| Density curve extends below zero or past a hard limit | Kernel smoothing ignores bounds | `distributions.md` |
| Box plots look the same but the groups differ | Quartiles hide shape | `distributions.md` |
| Smooth curve shows peaks that were never measured | Decorative curve interpolation | `comparison.md` |
| "Growth is slowing" read as "it is falling" | Rate confused with level | `explanation-and-honesty.md` |
| Event marker read as proof of cause | Timing is not causation | `explanation-and-honesty.md` |
| Front slice or front bar looks largest | 3D perspective | `comparison.md` |

`references/worked-redesigns.md` has before and after cases with numbers. Read it when you want a pattern to follow for a redesign.

## Reference files

Read only what the task needs.

| File | Read it when |
|---|---|
| `references/data-and-preparation.md` | Classifying variables, joining or reshaping, handling missing values or outliers, computing shares and rates, or working with time, map, hierarchy or network data |
| `references/encoding-and-perception.md` | Choosing marks and channels, encoding more than three variables, grouping and layout, emphasis, gridlines |
| `references/colour.md` | Choosing or checking any palette, accessibility, legends and colour bars |
| `references/comparison.md` | Bars, grouped bars, lines, time series, axes, baselines, log scales, aspect ratio, smoothing, small multiples, 3D |
| `references/composition.md` | Pies, donuts, stacked bars and areas, 100% stacks, treemaps, waterfalls, funnels |
| `references/relationships.md` | Scatterplots, trend lines, LOWESS, uncertainty bands, bubbles, heatmaps, matrices, correlation and causation |
| `references/distributions.md` | Histograms, bins, density, box plots, violins, ECDFs, comparing groups |
| `references/explanation-and-honesty.md` | Titles, labels, annotation, emphasis, levels versus rates, and the list of misleading patterns with repairs |
| `references/worked-redesigns.md` | You want a concrete before and after example for a common problem |
| `references/review-checklist.md` | Before delivering any chart, and for per-chart recipes |
| `references/library-notes.md` | Writing code in matplotlib, seaborn, pandas, plotly, ggplot2, Vega-Lite or D3, where library defaults affect meaning |
| `references/sources.md` | The user asks where a rule comes from, or you need to cite the research |

## Palette checker

`scripts/check_palette.py` needs only Python 3. It checks contrast against the background, whether colours stay distinct under simulated colour-vision deficiency and in greyscale, and whether a sequential or diverging ramp is properly ordered.

```bash
python scripts/check_palette.py "#0072B2" "#D55E00" "#009E73" --background "#FFFFFF"
python scripts/check_palette.py "#f7fbff" "#6baed6" "#08306b" --type sequential
python scripts/check_palette.py "#b2182b" "#f7f7f7" "#2166ac" --type diverging --json
```

It reports FAIL, WARN or PASS and exits with status 1 on a failure. Notes are information only. Its thresholds are heuristics, so treat a warning as a prompt to look at the rendered chart, not as a verdict.
