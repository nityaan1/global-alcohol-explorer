# Global Alcohol Consumption Explorer

A single notebook that explores global alcohol consumption using open data from
**Our World in Data** (based on WHO figures). Built as an IE University group
capstone project.

The project is available in **two forms** that share the same data and analysis:

- **An interactive Streamlit dashboard** (`app.py`) — the main application,
  which you can run locally or open as a live web app.
- **A Colab / Jupyter notebook** (`Global_Alcohol_Consumption_Explorer.ipynb`) —
  the whole project in one file, reproducing the same analysis and charts with
  step-by-step explanations.

All values are measured in **litres of pure alcohol per person per year**.

## Team

Group members:

- Nityaan
- Oscar
- Nico

All members contributed to the overall solution and understand the data, the
code, and the main findings.

## Questions this project answers

1. **How does alcohol consumption differ across countries?**
2. **How has alcohol consumption changed over time?**
3. **Which beverage type – beer, wine or spirits – dominates in each country?**

## What it does

The dashboard (and the notebook) are organised into three sections:

1. **Overview** – a world map of total consumption for a chosen year, the top 10
   countries, and headline statistics (world average, highest, lowest).
2. **Country Explorer** – one country's total-consumption trend (2000–2020), its
   beer/wine/spirits history (1960–2022), and its most recent drink mix.
3. **Beverage Analysis** – rank countries by a chosen drink, see which drink
   dominates in the most countries, and view the global trend of each drink.

In a few places you can change a simple variable (the year, the country, the
drink) and re-run that cell to explore different views.

## Key findings

A few headline results taken directly from the data (all figures are litres of
pure alcohol per person per year):

- **Consumption varies widely across countries.** In 2020 the highest total
  consumption was **Romania (about 16.8 L)** and the lowest was **Kuwait
  (about 0.0 L)**, against a world average of roughly **4.9 L**.
- **Beer is the most common leading drink.** In 2022, beer was the
  most-consumed beverage type in **103** countries, spirits in **64**, and wine
  in **20**.
- **Different drinks lead in different places.** In 2022 the top country for
  each drink was **Czechia (beer)**, **Portugal (wine)** and **Saint Lucia
  (spirits)**.

## Project structure

```
global-alcohol-explorer/
├── data/                                       # the 4 raw CSV files (never modified)
├── app.py                                      # the Streamlit dashboard (main application)
├── data_loader.py                              # loads and cleans the data (used by app.py)
├── requirements.txt                            # libraries needed to run the dashboard
├── Global_Alcohol_Consumption_Explorer.ipynb   # the same project as a Colab notebook
├── .gitignore
└── README.md                                   # this file
```

## The data

Four CSV files in `data/`, all with the columns `Entity, Code, Year, <value>`:

| File | Indicator | Years |
|------|-----------|-------|
| `total-alcohol-consumption-per-capita-litres-of-pure-alcohol.csv` | total alcohol | 2000–2020 |
| `beer-consumption-per-person.csv` | beer | 1960–2022 |
| `wine-consumption-per-capita.csv` | wine | 1960–2022 |
| `spirits-consumption-per-person.csv` | spirits | 1960–2022 |

### Cleaning steps

- **Data-quality check:** we inspected all four files for missing values and
  duplicate rows. The data was already complete — **no missing values and no
  duplicate Entity–Year rows** — so no rows had to be dropped or filled in.
- Rename each long value column to a short name (`total`, `beer`, `wine`, `spirits`).
- Merge the three beverage files into one table on `Entity, Code, Year`.
- Separate real **countries** (3-letter ISO code, e.g. `FRA`) from regional
  **aggregates** (longer codes such as `OWID_WRL` for World or `WB_EAP` for a
  region). Aggregates are used only for the "world average" figure; rankings
  and maps use countries only.

The raw CSV files themselves are **never modified**.

## Tools and technology

- **Python** – the programming language used for the whole project.
- **Pandas** – loading, cleaning, merging and analysing the data.
- **Streamlit** – builds the interactive dashboard (the main application).
- **Plotly** – the interactive charts (world map, bar charts, line charts).
- **Jupyter / Google Colab** – runs the notebook version.

The exact versions for the dashboard are pinned in `requirements.txt`. Google
Colab already includes Pandas and Plotly for the notebook.

## Why Pandas (and not PySpark)

The whole dataset is under 1 MB (about 40,000 rows in total). This fits easily
in memory, and Pandas processes it instantly. PySpark is designed for very
large, distributed datasets, so using it here would add complexity without any
benefit. **Pandas is the right tool for data of this size.**

## Important note on method

The **total** indicator and the **beer / wine / spirits** indicators come from
different data series with different year ranges and coverage. Therefore:

- **beer + wine + spirits does not equal the total** – we treat them as
  separate measures and never add them together.
- Beverage figures are *recorded* consumption only (they exclude unrecorded or
  home-made alcohol).
- A value of `0` means "reported as zero" and cannot be distinguished from
  "not reported".

## Conclusion

The project set out to answer three questions, and the notebook answers all
three:

1. **Differences across countries** – consumption is very uneven (for example,
   Romania near 16.8 L versus Kuwait near 0 L in 2020), which the world map and
   top-10 rankings make easy to see.
2. **Change over time** – the trend charts show how each country's total and
   beverage consumption has moved since 1960 (beverages) and 2000 (total).
3. **Which drink dominates** – beer leads in the largest number of countries,
   followed by spirits and then wine.

The main thing we learned is that careful data processing plus a few
well-chosen charts can turn four raw CSV files into a clear, interactive story
about global drinking patterns. The main limitation is that the total and
beverage indicators are separate measures with different coverage, so they must
be read side by side rather than added together.

## Future improvements

If we continued the project, we could:

- Let the user compare two or more countries on the same chart.
- Add more recent years as updated data becomes available.
- Add a button to download the filtered data as a CSV.
- Bring in population or income data to explore possible relationships.

## How to run

### The dashboard (Streamlit app)

**Live version:** _add your Streamlit Community Cloud URL here once deployed._

**Run it locally (PyCharm or terminal):**

1. Install the libraries: `pip install -r requirements.txt`.
2. From the project folder, start it **from the terminal** (not the plain Run
   button): `streamlit run app.py`.
3. It opens in your browser at <http://localhost:8501>.

### The notebook (Google Colab)

1. Open it in Colab:
   <https://colab.research.google.com/github/nityaan1/global-alcohol-explorer/blob/main/Global_Alcohol_Consumption_Explorer.ipynb>
2. Choose **Runtime ▸ Run all**. The notebook automatically downloads the data
   from GitHub and shows every chart inline.

## Data source

Our World in Data – Alcohol Consumption (based on WHO data).
<https://ourworldindata.org/alcohol-consumption>
