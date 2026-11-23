# app.py
# Global Alcohol Consumption Explorer - a Streamlit dashboard.
# Run with: streamlit run app.py

import pandas as pd
import plotly.express as px
import streamlit as st

import data_loader


@st.cache_data
def get_total():
    return data_loader.load_total()


@st.cache_data
def get_beverages():
    return data_loader.load_beverages()


total_df = get_total()
beverage_df = get_beverages()
total_countries = data_loader.only_countries(total_df)
beverage_countries = data_loader.only_countries(beverage_df)


st.set_page_config(page_title="Global Alcohol Consumption Explorer",
                   page_icon="🍷", layout="wide")

st.title("🍷 Global Alcohol Consumption Explorer")
st.write(
    "Explore how alcohol consumption varies across countries, how it has "
    "changed over time, and which drink dominates where. "
    "All values are in **litres of pure alcohol per person per year**."
)

with st.expander("ℹ️ Important note about the data (please read)"):
    st.markdown(
        """
**Please read before interpreting the charts - these are separate measures.**

- **Total alcohol is a separate indicator** from beer, wine and spirits. The
  total and the beverage figures come from different data series.
- **Do not add beer + wine + spirits together to equal total alcohol.** They
  have different coverage and definitions, so the three beverages should not be
  summed to reproduce the total.
- **Different time spans:** the total dataset covers **2000-2020**, while the
  beer, wine and spirits datasets cover **1960-2022**.
- The beverage figures are *recorded* consumption only (they exclude home-made
  or unrecorded alcohol).
- **Some zero values may reflect reporting limitations:** a value of 0 can mean
  "reported as zero" or "not reported", and the two cannot be told apart.
"""
    )

section = st.sidebar.radio(
    "Choose a section:",
    ["Overview", "Country Explorer", "Beverage Analysis"]
)


def show_overview():
    st.header("Overview")
    st.write("Total alcohol consumption across the world for a chosen year.")

    year = st.slider("Select a year",
                     int(total_df["Year"].min()),
                     int(total_df["Year"].max()),
                     int(total_df["Year"].max()))

    countries_year = total_countries[total_countries["Year"] == year]

    # World average comes from the official "World" row, not a country average.
    world_row = data_loader.only_aggregates(total_df)
    world_row = world_row[(world_row["Entity"] == "World") &
                          (world_row["Year"] == year)]
    world_value = world_row["total"].iloc[0] if not world_row.empty else None

    highest = countries_year.loc[countries_year["total"].idxmax()]
    lowest = countries_year.loc[countries_year["total"].idxmin()]

    col1, col2, col3 = st.columns(3)
    if world_value is not None:
        col1.metric("World average", f"{world_value:.1f} L")
    col2.metric(f"Highest: {highest['Entity']}", f"{highest['total']:.1f} L")
    col3.metric(f"Lowest: {lowest['Entity']}", f"{lowest['total']:.1f} L")

    st.subheader(f"World map - total consumption in {year}")
    map_fig = px.choropleth(
        countries_year, locations="Code", color="total", hover_name="Entity",
        color_continuous_scale="Reds", labels={"total": "Litres"},
    )
    map_fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(map_fig, width="stretch")

    st.subheader(f"Top 10 countries in {year}")
    top10 = countries_year.sort_values("total", ascending=False).head(10)
    bar_fig = px.bar(
        top10.sort_values("total"),
        x="total", y="Entity", orientation="h",
        labels={"total": "Litres of pure alcohol", "Entity": ""},
    )
    st.plotly_chart(bar_fig, width="stretch")


def show_country_explorer():
    st.header("Country Explorer")
    st.write("Look at one country's history and its drink breakdown.")

    country_list = sorted(total_countries["Entity"].unique())
    default_index = country_list.index("France") if "France" in country_list else 0
    country = st.selectbox("Select a country", country_list, index=default_index)

    st.subheader(f"Total alcohol consumption in {country} (2000-2020)")
    country_total = total_countries[total_countries["Entity"] == country]
    trend_fig = px.line(
        country_total, x="Year", y="total", markers=True,
        labels={"total": "Litres of pure alcohol"},
    )
    st.plotly_chart(trend_fig, width="stretch")

    country_bev = beverage_countries[beverage_countries["Entity"] == country]
    if country_bev.empty:
        st.info(f"No beer/wine/spirits data is available for {country}.")
        return

    st.subheader(f"Beer, wine and spirits in {country} (1960-2022)")
    long_bev = country_bev.melt(
        id_vars="Year", value_vars=["beer", "wine", "spirits"],
        var_name="Drink", value_name="Litres",
    )
    multi_fig = px.line(long_bev, x="Year", y="Litres", color="Drink", markers=False)
    st.plotly_chart(multi_fig, width="stretch")

    latest_year = int(country_bev["Year"].max())
    latest = country_bev[country_bev["Year"] == latest_year]
    mix = pd.DataFrame({
        "Drink": ["beer", "wine", "spirits"],
        "Litres": [latest["beer"].iloc[0], latest["wine"].iloc[0],
                   latest["spirits"].iloc[0]],
    })
    st.subheader(f"Drink mix in {country} ({latest_year})")
    mix_fig = px.bar(mix, x="Drink", y="Litres", color="Drink",
                     labels={"Litres": "Litres of pure alcohol"})
    st.plotly_chart(mix_fig, width="stretch")


def show_beverage_analysis():
    st.header("Beverage Analysis")
    st.write("Compare beer, wine and spirits across countries and over time.")

    latest_year = int(beverage_countries["Year"].max())
    latest = beverage_countries[beverage_countries["Year"] == latest_year]

    st.subheader(f"Top 10 countries by drink ({latest_year})")
    drink = st.selectbox("Choose a drink", ["beer", "wine", "spirits"])
    top10 = latest.sort_values(drink, ascending=False).head(10)
    rank_fig = px.bar(
        top10.sort_values(drink),
        x=drink, y="Entity", orientation="h",
        labels={drink: "Litres of pure alcohol", "Entity": ""},
    )
    st.plotly_chart(rank_fig, width="stretch")

    st.subheader(f"Which drink dominates? (number of countries, {latest_year})")
    dominant = latest[["beer", "wine", "spirits"]].idxmax(axis=1)
    counts = dominant.value_counts().reset_index()
    counts.columns = ["Drink", "Number of countries"]
    dom_fig = px.bar(counts, x="Drink", y="Number of countries", color="Drink")
    st.plotly_chart(dom_fig, width="stretch")

    st.subheader("Global average by drink over time (1960-2022)")
    yearly_avg = (beverage_countries
                  .groupby("Year")[["beer", "wine", "spirits"]]
                  .mean()
                  .reset_index())
    long_avg = yearly_avg.melt(
        id_vars="Year", value_vars=["beer", "wine", "spirits"],
        var_name="Drink", value_name="Litres",
    )
    trend_fig = px.line(long_avg, x="Year", y="Litres", color="Drink")
    st.plotly_chart(trend_fig, width="stretch")
    st.caption(
        "Note: this averages the countries that reported in each year. Fewer "
        "countries reported in the early years, so early values are less "
        "representative than recent ones."
    )


if section == "Overview":
    show_overview()
elif section == "Country Explorer":
    show_country_explorer()
else:
    show_beverage_analysis()

st.sidebar.caption("Data: Our World in Data (WHO). University capstone project.")
