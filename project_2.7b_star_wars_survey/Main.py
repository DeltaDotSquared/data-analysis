# %% [markdown]
# The aim of this project is to determine the relative popularity of the first six Star Wars movies thru analysis of a survey by FiveThirtyEight. In particular we would like to see how the original trilogy compares to the sequel, and how the movies are viewed by self-proclaimed fans vs. non-fans and men vs. women. The original survey data can be found here: https://github.com/fivethirtyeight/data/tree/master/star-wars-survey

# %%
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

%matplotlib inline

def get_path(path):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(dir_path, path)

star_wars = pd.read_csv(get_path("star_wars.csv"), encoding="ISO-8859-1")
star_wars.info()

# %%
print(star_wars.head(10))
print(star_wars.columns)

# %% [markdown]
# The column "RespondentID" is meant to be a unique ID for each respondent, so we should make sure to remove any missing values. It turns out that the only such row is the first one, which has nonsensical values for other columns too. We will remove this row.

# %%
star_wars = star_wars[star_wars["RespondentID"].notnull()]

# %% [markdown]
# The next two columns represent questions on the survey about whether the respondents had seen any of the first 6 films and whether they consider themselves a fan of the franchise. We will convert the Yes/No answers to True/False respectively to make working with the data easier.

# %%
print(star_wars["Have you seen any of the 6 films in the Star Wars franchise?"].value_counts(dropna=False))
print(star_wars["Do you consider yourself to be a fan of the Star Wars film franchise?"].value_counts(dropna=False))

# %%
yes_no = {
    "Yes": True,
    "No":  False
}
for col in [
    "Have you seen any of the 6 films in the Star Wars franchise?",
    "Do you consider yourself to be a fan of the Star Wars film franchise?"
    ]:
    star_wars[col] = star_wars[col].map(yes_no)

star_wars.head()

# %% [markdown]
# The next six columns ask respondents if they've seen the last 6 star wars movies. The values in these columns are either the name of the movie (if they've seen it) or "NaN" ("missing value", which means they've not seen the movie). We will again convert these to True/False to make it easier to work with them later. Moreover the columns will be renamed.

# %%
film_mapping = {
    "Star Wars: Episode I  The Phantom Menace":     True,
    "Star Wars: Episode II  Attack of the Clones":  True,
    "Star Wars: Episode III  Revenge of the Sith":  True,
    "Star Wars: Episode IV  A New Hope":            True,
    "Star Wars: Episode V The Empire Strikes Back": True,
    "Star Wars: Episode VI Return of the Jedi":     True,
    np.NaN:                                         False
}
for col in star_wars.columns[3:9]:
    star_wars[col] = star_wars[col].map(film_mapping)

rename_mapping = {
    "Which of the following Star Wars films have you seen? Please select all that apply.":              "seen_1",
    "Unnamed: 4":   "seen_2",
    "Unnamed: 5":   "seen_3",
    "Unnamed: 6":   "seen_4",
    "Unnamed: 7":   "seen_5",
    "Unnamed: 8":   "seen_6"
}

star_wars = star_wars.rename(columns=rename_mapping)
star_wars.head()

# %% [markdown]
# The next six columns ask respondents to rank their movies on a scale of 1 to 6 based on their own enjoyment, with 1 being their most liked movie and 6 their least liked movie. These numbers will be converted to floats so they're easier to work with and the columns will again be renamed.

# %%
star_wars[star_wars.columns[9:15]] = star_wars[star_wars.columns[9:15]].astype(float)

rename_mapping_ranking = {
    "Please rank the Star Wars films in order of preference with 1 being your favorite film in the franchise and 6 being your least favorite film.":    "ranking_1",
    "Unnamed: 10":                                           "ranking_2",
    "Unnamed: 11":                                           "ranking_3",
    "Unnamed: 12":                                           "ranking_4",
    "Unnamed: 13":                                           "ranking_5",
    "Unnamed: 14":                                           "ranking_6"
}

star_wars = star_wars.rename(columns=rename_mapping_ranking)
star_wars.head()

# %% [markdown]
# We now have the data in a format conducive to analysis. We will first calculate the mean rankings and the total view counts of the 6 movies and present them in bar plots.

# %%
ranking_mean = star_wars[star_wars.columns[9:15]].mean()

fig, ax = plt.subplots() # TODO make bar plots prettier
bar_rank_counts = ax.bar(np.arange(6), ranking_mean, color='b')

ax.set_ylabel('Average ranking')
ax.set_xticks(np.arange(6))
ax.set_xticklabels(['Episode I', 'Episode II', 'Episode III', 'Episode IV', 'Episode V', 'Episode VI'])

# %% [markdown]
# The later movies score higher on average than the earlier movies, with Episode V scoring best and Episode III scoring worst.

# %%
view_total = star_wars[star_wars.columns[3:9]].sum()
print(view_total)

fig, ax = plt.subplots()
bar_view_counts = ax.bar(np.arange(6), view_total, color='b')

ax.set_ylabel('View counts')
ax.set_xticks(np.arange(6))
ax.set_xticklabels(['Episode I', 'Episode II', 'Episode III', 'Episode IV', 'Episode V', 'Episode VI'])

# %% [markdown]
# The movies that we previously found are more popular are also the most-viewed movies.

# Let's finally see how different demographics view the movies.

# %%
males = star_wars[star_wars["Gender"] == "Male"]
females = star_wars[star_wars["Gender"] == "Female"]

fans = star_wars[star_wars["Do you consider yourself to be a fan of the Star Wars film franchise?"] == True]
non_fans = star_wars[star_wars["Do you consider yourself to be a fan of the Star Wars film franchise?"] == False]

# %%
males_ranking = males[males.columns[9:15]].mean()
females_ranking = females[females.columns[9:15]].mean()

fig, ax = plt.subplots()
male_bar = ax.bar(np.arange(6), males_ranking, 0.35, color='r')
female_bar = ax.bar(np.arange(6) + 0.35, females_ranking, 0.35, color='y')

ax.set_ylabel('Average ranking')
ax.set_xticks(np.arange(6) + 0.35 / 2)
ax.set_xticklabels(['Episode I', 'Episode II', 'Episode III', 'Episode IV', 'Episode V', 'Episode VI'])

ax.legend((male_bar[0], female_bar[0]), ('Men', 'Women'))

# %%
males_views = males[males.columns[3:9]].sum()
females_views = females[females.columns[3:9]].sum()

fig, ax = plt.subplots()
male_bar = ax.bar(np.arange(6), males_views, 0.35, color='r')
female_bar = ax.bar(np.arange(6) + 0.35, females_views, 0.35, color='y')

ax.set_ylabel('View counts')
ax.set_xticks(np.arange(6) + 0.35 / 2)
ax.set_xticklabels(('Episode I', 'Episode II', 'Episode III', 'Episode IV', 'Episode V', 'Episode VI'))
ax.set_ylim(0, 500)

ax.legend((male_bar[0], female_bar[0]), ('Men', 'Women'))

# %%
fans_ranking = fans[fans.columns[9:15]].mean()
non_fans_ranking = non_fans[non_fans.columns[9:15]].mean()

fig, ax = plt.subplots()
fans_bar = ax.bar(np.arange(6), fans_ranking, 0.35, color='b')
non_fans_bar = ax.bar(np.arange(6) + 0.35, non_fans_ranking, 0.35, color='g')

ax.set_ylabel('Average ranking')
ax.set_xticks(np.arange(6) + 0.35 / 2)
ax.set_xticklabels(['Episode I', 'Episode II', 'Episode III', 'Episode IV', 'Episode V', 'Episode VI'])

ax.legend((fans_bar[0], non_fans_bar[0]), ('Fans', 'Non-fans'))

# %%
fans_views = fans[fans.columns[3:9]].sum()
non_fans_views = non_fans[non_fans.columns[3:9]].sum()

fig, ax = plt.subplots()
fans_bar = ax.bar(np.arange(6), fans_views, 0.35, color='b')
non_fans_bar = ax.bar(np.arange(6) + 0.35, non_fans_views, 0.35, color='g')

ax.set_ylabel('View counts')
ax.set_xticks(np.arange(6) + 0.35 / 2)
ax.set_xticklabels(['Episode I', 'Episode II', 'Episode III', 'Episode IV', 'Episode V', 'Episode VI'])
ax.set_ylim(0, 700)

ax.legend((fans_bar[0], non_fans_bar[0]), ('Fans', 'Non-fans'))

# %% [markdown]
# In general the ranking of the movies is similar for men and women, except women ranked Episode higher than men and men ranked Episode IV higher than women. The total view counts for the movies are higher for men than women, suggesting the fanbase is primarily male. 

# It is interesting to note that respondents who consider themselves fans rated the last 3 movies much higher than than non-fans, and vice versa for the first three movies. The view counts are significantly higher for fans than non-fans, as is to be expected.
