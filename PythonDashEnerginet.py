import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Values shown in the Power BI dashboard
expected = {
    "wind_mwh": 19.09,
    "wind_share": 47.12,
    "hours": 588,
    "peak_share": 119.45,
}

df = pd.read_csv("EnerginetDash_cleaned_2025.csv", parse_dates=["Date"])
df["Wind_MWh"] = df["OffshoreWind_MWh"] + df["OnshoreWind_MWh"]

wind = df["Wind_MWh"].sum()
consumption = df["GrossConsumptionMWh"].sum()

hourly = df.groupby(["Date", "Hour"])[["Wind_MWh", "GrossConsumptionMWh"]].sum()
hours_wind_exceeds = (hourly["Wind_MWh"] > hourly["GrossConsumptionMWh"]).sum()

daily = df.groupby("Date")[["Wind_MWh", "GrossConsumptionMWh", "NetExchange_MWh"]].sum()
daily["WindShare"] = daily["Wind_MWh"] / daily["GrossConsumptionMWh"]
peak_day = daily["WindShare"].idxmax()

# Pyhon calculated measures
calculated = {
    "wind_mwh": round(wind / 1_000_000, 2),
    "wind_share": round(wind / consumption * 100, 2),
    "hours": int(hours_wind_exceeds),
    "peak_share": round(daily.loc[peak_day, "WindShare"] * 100, 2),
}
 #Comparison
for key in expected:
    status = "OK" if calculated[key] == expected[key] else "MISMATCH"
    print(f"{key}: expected {expected[key]}, calculated {calculated[key]} -> {status}")

assert calculated == expected, "Python results do not match Power BI"
print("All measures match Power BI")

app = Dash(__name__)
app.layout = html.Div([
    html.H2("Wind in the Danish power system 2025"),
    dcc.RadioItems(
        id="area",
        options=["All", "DK1", "DK2"],
        value="All",
        inline=True,
    ),
    dcc.Graph(id="scatter"),
])

@app.callback(
    Output("scatter", "figure"),
    Input("area", "value"),
)
def update_scatter(area):
    d = df if area == "All" else df[df["PriceArea"] == area]

    daily = d.groupby("Date")[["Wind_MWh", "GrossConsumptionMWh", "NetExchange_MWh"]].sum().reset_index()
    daily["WindShare"] = daily["Wind_MWh"] / daily["GrossConsumptionMWh"]

    fig = px.scatter(
        daily, x="WindShare", y="NetExchange_MWh",
        trendline="ols",
        title=f"When it's windy, Denmark exports ({area})",
        labels={"WindShare": "Wind share of consumption", "NetExchange_MWh": "Net import (MWh)"},
    )
    return fig

if __name__ == "__main__":
    app.run(debug=True)