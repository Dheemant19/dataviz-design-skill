# Sources

The rules in this skill summarise established findings from statistics, perception research and visualisation design. This file lists the primary sources, grouped by topic, so that a rule can be traced and cited.

## Data and measurement

- Stevens, S. S. (1946). On the theory of scales of measurement. *Science*, 103(2684), 677-680. Nominal, ordinal, interval and ratio scales.
- Tukey, J. W. (1977). *Exploratory Data Analysis*. Addison-Wesley. Looking at data before modelling it. The box plot.
- Wickham, H. (2014). Tidy data. *Journal of Statistical Software*, 59(10). Long and wide table shapes.
- Anscombe, F. J. (1973). Graphs in statistical analysis. *The American Statistician*, 27(1), 17-21. Four datasets with the same summary statistics.
- Matejka, J., and Fitzmaurice, G. (2017). Same stats, different graphs. *Proceedings of CHI 2017*. The Datasaurus collection.

## Encoding and graphical perception

- Bertin, J. (1983). *Semiology of Graphics* (W. J. Berg, Trans.). University of Wisconsin Press. Original work published 1967. Marks and visual variables.
- Cleveland, W. S., and McGill, R. (1984). Graphical perception: Theory, experimentation, and application to the development of graphical methods. *Journal of the American Statistical Association*, 79(387), 531-554. The accuracy ranking of position, length, angle and area.
- Mackinlay, J. (1986). Automating the design of graphical presentations of relational information. *ACM Transactions on Graphics*, 5(2), 110-141. Expressiveness and effectiveness.
- Heer, J., and Bostock, M. (2010). Crowdsourcing graphical perception. *Proceedings of CHI 2010*. Replication of the Cleveland and McGill ranking.
- Munzner, T. (2014). *Visualization Analysis and Design*. CRC Press. Marks, channels and task-based design.
- Stevens, S. S. (1957). On the psychophysical law. *Psychological Review*, 64(3), 153-181. The power law for perceived magnitude.
- Fechner, G. T. (1860). *Elemente der Psychophysik*. Breitkopf und Härtel. Weber's law and just-noticeable differences.
- Flannery, J. J. (1971). The relative effectiveness of some common graduated point symbols in the presentation of quantitative data. *Canadian Cartographer*, 8(2), 96-109. Perceptual scaling of map symbols.

## Attention, memory and grouping

- Treisman, A. M., and Gelade, G. (1980). A feature-integration theory of attention. *Cognitive Psychology*, 12(1), 97-136. Single-feature versus conjunction search.
- Healey, C. G., and Enns, J. T. (2012). Attention and visual memory in visualization and computer graphics. *IEEE Transactions on Visualization and Computer Graphics*, 18(7), 1170-1188. Review of preattentive features.
- Miller, G. A. (1956). The magical number seven, plus or minus two. *Psychological Review*, 63(2), 81-97.
- Cowan, N. (2001). The magical number 4 in short-term memory. *Behavioral and Brain Sciences*, 24(1), 87-114.
- Wertheimer, M. (1923). Untersuchungen zur Lehre von der Gestalt II. *Psychologische Forschung*, 4, 301-350. The grouping principles.

## Design principles

- Tufte, E. R. (1983). *The Visual Display of Quantitative Information*. Graphics Press. Data-ink, graphical integrity and small multiples.
- Kosslyn, S. M. (2006). *Graph Design for the Eye and Mind*. Oxford University Press. The eight principles used in `explanation-and-honesty.md`.
- Bartram, L., and Stone, M. C. (2011). Whisper, don't scream: Grids and transparency. *IEEE Transactions on Visualization and Computer Graphics*, 17(10), 1444-1458. Gridline strength.
- Cleveland, W. S., McGill, M. E., and McGill, R. (1988). The shape parameter of a two-variable graph. *Journal of the American Statistical Association*, 83(402), 289-300. Aspect ratio and banking to 45 degrees.
- Abela, A. (2006). *Chart Suggestions: A Thought-Starter*. Extreme Presentation. The comparison, composition, relationship and distribution families.
- Few, S. (2006). *Bullet Graph Design Specification*. Perceptual Edge.

## Colour

- Harrower, M., and Brewer, C. A. (2003). ColorBrewer.org: An online tool for selecting colour schemes for maps. *The Cartographic Journal*, 40(1), 27-37. Qualitative, sequential and diverging schemes.
- Borland, D., and Taylor, R. M. (2007). Rainbow color map (still) considered harmful. *IEEE Computer Graphics and Applications*, 27(2), 14-17.
- Okabe, M., and Ito, K. (2008). *Color Universal Design: How to make figures and presentations that are friendly to colorblind people*. https://jfly.uni-koeln.de/color/
- Machado, G. M., Oliveira, M. M., and Fernandes, L. A. F. (2009). A physiologically-based model for simulation of color vision deficiency. *IEEE Transactions on Visualization and Computer Graphics*, 15(6), 1291-1298. The simulation used in `scripts/check_palette.py`.
- Ottosson, B. (2020). *A perceptual color space for image processing*. https://bottosson.github.io/posts/oklab/ The Oklab space used in `scripts/check_palette.py`.
- World Wide Web Consortium (2018). *Web Content Accessibility Guidelines (WCAG) 2.1*. Success criteria 1.4.3 (contrast) and 1.4.11 (non-text contrast). https://www.w3.org/TR/WCAG21/

## Specific chart forms and methods

- Playfair, W. (1786). *The Commercial and Political Atlas*. London. The first line and bar charts of economic data.
- Cleveland, W. S. (1979). Robust locally weighted regression and smoothing scatterplots. *Journal of the American Statistical Association*, 74(368), 829-836. LOWESS.
- Freedman, D., and Diaconis, P. (1981). On the histogram as a density estimator: L2 theory. *Zeitschrift für Wahrscheinlichkeitstheorie und verwandte Gebiete*, 57, 453-476. A bin-width rule.
- Hintze, J. L., and Nelson, R. D. (1998). Violin plots: A box plot-density trace synergism. *The American Statistician*, 52(2), 181-184.
- Shneiderman, B. (1992). Tree visualization with tree-maps: 2-d space-filling approach. *ACM Transactions on Graphics*, 11(1), 92-99.
- Heiberger, R. M., and Robbins, N. B. (2014). Design of diverging stacked bar charts for Likert scales and other applications. *Journal of Statistical Software*, 57(5).

## Library documentation

Behaviour described in `library-notes.md` comes from the official documentation of each project: pandas, Matplotlib, seaborn, statsmodels, Plotly, ggplot2, Vega-Lite, Altair and D3. Defaults change between versions, so check the documentation for the installed version.
