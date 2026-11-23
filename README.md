# Global Alcohol Consumption Explorer

An IE University group capstone project by **Nityaan, Oscar and Nico**.

It explores global alcohol consumption using open data from Our World in Data
(based on WHO figures). All values are in litres of pure alcohol per person per
year.

**Live dashboard:** <https://global-alcohol-explorer-fqf95zk6dncjzmffgmmygp.streamlit.app/>

The project comes in two forms that share the same data and analysis:

- a Streamlit dashboard (`app.py`), and
- a Colab / Jupyter notebook (`Global_Alcohol_Consumption_Explorer.ipynb`) that
  runs the same analysis with explanations.

## Questions

1. How does alcohol consumption differ across countries?
2. How has it changed over time?
3. Which drink – beer, wine or spirits – dominates in each country?

## What it does

Three sections:

1. **Overview** – world map, top 10 countries and summary stats for a chosen year.
2. **Country Explorer** – one country's total trend, its beer/wine/spirits
   history, and its latest drink mix.
3. **Beverage Analysis** – rankings by drink, which drink dominates the most
   countries, and the global trend of each drink over time.

## Key findings

- In 2020 the highest total consumption was Romania (~16.8 L) and the lowest was
  Kuwait (~0.0 L), with a world average around 4.9 L.
- In 2022, beer was the most-consumed drink in 103 countries, spirits in 64 and
  wine in 20.
- The 2022 leader for each drink was Czechia (beer), Portugal (wine) and Saint
  Lucia (spirits).

## Data

Four CSV files in `data/`, each with columns `Entity, Code, Year, <value>`:

| File | Indicator | Years |
|---|---|---|
| total-alcohol-consumption-per-capita-litres-of-pure-alcohol.csv | total | 2000–2020 |
| beer-consumption-per-person.csv | beer | 1960–2022 |
| wine-consumption-per-capita.csv | wine | 1960–2022 |
| spirits-consumption-per-person.csv | spirits | 1960–2022 |

Source: Our World in Data – <https://ourworldindata.org/alcohol-consumption>

Cleaning: we checked for missing values and duplicates (there were none), renamed
the long value columns, merged the three beverage files, and split real countries
(3-letter ISO code) from regional aggregates such as World.

## Note on method

The total indicator and the beer/wine/spirits indicators come from different data
series, so beer + wine + spirits does not equal the total and we never add them
together. Beverage figures are recorded consumption only, and a 0 can mean
"reported as zero" or "not reported".

## Tools

Python, pandas (data), Plotly (charts), Streamlit (dashboard) and Jupyter/Colab
(notebook). The dashboard's versions are pinned in `requirements.txt`. We used
pandas rather than PySpark because the data is small (under 1 MB).

## How to run

**Dashboard:** `pip install -r requirements.txt`, then `streamlit run app.py`
(run it from the terminal, not the plain Run button). It opens at
<http://localhost:8501>. The live version is linked at the top.

**Notebook:** open it in Colab
(<https://colab.research.google.com/github/nityaan1/global-alcohol-explorer/blob/main/Global_Alcohol_Consumption_Explorer.ipynb>)
and choose Runtime ▸ Run all.

## Limitations and possible improvements

The datasets stop at 2020 (total) and 2022 (beverages), and the global trend
chart averages whichever countries reported each year. In future we could let
users compare several countries at once, add newer data, or bring in population
or income data.

## Project structure

```
global-alcohol-explorer/
├── data/                                       # the 4 raw CSV files
├── app.py                                      # the Streamlit dashboard
├── data_loader.py                              # loads and cleans the data
├── requirements.txt                            # libraries for the dashboard
├── Global_Alcohol_Consumption_Explorer.ipynb   # the project as a notebook
├── .gitignore
└── README.md
```
