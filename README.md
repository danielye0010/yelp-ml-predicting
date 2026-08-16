# Yelp Burger Restaurant Success Modeling

A machine-learning and contextual-data project for modeling **burger restaurant success** from Yelp business attributes and state-level conditions.

The project defines a success score that combines rating quality with review volume,

\[
\text{success} = \text{stars} \times \log(\text{review count}+1),
\]

then compares **Linear Regression, Random Forest, and Support Vector Regression (SVR)** using interpretable restaurant attributes such as delivery, takeout, reservations, outdoor seating, group suitability, and bike parking.

## Highlights

- extracts burger restaurants from Yelp's business JSON data
- converts semi-structured business attributes into a model-ready table
- constructs a success metric balancing review quality and popularity
- compares Linear Regression, Random Forest, and SVR on an 80/20 split
- retains a trained SVR artifact for downstream prediction
- includes an independent R/e1071 SVR implementation
- explores state-level relationships using mobility, income, density, ratings, and review volume

## Modeling data

`burgers_business.csv` contains the prepared restaurant-level dataset with:

- `stars`
- `review_count`
- `BusinessAcceptsCreditCards`
- `OutdoorSeating`
- `RestaurantsReservations`
- `Caters`
- `RestaurantsTakeOut`
- `GoodForKids`
- `RestaurantsGoodForGroups`
- `RestaurantsDelivery`
- `HasTV`
- `BikeParking`

`burgers_business_state.csv` retains the state identifier for geographic analysis.

## Model comparison

`model.py`:

1. loads the prepared burger-business table;
2. handles missing boolean attributes;
3. constructs the success metric;
4. creates a fixed 80/20 train-test split;
5. compares Linear Regression, Random Forest, and SVR using MSE and R²;
6. fits an SVR on the full prepared dataset and saves `svr_model.joblib`.

Run:

```bash
pip install -r requirements.txt
python model.py
```

## Rebuild the Yelp business dataset

If you have Yelp's `business.json`, the preprocessing script no longer requires a machine-specific path:

```bash
python bus_convert.py /path/to/business.json
```

It filters businesses whose categories include `Burgers` and writes the selected modeling attributes to `burgers_business.csv`.

## State-level contextual analysis

The project also studies whether restaurant outcomes move with broader state characteristics.

`average_by_state.csv` combines restaurant outcomes with state-level contextual variables including:

- population mobility / trips by distance
- income
- population density

`state.py` calculates correlations with Yelp stars and review count and summarizes the success metric by state.

The transportation aggregation can be rebuilt from a Trips by Distance CSV:

```bash
python transportation.py /path/to/Trips_by_Distance.csv
```

## R SVR implementation

`R-svm.R` provides a parallel R implementation using `e1071`:

```r
install.packages(c("dplyr", "tidyr", "e1071", "readr"))
```

```bash
Rscript R-svm.R
```

It trains an SVR, reports test MSE/R², saves the fitted R model, and demonstrates prediction for a hypothetical restaurant attribute profile.

## Repository structure

- `bus_convert.py` — Yelp JSON → burger restaurant feature table
- `model.py` — Python model comparison and serialized SVR
- `R-svm.R` — independent R SVR workflow
- `transportation.py` — state-level mobility aggregation
- `state.py` — geographic/contextual correlation analysis
- `burgers_business.csv` — prepared restaurant modeling data
- `burgers_business_state.csv` — restaurant data with state identifiers
- `average_by_state.csv` — state-level contextual dataset
- `svr_model.joblib` — retained fitted SVR artifact

## Project takeaway

This project connects **semi-structured data engineering, feature construction, comparative regression modeling, model serialization, and contextual geographic analysis** around a concrete business question: which observable characteristics are associated with stronger Yelp restaurant performance?

Developed as a UW–Madison STAT 628 final project.
