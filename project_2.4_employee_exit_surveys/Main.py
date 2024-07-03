# %% [markdown]

# The aim of this project is to find out to what extent employees leave the company due to some kind of dissatisfaction, and whether the resignation rates are correlated with age or time spent at the company. First the data from the two surveys has to be cleaned and combined.

# %%

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

%matplotlib inline

def get_path(path):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(dir_path, path)


dete_survey = pd.read_csv(get_path("dete_survey.csv"))
tafe_survey = pd.read_csv(get_path("tafe_survey.csv"))

# %%

# print(dete_survey.info())
# print(dete_survey.head())

# %%

# print(tafe_survey.info())
# print(tafe_survey.head())

# %% [markdown]

# There are several things to note:
# Firstly there are columns that appear in both surveys but are named differently. These need to be made consistent.
# Secondly, there are multiple columns that suggest resignation due to dissatisfaction.
# Thirdly, the dete_survey dataframe has NaN values that are not designated as such (e.g. "Not Stated" in the "DETE Start Date" column). This also needs to be addressed.
# And lastly, both dataframes contain many columns that are not needed for our purposes. We will get rid of those.

# We begin by addressing the last two points.

# %%

dete_survey = pd.read_csv(get_path("dete_survey.csv"), na_values="Not Stated")
drop_dete_col = dete_survey.iloc[:, 28:49]
drop_tafe_col = tafe_survey.iloc[:, 17:66]
dete_survey_updated = dete_survey.drop(drop_dete_col, axis=1)
tafe_survey_updated = tafe_survey.drop(drop_tafe_col, axis=1)

# %%

# print(dete_survey_updated.info())
# print(dete_survey_updated.head())

# %%

# print(tafe_survey_updated.info())
# print(tafe_survey_updated.head())

# %% [markdown]

# Next we will standardize the column names we will wish to use for when we combine the data later.

# %%

dete_survey_updated.columns = (
    dete_survey_updated.columns.str.lower().str.strip().str.replace(" ", "_")
)
col_update = {
    "Record ID": "id",
    "CESSATION YEAR": "cease_date",
    "Reason for ceasing employment": "separationtype",
    "Gender. What is your Gender?": "gender",
    "CurrentAge. Current Age": "age",
    "Employment Type. Employment Type": "employment_status",
    "Classification. Classification": "position",
    "LengthofServiceOverall. Overall Length of Service at Institute (in years)": "institute_service",
    "LengthofServiceCurrent. Length of Service at current workplace (in years)": "role_service",
}
tafe_survey_updated = tafe_survey_updated.rename(col_update, axis=1)

# print(dete_survey_updated.head())
# print(tafe_survey_updated.head())

# %%

# print(dete_survey_updated["separationtype"].value_counts())
# print(tafe_survey_updated["separationtype"].value_counts())

# %% [markdown]

# Since we are only interested in the resignation data the rows pertaining to employees who left for other reasons can be discarded.

# %%

dete_survey_updated["separationtype"] = (
    dete_survey_updated["separationtype"].str.split("-").str[0]
)
dete_resignations = dete_survey_updated[
    dete_survey_updated["separationtype"] == "Resignation"
].copy()
tafe_resignations = tafe_survey_updated[
    tafe_survey_updated["separationtype"] == "Resignation"
].copy()
# print(dete_resignations.info())
# print(tafe_resignations.info())

# %% [markdown]

# Before we continue let us confirm that the data is, to the best of our knowledge, valid. For example, we should check if the start dates are not later than the cease dates, and that people didn"t start working at the company before 1940, since that would also suggest incorrect data.

# %%

# print(dete_resignations["cease_date"].value_counts().sort_index(ascending=False))
# print(tafe_resignations["cease_date"].value_counts().sort_index(ascending=False))
# dete_resignations["cease_date"] = dete_resignations["cease_date"].str.split("/").str[-1].astype("float")
# print(dete_resignations["dete_start_date"].value_counts().sort_index(ascending=False))
# print(dete_resignations["cease_date"].value_counts().sort_index(ascending=False))

# %% [markdown]

# The years in both dataframes don"t completely align, but that is not an issue for our purposes.

# %% [markdown]

# Next we will create an "institute_service" column in the dete survey dataframe for when we merge the dataframes later. We have to calculate the values ourselves by subtracting the "dete_start_date" from the "cease_date" values.

# %%

dete_resignations["institute_service"] = (
    dete_resignations["cease_date"] - dete_resignations["dete_start_date"]
)
# dete_resignations["institute_service"].head()

# %% [markdown]

# Next we"ll create a new column in which we"ll track if employees resigned due to being dissatisfied for whatever work-related reason.

# %%

# print(tafe_resignations["Contributing Factors. Dissatisfaction"].value_counts())
# print(tafe_resignations["Contributing Factors. Job Dissatisfaction"].value_counts())

# %%

def update_vals(val):
    if pd.isnull(val):
        return np.nan
    elif val == "-":
        return False
    else:
        return True


dete_resignations["dissatisfied"] = dete_resignations[
    [
        "job_dissatisfaction",
        "dissatisfaction_with_the_department",
        "physical_work_environment",
        "lack_of_recognition",
        "lack_of_job_security",
        "work_location",
        "employment_conditions",
        "work_life_balance",
        "workload",
    ]
].any(axis=1, skipna=False)
tafe_resignations["dissatisfied"] = (
    tafe_resignations[
        [
            "Contributing Factors. Dissatisfaction",
            "Contributing Factors. Job Dissatisfaction",
        ]
    ]
    .applymap(update_vals)
    .any(axis=1, skipna=False)
)

dete_resignations_up = dete_resignations.copy()
tafe_resignations_up = tafe_resignations.copy()
dete_resignations_up["dissatisfied"].value_counts(dropna=False)

# %% [markdown]

# The final step before we combine the dataframes is to add a column denoting which dataframe the data originally came from.

# %%

dete_resignations_up["institute"] = "DETE"
tafe_resignations_up["institute"] = "TAFE"

# %%

combined = pd.concat(
    [dete_resignations_up, tafe_resignations_up], axis=0, ignore_index=True
)
# print(combined.notnull().sum().sort_values())
combined_updated = combined.dropna(thresh=500, axis=1).copy()

# %% [markdown]

# Next we will convert the "institute_service" data into categories, based on an article which makes the argument that understanding employee"s needs according to career stage instead of age is more effective.

# https://www.businesswire.com/news/home/20171108006002/en/Age-Number-Engage-Employees-Career-Stage

# %%

# print(combined_updated["institute_service"].value_counts(dropna=False))

# %%

combined_updated["institute_service"] = (
    combined_updated["institute_service"]
    .astype("str")
    .str.extract(r"(\d+)")
    .astype("float")
)
# print(combined_updated["institute_service"].value_counts(dropna=False))

# %%


def map_cats(val):
    if pd.isnull(val):
        return np.nan
    elif val < 3.0:
        return "New"
    elif val < 7.0:
        return "Experienced"
    elif val < 11.0:
        return "Established"
    else:
        return "Veteran"


combined_updated["service_cat"] = combined_updated["institute_service"].apply(map_cats)
# print(combined_updated["service_cat"].value_counts())

# %% [markdown]

# Now we are ready to start the analysis

# %%

combined_updated["dissatisfied"].value_counts(dropna=False)
combined_updated["dissatisfied"] = combined_updated["dissatisfied"].fillna(False)

combined_pv = combined_updated.pivot_table(values="dissatisfied", index="service_cat")
combined_pv.plot(kind="bar", rot=30)

# %% [markdown]

# Employees with 7 years of experience or more are more likely to resign due to dissatisfaction.