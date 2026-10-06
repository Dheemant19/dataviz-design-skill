# Distribution charts

Histograms, density curves, box plots, violins and cumulative plots, and how to compare groups without hiding what matters.

## Contents

- What to look for
- Choosing a form
- Histograms
- Bins
- Counts, shares and density
- Box plots
- Density curves (KDE)
- Violin plots
- ECDF
- Small samples: show the points
- Comparing groups

## What to look for

An average is one fact about a distribution. Also look at:

- **Spread.** How wide is the range and the middle half?
- **Skew.** Is there a long tail to one side? (Incomes, waiting times and sizes usually have a long right tail.)
- **Peaks.** One, or several? Two peaks often mean two different populations mixed together.
- **Gaps and spikes.** Empty ranges, or pile-ups at round numbers or limits.
- **Unusual values.** See outliers in `data-and-preparation.md`.

Two groups with the same mean or median can differ in all of these. Peaks and skew can also appear or vanish with bin width or smoothing, so check them under more than one setting.

## Choosing a form

| Form | Shows well | Hides | Use when |
|---|---|---|---|
| Histogram | Shape, peaks, gaps, skew | Exact values. Depends on bins | One or a few groups, medium to large samples |
| Density curve (KDE) | Smooth shape, easy to overlay | Sample size. Can invent smoothness | Comparing shapes of a few groups |
| Box plot | Median, quartiles, extremes, compactly | Peaks, gaps, sample size | Many groups side by side |
| Violin | Shape plus summary | Sample size. Depends on smoothing | Several groups where shape differs |
| ECDF | Every value, no settings. Percentiles | Peaks are less obvious | Threshold questions, precise comparison |
| Strip or swarm plot | Each observation | Becomes a blob with large samples | Small samples |

There is no rule that large samples need one form and small samples another. Pick the form that exposes the feature the question is about, and combine two when one hides something important (a box plot over a strip plot, a histogram with a marked median).

## Histograms

A histogram cuts a numeric axis into intervals (bins) and draws a bar for how many values fall in each.

- The x-axis is a number line. Bars touch, and their order is fixed by the values. Never sort a histogram by bar height.
- It is not a bar chart of categories, where order and gaps carry no numeric meaning.
- Overlapping filled histograms hide each other. For two or three groups use outlines (step style) or transparency. For more, use small multiples with shared bins and a shared x-axis.

## Bins

Bin width changes the story.

- Too few bins merge separate peaks and hide gaps.
- Too many bins turn random noise into apparent structure.
- Moving the bin edges, at the same width, can also change the shape.

Practical rules:

- Start with a default rule (Freedman and Diaconis, 1981, is a robust one), then try a wider and a narrower setting. Report the shape only if it survives.
- Use round, meaningful edges (0, 5, 10) so the axis is readable.
- **Whole-number data** (counts, ages, ratings) needs bins that each cover the same number of whole values. Use an integer width, with edges at the half values (−0.5, 0.5, 1.5) so each value sits in the middle of its bin. A width of 1.5 puts two possible values in one bin and one in the next, which creates a false zigzag.
- Decide and state whether a value exactly on an edge goes left or right.
- Use the same bin edges for every group being compared.
- Do not tune bins to produce the peak you hoped for.

## Counts, shares and density

The y-axis of a histogram can mean three things. Label which.

- **Count.** Number of values in the bin. Shows sample size. Only comparable between groups of similar size.
- **Share (percent).** Count divided by the total. Comparable across group sizes. Hides the size.
- **Density.** Count divided by (total × bin width). The area of each bar is then the share in that bin, and all the areas sum to 1. Needed when bins have unequal widths, and when overlaying a density curve. A density value is not a percentage. With 200 values, a bin of width 5 holding 30 of them has density 30 / (200 × 5) = 0.03, and its area, 0.15, is the 15% share.

When groups differ in size, counts mainly show the size difference and normalised versions show shape. If both matter, normalise and print n for each group.

## Box plots

A box plot (Tukey, 1977) summarises a distribution with five numbers and flags extreme points.

| Part | Meaning |
|---|---|
| Line in the box | Median |
| Box | First to third quartile, the middle 50% of values. Its length is the interquartile range (IQR) |
| Whiskers | Reach to the most extreme data points still within 1.5 × IQR of the box |
| Separate points | Values beyond the whiskers |

Things that are often misread:

- **Whiskers end at real data points,** not at the 1.5 × IQR limit itself. With quartiles at 40 and 60, the IQR is 20 and the limits are 10 and 90. If the furthest values inside those limits are 14 and 87, the whiskers stop at 14 and 87. A value of 96 is drawn as a separate point.
- **Points beyond the whiskers are not errors.** The 1.5 rule is a convention for flagging values worth a look. Skewed data will always produce some.
- **Other whisker rules exist** (minimum to maximum, 5th to 95th percentile). State the rule in the caption if it is not the 1.5 convention.
- **The median is not the mean.** Add a separate marker if the mean matters.
- **The box says nothing about peaks, gaps or sample size.** A group with two peaks and a group with one can produce the same box. A box from 8 values looks as solid as one from 8,000.

To cover the gaps: overlay the raw points when the sample is small, print n under each box, or use a violin or histogram when shape matters. Use box plots when the audience knows how to read them, and explain the parts when they may not.

## Density curves (KDE)

A kernel density estimate draws a smooth curve by placing a small bump on every observation and adding the bumps up. The bandwidth sets how wide the bumps are.

- A small bandwidth gives a bumpy curve with peaks that may be noise.
- A large bandwidth gives a smooth curve that can merge real peaks.
- The area under the curve is 1. The height is density, not a count or a percentage.
- **Boundaries.** The curve spills past the data. It can show density for negative waiting times, or scores above 100. Clipping the plot at the limit hides this without fixing the estimate near the edge. Either use a method that respects the boundary or use a histogram or ECDF.
- **Small samples.** A smooth curve from 15 values looks far more certain than it is. Add a rug of tick marks or use points.
- When overlaying groups, decide whether each curve is scaled to area 1 on its own (compares shape) or scaled by group size (shows that one group is larger), and say which.
- Check any peak against a histogram or another bandwidth before reporting it.

## Violin plots

A violin is a density curve mirrored around a centre line, usually with a small box plot or quartile marks inside (Hintze and Nelson, 1998). It shows shape that a box plot hides.

- Both sides show the same data. The mirroring is decoration, and some readers will assume the two sides are two groups, so explain if needed.
- Every KDE caution applies: bandwidth, spill past limits, false confidence with small samples.
- **Width scaling varies.** A library may give every violin the same area, the same maximum width, or a width tied to sample size. With equal area or width, a group of 10 looks as substantial as a group of 10,000. Check the setting and print n.
- Trim the violin to the data range unless there is a reason not to.
- **Split violins** put a different group on each half to compare two distributions on one axis. Keep which group is on which side fixed, use the same bandwidth and scaling for both, label the sides, and use two distinct hues. The halves are not parts of a whole.

## ECDF

An empirical cumulative distribution function plots, for every value, the share of observations at or below it. The line climbs from 0 to 1.

- It needs no bin width and no bandwidth, so there is nothing to tune.
- It answers threshold questions directly: "what share finished within 30 seconds?" Read up from 30. "What time did the fastest quarter beat?" Read across from 0.25.
- Several groups overlay cleanly. A curve further left means lower values overall.
- Steep sections are where values concentrate. Flat sections are gaps. Peaks are less obvious than in a histogram.
- Many readers have not seen one. Label the y-axis in plain words, such as "share of orders delivered within this time".

## Small samples: show the points

With a few dozen observations or fewer per group, show every point (strip plot with a little jitter, or a swarm plot), with a median line or a light box behind if useful. A histogram, density curve or violin of 12 values manufactures a shape. The points show exactly how much evidence there is.

## Comparing groups

- Same variable, same units, same axis, same bins or bandwidth for every group.
- State n for each group.
- Decide whether to compare counts (how many) or normalised shapes (how they are spread), and label it.
- Compare more than the centre. Do the groups differ in spread, tails, number of peaks? How much do they overlap?
- A higher average for one group does not mean every member is higher. If the distributions overlap heavily, say so. Do not turn a difference between groups into a claim about individuals.
- A bar of means with nothing else hides everything on this list. At the least, add an interval and say what it is.
- A difference between groups is not evidence of why they differ. See the causation section in `relationships.md`.
