# Worked redesigns

Short before and after cases. All data is invented for illustration. Use them as patterns for reasoning, not as templates: the point is why each change was made.

## Contents

1. Bars with a cut axis
2. A 3D pie with close shares
3. Twelve colours for one series
4. Too many lines
5. One group that goes the other way
6. Survey answers reduced to one number
7. Nested numbers stacked as a whole
8. An ambiguous percentage
9. Value mapped to bubble radius
10. Two metrics on two axes
11. Flow and stock
12. Slowing growth read as decline
13. Same quartiles, different shapes
14. Finding the third largest
15. Compare within years, or follow each over time?
16. A treemap with two measures
17. A title the chart does not prove
18. A chart buried in its own notes

## 1. Bars with a cut axis

**Before.** Satisfaction scores of 82 and 85 for two products, as bars on an axis running from 80 to 86. The second bar is 2.5 times the height of the first.

**Problem.** Bar length is read as the value. The real difference is 3 points, under 4%.

**After.** Two options, depending on the message.

- If the message is "both are high and close": bars from zero, with values labelled.
- If the 3-point difference really matters (it is larger than the survey's margin of error): a dot plot on an axis from 75 to 90, with the interval for each score, and a title that says "3 points higher".

**Principle.** Bars need zero. Position marks (dots, lines) can use a narrower range, as long as the range is clear and the claim matches the size of the difference.

## 2. A 3D pie with close shares

**Before.** Three subscription plans with 31%, 34% and 35% of customers, in a tilted 3D pie with the 31% slice at the front. The front slice shows its thick edge and looks the biggest.

**Problem.** Angle is a weak channel, the shares are close, and perspective inflates the front slice. Printing the percentages on it does not undo the first impression.

**After.** Three horizontal bars sorted from largest to smallest, values at the bar ends, with the plan of interest in an accent colour and the others grey. If "parts of a whole" must be visible, a single flat 100% bar with three labelled segments.

**Principle.** Use position for close values. Emphasise with colour, never with geometry.

## 3. Twelve colours for one series

**Before.** Monthly rainfall for one year as twelve bars, each a different colour, with a twelve-entry legend.

**Problem.** Colour here carries no information that the x-axis does not already carry. Similar-looking things are read as a group, so twelve colours suggest twelve unrelated categories, and the legend adds lookup work.

**After.** One colour for all bars, month names on the axis, no legend. If the story is the wettest month, give that bar the accent colour and a value label.

To compare two years, draw two lines over the same month axis, one colour per year, each labelled at its end. That uses colour for the one thing that needs it.

**Principle.** A visual difference should mean a data difference.

## 4. Too many lines

**Before.** Monthly revenue for nine regions, as nine coloured lines with a legend at the side.

**Problem.** Nine hues are hard to tell apart, the lines cross, and every reading needs a trip to the legend.

**After.** Choose by the question.

- "How is the North doing against the others?" Eight grey lines and one accent line, labelled directly.
- "How is each region doing?" A 3 by 3 grid of small multiples with a shared y-axis, each panel showing its region in the accent colour over the other eight in faint grey.

**Principle.** Replace colour lookup with position and highlighting.

## 5. One group that goes the other way

**Data.** Average hours to resolve a support ticket, before and after a process change.

| Group | Before | After | Change |
|---|---:|---:|---:|
| Small team, basic plan | 42 | 37 | −5 |
| Small team, premium plan | 30 | 24 | −6 |
| Large team, basic plan | 55 | 41 | −14 |
| Large team, premium plan | 26 | 39 | +13 |

**Goal.** Make the reader see at once that large premium teams are the only group that got slower.

**Before.** Eight grouped bars in four colours. The exception is there, and nothing points to it.

**After.** A slope chart. "Before" and "After" on x, hours on y, one line per group. Three lines in grey, the large premium line in an accent colour. Each line labelled at its right end with the group name and the change. One annotation: "Only group that slowed: +13 hours".

**Principle.** Shared position for the values, a connecting line for the pairing, one colour difference for the exception. If the lines cross too much, four small panels with the same y-axis do the same job.

**Wording.** These are averages for groups. "Large premium teams took longer after the change" is supported. "The change made them slower" needs more than this table.

## 6. Survey answers reduced to one number

**Data.** "The onboarding was clear", share of answers by team.

| Answer | Team X | Team Y | Team Z |
|---|---:|---:|---:|
| Strongly disagree | 3% | 12% | 5% |
| Disagree | 7% | 4% | 25% |
| Neutral | 10% | 4% | 42% |
| Agree | 50% | 18% | 22% |
| Strongly agree | 30% | 62% | 6% |

**Before.** A bar chart of "% favourable": X 80, Y 80, Z 28.

**Problem.** X and Y look identical. They are not. Y has twice the "strongly agree" share and four times the "strongly disagree" share. Y is split, X is broadly content. One number hid the shape.

**After.** One 100% horizontal bar per team, with answers in order from strongly disagree to strongly agree and a diverging palette: two shades of one hue for disagreement, grey for neutral, two shades of another hue for agreement. Line the bars up on the middle of the neutral segment so that the balance is visible. Label the segments and print the number of respondents per team.

If one answer level must be compared precisely across teams, add a small dot plot for that level.

**Principle.** The answer scale is ordinal, so keep its order and show the whole distribution. Palette type follows the variable.

## 7. Nested numbers stacked as a whole

**Data.** In one month: 10,000 visitors, 1,200 sign-ups, 300 purchases.

**Before.** A stacked bar with three segments totalling 11,500.

**Problem.** Every purchaser also signed up, and every sign-up also visited. The segments overlap, so the stack counts people two or three times and shows a total that does not exist.

**After.** Two valid options.

- Funnel as plain bars: three horizontal bars of 10,000, 1,200 and 300, in process order, each labelled with its conversion from the previous stage (12% and 25%).
- A true part-to-whole: split the 10,000 into disjoint groups. Visited only: 8,800. Signed up, no purchase: 900. Purchased: 300.

**Principle.** Stack only parts that do not overlap and that add up to the whole.

## 8. An ambiguous percentage

**Data.** A table of subscription plan by customer tenure band (under 1 year, 1 to 3 years, over 3 years), with one percentage per cell.

**Problem.** "50% for Premium and under 1 year" has two readings. Half of Premium customers joined in the last year (shares within a plan). Or half of the newest customers chose Premium (shares within a tenure band). The chart and every sentence about it depend on which.

**After.** Find out which total each percentage was divided by. Then:

- Shares within each plan: one 100% bar per plan, split by tenure band, with a sequential palette for the ordered bands and n per plan.
- Shares within each tenure band: one 100% bar per band, split by plan, with distinct hues for the plans.

Put the denominator in the title: "How long each plan's customers have been with us".

**Principle.** A percentage is not defined until its denominator is.

## 9. Value mapped to bubble radius

**Before.** Cities on a scatterplot, with population mapped straight to circle radius. A city of 4 million gets four times the radius of a city of 1 million, and so sixteen times the area.

**Problem.** Readers judge area. The larger city looks four times more dominant than it is.

**After.** Radius proportional to the square root of population, so values 1 and 4 give radii 1 and 2 and areas 1 and 4. Add a size legend with two or three reference circles. Label the cities that matter.

**Principle.** Size means area.

## 10. Two metrics on two axes

**Before.** Advertising spend (left axis, thousands) and sign-ups (right axis, count) as two lines on one chart, scaled so that they overlap closely.

**Problem.** The overlap comes from the choice of the two axis ranges. Other ranges would make the lines diverge. The reader sees "they move together" as a fact about the data.

**After.** Depending on the question.

- "Do they move together?" A scatterplot of sign-ups against spend, one point per week.
- "How did each change?" Two panels, one above the other, sharing the time axis.
- "Which grew faster?" Both indexed to 100 in the first week, on one axis.

**Principle.** Avoid dual axes. The relationship should come from the data, not from scaling.

## 11. Flow and stock

**Data.** Tickets opened and tickets closed each week.

**Before.** A single line of "net tickets" (opened minus closed).

**Problem.** A net of +20 every week looks flat and harmless. Meanwhile the pile of open tickets grows by 20 a week.

**After.** Two aligned panels. Top: opened and closed as two labelled lines, so the gap is visible. Bottom: the backlog, where backlog this week = backlog last week + opened − closed. Starting from 40 open tickets, a week with 120 opened and 100 closed ends at 60.

If something relevant happened (two staff left in week 9), mark it with a labelled vertical line on both panels.

**Principle.** A rate and the total it feeds are different quantities. Show both when both matter. An event marker gives timing, not proof of cause.

## 12. Slowing growth read as decline

**Data.** Users at year end: 100k, 110k, 118k, 124k. Growth: 10%, 7%, 5%.

**Before.** A line chart titled "User growth" plotting 10, 7, 5. It slopes down.

**Problem.** Many readers will conclude that users are falling.

**After.** Two aligned panels. Top: users (level), rising. Bottom: year-on-year growth in percent, falling. Title: "Users still growing, but more slowly each year". Axis labels name each measure.

**Principle.** Name the measure. Pair level and rate when they point in different directions.

## 13. Same quartiles, different shapes

**Before.** Box plots of delivery times for two warehouses. Medians, boxes and whiskers nearly match. Conclusion drawn: "the warehouses perform the same".

**Problem.** One warehouse has a single peak around the median. The other has two peaks, a fast one and a slow one, with few deliveries in between. Probably two different routes or shifts. Quartiles cannot show this.

**After.** Violins with the quartiles marked inside, or small-multiple histograms with shared bins. Check that the two peaks survive a change of bandwidth or bin width before reporting them. Print n for each warehouse.

**Principle.** Summaries compress. When shape might matter, show the shape.

## 14. Finding the third largest

**Before.** Eight categories in a pie chart in alphabetical order. The reader is asked which is third largest.

**Problem.** The reader has to compare eight angles, remember the top few and rank them mentally.

**After.** Horizontal bars sorted from largest to smallest on a common scale. The third bar is the answer. If two categories tie within the precision of the data, say so and do not force a strict rank.

**Principle.** Do the sorting for the reader. Do not sort like this when the categories have a natural order such as time.

## 15. Compare within years, or follow each over time?

**Data.** Profit in millions for three divisions.

| Year | Division A | Division B | Division C |
|---|---:|---:|---:|
| 2019 | 6.0 | 4.1 | 1.2 |
| 2020 | 5.6 | 4.3 | 1.5 |
| 2021 | 5.1 | 4.2 | 2.4 |
| 2022 | 4.3 | 4.4 | 3.6 |
| 2023 | 3.8 | 4.5 | 5.2 |

**If the question is "who led each year?"** Grouped bars with year as the outer group and divisions as three fixed colours. Zero baseline, equal widths.

**If the question is "how did each division change?"** Three lines over the years, labelled at the right end. A falls steadily, B is flat, C rises and overtakes both in 2023.

**If the question is the company total.** Sum the three (they are disjoint) and plot the total as its own line: 11.3, 11.4, 11.7, 12.3, 13.5. The total never goes into the same stack as the divisions.

**Framing to avoid.** Showing only B from 2021 to 2023 on an axis from 4.1 to 4.6 makes a 0.3 rise look steep and hides both A's decline and C's surge. Showing A on a log axis shrinks its fall.

**Principle.** The same table supports several correct charts. The question picks the chart, and the frame must not hide what a fair reader would want to know.

## 16. A treemap with two measures

**Before.** A treemap of companies grouped by sector. Area is market value. Colour runs from red to green for the day's price change. No legend.

**Problem.** Two different measures are on two channels with no explanation. The biggest rectangle and the most intense colour are usually different companies. Red against green is unreadable for many people.

**After.** Keep the treemap if the goal is an overview of where the value sits and which areas moved. Add a legend that says "area = market value" and a colour bar centred on 0% using a blue and orange diverging palette, with signed percentages on the large cells. For precise ranking, add a sorted bar chart of the top movers.

**Principle.** One measure per channel, each explained. Area gives an impression, bars give a ranking.

## 17. A title the chart does not prove

**Before.** Monthly active users for ten apps over five years, one line each, with the smaller apps in grey and one app highlighted. Title: "Pinecone grew faster than any other app". The largest app has ten times the users of the rest, so the other nine lines sit in a band at the bottom of the axis.

**Problem.** The title claims something about growth for every app. The chart shows levels, and nine of the ten lines are unreadable. A reader cannot check "faster than any other" and has to take it on trust.

**After.** Choose by the claim.

- If growth is the whole story: index every app to 100 in the first month and plot the ten lines, with Pinecone highlighted. Now the steepest line is the fastest growth, and the small apps are as readable as the large one.
- If size matters too: keep the level chart on the left and add a sorted bar panel on the right showing the five-year change for every app, with Pinecone in the same accent colour.

Then apply the cover test: hide the title and check that the chart alone says Pinecone grew fastest.

**Principle.** The evidence must match the type of claim. A superlative needs every item visible in the measure it refers to.

## 18. A chart buried in its own notes

**Before.** A clean bar chart of energy use by building, with a two-line subtitle, three callouts, and a four-line footnote covering metering changes, a missing month, the conversion factor and the source.

**Problem.** Every note is true, but the reader now has to read a paragraph to read a chart. The one caveat that changes the reading (one building was only metered for nine months) is lost among the others.

**After.** Keep on the chart only what changes the reading: a one-line subtitle with measure, unit and period, a single note "Building C: nine months of data", and the source. Mark Building C's bar with a lighter fill and the same note. Move the metering history and the conversion factor into the message that goes with the chart.

**Principle.** Text has a budget. Put the caveat that changes the conclusion on the chart, and everything else in the reply.
