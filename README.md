# COVID-19 Data Visualization Using Python 📊

A Python data exploration and visualization project based on the supplied report. It demonstrates cleaning tabular COVID-19 statistics and generating plots that help explore reported cases, deaths, and recoveries over time.

## Features
- Load a CSV dataset with Pandas
- Normalize column names and validate required fields
- Plot daily cases/deaths when time-series columns are available
- Plot top regions by confirmed cases when regional data is available
- Save charts to the `outputs/` directory

## Setup
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/visualize_covid.py --input data/covid_data.csv
```

## Dataset
Place a dataset you have permission to use in `data/covid_data.csv`. The script accepts common columns such as `date`, `country/region`, `confirmed`, `deaths`, and `recovered`; see `data/README.md`. The included sample is synthetic and is not real epidemiological data.

## Disclaimer
Visualizations are descriptive and depend on the quality and definitions of the chosen dataset. They are not medical advice.
