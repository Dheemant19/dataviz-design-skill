# Data meaning and preparation

Most misleading charts are wrong before anything is drawn. Use this file to check that the numbers mean what the chart will claim.

## Contents

- First look at a new dataset
- Scale types and what they allow
- Classification traps
- Grain and keys
- Rows that are not what they seem
- The latest period
- Units and scale
- Joins and appends
- Long and wide shape
- Ordering
- Missing values
- Outliers
- Aggregation and derived values
- Denominators and normalisation
- Data with structure: time, space, hierarchy, network
- Preparation audit

## First look at a new dataset

Spend a minute profiling before choosing anything. Print, do not assume:

- number of rows and columns, and the column names with their types,
- for each key column (entity, category, date): the number of distinct values and a sample of them, including the longest and strangest names,
- the first and last date or period, and whether every entity covers the same range,
- the share of missing values in each column you plan to use, by period if the data is a time series,
- the minimum, maximum and a few quantiles of each measure, with its unit if the documentation gives one.

Read the documentation or codebook if there is one. Column names lie more often than you would think.

## Scale types and what they allow

How a value is stored (int, float, string) says nothing about what it means. Classify each variable by meaning. The four scale types come from Stevens (1946).

| Scale | What the values tell you | Valid comparisons | Encode with | Do not |
|---|---|---|---|---|
| Nominal | Which group | Same or different, counts per group | Separate positions, distinct hues, shapes, facets | Use a colour ramp, average the codes |
| Ordinal | Which group, and rank | Higher or lower | Ordered positions, a sequential ramp | Assume equal gaps, sort alphabetically |
| Interval | Differences, zero is arbitrary | "10 more than" | Position on an axis with a sensible range | Say "twice as", force a zero baseline, compute percent change |
| Ratio | Amounts, zero means none | "Twice as much" | Position, length, proportional area | Forget units and what is being counted |

Why it matters for design:

- Bars encode length from zero, so they imply ratios. That suits ratio data. For interval data such as temperature in Celsius, a bar from zero implies that 20 degrees is twice 10 degrees, which is false. Use dots or a line instead.
- A diverging palette needs a meaningful midpoint. A ratio variable having a zero is not enough reason to use one. Population by region is low to high, so it is sequential.
- Averaging ordinal codes (1 to 5 survey answers) assumes equal gaps between answers. Prefer showing the full distribution of answers or the median.

## Classification traps

- **Numeric labels are nominal.** Postcodes, customer IDs, jersey numbers and category codes are names. Never put them on a numeric axis or include them in a correlation matrix.
- **A category and its count are different variables.** "Returned" is a nominal order status. "Orders returned this month" is a ratio count. A bar chart of categories therefore pairs a nominal axis with a ratio axis.
- **Discrete is not the same as "use bars".** Daily counts are discrete and still form a time series that a line can show. Chart type follows the role of the x variable, not whether values are whole numbers.
- **The same thing can be measured at different scales.** A temperature reading is interval. "Frozen or not" is nominal. "Cold, mild, hot" is ordinal with thresholds you chose. Binning throws away detail, so say where the cut points are.
- **A score is not the thing it measures.** 80% on a test is twice the marks of 40%. It is not twice the ability.
- **Calendar time is uneven.** Months differ in length and local clocks jump. Use real elapsed time when spacing matters.

## Grain and keys

Grain means the thing a single row stands for: one order, one customer per day, one country per year. Write it down before joining or aggregating, because every count and average depends on it.

- A row index is not an identity. It changes after filtering or reloading.
- Check that rows are unique at the intended grain. If a country and year pair appears twice, find out why before a library quietly averages or sums it.
- Know what one mark on the chart represents. A point that is a group mean reads very differently from a point that is one person.

## Rows that are not what they seem

Many public and business datasets mix individual entities with rows that summarise them. Ranking, summing or colouring them together double counts and produces nonsense such as "World" ranked as the largest country.

Look for:

- **Totals and subtotals:** "Total", "All", "World", "Grand total", a row equal to the sum of others.
- **Groups of entities:** regions, continents, income groups, "European Union", "Other", "Rest of world", sector totals.
- **Placeholders:** "Unknown", "Not stated", "N/A", "Unallocated", "Unclassified", "International".
- **Entities that changed:** renamed, merged or split units (a company acquired, a country that split), which create breaks or duplicates in time series.

How to find them: the entity's code column is often blank or in a different format for aggregates. Their values are often far larger than the rest, or exactly the sum of others. Check a few by hand.

Then decide deliberately. Keep only true entities for rankings and comparisons. Use the official total row (not your own sum) when you need the whole, because the parts may not cover it. Say in the note what was excluded if it matters.

## The latest period

The most recent period is often different from the rest:

- **Incomplete.** A month or year still in progress, or data that arrives late, shows a false drop.
- **Provisional.** Recent values are often estimates that get revised.
- **Thinner coverage.** Fewer entities may have reported yet, so a total or average shifts for reasons that have nothing to do with the trend.

Check the row count and the share of missing values for the last period against earlier ones. If it is incomplete, drop it, mark it as partial, or use the last complete period and say so.

## Units and scale

- Check whether values are in units, thousands, millions or percent. Columns often hold different scales.
- Check whether a percentage column is stored as 0 to 1 or 0 to 100.
- Check whether money is nominal or adjusted for inflation, and in which currency.
- Put the unit on the chart. A number without a unit is not a finding.

## Joins and appends

A join matches rows by key. It changes which rows survive.

| Join | Rows kept | Risk |
|---|---|---|
| Inner | Only keys found in both tables | Silently drops entities with no match |
| Left | Everything from the left table | Unmatched columns become missing, not zero |
| Outer | Everything from both | Many missing values to handle |

Checks after every join:

- Row count before and after. A many-to-many match multiplies rows and inflates totals.
- A known total (revenue, population) before and after.
- How many keys did not match, and which ones.

Appending tables (stacking rows) needs the same columns, units and definitions. Keep a column that says which source or period each row came from. Putting two tables side by side by row position does not prove that row 5 in one is the same entity as row 5 in the other. Match on a key.

## Long and wide shape

Wide data has one column per measurement (`name, jan, feb, mar`). Long data has one row per observation (`name, month, value`). Most plotting libraries want long data when a variable maps to colour, facet or group (Wickham, 2014).

- Going wide to long (melt, unpivot): keep the identifier columns and check the row count is rows times melted columns.
- Going long to wide (pivot): needs one value per row and column pair. If there are duplicates you must choose an aggregation, and that choice is an analysis decision.
- After reshaping, month names and ordinal levels often end up in alphabetical order. Set the order explicitly.

## Ordering

Pick the order that serves the task:

- Time: chronological. Parse dates as dates, because text sorting puts "10" before "2".
- Ordinal levels: their real rank.
- Nominal categories where ranking is the question: by value, largest first.
- The same categories across several charts: the same order everywhere, so the reader learns it once.

Do not sort months by their values when the point is the seasonal shape. Do not reorder stack layers from bar to bar.

## Missing values

Missing can mean not measured, not applicable, withheld, or no match in a join. None of those is zero.

| Treatment | Reasonable when | Cost |
|---|---|---|
| Leave a visible gap | The reader should know data is absent | None. Often the most honest choice |
| Drop the rows | Exclusion is justified and stated | Changes the sample and every denominator |
| Fill with zero | Missing truly means none by definition | Otherwise invents data and drags averages down |
| Fill with a group average | You have a stated imputation model | Shrinks variation and can create patterns |
| Interpolate | The process is ordered and reasonably smooth, and the gap is short | Hides sudden changes and assumes what happened between points |

Rules:

- Interpolate only within one entity and in the right order. Never across different people or places that happen to sit in adjacent rows.
- A midpoint estimate is an estimate. If Tuesday is 12.4 and Thursday is 13.0, a linear fill gives Wednesday 12.7, and the chart should be able to show that point as estimated.
- In a line chart, break the line at a gap instead of drawing through it.
- In a heatmap, give missing cells their own look (hatched or mid grey), clearly different from the low end of the scale and from a neutral midpoint.
- Say how much data was affected.

## Outliers

An unusual value may be an error, a different kind of case, or the most important observation in the set. Look at the raw record before deciding.

- Check whether it comes from a unit mix-up, a duplicated join or a data-entry error.
- A point beyond a box-plot whisker is flagged by a rule of thumb. It is not proven wrong.
- A point far from a fitted line may mean the relationship is curved or a subgroup is missing from the model.
- If a conclusion changes when one point is removed, show both versions and say so. Do not remove points to make the chart tidier.

## Aggregation and derived values

Every count, sum, mean, share, rate or running total is a new quantity with a definition. Write the definition before plotting.

- Do not average columns just because they are numeric.
- Do not add averages together. A combined average needs weights (usually the group sizes).
- Check whether groups overlap before adding them. "All users", "active users" and "paying users" are nested. Their sum counts people more than once.
- Label what each mark is: one observation, a total, a mean, a median, an estimate.
- Large data must be reduced (aggregated, binned, sampled, filtered), and each reduction changes the question the chart can answer. Decide what must survive. If rare events matter, do not average them away. Compare the aggregate with the breakdown to make sure a subgroup pattern is not hidden.

## Denominators and normalisation

A percentage is a share of something. A rate is an amount per something. The "something" is part of the number.

- In a table of plan by region, "40%" in the Premium and Europe cell could mean that 40% of Premium customers are in Europe, or that 40% of European customers are on Premium. Those are different facts. State which.
- Normalising makes groups of different size comparable and hides their size. 50% of 20 people and 50% of 20,000 people look identical. Show the group size (n) when it matters.
- Different normalisations answer different questions. Counts show volume. Shares show mix. Per-capita rates show prevalence.
- Percent change and percentage-point change are different. See `explanation-and-honesty.md`.

## Data with structure: time, space, hierarchy, network

### Time

- Use a true time axis. Equal spacing for unequal intervals distorts slopes.
- Decide whether the question is about sequence (plot dates in order) or cycle (plot by weekday or month, one line per week or year). Both can be right and they answer different questions.
- A gap is not a zero. Missing periods, reporting changes and redefinitions should be visible or noted.

### Space

Use a map only when location is part of the question. For "which region is highest", sorted bars are easier to read.

| Map type | Shows | Main risk |
|---|---|---|
| Choropleth (shaded regions) | A rate or ratio per region | Big regions dominate the eye. Raw counts mostly reproduce population |
| Proportional symbols | A count at each place | Area scaling and overlap. See bubbles in `relationships.md` |
| Dot density | Spread of a count within areas | Dots look like exact locations when they are not |
| Density surface | Estimated intensity | Smoothing can suggest detail the data does not have |

Shade choropleths with rates (per person, per area), not raw totals. Use a sequential palette unless there is a real midpoint.

### Hierarchy

Parent and child structure (company, division, team). A tree shows the links. A treemap shows how sizes fill a whole. Child values must add up to the parent, and you must not add parents and children together as if they were separate items. See `composition.md`.

### Network

Entities and links between them. A node-link drawing works for small, sparse networks. For dense ones, a matrix with the same entities on rows and columns avoids crossing lines. State whether links have direction and weight. See `relationships.md`.

## Preparation audit

Run through this before designing:

- [ ] The dataset was profiled: columns, types, distinct keys, date range, missing values.
- [ ] Grain and keys are stated, and rows are unique at that grain.
- [ ] Totals, groups and placeholder rows were found and handled before ranking or summing.
- [ ] The latest period is complete, or marked as partial.
- [ ] Units and scales (thousands, millions, 0 to 1 versus 0 to 100) are confirmed.
- [ ] Units, category definitions and time period agree across sources.
- [ ] Row counts and a known total were checked after each join.
- [ ] Reshaping kept identities and did not aggregate duplicates silently.
- [ ] Dates and ordinal levels are in real order.
- [ ] Missing is kept separate from zero, and any imputation is recorded.
- [ ] Outliers were looked at, not just removed.
- [ ] Filters and exclusions are recorded, with their effect on denominators.
- [ ] Every derived value has a definition and a unit.
- [ ] You can trace any mark on the chart back to the rows behind it.
