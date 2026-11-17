import csv
from pathlib import Path

CSV_PATH = Path(__file__).with_name("stocks.csv")


def load_symbols(path=CSV_PATH):
   
    try:
        with open(path, newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            columns = {
                (name or "").strip().lower(): name
                for name in (reader.fieldnames or [])
            }

            symbol_col = next(
                (columns[c] for c in ("symbol", "ticker") if c in columns),
                None,
            )
            name_col = next(
                (columns[c] for c in ("name", "company", "security")
                 if c in columns),
                None,
            )

            if symbol_col is None:
                raise ValueError("no Symbol column")

            symbols = {}
            for row in reader:
                symbol = (row.get(symbol_col) or "").strip().upper()
                if symbol:
                    name = (row.get(name_col) or "").strip() if name_col else ""
                    symbols[symbol] = name

        if not symbols:
            raise ValueError("file is empty")

        return sorted(symbols.items()), None

    except (OSError, ValueError, csv.Error):
        return(
            "stocks.csv could not be read"
        )