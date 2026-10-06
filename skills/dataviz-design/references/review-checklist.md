# Recipes and review checklist

Use the design brief before building, the recipe for the chart type while building, and the final review before delivering.

## Contents

- Design brief
- Recipe: category comparison
- Recipe: time trend
- Recipe: part to whole
- Recipe: relationship
- Recipe: distribution comparison
- Final review
- Reporting back to the user

## Design brief

Fill this in, even if only mentally, before writing chart code. A field you cannot fill is a design problem to solve first.

| Field | Answer |
|---|---|
| Reader | Who, what they know, where they will see it |
| Purpose | The question being answered, and what the reader will do with the answer |
| Population | What is covered: which entities, which groups, what dates |
| Grain | What one row is, and what one mark will be |
| Variables | Meaning, unit and scale type of each |
| Preparation | Joins, filters, missing-value handling, derived values |
| Task | Comparison, composition, relationship or distribution |
| Key comparison | What must be easiest to compare |
| Encoding | Mark, and the channel for each variable |
| Scales | Baseline, range, direction, transformations, shared or free panels |
| Message | The supported finding, and what remains uncertain |
| Delivery | Static or interactive, size, medium |

## Recipe: category comparison

1. Define the value, its unit and its aggregation.
2. Decide what the reader will do: rank the items, read the gap between two of them, or judge each against a goal.
3. Use bars or dots on one common axis. Use a bullet chart for value against target.
4. Go horizontal when labels are long or there are many categories.
5. Bars from zero. For small but meaningful differences, dots on a stated range.
6. Sort by value, unless there is a natural order.
7. Equal widths, one colour, an accent only for the focus.
8. Add the few values and the context the reader needs. Add an interval if the values are estimates.

## Recipe: time trend

1. Parse dates. Define the period and the sampling interval.
2. Check order, gaps, revisions and changes of definition.
3. Line for the shape of change. Bars for totals per period.
4. Real time spacing. Connect only within one series.
5. Choose the aspect ratio and state the y-range.
6. If smoothing, state window and alignment, and keep the raw series visible when it matters.
7. Fixed colour per series, labelled at the line end.
8. Mark events, gaps and forecasts. Do not imply cause.

## Recipe: part to whole

1. State the whole, the population and the period.
2. Confirm parts are disjoint and add up.
3. Amounts or shares? Plain stack or 100% stack.
4. A few parts of one whole: sorted bars or a flat pie. Many parts or a hierarchy: treemap or bars.
5. Fixed segment order and colours. Key segment on the baseline.
6. Palette family from what the parts are.
7. Show n or totals whenever shares are shown.
8. If middle segments must be compared precisely, switch to grouped bars, dots or small multiples.

## Recipe: relationship

1. Define what one point is. Check units.
2. Draw the points before computing any coefficient or fit.
3. Look at direction, form, clusters, gaps, overlap and unusual points.
4. Investigate influential points and possible errors.
5. Add a fit only if it serves the question. If the shape is uncertain, compare two methods.
6. State the fit type and its settings. Do not extrapolate.
7. Label any band with what it is and its level.
8. For a third variable as size, scale area and add a size legend.
9. Describe an association as an association.

## Recipe: distribution comparison

1. Define the variable, its valid range and the groups.
2. Check group sizes and missing values.
3. Look at raw values or a simple histogram first.
4. Use shared bins and a shared axis. Try another bin width.
5. Label the y-axis as count, share or density.
6. Box plots for many groups, with shape added (violin, points) when peaks or tails matter.
7. For violins and density curves, check bandwidth, limits and width scaling.
8. Print n per group.
9. Describe overlap as well as difference. Make no claims about individuals from group summaries.

## Final review

Go through all four parts on the rendered image, at final size.

**Data**

- [ ] Population, grain, units and period are clear.
- [ ] Joins, filters and aggregations were checked against known totals.
- [ ] Every percentage has a stated denominator.
- [ ] Missing, estimated and zero values are distinguishable.
- [ ] Outliers were handled deliberately and that is recorded.
- [ ] Bins, smoothing, fits and normalisation are stated where they affect the reading.

**Encoding**

- [ ] Each channel suits the scale type of its variable.
- [ ] The key comparison uses position or length on a common scale.
- [ ] Bars start at zero and have equal widths. Sizes are scaled by area.
- [ ] Axis ranges, direction and transformations are honest and labelled.
- [ ] No decorative 3D. No unexplained dual axis.
- [ ] Layout groups things the way the data does.
- [ ] Grid, frame and decoration sit behind the data.
- [ ] Colour follows the palette checklist in `colour.md`.

**Message**

- [ ] The reader can tell what the main point is.
- [ ] Enough context is shown: baseline, peers, period.
- [ ] The title and notes do not overstate size, certainty or cause.
- [ ] Levels, changes, growth rates and percentage points are named correctly.
- [ ] Any interval or band says what it is.
- [ ] Nothing a fair reader would want to know has been left out to help the story.
- [ ] The five-second impression is supported by the data.

**Output**

- [ ] Text is readable at final size. No clipped or overlapping labels.
- [ ] Pale marks are visible on the real background.
- [ ] A static version works without hover or animation.
- [ ] Works in greyscale, or has a second cue for anything essential.
- [ ] The code or steps can reproduce the chart, including fixed colours and orders.

## Reporting back to the user

When you deliver a chart, briefly state:

- the question the chart answers,
- any choice that changes the reading (aggregation, filter, smoothing, scale, exclusions),
- anything the data cannot support that the user might assume, such as cause.

Keep this to two or three sentences. If you changed the chart type from what was asked because the requested form would mislead (a pie for overlapping categories, a dual axis), say what you did and why, and offer the original if they still want it.
