import requests
from flask import Flask, render_template, request

from api_client import extract_time_series, get_stock_data
from stocks import load_symbols
from validation import validate_date_range
from visualization import generate_chart_html

app = Flask(__name__)

CHART_TYPES = {"bar": "Bar", "line": "Line"}
TIME_SERIES = {
    "intraday": "Intraday (hourly)",
    "daily": "Daily",
    "weekly": "Weekly",
    "monthly": "Monthly",
}


@app.route("/", methods=["GET", "POST"])
def index():
    symbols, symbols_warning = load_symbols()

    form = {
        "symbol": "",
        "chart_type": "line",
        "time_series": "daily",
        "start_date": "",
        "end_date": "",
    }
    chart_html = None
    error = None

    if request.method == "POST":
        for field in form:
            form[field] = request.form.get(field, "").strip()

        valid_symbols = {symbol for symbol, _ in symbols}

        try:
            if form["symbol"].upper() not in valid_symbols:
                raise ValueError("Choose a stock symbol from the list.")
            if form["chart_type"] not in CHART_TYPES:
                raise ValueError("Choose a chart type.")
            if form["time_series"] not in TIME_SERIES:
                raise ValueError("Choose a time series.")

            start, end = validate_date_range(
                form["start_date"], form["end_date"]
            )

            api_response = get_stock_data(form["symbol"], form["time_series"])
            stock_data = extract_time_series(api_response)

            chart_html = generate_chart_html(
                stock_data, form["symbol"], form["chart_type"], start, end
            )

        except (ValueError, requests.RequestException) as exc:
            error = str(exc)

    return render_template(
        "index.html",
        symbols=symbols,
        symbols_warning=symbols_warning,
        chart_types=CHART_TYPES,
        time_series=TIME_SERIES,
        form=form,
        chart_html=chart_html,
        error=error,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0")

