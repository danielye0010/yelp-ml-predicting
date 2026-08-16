import argparse

import pandas as pd

TRIP_COLUMNS = [
    "Date",
    "State Postal Code",
    "Population Not Staying at Home",
    "Number of Trips",
    "Number of Trips <1",
    "Number of Trips 1-3",
    "Number of Trips 3-5",
    "Number of Trips 5-10",
    "Number of Trips 10-25",
    "Number of Trips 25-50",
    "Number of Trips 50-100",
    "Number of Trips 100-250",
    "Number of Trips 250-500",
    "Number of Trips >=500",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Aggregate Trips by Distance data to state-level averages."
    )
    parser.add_argument("trips_csv", help="Path to Trips_by_Distance.csv")
    parser.add_argument("--output", default="transportation_data.csv")
    return parser.parse_args()


def main():
    args = parse_args()
    df = pd.read_csv(args.trips_csv, usecols=TRIP_COLUMNS)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    numeric_columns = [column for column in TRIP_COLUMNS if column != "Date"]
    state_avg = (
        df[numeric_columns]
        .groupby("State Postal Code", as_index=False)
        .mean(numeric_only=True)
    )
    state_avg.to_csv(args.output, index=False)
    print(f"Saved state-level trip averages to {args.output}")


if __name__ == "__main__":
    main()
