# Encoding and perception

How to map variables to visual properties, and why some mappings are read more accurately than others.

## Contents

- Marks and channels
- Match the channel to the scale type
- Channel accuracy
- Size and area are underestimated
- Small differences
- Many variables
- Attention: making one thing stand out
- Grouping: how layout creates meaning
- Gridlines, decoration and the background
- Illusions to design around

## Marks and channels

A mark is the thing you draw: a point, a line, a bar, an area. A channel is a property of the mark that you vary to carry data: position, length, size, shape, lightness, hue, angle, texture (Bertin, 1983, and Munzner, 2014).

For each variable in the chart, be able to state: its scale type, the channel it uses, where the reader finds the key (axis, legend, label), and why they can read it. If you cannot state these, the mapping is not designed yet.

| Mark | Stands for | Ask |
|---|---|---|
| Point | A single record, or a summary of many | Does a dot stand for one customer, one order, or the mean of a group? |
| Line | A sequence, a route, or a model fit | Is there a real order that makes it valid to join the points? |
| Bar or area | An amount or an extent | Is the value carried by length, height or area? |
| Link | A relationship between two entities | Is the link real, directed, weighted? |
| Enclosure | Membership of a group | Is the boundary a category, a statistical region or just layout? |

## Match the channel to the scale type

Two tests, from Mackinlay (1986):

- **Expressiveness.** The channel shows the relationships the data has and no others. A colour ramp on unordered categories invents an order. Random hues on an ordered variable hide one.
- **Effectiveness.** Among channels that are valid, choose the one the reader decodes most accurately for the comparison that matters most.

| Channel | Good for | Limits |
|---|---|---|
| Position | Everything: amounts, order, categories | Strongest only on a shared, aligned scale |
| Length | Ratio amounts | Needs a common zero baseline |
| Area, size | A rough third quantity | Underestimated. Poor for close comparisons |
| Lightness | Ordered and numeric values | A few distinguishable steps. Affected by background |
| Hue | Categories | No natural order. Limited number of distinct hues |
| Shape | Categories, as a backup to hue | Few shapes stay distinct at small sizes |
| Angle, slope | Trend direction | Small differences are hard to judge |
| Texture, pattern | A few categories in print | Visual noise |

A parameter named `hue` or `color` in a library is not the hue channel. Passing a numeric column usually produces a lightness ramp. Check the rendered image, not the parameter name.

## Channel accuracy

Experiments on graphical perception (Cleveland and McGill, 1984, replicated by Heer and Bostock, 2010) rank how accurately people compare quantities:

1. Position on a common scale (bars or dots on one axis)
2. Position on identical but separate scales (small multiples with matching axes)
3. Length (segments without a common baseline, such as middle parts of a stack)
4. Angle and slope (pie slices, line steepness)
5. Area (bubbles, treemap cells)
6. Volume, colour lightness, colour saturation

Practical consequences:

- If two values must be compared precisely, they should share an axis and a baseline.
- A pie and a bar chart can show the same shares. The bar makes close shares easier to tell apart because it uses position instead of angle.
- Middle segments of a stacked bar are length without a common baseline, which is why they are hard to compare.
- Colour intensity is for seeing patterns across many cells, not for reading values.

This ranking is for quantities. For categories, position and hue work best, then shape.

## Size and area are underestimated

Perceived magnitude grows more slowly than physical magnitude for area and volume. Stevens (1957) modelled this as a power law, perceived = k × actual^n, with n close to 1 for length and around 0.7 for area. So a circle with four times the area tends to look about 2.6 times as big (4^0.7).

What to do:

- Prefer position or length when the size comparison matters.
- When you do use area (bubbles, map symbols), scale area exactly in proportion to the value, add a size legend, and label the important values. See `relationships.md` for the arithmetic.
- Do not secretly enlarge big symbols to compensate. Cartographers have used such corrections (Flannery, 1971), but then the drawn area no longer matches the stated value. If you ever do it, say so in the legend and never mix corrected and uncorrected symbols.

## Small differences

The smallest change people notice is roughly proportional to the size of the thing being judged (Weber's law). A 4-unit difference is obvious between short bars and invisible between very long ones. Two close shades are harder to tell apart at the dark and light extremes and against a similar background.

- When small differences are the point, show them with position on a suitable range (dot plot, line) or plot the difference itself, or print the numbers.
- Do not rely on subtle size or shade steps.
- Equal steps in RGB or HSL numbers are not equal steps to the eye. Use a tested palette.
- Very pale marks vanish on white and very dark marks vanish on black. Keep the lightest data colour clearly darker than a white background.

## Many variables

A scatterplot can carry x, y, size, colour, shape and a label. That is a limit, not a goal. Each added channel costs attention and can interfere with the others: big bubbles hide colours, small points hide shapes, labels cover marks.

- Decide the main task and give it x and y.
- Add at most one or two more channels.
- For more, split into small multiples (same chart repeated per group with the same axes) or separate linked views.
- Do not label every point. Label the few that matter.
- Animation over time makes readers remember earlier frames. Pair it with a static view of selected moments.

Using two channels for the same variable (colour and shape both meaning "group") is useful redundancy. Using colour for one variable and shape for another makes the reader search for combinations, which is slow. If readers must often find "the blue triangles", facet by one variable and colour by the other.

## Attention: making one thing stand out

Some differences are spotted almost instantly, before the reader searches: a different hue, a darker or lighter mark, a larger size, a different orientation, motion (Healey and Enns, 2012). A target defined by a combination of two features (green and round among green squares and blue circles) is not spotted this way and needs a slow search (Treisman and Gelade, 1980).

Use this for explanatory charts:

- Draw context in muted grey. Draw the focus in one accent colour or a heavier line.
- Add a short label next to the focus that says why it matters.
- Stand-out is relative. If everything is bold or bright, nothing leads.
- Emphasise with colour, weight, label or position. Never by changing geometry (a wider bar, an exploded slice, a cropped axis), because that changes the value the reader sees.
- Use motion rarely. It distracts and excludes some readers.

Working memory holds only a few unrelated items at once, often put at around four chunks (Cowan, 2001). This does not limit how many marks a chart can have, since a thousand points can read as one cloud. It does limit how many legend entries a reader can hold while scanning. So:

- Label directly, next to the marks.
- Keep the same colours for the same categories across charts.
- Put things to be compared side by side on the same scale.

## Grouping: how layout creates meaning

Readers group marks automatically, before reading any legend. These Gestalt tendencies (Wertheimer, 1923) are tools, and they also create false groupings when used carelessly.

| Principle | Readers assume | Use it to | Watch for |
|---|---|---|---|
| Proximity | Things close together belong together | Space grouped bars tighter within a group than between groups. Put labels next to marks | Clusters in a scatter that come from the axis scale or overplotting |
| Similarity | Same colour or shape means same kind | One colour per series across all panels | Twelve colours for twelve months of one series invents twelve categories |
| Connection | Joined things are one unit | Lines for a real series or for the same entity at two times | A line across unrelated categories implies a path that does not exist |
| Enclosure | Things inside a boundary are a set | Panels, shaded time bands, treemap nesting | An unexplained shaded region. A band marking an event does not show the event caused anything |
| Continuity | The eye follows smooth paths | Tracing lines through crossings | A line drawn across missing data, or a decorative curve between sparse points, implies values nobody measured |
| Symmetry | Mirrored shapes are one object | Violins, population pyramids | Readers may think the two sides of a plain violin are two groups |
| Figure and ground | One thing is foreground, the rest background | Data darker and stronger than grid and frame | Pale data on white. Decoration louder than data |

When cues disagree, connection and enclosure usually beat proximity and similarity. Make sure the strongest visual grouping is the one the data supports.

For grouped bars, the inner grouping decides what is easy to compare. Departments within each year makes within-year comparison easy. Years within each department makes each department's trend easy. Choose by the question.

## Gridlines, decoration and the background

- Remove ink that does not help reading: heavy frames, background fills, shadows, gradients, fake depth, and legends made redundant by direct labels (Tufte, 1983).
- Do not remove ink that carries meaning: axes, units, a zero line, a target line, uncertainty bands, annotations. Minimal is not the same as clear.
- Keep gridlines few and faint, well behind the data. Low-opacity lines (around 20% is a common starting point, from Bartram and Stone, 2011) usually work. Check on the actual background.
- A meaningful reference line (zero, target, threshold) can be stronger than ordinary gridlines, and should be labelled.
- Pictures and icons on bars can hide the bar ends or add an unintended size cue. Keep them off the data area.

## Illusions to design around

Vision interprets. Identical things can look different in different surroundings:

- A circle looks smaller among large circles and larger among small ones. Do not expect precise area comparison among very different neighbours.
- The same grey looks lighter on a dark surround and darker on a light one. A colour in a heatmap cell is judged against its neighbours, so colour is unreliable for exact values.
- Arrowheads, perspective and decorative ends change how long a line looks. Keep bar ends plain.
- Busy radial or patterned backgrounds make straight lines look bent.
- A bar partly hidden behind another in a 3D chart can look bigger than it is, because the eye reads it as further away.

The fix is always the same: plain backgrounds, shared baselines, no fake depth, and position for anything that must be compared exactly.
