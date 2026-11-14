# Global Air Quality & Urban Health Analysis

An exploratory data analysis and interactive dashboard project focused on comparing air-quality indicators across cities, countries, and continents.

The repository currently includes a Jupyter notebook, a Streamlit application, a CSV dataset, and Python dependencies.

## Project components

- **Jupyter notebook:** `DV_Final_Project_Aarushi_Singh (1).ipynb`
- **Streamlit dashboard:** `Global Air Quality & Urban Health Analysis Streamlit.py`
- **Dataset:** `global air pollution dataset.csv`
- **Dependencies:** `requirements.txt`

## Dashboard capabilities

The current Streamlit script is designed to provide:
- High-level AQI and geographic summary metrics
- Country and continent filters
- Best/worst city comparisons
- Country-level AQI rankings
- Distribution charts, including box, histogram, and violin plots
- A geographic hierarchy view and a raw-data explorer

## Tech stack

Python, pandas, NumPy, Streamlit, Plotly, and Jupyter.

## Run locally

```bash
git clone https://github.com/singhaarvi728/Global-Air-Quality-Urban-Health-Analysis.git
cd Global-Air-Quality-Urban-Health-Analysis
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows PowerShell:
# .venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run "Global Air Quality & Urban Health Analysis Streamlit.py"
```

## Data and interpretation

Use the CSV committed in this repository as the intended data source and inspect its schema before interpreting dashboard outputs. The current app contains a generated sample-data fallback if its expected input filename cannot be read. Sample data is synthetic and must not be presented as measured observations or used to make real-world public-health claims.

## Reproducibility checklist

- Confirm the dataset filename and columns match the app's expected schema.
- Run the notebook from top to bottom.
- Rerun the dashboard against the committed CSV.
- Verify all charts and filters against the actual data before reporting findings.

## Project status

The files currently available in this GitHub repository are preserved as the starting point for further cleanup and validation. This documentation does not imply that the original files from a previous laptop have been recovered byte-for-byte.
