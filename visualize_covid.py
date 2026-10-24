import argparse
from pathlib import Path
import re
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]


def normalized_name(name):
    return re.sub(r"[^a-z0-9]+", "_", str(name).strip().lower()).strip("_")


def main():
    parser = argparse.ArgumentParser(description="Explore COVID-19 statistics from a CSV file.")
    parser.add_argument("--input", default=str(ROOT / "data" / "sample_covid_data.csv"))
    parser.add_argument("--output", default=str(ROOT / "outputs"))
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    df.columns = [normalized_name(c) for c in df.columns]
    if "confirmed" not in df.columns:
        raise SystemExit("CSV must contain a 'confirmed' column.")
    df["confirmed"] = pd.to_numeric(df["confirmed"], errors="coerce")
    for col in ("deaths", "recovered"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    region_col = next((c for c in ("country_region", "country", "location", "region") if c in df.columns), None)
    if region_col:
        summary = df.groupby(region_col, dropna=False)["confirmed"].max().sort_values(ascending=False).head(10)
        ax = summary.sort_values().plot(kind="barh", figsize=(9, 5), title="Top Regions by Reported Confirmed Cases")
        ax.set_xlabel("Confirmed cases (dataset units)")
        ax.set_ylabel("Region")
        plt.tight_layout()
        plt.savefig(out / "top_regions.png", dpi=150)
        plt.close()

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        daily = df.dropna(subset=["date"]).groupby("date")[["confirmed"] + [c for c in ("deaths", "recovered") if c in df.columns]].sum()
        if not daily.empty:
            ax = daily.plot(figsize=(10, 5), marker="o", title="COVID-19 Reported Metrics Over Time")
            ax.set_xlabel("Date")
            ax.set_ylabel("Reported count")
            plt.tight_layout()
            plt.savefig(out / "time_series.png", dpi=150)
            plt.close()

    print(f"Rows loaded: {len(df)}")
    print(f"Columns: {', '.join(df.columns)}")
    print(f"Charts saved in: {out}")


if __name__ == "__main__":
    main()
