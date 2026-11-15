# Global Air Quality & Urban Health Analysis

An exploratory data analysis and interactive Streamlit dashboard for examining air-quality indicators across countries and cities.

## Repository contents

- `DV_Final_Project_Aarushi_Singh (1).ipynb` — exploratory notebook
- `Global Air Quality & Urban Health Analysis Streamlit.py` — interactive dashboard
- `global air pollution dataset.csv` — committed dataset
- `requirements.txt` — Python dependencies

## Dataset schema

The committed CSV includes:

- Location fields: `Country`, `City`
- Overall index: `AQI Value`, `AQI Category`
- Pollutant-specific indicators: CO, Ozone, NO2 and PM2.5 AQI values and categories

The dataset does **not** contain a `Continent` field or health-outcome measurements. The dashboard therefore compares countries and cities using the fields that are actually present; it does not invent continent labels or make causal public-health claims.

## Run locally

Use Python 3.10 or newer.

```bash
git clone https://github.com/singhaarvi728/Global-Air-Quality-Urban-Health-Analysis.git
cd Global-Air-Quality-Urban-Health-Analysis
python -m venv .venv

# macOS/Linux
source .venv/bin/activate

# Windows PowerShell
# .venv\\Scripts\\Activate.ps1

pip install -r requirements.txt
streamlit run "Global Air Quality & Urban Health Analysis Streamlit.py"
```

Keep `global air pollution dataset.csv` in the same directory as the Streamlit file.

## Data handling and limitations

The dashboard reads the committed CSV using its actual filename and column names. If the file is missing or required columns are absent, it displays an error and stops instead of silently substituting synthetic sample records.

This repository contains a static dataset snapshot, not a live air-quality feed. Dashboard summaries describe the supplied data only; they should not be interpreted as personal exposure measurements, causal evidence, or demonstrated health outcomes.

## Reproducibility checklist

- Confirm the CSV is present beside the Streamlit script.
- Install dependencies from `requirements.txt`.
- Run the notebook from top to bottom and inspect its outputs.
- Run the dashboard and compare its filters, metrics and charts with the CSV.
- Record the dataset's provenance and observation date before making time-based or public-health interpretations.

## Project status

The repository contains the starting notebook, dataset and dashboard. Further validation of the notebook's analysis and dataset provenance remains part of the project.
