# Relationship charts

Scatterplots, fitted lines, uncertainty, bubbles, heatmaps and matrices, and what a visible relationship does and does not show.

## Contents

- Plot before you summarise
- Scatterplots
- Reading a scatterplot
- Trend lines
- LOWESS and other smoothers
- Uncertainty bands
- Bubble charts
- Bubble area arithmetic
- Heatmaps
- Matrices and networks
- Association is not causation

## Plot before you summarise

A correlation coefficient or a fitted line compresses the data to one or two numbers. Very different data can produce the same numbers.

- Anscombe's quartet (1973) is four small datasets with nearly identical means, variances, correlation (about 0.82) and regression line. Plotted, one is a linear cloud, one is a clean curve, one is a perfect line with a single outlier, and one is a vertical stack of points plus one far-off point that creates the whole correlation.
- The "Datasaurus" collection (Matejka and Fitzmaurice, 2017) makes the same point with a dozen wildly different shapes that share summary statistics.

So always draw the points first. And the reverse also holds: a pattern you can see is not proof either. A visible cluster can come from rounding, sampling, filtering or overplotting. Let the plot and the numbers check each other.

## Scatterplots

Each point is one observation with two numeric values. State what a point is (a person, a store, a country in a year).

- By convention the suspected driver goes on x and the result on y. Placement on the x-axis does not make a variable the cause.
- Label both axes with units.
- Show the full range of the data. Cropping to a region where the trend looks strong is cherry-picking.
- **Overplotting.** When points pile up, density is hidden. Options: smaller points, transparency, hollow markers, a random sample, small multiples by group, or binning into a 2D heatmap or hexbin. Binning changes marks from observations to counts, so say so.
- **Discrete values.** Rounded or integer data forms stripes with many points on top of each other. A little jitter separates them, at the cost of moving points off their true positions. Keep jitter small and mention it.
- Colour by a category to reveal subgroups, with few categories. A pattern in the whole cloud can reverse inside each subgroup.

## Reading a scatterplot

| You see | It may mean | Check |
|---|---|---|
| Cloud rising to the right | Positive association | Is it linear? Is it driven by a few points? Are there subgroups? |
| Cloud falling to the right | Negative association | Same, plus whether the range is restricted |
| Round blob | No linear relationship | A curved relationship can still exist |
| Curve | Nonlinear relationship | A straight-line summary will mislead |
| Separate clusters | Different populations | What distinguishes them? Colour by candidate variables |
| Empty stretch of x | No data there | Do not trust a fit through the gap |
| One far-off point | Error, rare case, or influential point | The raw record. Refit without it and compare |
| Stripes | Rounding or integer values | Hidden overlap. Consider jitter or counts |

A strong correlation does not mean a strong causal effect. A weak linear correlation does not mean no relationship.

## Trend lines

A fitted line is a model laid over the data. It does not replace the points.

- Keep the points visible, in a quieter style than the line if the trend is the message.
- Look at whether the points scatter evenly around the line. If they sit above it at both ends and below in the middle, the relationship is curved.
- State the type of fit in the legend or caption (linear, quadratic, LOWESS).
- Higher-order polynomials bend to fit noise and swing wildly at the edges. Flexibility is not accuracy.
- Do not extend the line beyond the data unless forecasting is the purpose, and then mark the extension as a projection.
- A straight line with a nonzero intercept does not describe a constant proportion. If fee = 2 + 0.1 × order, the fee is 30% of a 10 order and 12% of a 100 order. Be careful turning a slope into "x% of".

## LOWESS and other smoothers

LOWESS (Cleveland, 1979) draws a smooth curve by fitting a small weighted regression around each x position, using only nearby points, with closer points counting more. It follows the data's shape without assuming one global formula.

The key setting is the span (often called `frac`): the share of points used in each local fit.

- A small span (for example 0.2) follows local wiggles and can chase noise.
- A large span (for example 0.6) gives a calmer curve and can flatten real features.
- There is no single correct value. Try two or three and see whether the story changes. If it does, the data does not settle the shape.

Cautions:

- The curve is least reliable at the ends and where points are sparse, because few neighbours are available.
- The curve alone carries no uncertainty. A band needs a separate calculation.
- "Nonparametric" means no global formula. It does not mean no assumptions. Span, weighting and robustness settings are all choices to report.

When a straight line, a polynomial and a smoother tell different stories on the same data, show that, or at least say which one you chose and why.

## Uncertainty bands

A shaded band or error bar must say what it is. These are different things:

| Display | Means | Does not mean |
|---|---|---|
| Standard deviation | How spread out the observations are | How precisely the mean is known |
| Standard error or confidence interval | How precisely an estimate (mean, fitted line) is known | Where individual observations fall |
| Prediction interval | Where a new observation is likely to fall | A guarantee |
| Box and whiskers | Quartiles and a whisker rule | A confidence interval |
| Hand-drawn shaded region | A visual grouping | Anything statistical |

- The confidence band around a regression line can be narrow while the points are widely scattered. Readers often take it for the range of the data, so label it ("95% confidence interval for the fitted line").
- Always state the level (95%, 80%) and the kind of interval in the caption.
- More data narrows a confidence interval. It does not remove bias from how the data was collected.
- Do not add a shaded band for style. If nothing was computed, draw nothing.

## Bubble charts

A scatterplot where point size carries a third numeric variable.

- Use it when the third variable adds context (population, revenue) and rough reading is enough. If the third variable is the main comparison, give it its own bar chart.
- Add a size legend with two or three reference circles and their values.
- Use transparency or thin outlines so overlapping bubbles stay visible. Draw large bubbles first so that small ones sit on top.
- Label only the important bubbles.
- Every additional channel (colour for group, shape for type) adds reading effort. Stop at four variables in total.

## Bubble area arithmetic

Readers see the area of a circle, so area must be proportional to the value.

- Area = k × value, and area = π × r², so **radius = sqrt(k × value / π)**. In short, radius scales with the square root of the value.
- Values of 10 and 40 should have areas in the ratio 1 to 4, which means radii in the ratio 1 to 2. Mapping the value straight to radius would give areas of 1 to 16 and make the larger look four times too big.
- Check what the library's size argument means. Some take area, some take radius or diameter. See `library-notes.md`.
- Many libraries rescale sizes to run from a minimum to a maximum marker size. That keeps small points visible and breaks proportionality, since the smallest value no longer maps toward zero area. If ratios matter, set the scale so that zero maps to zero area.
- A value of zero has no area and disappears. Negative values cannot be shown as area. Use filled and hollow circles for sign, or put that variable on an axis.

Area has one real advantage: range. Values from 1 to 1,000 need bar lengths from 1 to 1,000, so the small bars vanish. As circles the radii run from 1 to about 32, so everything stays visible. The price is precision.

## Heatmaps

A grid of cells, with rows and columns for two variables and colour for a value. Good for dense patterns across many combinations (hour by weekday, product by region, month by year). Poor for reading exact values.

- Say what each cell is: a count, a mean, a share, a correlation.
- Choose the palette from the cell value. Sequential for low to high. Diverging for values around a stated centre such as zero or the average. Distinct hues only for categories. See `colour.md`.
- Add a colour bar with units.
- Order rows and columns meaningfully. Time in time order. Categories by a total, or by clustering similar rows together. Alphabetical order usually hides the pattern.
- State any normalisation. Row percentages show the mix inside each row and hide which rows are big.
- Draw missing cells differently from low values and from the neutral centre (grey or hatched).
- Print values in the cells only when there are few cells and the text is readable. Choose text colour for contrast with the cell.
- A correlation heatmap shows only linear, pairwise relationships. Look at scatterplots for the pairs that matter.

A density heatmap on a map is a different thing. It is a smoothed estimate of intensity, and the smoothing radius shapes what it shows.

## Matrices and networks

For relationships between pairs of entities:

- **Node-link diagram.** Good for small, sparse networks and for following paths. Becomes a hairball when dense.
- **Matrix.** The same entities on rows and columns, with a cell for each pair. Scales to dense networks and makes any pair easy to look up.

For a matrix:

- Use the same order on rows and columns. Group related entities so that blocks appear.
- If the relationship is a category (ally, rival, neutral), use distinct colours with a categorical key, and consider a symbol in each cell as a second cue. A gradient colour bar is wrong for categories.
- State whether direction matters. If A to B can differ from B to A, the matrix need not be symmetric.
- Style the diagonal (an entity with itself) so it does not read as data or as missing.

## Association is not causation

Keep three kinds of statement apart:

1. **Description.** "Orders rose in the second quarter."
2. **Association.** "Orders rose after the redesign went live."
3. **Causal claim.** "The redesign increased orders."

A chart can support the first two by itself. The third needs evidence the chart does not contain: a comparison group, a controlled experiment, or at least alternative explanations ruled out (seasonality, a price change, a campaign that ran at the same time).

- A vertical line marking an event shows when it happened. It does not attribute what follows to it.
- Differences between age groups in one snapshot do not show what happens to people as they age. That needs the same people followed over time.
- A difference between group averages says nothing certain about any individual.
- Write titles and annotations at the level the evidence supports. "Orders rose 18% in the quarter after the redesign" is honest. "Redesign lifts orders 18%" is a causal claim.
