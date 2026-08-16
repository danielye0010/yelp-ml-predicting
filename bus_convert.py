import argparse
import json

import pandas as pd

BUSINESS_ATTRIBUTES = [
    "BusinessAcceptsCreditCards",
    "OutdoorSeating",
    "RestaurantsReservations",
    "Caters",
    "RestaurantsTakeOut",
    "GoodForKids",
    "RestaurantsGoodForGroups",
    "RestaurantsDelivery",
    "HasTV",
    "BikeParking",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Extract burger restaurants and selected attributes from Yelp business JSON."
    )
    parser.add_argument("business_json", help="Path to Yelp business.json")
    parser.add_argument("--output", default="burgers_business.csv")
    return parser.parse_args()


def main():
    args = parse_args()

    with open(args.business_json, "r", encoding="utf-8") as file:
        records = [json.loads(line) for line in file]

    businesses = pd.DataFrame(records)
    burgers = businesses[
        businesses["categories"].str.contains("Burgers", na=False)
    ].copy()

    attributes = burgers["attributes"].apply(
        lambda value: value if isinstance(value, dict) else {}
    )
    for column in BUSINESS_ATTRIBUTES:
        burgers[column] = attributes.apply(lambda attr: attr.get(column))

    columns = ["state", "business_id", "stars", "review_count"] + BUSINESS_ATTRIBUTES
    burgers[columns].to_csv(args.output, index=False)
    print(f"Saved {len(burgers):,} burger businesses to {args.output}")


if __name__ == "__main__":
    main()
