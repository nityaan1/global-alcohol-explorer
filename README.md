# Global Alcohol Consumption Explorer

A simple interactive dashboard that explores global alcohol consumption using
open data from **Our World in Data** (based on WHO figures). Built as an
IE University group capstone project.

All values are measured in **litres of pure alcohol per person per year**.

## Questions this project answers

1. **How does alcohol consumption differ across countries?**
2. **How has alcohol consumption changed over time?**
3. **Which beverage type – beer, wine or spirits – dominates in each country?**

## The dashboard

The app has three sections (chosen from the sidebar):

1. **Overview** – pick a year and see a world map of total consumption, the top
   10 countries, and headline statistics (world average, highest, lowest).
2. **Country Explorer** – pick a country and see its total-consumption trend
   (2000–2020), its beer/wine/spirits history (1960–2022), and its most recent
   drink mix.
3. **Beverage Analysis** – rank countries by a chosen drink, see which drink
   dominates in the most countries, and view the global trend of each drink
   over time.

## Project structure

```
global-alcohol-explorer/
├── data/                 # the 4 raw CSV files (never modified)
├── data_loader.py        # loads and cleans the data (Pandas)
├── app.py                # the Streamlit dashboard
├── requirements.txt      # the libraries needed
└── README.md             # this file
```

## The data

Four CSV files in `data/`, all with the columns `Entity, Code, Year, <value>`:

| File | Indicator | Years |
|------|-----------|-------|
| `total-alcohol-consumption-per-capita-litres-of-pure-alcohol.csv` | total alcohol | 2000–2020 |
| `beer-consumption-per-person.csv` | beer | 1960–2022 |
| `wine-consumption-per-capita.csv` | wine | 1960–2022 |
| `spirits-consumption-per-person.csv` | spirits | 1960–2022 |

### Cleaning steps (in `data_loader.py`)

- Rename each long value column to a short name (`total`, `beer`, `wine`, `spirits`).
- Merge the three beverage files into one table on `Entity, Code, Year`.
- Separate real **countries** (3-letter ISO code, e.g. `FRA`) from regional
  **aggregates** (longer codes such as `OWID_WRL` for World or `WB_EAP` for a
  region). Aggregates are used only for the "world average" figure; rankings
  and maps use countries only.

The raw CSV files themselves are **never modified**.

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

## How to run

1. Install the libraries (ideally inside a virtual environment or a PyCharm
   project interpreter):

   ```
   pip install -r requirements.txt
   ```

2. From the project folder, start the app:

   ```
   streamlit run app.py
   ```

3. The dashboard opens in your web browser.

### Running in PyCharm

Open the project folder in PyCharm, set a Python interpreter that has the
libraries from `requirements.txt` installed, then either run the command above
in the terminal or add a run configuration with `streamlit run app.py`.

## Data source

Our World in Data – Alcohol Consumption (based on WHO data).
<https://ourworldindata.org/alcohol-consumption>
