# %% The goal of this project is to determine to what extent SAT tests are unfair towards certain demographics. De data used is from New York City high schools.

# %%

import pandas as pd
import numpy
import re
import os
import matplotlib.pyplot as plt
import folium
import branca.colormap as cm

%matplotlib inline

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)

def get_path(path):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(dir_path, path)

data_files = [
    "ap_2010.csv",
    "class_size.csv",
    "demographics.csv",
    "graduation.csv",
    "hs_directory.csv",
    "sat_results.csv"
]

data = {}

for f in data_files:
    d = pd.read_csv(get_path("schools/{0}".format(f)))
    data[f.replace(".csv", "")] = d

# %%

all_survey = pd.read_csv("schools/survey_all.txt", delimiter="\t", encoding='windows-1252')
d75_survey = pd.read_csv("schools/survey_d75.txt", delimiter="\t", encoding='windows-1252')
survey = pd.concat([all_survey, d75_survey], axis=0)

survey["DBN"] = survey["dbn"]

survey_fields = [
    "DBN", 
    "rr_s", 
    "rr_t", 
    "rr_p", 
    "N_s", 
    "N_t", 
    "N_p", 
    "saf_p_11", 
    "com_p_11", 
    "eng_p_11", 
    "aca_p_11", 
    "saf_t_11", 
    "com_t_11", 
    "eng_t_11", 
    "aca_t_11", 
    "saf_s_11", 
    "com_s_11", 
    "eng_s_11", 
    "aca_s_11", 
    "saf_tot_11", 
    "com_tot_11", 
    "eng_tot_11", 
    "aca_tot_11",
]
survey = survey.loc[:,survey_fields]
data["survey"] = survey

# %%

data["hs_directory"]["DBN"] = data["hs_directory"]["dbn"]

def pad_csd(num):
    string_representation = str(num)
    if len(string_representation) > 1:
        return string_representation
    else:
        return "0" + string_representation
    
data["class_size"]["padded_csd"] = data["class_size"]["CSD"].apply(pad_csd)
data["class_size"]["DBN"] = data["class_size"]["padded_csd"] + data["class_size"]["SCHOOL CODE"]

# %%

cols = ['SAT Math Avg. Score', 'SAT Critical Reading Avg. Score', 'SAT Writing Avg. Score']
for c in cols:
    data["sat_results"][c] = pd.to_numeric(data["sat_results"][c], errors="coerce")

data['sat_results']['sat_score'] = data['sat_results'][cols[0]] + data['sat_results'][cols[1]] + data['sat_results'][cols[2]]

def find_lat(loc):
    coords = re.findall("\(.+, .+\)", loc)
    lat = coords[0].split(",")[0].replace("(", "")
    return lat

def find_lon(loc):
    coords = re.findall("\(.+, .+\)", loc)
    lon = coords[0].split(",")[1].replace(")", "").strip()
    return lon

data["hs_directory"]["lat"] = data["hs_directory"]["Location 1"].apply(find_lat)
data["hs_directory"]["lon"] = data["hs_directory"]["Location 1"].apply(find_lon)

data["hs_directory"]["lat"] = pd.to_numeric(data["hs_directory"]["lat"], errors="coerce")
data["hs_directory"]["lon"] = pd.to_numeric(data["hs_directory"]["lon"], errors="coerce")

# %%

class_size = data["class_size"]
class_size = class_size[class_size["GRADE "] == "09-12"]
class_size = class_size[class_size["PROGRAM TYPE"] == "GEN ED"]

class_size = class_size.groupby("DBN").agg(numpy.mean)
class_size.reset_index(inplace=True)
data["class_size"] = class_size

data["demographics"] = data["demographics"][data["demographics"]["schoolyear"] == 20112012]

data["graduation"] = data["graduation"][data["graduation"]["Cohort"] == "2006"]
data["graduation"] = data["graduation"][data["graduation"]["Demographic"] == "Total Cohort"]

# %%

cols = ['AP Test Takers ', 'Total Exams Taken', 'Number of Exams with scores 3 4 or 5']

for col in cols:
    data["ap_2010"][col] = pd.to_numeric(data["ap_2010"][col], errors="coerce")

# %%
    
combined = data["sat_results"]

combined = combined.merge(data["ap_2010"], on="DBN", how="left")
combined = combined.merge(data["graduation"], on="DBN", how="left")

to_merge = ["class_size", "demographics", "survey", "hs_directory"]

for m in to_merge:
    combined = combined.merge(data[m], on="DBN", how="inner")

combined = combined.fillna(combined.mean())
combined = combined.fillna(0)

# %%

def get_first_two_chars(dbn):
    return dbn[0:2]

combined["school_dist"] = combined["DBN"].apply(get_first_two_chars)

# %%

correlations = combined.corr()
correlations = correlations["sat_score"]
print(correlations)

# %%

# Remove DBN since it's a unique identifier, not a useful numerical value for correlation.
survey_fields.remove("DBN")
print(survey_fields)

# %%

correlations[survey_fields].plot.bar()

# %% [markdown]

# We can see that N_s, N_t and N_p are strongly correlated with sat_score. These are all measures of total_enrollment which we already saw was correlated with sat_scores so this makes sense.
# Interestingly the response rate of students, rr_s, is correlated with sat_scores, suggesting that students who perform well academically are more likely to fill out surveys (and/or vice versa).
# The perceived safety of teachers (saf_t_11) and students (saf_s_11) also correlate with sat_score. We can make sense of this by saying that learning and teaching in unsafe environments is harder than in safe environments.
# Finally, it is interesting to note that how students perceive academic standards (aca_s_11) correlates with sat_score much more strongly than how teachers (aca_t_11) or parents (aca_p_11) perceive them. 

# Let's look more closely at the safety scores of schools.

# %% 

plt.scatter(combined["saf_s_11"], combined["sat_score"])
plt.title("SAT results versus. safety score as perceived by students")
plt.xlabel("saf_s_11")
plt.ylabel("sat_score")

# %% [markdown]

# There appears to be a (small) positive correlation between school safety and sat scores.

# %%

districts = combined.groupby("school_dist").agg(numpy.mean)
districts.reset_index(inplace=True)
latitudes = districts["lat"].tolist()
longitudes = districts["lon"].tolist()

# Create a map
map_school = folium.Map(
                location = [numpy.mean(latitudes), numpy.mean(longitudes)],
                tiles = "CartoDB positron"
)

# Create a color map to color code the circles on the map
color_lower = districts["saf_s_11"].min()
color_upper = districts["saf_s_11"].max()
colormap = cm.LinearColormap(
                colors = ["#d43e0c", "#4fd40c"],
                vmin = color_lower,
                vmax = color_upper
)
colormap.caption = "Perceived Safety Score of Students"
map_school.add_child(colormap)

# Create the circles on the map
for index, row in districts.iterrows():
    folium.Circle(
        location = [row["lat"], row["lon"]],
        color = colormap(row["saf_s_11"]),
        fill_color = colormap(row["saf_s_11"]),
        fill_opacity = 0.75,
        radius = row["total_enrollment"],
        weight = 0,
        tooltip = "school_dist "+row["school_dist"]+
                  " <br> Perceived Safety Score of Students: {:.1f}".format(row["saf_s_11"])+
                  " <br> Average enrollment per school: {:.0f}".format(row["total_enrollment"])
    ).add_to(map_school)

map_school

# %% [markdown]

# Schools that score low on safety as perceived by the students are mainly situated in northern Brooklyn and upper Manhatten, whereas those that score high can mainly be found in Queens and lower Manhatten

# Let's next investigate the racial differnces in SAT scores.

# %%

fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
xlabels = ["white_per", "asian_per", "black_per", "hispanic_per"]
race_per = [correlations["white_per"], correlations["asian_per"], correlations["black_per"], correlations["hispanic_per"]]
ax.bar(xlabels, race_per)
ax.set_title('Correlation with sat_score')
plt.show()

# %% [markdown]

# Race is strongly correlated with SAT results: white and Asian students score relatively well, while black and hispanic students score lower. Let's look at the correlation with hispanic_per more closely.

# %%

plt.scatter(combined["hispanic_per"], combined["sat_score"])
plt.title("SAT results versus. percentage of students being hispanic")
plt.xlabel("hispanic_per")
plt.ylabel("sat_score")

# %%
print(combined["SCHOOL NAME"][combined["hispanic_per"] > 95])

# %% [markdown]

# These schools are primarily geared towards recent immigrants to the US. The low SAT scores could be explained due to a low understanding of English

# %%

print(combined["SCHOOL NAME"][(combined["hispanic_per"] < 10) & (combined["sat_score"] > 1800)])

# %% [markdown]

# These schools specialize in sciences and receive extra funding. They also have entrance exams, explaining why their students do well on SAT: they select those that perform well academically.

# Let us next investigate gender differences.

# %%

fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
xlabels = ["male", "female_per"]
gender_per = [correlations["male_per"], correlations["female_per"]]
ax.bar(xlabels, gender_per)
ax.set_title('Correlation with sat_score')
plt.show()

# %% [markdown]

# There are weak correlations between female students (positive) and SAT scores, and male students (negative) and SAT scores.

# %%

plt.scatter(combined["female_per"], combined["sat_score"])
plt.title("SAT results versus. percentage of female students")
plt.xlabel("female_per")
plt.ylabel("sat_score")

# %% [markdown]

# There doesn't appear to be a clear correlation. However, the positive outliers appear where the percentage of female students is around 40-80%, roughly in the middle.

# %%

print(combined["SCHOOL NAME"][(combined["female_per"] > 60) & (combined["sat_score"] > 1700)])


# %% [markdown]

# These schools also appear to be higly-selective, explaining the high SAT scores.

# Let's finally look at the correlation between AP exam and SAT scores.

# %%

combined["ap_per"] = combined["AP Test Takers "] / combined["total_enrollment"]

plt.scatter(combined["ap_per"], combined["sat_score"])
plt.title("SAT results versus. AP exam results")
plt.xlabel("ap_per")
plt.ylabel("sat_score")

# %% [markdown]

# It looks like there might be a weak correlation between the percentage of students who took the AP exam and their average SAT scores.