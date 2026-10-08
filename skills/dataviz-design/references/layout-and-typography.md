# Layout and typography

How a finished static chart is put together: size, type scale, text budget, labels, number formats and export. `scripts/chartkit.py` applies these defaults for matplotlib. For other tools, use the numbers here directly.

## Contents

- Size for the destination
- Anatomy of a finished chart
- Type scale
- Text budget
- Alignment and spacing
- Direct labels
- Value labels on bars
- Legends
- Number formatting
- Annotations
- Small multiples
- Dark backgrounds
- Export
- Alt text

## Size for the destination

Design at the size the chart will be seen. A chart drawn at 15 inches and shrunk onto a phone has 5-point text.

| Destination | Size (inches) | Export | Base font |
|---|---|---|---|
| Slide, 16:9 | 13.33 x 7.5 | 150 dpi, 2000 x 1125 px | 13 pt |
| Report column (A4 or Letter) | 6.5 x 4.2 | 220 dpi | 9.5 pt |
| Web article or README | 9 x 5.6 | 200 dpi | 11 pt |
| Social post (read on phones) | 12 x 6.75 | 150 dpi | 15 pt |
| Square | 8 x 8 | 180 dpi | 12 pt |

If the user does not say where the chart goes, assume a web page and say so.

## Anatomy of a finished chart

From top to bottom, everything left-aligned to one edge:

1. **Title.** The finding, one line, bold.
2. **Subtitle.** What is plotted: measure, unit, scope, period. One line, two at most.
3. **Plot.** Panel titles above each panel when there are several.
4. **Footer.** A note only if it changes the reading, then the source.

Put the unit where the eye needs it: in the subtitle or panel title for a single measure, on the axis when panels differ.

## Type scale

Sizes as multiples of the base font for the destination:

| Role | Size | Weight and colour |
|---|---|---|
| Title | 1.55 x | Bold, near black |
| Subtitle | 1.0 x | Regular, dark grey |
| Panel title | 1.0 x | Bold, near black |
| Axis label | 0.9 x | Regular, dark grey |
| Tick labels | 0.85 x | Regular, dark grey |
| Direct labels and annotations | 0.9 x | Regular. Bold for the focus |
| Note and source | 0.78 x | Regular, mid grey, still at least 4.5:1 contrast |

Use one sans-serif family throughout. Never go below 7 pt at the final size, or below 8 pt for ticks and axis labels.

## Text budget

Text competes with data for attention. Limits that work for most charts:

- Title: one line, under about 70 characters.
- Subtitle: one line. Two only if the second carries context that changes the reading.
- Annotations: at most two in one panel, each under about ten words.
- Note: one or two lines. Source: one line.
- In total, the title, subtitle and notes should stay under about 350 characters.

Everything that does not fit goes in the message that accompanies the chart. Definitions, methods and secondary numbers belong there.

## Alignment and spacing

- Left-align the title, subtitle, panel titles and footer to the same edge as the leftmost tick labels. Centred titles float.
- Leave clear space between the title block and the plot (about one line of subtitle text).
- Do not stretch a chart to fill space. Leave margins.
- Keep panels in a grid on the same baseline, with the same width for panels that are compared.

## Direct labels

Label lines at their right end, in the same order as the line endings, and remove the legend.

- The focus label is bold in the series colour, if that colour has at least 3:1 contrast with the background. Otherwise use near-black text.
- Context labels are regular weight in mid grey.
- When ends crowd together, spread the labels vertically and draw thin leader lines from line to label. Keep all labels in one aligned column.
- When more than about six context lines end in one small band, label them as a group ("Six other regions, 5 to 9 thousand") instead of one by one.
- `chartkit.label_lines` does the spreading and leaders.

## Value labels on bars

- Put the value just past the end of the bar, with the same gap for every bar.
- Use one precision for all labels in a set. "322%, 84%, 45%", not "322%, 83.8%, 44.9%".
- A second label (an amount next to a share) goes after the first, in quieter grey, with an even gap. Or combine them into one label: "42% ($42k)".
- When every bar is labelled, remove the value axis. Do not show both.
- Negative bars take their label on the left.
- `chartkit.bar_labels` does all of this and widens the axis so labels stay inside.

## Legends

Use a legend only when direct labels would collide or there are many small marks (a scatter with colour groups).

- Place it above the plot, left-aligned, in one row if it fits.
- Order entries the way they appear in the chart.
- One legend for the whole figure when panels share the same series.
- No legend for a single series. The title already names it.

## Number formatting

- Thousands separators: 12,289, not 12289.
- Big numbers: either full values with a unit in the subtitle ("million tonnes") or compact values (15.8k, 3.2M, 4.1bn). Do not mix the two in one chart.
- Significant figures: two or three in labels. "41%", not "40.94%". Keep more only when the decimal matters.
- Percent versus percentage points: a change from 20% to 22% is "+2 points" or "+10%". Never write "+2%" for that.
- Signs: use a true minus sign (−) and show "+" for positive changes.
- Dates: "Mar 2025" or "2025-03" on axes. Whole years as plain integers, never 2,020 or 2020.0 or 2002.5.
- Currency: put the symbol and the unit in one place ("thousand dollars" in the subtitle, or "$15.8k" on labels).

## Annotations

- Annotate the one or two things the reader must not miss: the turning point, the outlier, the event.
- Place the text in empty space near the point, with a thin grey leader line. Never cover data.
- Write facts, not adjectives. "Plant closed, March 2021" beats "Dramatic drop".
- Annotation text is dark grey, or the accent colour if it belongs to the focus series.

## Small multiples

- Shared axes by default. If you free them, say so in the subtitle.
- Each panel shows its own series in colour over the other series in light grey, so every panel carries the comparison.
- Order panels by something meaningful: size, change, or a natural order. Alphabetical only when readers will look things up.
- Panel titles are just the item name. Tick labels on the outer edge only, where possible.
- `chartkit.grid` makes the grid and removes unused cells.

## Dark backgrounds

Do not just invert colours. On a dark background:

- Use a near-black or dark grey surface, not pure black.
- Text is off-white for titles and light grey for the rest, at 4.5:1 contrast or more.
- Context marks are a mid grey that is clearly visible but quieter than the accent.
- Re-check every data colour against the dark surface with `scripts/check_palette.py --background "#1E1E1E"`.

## Export

- Export at the destination size and dpi in the table above. Do not rely on `bbox_inches="tight"` to rescue a cramped layout. It changes the final size.
- PNG for slides and web. SVG or PDF for print and for editing later.
- White background unless the destination is dark.
- Open the exported file and look at it at its real size.

## Alt text

Every chart that leaves the conversation needs alt text. Write two to four sentences:

1. Chart type and what is plotted ("Line chart of annual sales for eight regions, 2005 to 2024").
2. The main finding with its key number ("Dunmore's sales rose by 322%, the most of any region").
3. One supporting detail if it matters ("The three largest regions changed by less than 20%").

`chartkit.finish(..., alt="...")` writes it to a `.alt.txt` file next to the image.
