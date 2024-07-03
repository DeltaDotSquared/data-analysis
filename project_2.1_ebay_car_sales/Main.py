import os
import pandas as pd
import numpy as np

# The aim of this project is to clean and analyze a data set of used car listings on German eBay.


def get_path(path):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(dir_path, path)


autos = pd.read_csv(get_path("autos.csv"), encoding="Latin-1")

# autos.info()
# autos.head()

# print(autos.columns)

autos.columns = [
    "date_crawled",
    "name",
    "seller",
    "offer_type",
    "price",
    "abtest",
    "vehicle_type",
    "registration_year",
    "gearbox",
    "power_ps",
    "model",
    "odometer",
    "registration_month",
    "fuel_type",
    "brand",
    "unrepaired_damage",
    "ad_created",
    "nr_of_pictures",
    "postal_code",
    "last_seen",
]

# autos.describe(include="all")

# Columns of note: "price" and "odometer" (numbers stored as text); "seller" and "offer_type" (mostly one value, so not interesting for analysis); "nr_of_pictures", "registration_year" (requires more investigation)


# autos["nr_of_pictures"].value_counts()


# "seller", "offer_type" and "nr_of_pictures" are mostly one value and will be dropped due to not being interesting for analysis

autos.drop(["seller", "offer_type", "nr_of_pictures"], axis=1)


# Now let us clean "price" and "odometer" so that they can be stored as numeric data instead of strings

# print(autos["price"].unique())
# print(autos["odometer"].unique())


autos["price"] = autos["price"].str.replace("$", "").str.replace(",", "").astype(int)
autos["odometer"] = (
    autos["odometer"].str.replace("km", "").str.replace(",", "").astype(int)
)
autos.rename(columns={"price": "price_dollar"}, inplace=True)
autos.rename(columns={"odometer": "odometer_km"}, inplace=True)


# print(autos["price_dollar"].unique().shape)
# print(autos["price_dollar"].value_counts().sort_index(ascending=False).head(20))

# Prices increase steadily till about $350.000, after which they bceome unrealistically high. Let us remove these listings. Prices of $1 are not necessarily unrealistic as these could simply be the opening bids.

autos = autos[autos["price_dollar"].between(1, 350001)]


# autos["odometer_km"].unique().shape
# autos["odometer_km"].value_counts().sort_index(ascending=False).head(15)

# Since these numbers are rounded users probably had to choose from a list of pre-chosen values. We will keep these.


# autos[['date_crawled','ad_created','last_seen']][0:5]


# print(
#     autos["date_crawled"]
#     .str[:10]
#     .value_counts(normalize=True, dropna=False)
#     .sort_index()
# )
# print(
#     autos["ad_created"].str[:10].value_counts(normalize=True, dropna=False).sort_index()
# )
# print(
#     autos["last_seen"].str[:10].value_counts(normalize=True, dropna=False).sort_index()
# )


autos["registration_year"].describe()

# The minimum value is 1000 and the maximum 9999, which are incorrect. This column needs cleaning as well.


# print(autos["registration_year"].value_counts().sort_index(ascending=False).head(15))
# print(autos["registration_year"].value_counts().sort_index(ascending=True).head(15))

# Cars cannot be registered before they were invented or after the listings were posted, so these incorrect values have to be pruned. All values before 1900 and after 2016 will be considered wrong.

autos = autos[autos["registration_year"].between(1900, 2016)]

# print(
#     autos["registration_year"].value_counts(normalize=True, dropna=False).head(10)
# )

# It seems most cars were registered in the last 20 years.


autos["brand"].value_counts().head(20)
autos["brand"].describe()

# We will select the brands for inspection that appear in at least 5% of all listings, as the others are hardly relevant.

brand_counts = autos["brand"].value_counts(normalize=True)
sel_brands = brand_counts[brand_counts > 0.05].index


brand_data = {}
for b in sel_brands:
    sel_rows = autos[autos["brand"] == b]
    brand_data[b] = int(sel_rows["price_dollar"].mean())

# print("Average prices in dollars")
# print(brand_data)

# "BMW", "Mercedes" and "Audi" cars are significantly more expensive than "Opel" and "Ford" cars, which are very cheap. "Volkswagen" cars are in between, which could explain its popularity.

# Let us now do the same for mileage and then combine the data into a new dataframe

mileage_data = {}
for b in sel_brands:
    sel_rows = autos[autos["brand"] == b]
    mileage_data[b] = int(sel_rows["odometer_km"].mean())

brand_data_series = pd.Series(brand_data).sort_values(ascending=False)
mileage_data_series = pd.Series(mileage_data)

brand_df = pd.DataFrame(data=brand_data_series, columns=["average_price_dollar"])
brand_df["average_odometer_km"] = mileage_data_series

print(brand_df)

# There is no signifcant correlation between average price and average mileage.
