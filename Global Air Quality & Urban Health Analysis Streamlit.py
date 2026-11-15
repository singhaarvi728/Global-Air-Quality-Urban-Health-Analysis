from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Global Air Quality Explorer",
    page_icon="🌍",
    layout="wide",
)

DATA_PATH = Path(__file__).resolve().parent / "global air pollution dataset.csv"
REQUIRED_COLUMNS = {"Country", "City", "AQI Value", "AQI Category"}
POLLUTANT_COLUMNS = {
    "CO AQI Value": "Carbon monoxide",
    "Ozone AQI Value": "Ozone",
    "NO2 AQI Value": "Nitrogen dioxide",
    "PM2.5 AQI Value": "PM2.5",
}


@st.cache_data(show_spinner=False)
def load_data(csv_path: str, _file_mtime: float) -> tuple[pd.DataFrame, int]:
    """Load and validate the committed dataset; never invent replacement records."""
    data = pd.read_csv(csv_path, encoding="utf-8-sig")
    data.columns = [str(column).strip() for column in data.columns]

    missing = REQUIRED_COLUMNS.difference(data.columns)
    if missing:
        raise ValueError(
            "The CSV is missing required columns: " + ", ".join(sorted(missing))
        )

    for column in ("Country", "City", "AQI Category"):
        data[column] = data[column].astype("string").str.strip()

    numeric_columns = ["AQI Value", *POLLUTANT_COLUMNS.keys()]
    for column in numeric_columns:
        if column in data.columns:
            data[column] = pd.to_numeric(data[column], errors="coerce")

    invalid_rows = (
        data["Country"].isna()
        | data["City"].isna()
        | data["AQI Value"].isna()
        | (data["Country"] == "")
        | (data["City"] == "")
    )
    rows_removed = int(invalid_rows.sum())
    data = data.loc[~invalid_rows].copy()

    if data.empty:
        raise ValueError("No usable rows remain after validating the required fields.")

    data["AQI Category"] = data["AQI Category"].fillna("Unknown")
    return data.reset_index(drop=True), rows_removed


st.title("🌍 Global Air Quality Explorer")
st.write(
    "Explore the committed air-quality dataset by country, city, AQI category "
    "and pollutant-specific AQI indicators."
)

if not DATA_PATH.is_file():
    st.error(
        "Dataset not found. Place 'global air pollution dataset.csv' next to "
        "this Streamlit file, then reload the app."
    )
    st.stop()

try:
    df, rows_removed = load_data(str(DATA_PATH), DATA_PATH.stat().st_mtime)
except Exception as error:
    st.error(f"Dataset could not be loaded: {error}")
    st.stop()

st.caption(
    f"Source: repository CSV snapshot · {len(df):,} usable records · "
    f"{rows_removed:,} rows excluded for missing location or AQI values · "
    "This is a static dataset, not a live air-quality feed."
)

st.sidebar.header("Filters")
countries = sorted(df["Country"].dropna().astype(str).unique().tolist())
categories = sorted(df["AQI Category"].dropna().astype(str).unique().tolist())

selected_countries = st.sidebar.multiselect(
    "Countries",
    options=countries,
    default=countries,
)
selected_categories = st.sidebar.multiselect(
    "AQI categories",
    options=categories,
    default=categories,
)

filtered = df[
    df["Country"].isin(selected_countries)
    & df["AQI Category"].isin(selected_categories)
].copy()

if filtered.empty:
    st.warning("No records match the selected filters. Adjust the sidebar filters.")
    st.stop()

metric_1, metric_2, metric_3 = st.columns(3)
metric_1.metric("Records in view", f"{len(filtered):,}")
metric_2.metric("Countries in view", f"{filtered['Country'].nunique():,}")
metric_3.metric("Mean AQI value", f"{filtered['AQI Value'].mean():.1f}")

st.divider()

st.subheader("City comparisons")
city_stats = (
    filtered.groupby(["Country", "City"], as_index=False)["AQI Value"]
    .mean()
)
city_stats["Location"] = (
    city_stats["City"].astype(str) + ", " + city_stats["Country"].astype(str)
)

left, right = st.columns(2)
with left:
    worst = city_stats.nlargest(10, "AQI Value").sort_values("AQI Value")
    worst_chart = px.bar(
        worst,
        x="AQI Value",
        y="Location",
        orientation="h",
        title="10 highest city AQI averages",
        labels={"AQI Value": "Mean AQI value", "Location": "City"},
    )
    st.plotly_chart(worst_chart, use_container_width=True)

with right:
    best = city_stats.nsmallest(10, "AQI Value").sort_values(
        "AQI Value", ascending=False
    )
    best_chart = px.bar(
        best,
        x="AQI Value",
        y="Location",
        orientation="h",
        title="10 lowest city AQI averages",
        labels={"AQI Value": "Mean AQI value", "Location": "City"},
    )
    st.plotly_chart(best_chart, use_container_width=True)

st.subheader("Country-level comparison")
country_stats = (
    filtered.groupby("Country", as_index=False)["AQI Value"]
    .mean()
    .nlargest(15, "AQI Value")
    .sort_values("AQI Value")
)
country_chart = px.bar(
    country_stats,
    x="AQI Value",
    y="Country",
    orientation="h",
    title="15 highest country-level mean AQI values",
    labels={"AQI Value": "Mean AQI value"},
)
st.plotly_chart(country_chart, use_container_width=True)

st.subheader("AQI category distribution")
category_stats = (
    filtered["AQI Category"]
    .value_counts()
    .rename_axis("AQI Category")
    .reset_index(name="Records")
)
category_chart = px.bar(
    category_stats,
    x="AQI Category",
    y="Records",
    title="Records by AQI category",
)
st.plotly_chart(category_chart, use_container_width=True)

st.subheader("AQI value distribution")
histogram = px.histogram(
    filtered,
    x="AQI Value",
    color="AQI Category",
    nbins=35,
    title="Distribution of AQI values",
)
st.plotly_chart(histogram, use_container_width=True)

available_pollutants = [
    column for column in POLLUTANT_COLUMNS if column in filtered.columns
]
if available_pollutants:
    st.subheader("Pollutant-specific AQI indicators")
    pollutant_data = filtered[available_pollutants].rename(
        columns=POLLUTANT_COLUMNS
    ).melt(var_name="Pollutant", value_name="AQI sub-index")
    pollutant_data = pollutant_data.dropna(subset=["AQI sub-index"])
    if not pollutant_data.empty:
        pollutant_chart = px.box(
            pollutant_data,
            x="Pollutant",
            y="AQI sub-index",
            color="Pollutant",
            title="Distribution of pollutant-specific AQI values",
        )
        st.plotly_chart(pollutant_chart, use_container_width=True)

with st.expander("Explore the filtered records"):
    st.dataframe(filtered, use_container_width=True, hide_index=True)

st.caption(
    "Interpretation note: this dashboard summarises the fields in the supplied "
    "dataset. It does not measure personal exposure, establish causation, or "
    "demonstrate health outcomes."
)
