# data_loader.py
# Loads and cleans the four alcohol-consumption CSV files.
# Data: Our World in Data (WHO). Values are litres of pure alcohol per person per year.

import os
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

FILES = {
    "total":   "total-alcohol-consumption-per-capita-litres-of-pure-alcohol.csv",
    "beer":    "beer-consumption-per-person.csv",
    "wine":    "wine-consumption-per-capita.csv",
    "spirits": "spirits-consumption-per-person.csv",
}


def _load_one(key):
    # Load one file and rename its long value column to a short name.
    path = os.path.join(DATA_DIR, FILES[key])
    df = pd.read_csv(path)
    df = df.rename(columns={df.columns[3]: key})
    return df


def load_total():
    return _load_one("total")


def load_beverages():
    # Merge beer, wine and spirits into one table.
    beer = _load_one("beer")
    wine = _load_one("wine")
    spirits = _load_one("spirits")
    merged = beer.merge(wine, on=["Entity", "Code", "Year"])
    merged = merged.merge(spirits, on=["Entity", "Code", "Year"])
    return merged


def only_countries(df):
    # Real countries have a 3-letter ISO code; aggregates (World, regions) are longer.
    return df[df["Code"].str.len() == 3].copy()


def only_aggregates(df):
    return df[df["Code"].str.len() != 3].copy()
