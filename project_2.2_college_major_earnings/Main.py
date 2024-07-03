# %% [markdown]
# We will be working with a dataset from the American Community Survey, cleaned by FiveThirtyEight, about the job outcomes of college graduates of the classes of 2010-2012. We are interested in earnings, gender and number of graduates of different majors.

# We begin by importing the relevant libraries, inspecting the data and removing all rows containing null values.

# %%
import os
import pandas as pd
import matplotlib as plt
from pandas.plotting import scatter_matrix
%matplotlib inline


def get_path(path):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(dir_path, path)


recent_grads = pd.read_csv(get_path("recent-grads.csv"))

# %%
print(recent_grads.iloc[0])
print(recent_grads.head())
print(recent_grads.tail())
print(recent_grads.describe())

# %%
raw_data_count = len(recent_grads.index)
print(raw_data_count)
# %%
recent_grads = recent_grads.dropna()
# %% [markdown]
# Only one row contained null values.
# %%
cleaned_data_count = len(recent_grads.index)
print(cleaned_data_count)

# %% [markdown]
# Looking at the first two graphs it seems that, apart from a few outliers, graduates of more popular majors do not make more money, nor have a higher or lower  unemployment rate. However, for the outliers it seems to be the case that the less popular they are the higher their median salary.
# %%
recent_grads.plot(
    x="Sample_size", y="Median", kind="scatter", title="Median vs. Sample_size"
)

# %%
recent_grads.plot(
    x="Sample_size",
    y="Unemployment_rate",
    kind="scatter",
    title="Unemployment_rate vs. Sample_size",
)

# %% [markdown]
# The next graph suggests that a higher number of full-time employees does not promise a higher median salary, apart from a few outliers. For the outliers it seems to be true that the fewer full-time employees there are the higher the median salary.
# %%
recent_grads.plot(
    x="Full_time", y="Median", kind="scatter", title="Median vs. Full_time"
)

# %% [markdown]
# The last three graphs suggest that graduates who majored in subjects that were majority female do not have higher median salaries. Moreover, graduates who majored in subjects that were majority male have higher median salaries than those that were majority female.
# %%
recent_grads.plot(
    x="ShareWomen",
    y="Unemployment_rate",
    kind="scatter",
    title="Unemployment_rate vs. ShareWomen",
)

# %%
recent_grads.plot(x="Men", y="Median", kind="scatter", title="Median Vs. Men")

# %%
recent_grads.plot(x="Women", y="Median", kind="scatter", title="Median Vs. Women")

# %%
recent_grads["Sample_size"].hist(bins=50, range=(0, 5000))

# %%
recent_grads["Median"].hist(bins=25, range=(0, 125000))

# %%
recent_grads["Employed"].hist(bins=50, range=(0, 350000))

# %%
recent_grads["Full_time"].hist(bins=50, range=(0, 300000))

# %%
recent_grads["ShareWomen"].hist(bins=30, range=(0, 1))

# %%
recent_grads["Unemployment_rate"].hist(bins=40, range=(0, 0.2))

# %%
recent_grads["Men"].hist(bins=50, range=(0, 200000))

# %%
recent_grads["Women"].hist(bins=50, range=(0, 350000))

# %% [markdown]
# Let us now create some scatter matrix plots.

# %%
scatter_matrix(recent_grads[["Sample_size", "Median"]], figsize=(10, 10))

# %%
scatter_matrix(
    recent_grads[["Sample_size", "Median", "Unemployment_rate"]], figsize=(10, 10)
)

# %% [markdown]
# Analysis. Bar plots next.

# %%
recent_grads[:10].plot.bar(x="Major", y="ShareWomen", legend=False)

# %%
recent_grads[-9:].plot.bar(x="Major", y="ShareWomen", legend=False)