# Colour

Colour in a chart should have a job. Decide the job first, then pick the palette.

## Contents

- The four jobs of colour
- Pick the palette family from the data
- Qualitative palettes
- Sequential palettes
- Diverging palettes
- Emphasis: grey plus one accent
- Accessibility
- Legends and colour bars
- Consistency across charts
- Context, screen and print
- Associations and tone
- Palette checklist

## The four jobs of colour

1. **Identity.** Which category is this?
2. **Order or amount.** How much, from low to high?
3. **Direction.** Which side of a reference, and how far?
4. **Emphasis.** Where should the reader look?

If a colour difference does none of these jobs, remove it. A single series does not need a different colour for each bar.

## Pick the palette family from the data

| The variable is | Family | What the reader must see | Examples |
|---|---|---|---|
| Unordered categories | Qualitative | Different, with no ranking | Departments, products, countries |
| Ordered levels or a low-to-high quantity | Sequential | A steady progression | Counts in a heatmap, age bands, density |
| Values on two sides of a meaningful centre | Diverging | Which side, and how far from the centre | Change from last year, deviation from target, disagree to agree |
| Values that wrap around | Cyclic | Start and end meet | Wind direction, hour of day (only when colour is really needed) |

The chart type does not decide the palette. A stacked bar of departments is qualitative. A stacked bar of age bands is sequential. A stacked bar of survey answers from "strongly disagree" to "strongly agree" is diverging.

Having a zero does not make data diverging. Use a diverging palette only when both sides of the centre mean something different (loss and gain, below and above target).

## Qualitative palettes

- Use clearly different hues with similar lightness and saturation, so that no category shouts unless you mean it to.
- Keep the number small. Past about six to eight colours, readers cannot match marks to a legend reliably, and small marks make it worse. Two or three is often best for an explanatory chart.
- When there are too many categories for colour: label directly, use small multiples, highlight a few and grey the rest, or group minor ones into a clearly defined "Other". Do not fold an important category into "Other" just to fit the palette.
- Fix the mapping from category to colour in code (a dictionary), so that filtering or re-sorting never reshuffles colours.

A safe starting set is the Okabe-Ito palette, designed to stay distinct for common colour-vision deficiencies:

```
#0072B2 blue        #E69F00 orange     #009E73 green      #CC79A7 pink
#56B4E9 sky blue    #D55E00 vermilion  #F0E442 yellow     #000000 black
```

Yellow is weak on a white background, so keep it for fills, not thin lines or text.

## Sequential palettes

- Lightness must change steadily in one direction. That is what makes "more" look like more. On a light background, darker usually means more.
- One hue (light blue to dark blue) or a designed multi-hue ramp (viridis, cividis, ColorBrewer YlGnBu) both work.
- Do not use rainbow or "jet" maps for numeric data. Their lightness goes up and down, which creates bands and edges that are not in the data and makes mid values (bright yellow) look most important (Borland and Taylor, 2007).
- Decide whether colour is continuous or in classes. For classes, state the break points. Equal-width classes and equal-count classes tell different stories.
- A ramp that starts near white is fine for filled cells and bad for points or lines on a white background, because the low end disappears.

Examples that pass the checker:

```
Blues (5):    #eff3ff #bdd7e7 #6baed6 #3182bd #08519c
Viridis (5):  #440154 #3b528b #21918c #5ec962 #fde725
```

## Diverging palettes

- Name the centre before choosing colours: zero change, a target, an average, a neutral answer. Say it in the legend.
- The centre should be the quietest colour (light grey or off-white). Each arm should get steadily darker toward its end, and the two ends should be about equally strong.
- Use symmetric limits around the centre (for example −20 to +20) when equal distances on either side should look equally strong, even if the data is lopsided.
- Missing must not look like the neutral centre. Give missing its own treatment.
- Prefer pairs such as blue and red, blue and orange, or brown and teal. Avoid red against green.

Examples:

```
RdBu (5):  #ca0020 #f4a582 #f7f7f7 #92c5de #0571b0
BrBG (5):  #a6611a #dfc27d #f5f5f5 #80cdc1 #018571
```

For survey scales, the two arms show negative and positive answers. That shows direction. It does not claim the answers are equally spaced.

## Emphasis: grey plus one accent

For an explanatory chart with one main point, the most effective scheme is usually:

- context series in a mid grey,
- the focus in one saturated colour,
- a direct label on the focus.

Keep the role stable. A series that is the accent colour on one chart and grey on the next looks as if something about it changed.

## Accessibility

Roughly 1 in 12 men and 1 in 200 women have some colour-vision deficiency, most often trouble separating red from green. Design so the chart still works for them and in greyscale.

- Do not use red against green as the only signal for bad and good, loss and gain.
- Pairs that often fail: red and green, green and brown, blue and purple, light green and yellow, blue and grey. Lightness differences rescue many pairs, so vary lightness as well as hue.
- Add a second cue for anything essential: direct labels, marker shapes, dash patterns, position, or a sign (+ and −).
- Check small marks and thin lines, not just big swatches. Colours that differ as large blocks can merge as 1-pixel lines.
- Non-text marks need enough contrast with the background to be seen. WCAG 2.1 asks for at least 3:1 for graphical objects and 4.5:1 for normal text.
- Run `scripts/check_palette.py` on custom palettes. It simulates three types of colour-vision deficiency and greyscale and reports pairs that become too similar.

## Legends and colour bars

- Numeric colour needs a colour bar with units, end values and the centre if there is one.
- Classed colour needs a key showing the class boundaries.
- Categorical colour is best labelled directly on the chart. If a legend is needed, list entries in the same order as they appear in the chart.
- When small multiples are meant to be compared, they must share one colour scale. A given shade must stand for the same value in every panel. If scales differ, say so on each panel.
- Colour shows pattern, not exact values. If exact values matter, add labels or use position.

## Consistency across charts

- One category, one colour, in every chart, panel and filter state of the same piece of work.
- Keep stack order and legend order fixed.
- If colour switches meaning between charts (category in one, intensity in the next), use visibly different palettes and a new key, so the reader does not carry the old meaning over.

## Context, screen and print

- The same colour code looks different depending on its neighbours and background. Judge the palette on the finished chart, not as isolated swatches.
- Avoid gradient or patterned backgrounds behind data.
- Screens emit light (RGB) and print reflects it (CMYK). Bright saturated screen colours often print duller. If the chart will be printed or projected, test it that way.
- HSL and HSV are convenient ways to pick colours, but equal numeric steps in them are not equal steps to the eye. Two colours with the same HSL lightness (pure yellow and pure blue) look very different in brightness. Build ramps with a tested palette or check them with the script, which uses a perceptual colour space.

## Associations and tone

- Colours carry meanings that depend on domain and culture. Red is loss in some financial contexts and gain in others. Always label direction with words or signs.
- Strong red feels urgent. Use that weight only when the evidence justifies alarm.
- Natural colours (blue for water, green for vegetation) help recognition when they fit. Do not force them when they would break the palette rules above.

## Palette checklist

- [ ] The job of colour is stated: identity, order, direction or emphasis.
- [ ] The palette family matches the variable.
- [ ] A numeric ramp changes lightness steadily. No rainbow.
- [ ] The number of category colours is small enough for the mark size and audience.
- [ ] Each category keeps its colour across views and filters.
- [ ] Numeric scales show units, range and any centre.
- [ ] Missing, zero and neutral look different from each other.
- [ ] The meaning survives colour-vision deficiency and greyscale through a second cue.
- [ ] Every data colour is visible against the final background at the real mark size.
- [ ] The tone fits the evidence.
