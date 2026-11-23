"""
data_loader.py
--------------
Loads and cleans the four alcohol-consumption CSV files for the
Global Alcohol Consumption Explorer.

We keep ALL data logic in this one small file so that app.py can focus on
the dashboard. The raw CSV files in data/ are never modified.

Data source: Our World in Data (WHO). Every value is measured in
litres of pure alcohol per person per year.
"""

import os
import pandas as pd

# Folder that holds the raw CSV files (next to this script, inside "data/").
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

# The file name for each indicator. The key is the short name we will use.
FILES = {
    "total":   "total-alcohol-consumption-per-capita-litres-of-pure-alcohol.csv",
    "beer":    "beer-consumption-per-person.csv",
    "wine":    "wine-consumption-per-capita.csv",
    "spirits": "spirits-consumption-per-person.csv",
}


def _load_one(key):
    """
    Load one CSV file and give its value column a short, tidy name.

    Input:  key - one of "total", "beer", "wine", "spirits"
    Output: a DataFrame with columns [Entity, Code, Year, <key>]

    Each raw file has the layout: Entity, Code, Year, <very long value name>.
    We rename that 4th column to the short key (e.g. "beer") so the rest of
    the project is easy to read.
    """
    path = os.path.join(DATA_DIR, FILES[key])
    df = pd.read_csv(path)
    value_column = df.columns[3]            # the 4th column holds the numbers
    df = df.rename(columns={value_column: key})
    return df


def load_total():
    """
    Load the TOTAL alcohol consumption dataset (years 2000-2020).

    Output: DataFrame [Entity, Code, Year, total]
    """
    return _load_one("total")


def load_beverages():
    """
    Load beer, wine and spirits and merge them into ONE table.

    Output: DataFrame [Entity, Code, Year, beer, wine, spirits]
            (years 1960-2022)

    The three beverage files share the same countries and years, so an inner
    merge on Entity + Code + Year lines them up row by row.
    """
    beer = _load_one("beer")
    wine = _load_one("wine")
    spirits = _load_one("spirits")

    merged = beer.merge(wine, on=["Entity", "Code", "Year"])
    merged = merged.merge(spirits, on=["Entity", "Code", "Year"])
    return merged


def only_countries(df):
    """
    Keep real countries and drop regional aggregates.

    Rule: Our World in Data gives real countries a 3-letter ISO code
    (e.g. "FRA"), while aggregates use longer codes (e.g. "OWID_WRL" for
    World, "WB_EAP" for a World Bank region). So a code length of 3 means
    "this is a country".

    Input:  any of our DataFrames (must contain a "Code" column)
    Output: the same DataFrame with aggregates removed
    """
    return df[df["Code"].str.len() == 3].copy()


def only_aggregates(df):
    """
    Keep only the regional aggregates (World, regions, income groups).

    This is the opposite of only_countries() and is used for the "World
    average" reference line in the Overview section.
    """
    return df[df["Code"].str.len() != 3].copy()
