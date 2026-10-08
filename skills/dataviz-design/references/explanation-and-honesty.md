# Explanation and honesty

How to turn a correct chart into one that communicates, and how to make sure the impression it leaves is true.

## Contents

- Exploring versus explaining
- Know the reader
- Eight questions for any explanatory chart
- Titles, labels and legends
- Annotation
- Emphasis without distortion
- Levels, changes and rates
- Misleading patterns and their repairs
- The two-question test

## Exploring versus explaining

| When exploring | When explaining |
|---|---|
| Ask many questions | State one question or finding |
| Look at raw points and distributions | Keep enough evidence to support the finding |
| Try many groupings and scales | Settle on one stable arrangement |
| Chase the exceptions | Explain the important exceptions, do not hide them |
| Rely on interaction and quick redraws | Make the point visible without interaction |

Moving from one to the other is a design step. A screenshot of an analysis notebook is rarely a good presentation chart, and a tightly edited story chart is rarely enough for an analyst.

Being selective is necessary. Leaving out evidence that contradicts the message is misleading. Explore widely, explain narrowly, and keep the counter-evidence in view.

## Know the reader

- **What do they already know?** A finance team reads candlesticks. A science audience reads box plots and error bars. A general audience may need a bar chart and a sentence. A valid chart fails if the reader does not know how to read it.
- **What must they know to read this chart?** Units, baseline, what a percentage is a share of, what a band means, whether a line is a forecast. Supply whatever is missing on the chart itself.
- **Where will they see it?** A projected slide needs bigger text and fewer fine distinctions than a report. Print has no tooltips. A phone screen holds far fewer labels than a desktop.
- **Can they perceive it?** Do not judge legibility by your own eyes on your own screen. Check at final size, on the final background.

## Eight questions for any explanatory chart

These follow Kosslyn's (2006) principles for graph design, grouped by what they protect.

**Connecting with the reader**

1. **Relevance.** Does the chart show what the reader needs for this question, no more and no less? Too little context makes a finding uninterpretable. Too much buries it. Context means units, period, denominator, a baseline or benchmark, and relevant peers. It does not mean every column in the data.
2. **Appropriate knowledge.** Does it use forms, terms and conventions this reader understands? Define abbreviations and any metric whose meaning is not obvious ("rate" per what?).

**Directing attention**

3. **Salience.** Is the most important thing the most visible thing? A reader's eye goes to the strongest contrast first.
4. **Discriminability.** Are the differences that matter big enough to see at final size? Tiny slices, near-identical shades and hairline strokes carry information nobody can recover.
5. **Perceptual organisation.** Does the layout group things the way the data groups them? Spacing, colour, connecting lines and boxes are read as grouping before any legend is read. See grouping in `encoding-and-perception.md`.

**Supporting understanding and memory**

6. **Compatibility.** Does the form match the meaning? More is up or longer. Time runs left to right. Ordered processes get lines and separate categories do not. Where lower is better, say so.
7. **Informative changes.** Does every visual difference mean something, and does every important difference in the data get a visual difference? No random colours. A dashed line for a forecast. A visible break where a definition changed.
8. **Capacity limits.** Can the reader follow it without holding many things in mind? Label directly. Keep colour meanings fixed. Put compared things next to each other.

Apply them together. A chart can be eye-catching and irrelevant, or simple and in a form the reader cannot decode.

## Titles, labels and legends

- **Title.** Say what the chart shows as a finding or a question. "Support tickets doubled after the March release" is better than "Tickets by month". Keep it honest: the title is where overclaiming usually happens. Every number and comparison in it must be readable from the chart. See `claims-and-evidence.md`.
- **Subtitle.** Population, period, unit, and transformations. "Weekly active users, 2023 to 2025, 4-week average."
- **Axis labels.** Name and unit. Drop the axis title only when the tick labels make it obvious (years, month names).
- **Direct labels.** Put series names at the ends of lines and values on or beside bars when that fits. This removes the back-and-forth to a legend.
- **Legends.** When needed, place them close to the data, in the same order as the marks appear.
- **Value labels.** Label the values that matter, not all of them. A label on every point hides the pattern.
- **Precision.** Round to what the data supports and the reader needs. "23.4%" from a sample of 60 claims too much. "About 23%" is more honest.
- **Notes.** Source, sample size, exclusions, and definitions that change the reading. Keep the rest for the reply. See the text budget in `layout-and-typography.md`.
- For colour and size, explain the mapping ("darker = more orders", "circle area = population"), not the palette name.

## Annotation

Annotations tie the finding to the evidence. Use them to mark an unusual point, a turning point, an event, a target or a comparison.

- Place the note next to what it refers to. Use a thin leader line only if needed.
- Keep it to a few words. One or two annotations per chart.
- Separate fact from interpretation. "Two engineers left in May" is context. "The backlog grew from June" is a description of the chart. "The departures caused the backlog" is a causal claim the chart cannot prove.
- Annotate transformations that affect reading: a 7-day average, an estimated period, a change of definition, a restricted sample.
- A note cannot rescue a misleading design. If the axis or geometry gives a false impression, fix that.

## Emphasis without distortion

To direct attention, change how a mark looks. Never change what it measures.

Fine:

- an accent colour on the focus and grey for the rest,
- a heavier line, a larger label, a callout,
- putting the key item first.

Not fine:

- a wider bar for the favoured category,
- an exploded or front-facing slice in a tilted pie,
- cropping the axis or the time range to make a change look bigger,
- choosing a scale because it shrinks an inconvenient gap.

If everything is emphasised, nothing is. Decide on a three-level order: the finding, the supporting data, the scaffolding (axes, grid, notes).

## Levels, changes and rates

The same data can be shown as a level, a change, or a rate of change. They can point in different directions.

- **Level:** the value itself.
- **Absolute change:** this period minus the last.
- **Relative change:** absolute change divided by the last value. Only meaningful for ratio data with a nonzero base.
- **Percentage points:** the difference between two percentages. A share rising from 20% to 22% is up 2 percentage points and up 10% in relative terms. Mixing the two is one of the commonest errors in data reporting.

A level can keep rising while its growth rate falls. Sales of 100, 110, 118, 124 grow by 10%, 7%, 5%. A chart of the growth rate slopes down, and readers may conclude sales are falling. So:

- Name the measure in the title and axis: "Year-on-year growth (%)", not "Sales".
- When the difference matters, show the level and the change in two aligned panels.
- A small growth rate on a large base can still be a large absolute increase.
- Never compute percentage change on interval data such as temperature in Celsius or a calendar year.

## Misleading patterns and their repairs

| Pattern | Why it misleads | Repair |
|---|---|---|
| Bar axis that does not start at zero | Small differences look like large ratios | Start at zero, or switch to dots or a line with a stated range |
| Inverted y-axis | A rise looks like a fall | Up means more. If reversal is really needed, label it prominently |
| One bar wider than the others | Extra area reads as extra importance | Equal widths. Highlight with colour or a label |
| 3D pie or 3D bars | Front items look bigger. Back items are hidden | Draw flat. Use sorted bars for close values |
| Cherry-picked time window or peers | Hides the wider trend or a competitor | Show the relevant period and peers. Mark any zoomed detail as a detail |
| Dual axes tuned to cross or align | Suggests a relationship that the scaling created | Separate panels, or index both to a common base |
| Log scale on amounts where absolute gaps matter | Compresses the gap | Linear scale, or state clearly that ratios are the question |
| Growth rate presented as the level | Slowing growth read as decline | Name the measure. Pair with the level |
| Smoothed or curved line presented as raw data | Hides variation and invents shape | Show raw data faintly. State the smoothing |
| Radius used for bubble size | Large values look far too large | Scale area. Add a size legend |
| Share shown without the group size | 50% of 20 looks like 50% of 20,000 | Print n or totals |
| Missing data drawn as zero or bridged by a line | Invents a drop or a continuity | Leave a gap. Mark estimates |
| Different colour scale ranges across panels that look the same | Same colour means different values | One shared scale, or label each clearly |
| Red and green as the only signal | Unreadable for many readers | Add signs, labels or shapes. Use blue and orange |
| Overlapping categories drawn as parts of a whole | Double counting | Disjoint groups, or separate bars |
| Mean bars with no spread | Hides overlap between groups | Show the distribution or an interval |
| Title that claims a cause | The chart shows timing or correlation only | Describe what happened. Keep causal language for causal evidence |

## The two-question test

Before delivering, ask:

1. **Are the numbers and transformations correct?**
2. **What will a reasonable reader conclude in five seconds, and is that conclusion supported?**

A chart with accurate numbers still fails the second question if its dominant impression is false. Printing the true values on a distorted chart does not undo the distortion, and a footnote does not license a design whose first impression misleads. Do not choose a design only because it makes one side look better.
