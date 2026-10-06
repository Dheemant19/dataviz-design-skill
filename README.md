# dataviz-design

An agent skill that teaches AI coding agents to design charts, not just draw them.

Ask an AI agent for a chart and you get working code in seconds. Whether the chart is any good is a different question. Agents tend to accept whatever the plotting library does by default. That means a new colour for every bar, a legend with nine entries, an axis that starts wherever the data happens to start, and a title that repeats the column names. The code runs and the numbers are correct, but the reader still has to work out what the chart is trying to say. Sometimes the result is worse than unclear. A cut axis or a bubble sized by its radius can make a small difference look like a large one.

What is missing is design judgment. Someone who is good at charts asks a few questions before writing any code. Who is reading this, and what do they need to see? What does one row of the data stand for? Which comparison matters most, and is it shown in the way people read most accurately? Does every colour mean something? Would a reasonable reader come away with the right impression?

`dataviz-design` gives an agent that way of working. It takes well-established research on perception and statistical graphics and turns it into instructions an agent can follow:

- a seven-step workflow that goes from the question to the finished chart
- a chart chooser that starts from what the reader needs to do
- fifteen defaults that prevent the most common mistakes, each with the reason behind it
- reference files for each chart family, colour, data preparation and honest presentation
- sixteen worked redesigns, each with numbers you can check
- review checklists to run before a chart is delivered
- a palette checker script for contrast and colour-blind safety

It also stays out of the way. The agent reads a short entry file when a charting task comes up, and opens a reference file only when the task calls for it.

The skill is about design decisions, so it works with any plotting tool: matplotlib, seaborn, plotly, ggplot2, D3, Vega-Lite, Excel, Tableau, Power BI.

## Install

```bash
npx skills add Dheemant19/dataviz-design-skill
```

This uses the [skills CLI](https://github.com/vercel-labs/skills), which installs into Claude Code, Cursor, Codex and other agents that support the [Agent Skills](https://agentskills.io) format.

To install by hand, copy the `skills/dataviz-design` folder into your agent's skills directory (for Claude Code, `.claude/skills/` in a project or `~/.claude/skills/` for all projects).

## What it changes

Each pair below shows one rule from the skill. The data is invented, and the figures are drawn by [`examples/make_examples.py`](examples/make_examples.py).

### Bars start at zero

A bar's length is its value. Cutting the axis turns a 3-point gap into a bar 2.5 times as tall.

![Two bar charts of the same satisfaction scores. The first uses an axis from 80 to 86 and exaggerates the gap. The second starts at zero and labels the values.](docs/images/01-zero-baseline.png)

### Grey for context, one colour for the point

Seven colours and a legend make the reader do the work. One accent colour and direct labels make the chart say something.

![Two line charts of revenue for seven regions. The first uses seven colours and a legend. The second draws six regions in grey and highlights one region with a direct label.](docs/images/02-highlight-one-series.png)

### Sort it, and use position instead of angle

People compare lengths on a shared scale far more accurately than angles. If the reader has to rank, do the ranking for them.

![A pie chart with eight slices and a legend, next to the same data as sorted horizontal bars with the third bar highlighted.](docs/images/03-sorted-bars-not-pie.png)

### The palette follows the data

Numeric data needs a ramp whose lightness changes steadily. A rainbow scale creates bright bands that look like boundaries in the data.

![The same heatmap of orders by hour and weekday drawn with a rainbow colour scale and with a single blue ramp.](docs/images/04-sequential-not-rainbow.png)

### Show the distribution, not one number

Two teams with the same "80% favourable" can be very different. A diverging stacked bar keeps the answer scale in order and shows the whole picture.

![A bar chart of percent favourable for three teams, next to diverging stacked bars showing all five answer levels for each team.](docs/images/05-show-the-distribution.png)

### Size means area

Map a value to circle radius and a city 8 times as large is drawn 64 times as big. Radius must follow the square root of the value.

![Four circles for city populations scaled by radius, next to the same four scaled by area.](docs/images/06-bubble-area.png)

## What is inside

```
skills/dataviz-design/
├── SKILL.md                         workflow, chart chooser, 15 core defaults
├── references/
│   ├── data-and-preparation.md      scale types, joins, missing data, denominators, maps
│   ├── encoding-and-perception.md   channels, accuracy ranking, attention, grouping
│   ├── colour.md                    palette families, accessibility, legends
│   ├── comparison.md                bars, lines, axes, log scales, smoothing, small multiples
│   ├── composition.md               pies, stacked bars and areas, treemaps, waterfalls, funnels
│   ├── relationships.md             scatterplots, trend lines, uncertainty, bubbles, heatmaps
│   ├── distributions.md             histograms, box plots, violins, density, ECDF
│   ├── explanation-and-honesty.md   titles, annotation, emphasis, misleading patterns
│   ├── worked-redesigns.md          16 before and after cases with numbers
│   ├── review-checklist.md          design brief, recipes, final review
│   ├── library-notes.md             defaults that matter in matplotlib, seaborn, pandas,
│   │                                plotly, ggplot2, Vega-Lite and D3
│   └── sources.md                   the research each rule comes from
└── scripts/
    └── check_palette.py             palette checker, Python standard library only
```

The agent always sees only the skill's name and description. It loads `SKILL.md` (about 200 lines) when a charting task comes up, and opens a reference file only when the task needs it. A request for a stacked bar chart pulls in `composition.md` and nothing else.

## Try it

After installing, ask your agent things like:

- "Plot monthly revenue for our nine regions from sales.csv."
- "Which chart should I use to show how survey answers differ between three teams?"
- "Here is my chart code. Is anything about this misleading?"
- "Pick colours for a heatmap of change versus last year."
- "My boss wants a pie chart of these 12 categories. Make it work."

## Palette checker

`check_palette.py` checks a palette before it goes into a chart. It tests contrast against the background, whether colours stay distinct under three simulated types of colour-vision deficiency, and whether a sequential or diverging ramp is properly ordered.

```console
$ python skills/dataviz-design/scripts/check_palette.py "#FF0000" "#00A000"
Palette type: qualitative    Background: #FFFFFF

Contrast against background (3:1 or more recommended for lines and points)
  #FF0000   4.00:1
  #00A000   3.48:1

Closest pair: #FF0000 and #00A000, distance 0.041 under deuteranopia
  (below 0.07 is hard to tell apart, below 0.05 is nearly identical)

FAIL [distinct] #FF0000 and #00A000 are nearly identical under deuteranopia (distance 0.041).
NOTE [greyscale] 1 pair(s) have almost the same lightness and will merge in greyscale print
(#FF0000/#00A000). Balanced lightness is normal for category colours. Add labels, shapes or
dash styles if the chart may be printed without colour.

Result: FAIL
```

Use `--type sequential` or `--type diverging` for ramps, `--background` for dark themes, and `--json` for machine-readable output.

## Where the rules come from

The skill summarises established findings from statistics, perception research and visualisation design, including work by Bertin, Cleveland and McGill, Stevens, Tufte, Tukey, Kosslyn, Mackinlay, Brewer and Munzner. Every source is listed in [`sources.md`](skills/dataviz-design/references/sources.md), so any rule can be traced and cited.

The checker's thresholds are heuristics, and so are several of the design rules. The skill says which rules are arithmetic, which are strong defaults and which are judgment calls.

## Contributing

Issues and pull requests are welcome. Useful contributions include corrections with a source, notes on library defaults that have changed, and new worked redesigns.

To redraw the README figures:

```bash
pip install matplotlib numpy
python examples/make_examples.py
```

Test prompts for evaluating changes to the skill are in [`evals/evals.json`](evals/evals.json).

## Licence

MIT. See [LICENSE](LICENSE).
