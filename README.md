Small project on Energinet's open electricity data for 2025 (hourly, DK1 and DK2).

**Power BI dashboard**: ETL in Power Query, 12 DAX measures, two report pages
- **Python check + Dash app** (`PythonDashEnerginet.py`): recalculates the key
  Power BI measures in pandas and asserts they match, then serves an interactive
  scatter of daily wind share vs. net exchange, filterable by price area

## Run it
pip install -r requirements.txt
python PythonDashEnerginet.py
Then open http://127.0.0.1:8050

## Data
Energinet, Energi Data Service — Production and Consumption – Settlement, 2025.
Licensed under CC BY 4.0. The CSV here is the cleaned output of my Power Query steps.
