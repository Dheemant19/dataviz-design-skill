# Composition charts

Charts that show how a whole divides into parts: pies, donuts, stacked bars and areas, treemaps, waterfalls and funnels.

## Contents

- First check that there is a valid whole
- Pie charts
- Donuts
- Stacked bars
- 100% stacked bars
- The floating baseline problem
- Stacked areas
- Treemaps and other hierarchy charts
- Waterfalls
- Funnels
- Composition checklist

## First check that there is a valid whole

A part-to-whole chart claims three things. Check all three before drawing.

1. **There is a defined whole.** What is being counted, for which population and period?
2. **Parts do not overlap.** No record belongs to two parts.
3. **Parts cover the whole.** They add up to the total, or the remainder is shown as its own part.

Common violations:

- **Multi-select survey answers.** People can tick several options, so the percentages add to more than 100. That is not a pie. Use bars, one per option.
- **Nested metrics.** "Total cases", "in hospital" and "in intensive care" overlap. Stacking them counts people two or three times. Either compute disjoint groups (intensive care, hospital but not intensive care, not in hospital) or draw separate lines.
- **A total stacked with its own parts.**
- **Unrelated quantities** that happen to share a unit.
- **Negative parts.** Ordinary stacks and pies cannot show them.

Then decide what the reader needs: the absolute size of parts, their shares, how the total changes, or the hierarchy. That decides between a plain stack, a 100% stack, a pie, a treemap or something else.

## Pie charts

A pie encodes share as angle, which people judge less accurately than length. It works in a narrow case:

- one whole, at one moment,
- about five slices or fewer,
- shares that differ clearly, or a simple message such as "about a quarter" or "more than half".

Use bars instead when shares are close, when there are many slices, when the reader needs to rank, or when the same categories must be compared across several wholes. Comparing slices across two pies is especially hard.

If you do use a pie:

- Keep it flat. No 3D, no tilt.
- Do not explode slices. To emphasise one, use colour or a label.
- Order slices from largest to smallest starting at 12 o'clock, unless the categories have their own order.
- Label slices directly with name and percentage. State the total (n) somewhere.
- If small slices are merged into "Other", say what is in it.

## Donuts

A donut is a pie with the centre removed. The centre is a good place for the total or a key figure. It does not fix the precision problem, since the reader now compares arc lengths.

Nested rings are harder still. The same share is a longer arc on an outer ring than on an inner one, so arcs on different rings cannot be compared by length. Prefer two aligned 100% bars.

## Stacked bars

A stacked bar shows a total (full length) and its parts (segments).

- Keep segment order and colours identical in every bar. Do not reorder each bar to put its biggest part first, because readers lose track of which part is which.
- Put the most important component at the bottom (or left), where it sits on the common baseline and can be compared accurately.
- Order the bars themselves by time, by natural order, or by total.
- Choose the palette from what the components are: distinct hues for unordered parts, a sequential ramp for ordered bands, a diverging pair for negative to positive answers. See `colour.md`.
- Label totals at the end of the bars when totals matter.

## 100% stacked bars

Every bar is rescaled to the same length, so segments show shares. This makes mix comparable across groups of different size, and hides the size.

- Compute each share within its own bar: part divided by that bar's total.
- Show the group size (n or total) next to each bar. Two bars of equal length can stand for 20 people and 20,000.
- The two outer segments are easy to compare because each touches an edge. Middle segments are not.
- For survey scales, a diverging stacked bar lines the bars up on the neutral midpoint, so the reader sees the balance of negative and positive answers at a glance (Heiberger and Robbins, 2014). Say how the neutral answers are placed: split across the centre line or shown separately at the side.

## The floating baseline problem

Only the first segment of a stack starts at zero. Every other segment starts wherever the ones below it end, so both its edges move from bar to bar.

Consequences:

- The reader must compare segment thicknesses with no shared starting line. That is a weak judgment.
- An upper boundary moving up does not mean that segment grew. A lower segment may have grown and pushed it up.
- This applies equally to stacked bars, stacked areas and their 100% versions. Better colours do not fix it.

What to do instead, depending on the task:

| The reader needs | Use |
|---|---|
| Total and rough make-up | Keep the stack |
| One component compared across bars | Put that component on the baseline |
| Several components compared precisely | Grouped bars, or dots on a common axis |
| Each component's trend over time | Separate lines, or small multiples |
| A few specific numbers | Direct value labels on the segments |

## Stacked areas

A stacked area is a stacked bar over continuous time. The top edge is the total. Each band's thickness is one component.

- The bottom band can be read directly. Every other band must be read by thickness, and its slope mixes its own change with the change of everything below it.
- Keep the layer order fixed across the whole chart. Put the steadiest or the most important layer at the bottom.
- A plain stack shows the total changing as well as the mix. A 100% stacked area holds the top at 100% and shows only the mix, so if the total changes a lot, add a small line chart of the total beside it.
- Do not use stacked areas for values that can go negative.
- Streamgraphs (stacks with a wavy central baseline) look good and make every value hard to read. Use them only when the overall impression matters more than any number.
- If the reader must compare component trends, use lines or small multiples.

## Treemaps and other hierarchy charts

A treemap divides a rectangle into nested rectangles whose areas are proportional to a value (Shneiderman, 1992). It shows many parts in little space and makes the biggest contributors obvious.

- The value must add up through the hierarchy. Check that children sum to parents.
- Area is read roughly, and rectangles of different shapes are harder to compare than bars. If precise ranking matters, add a sorted bar chart or use one instead.
- Label only cells large enough to hold text. Provide the rest another way (tooltip, table).
- Colour can show the group, or a second measure. Not both at once without a clear key. A treemap with area for size and a diverging colour for change carries two different measures, and the biggest cell and the most intense cell will usually be different items. Explain both in the legend.
- Sunbursts and circle packing show the same structure with weaker size comparison. Choose them only if the nesting itself is the message.

## Waterfalls

A waterfall explains how a starting total becomes an ending total through a series of additions and subtractions.

- Start and end bars are totals and stand on the baseline. The bars between are changes and float.
- Make totals and changes look different, and make increases and decreases look different, with signs on the labels as well as colour.
- Check the arithmetic. Start plus all changes must equal the end.

## Funnels

A funnel shows how many items remain at each stage of a process (visited, signed up, paid).

- Stages are nested. Everyone who paid also signed up and visited. They are not parts of one whole, so never draw them as a pie or a stack.
- Plain horizontal bars, one per stage, sorted in process order, are clearer than a tapering funnel shape, whose slanted sides distort the lengths.
- State which percentage is shown: share of the first stage, or share of the previous stage. They give very different numbers.

## Composition checklist

- [ ] The whole, population, period and denominator are stated.
- [ ] Parts are disjoint and together cover the whole.
- [ ] Totals were checked. Nothing is counted twice.
- [ ] Plain stack for amounts or 100% stack for shares, chosen by the question.
- [ ] Group sizes are shown when shares hide them.
- [ ] Segment order and colours are the same in every bar.
- [ ] The key component sits on the baseline.
- [ ] If middle segments must be compared precisely, a different chart is used or values are labelled.
- [ ] The palette family fits what the components are.
- [ ] The chart is a stack because total or mix matters, not because it looks full.
