from datetime import datetime, date

import pandas as pd
import plotly.graph_objects as go


def _parse_date(value):
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return datetime.strptime(value, "%Y-%m-%d").date()


def build_figure(data, symbol, chart_type, start_date, end_date):
    if chart_type not in ("line", "bar"):
        raise ValueError("Chart type must be 'line' or 'bar'.")

   
    if isinstance(data, dict):
        for key, value in data.items():
            if "Time Series" in key and isinstance(value, dict):
                data = value
                break

    if not isinstance(data, dict) or not data:
        raise ValueError("No stock data available to display.")

    start = _parse_date(start_date)
    end = _parse_date(end_date)

    if start > end:
        raise ValueError("End date cannot be before start date.")

    records = []
    for timestamp, values in data.items():
        try:
            stock_date = datetime.strptime(timestamp[:10], "%Y-%m-%d").date()
            if start <= stock_date <= end:
                records.append({
                    "Date": timestamp,
                    "Close": float(values["4. close"]),
                })
        except (ValueError, TypeError, KeyError):
            continue

    if not records:
        raise ValueError("No stock data found for the selected date range.")

    df = pd.DataFrame(records)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")

    fig = go.Figure()
    if chart_type == "line":
        fig.add_trace(go.Scatter(
            x=df["Date"], y=df["Close"], mode="lines", name="Closing Price"
        ))
    else:
        fig.add_trace(go.Bar(
            x=df["Date"], y=df["Close"], name="Closing Price"
        ))

    fig.update_layout(
        title=f"{symbol.upper()} Stock Price ({start} to {end})",
        xaxis_title="Date",
        yaxis_title="Closing Price (USD)",
        template="plotly_white",
        hovermode="x unified",
        margin=dict(l=60, r=20, t=60, b=50),
    )
    return fig


def generate_chart_html(data, symbol, chart_type, start_date, end_date):
    """Return the chart as an HTML fragment that can be embedded in a page."""
    fig = build_figure(data, symbol, chart_type, start_date, end_date)
    return fig.to_html(full_html=False, include_plotlyjs="cdn")

