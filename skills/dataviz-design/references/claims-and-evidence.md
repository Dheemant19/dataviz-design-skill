# Claims and evidence

A chart is an argument. The title makes a claim, and the marks are the evidence. Most weak charts are not ugly. They show the right data in a way that does not prove the point, or they prove a point nobody asked about. Use this file before choosing the form.

## Contents

- Write the headline first
- Match the claim to the evidence
- Choose the measure
- Series of very different sizes
- One view or two
- Choosing context
- The cover test

## Write the headline first

Before any plotting code, write the sentence you expect the chart to support. Then look at the data to confirm or correct it. A good headline has:

- **a subject** (who or what),
- **a comparison or change** (more than, fell, overtook, the only, half of),
- **a number** when one exists,
- **a scope** if it is not obvious (since 2010, among the ten largest).

| Weak | Strong |
|---|---|
| Revenue by region | The North overtook every other region in 2024 |
| Survey results | Two thirds of new staff found onboarding unclear |
| Delivery times | Half of late deliveries come from one warehouse |

If you cannot write the sentence, the analysis is not finished. Explore more, or make an exploratory chart and say it is one.

Claims must be the size of the evidence. "Rose after" is not "rose because of". "In our sample" is not "everywhere". A difference smaller than the noise is not a finding.

## Match the claim to the evidence

Every claim type has a view that proves it at a glance. If the title makes a claim of one type and the chart shows another, the reader has to take the claim on trust.

| The headline says | The reader must be able to see | Use |
|---|---|---|
| X is the largest, smallest, or ranks Nth | All the items on one scale, in order | Sorted bars or dots |
| X grew fastest, fell most, changed most | The change itself for every item | Bars of percent or absolute change, sorted, or lines indexed to a common start |
| X overtook Y, or X passed a threshold | Both series over time and the crossing | Lines with the crossing point marked |
| X is N% of the total | The part next to the whole | Bar of shares, or one stacked bar |
| X is unusual, the only one, an exception | X against everything else | Everything in grey, X in colour, on a shared scale |
| X and Y move together | Paired values | Scatterplot, one point per unit |
| Growth is slowing (or speeding up) | The rate of change over time | A growth-rate panel, paired with the level |
| X is still far below or above Y | The gap at the latest point | Dots or bars for the latest values, or a labelled gap |
| Groups A and B differ | Both distributions and their overlap | Shared-axis histograms, box plots or strip plots |
| X is concentrated in a few places | The cumulative share | Sorted bars with a running total, or a cumulative line |

Superlatives need special care. "Most", "fastest", "largest", "first", "only", "record" and "all" each claim something about every item, so every item must be visible in the measure the superlative refers to. A line chart of levels does not prove "fastest growth". A bar chart of growth does.

## Choose the measure

The same data can be shown as several different quantities. They answer different questions and can point in different directions.

| Measure | Answers | Watch for |
|---|---|---|
| Level (the value) | How big is it now? | Large items dominate the scale |
| Absolute change | How much was added or lost? | Favours large items |
| Percent change | How fast did it change? | Explodes for small bases. A rise from 2 to 6 is +200% |
| Index (start = 100) | How has each changed since a common start? | The choice of start year changes the story. Say what it is |
| Share of total | How big is it relative to the whole? | Hides whether the whole grew |
| Rate or per person | How intense is it, allowing for size? | State the denominator |
| Cumulative | How much has built up over time? | Always rises. Do not read slope as level |
| Rank | Where does it stand? | Hides the size of gaps |

Pick the measure the headline is about. If the honest story needs two measures (a level that keeps rising and a growth rate that is slowing), show two aligned panels instead of choosing the more dramatic one.

## Series of very different sizes

When one series is ten or more times larger than the others, a shared linear axis squashes the small ones into an unreadable band. Decide by the question:

| The question is about | Do this |
|---|---|
| The big items, and the small ones only as context | Keep the linear scale. Grey and group the small series, label the group |
| How each one changed | Index every series to 100 at a common start, or plot percent change |
| Ratios or growth across orders of magnitude | Log scale, labelled with plain numbers (50, 100, 200), and say it is a log scale |
| The shape of each series on its own | Small multiples. Shared axes if sizes are compared, free axes if only shape matters, and say which |
| Both size and change | Two panels: levels on the left, change on the right |

`scripts/chartlint.py` flags squashed series automatically.

## One view or two

A single chart should make one point. Use a second panel when the headline contains a second claim that the first view cannot prove, for example:

- levels over time, plus the change for each item ranked,
- a share of the total, plus the total itself over time,
- a level, plus its growth rate,
- a map, plus a ranked bar of the same values,
- an overall trend, plus the breakdown that explains it.

Rules for composite charts:

- The main view is larger and on the left or top.
- The focus item has the same colour in every panel.
- Each panel gets a short title that says what it measures, with the unit.
- Keep the same item order across panels where items repeat.
- At most three panels on one slide. Beyond that, split into separate charts.

## Choosing context

Context is anything beyond the data needed for the headline: a benchmark, a per-person figure, a definition, a coverage note. Add context only if it could change what a reasonable reader concludes. Examples:

- A total that is large only because the population is large: add the per-person figure.
- A share of a total that has itself shrunk: add the total.
- A rise that is mostly one category reclassified: say so.
- A comparison where one group's data is incomplete: say so.

Put the context that changes the reading in one subtitle sentence or one short note. Put everything else (methods, extra numbers, nice-to-know facts) in the message that goes with the chart. A chart with a paragraph under it is a chart the reader will not finish.

## The cover test

Before delivering:

1. Cover the title. Look only at the chart. What would you conclude?
2. Now read the title. Does it say the same thing?
3. Is every number in the title readable from the chart, or from a label on it?

If the chart alone suggests something else, change the chart or change the title. Do not leave the gap for the reader to resolve.
