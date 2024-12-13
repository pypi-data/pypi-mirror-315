# NST_Scrape

NST_Scrape is a simple Python package for scraping National Hockey League information and stats from Natural Stat Trick.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install NST_Scrape.

```bash
pip install NST_scrape
```

## Usage
Currently, three functions are available in the package:

```python
# The "season" argument refers to a given NHL season as far back as 2007-2008.  Format season as "20212022" if you want to scrape NHL data from the 2021-2022 season, for example.

SkaterScrape(season)
BioScrape(season)
TeamScrape(season)
```

Note that these are not particularly comprehensive, as they were developed exclusively to generate public data visualizations for WeakSide Breakout Analysis, which can be viewed at https://docs.google.com/spreadsheets/d/1kYaFsDgVlWbzOO2T67jW9Tu1Gu9Lw974flU1dkQBMO4/.

