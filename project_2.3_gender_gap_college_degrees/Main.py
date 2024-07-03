# The aim of this project is to examine the gender gap across US college degrees from 1968-2011.

import os
import pandas as pd
import matplotlib.pyplot as plt

# %matplotlib inline


def get_path(path):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(dir_path, path)


women_degrees = pd.read_csv(get_path("percent-bachelors-degrees-women-usa.csv"))

# So far we've plotted the gender gap across STEM degrees.

cb_dark_blue = (0 / 255, 107 / 255, 164 / 255)
cb_orange = (255 / 255, 128 / 255, 14 / 255)

stem_cats = [
    "Engineering",
    "Computer Science",
    "Psychology",
    "Biology",
    "Physical Sciences",
    "Math and Statistics",
]

fig = plt.figure(figsize=(18, 3))

for sp in range(0, 6):
    ax = fig.add_subplot(1, 6, sp + 1)
    ax.plot(
        women_degrees["Year"],
        women_degrees[stem_cats[sp]],
        c=cb_dark_blue,
        label="Women",
        linewidth=3,
    )
    ax.plot(
        women_degrees["Year"],
        100 - women_degrees[stem_cats[sp]],
        c=cb_orange,
        label="Men",
        linewidth=3,
    )
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.set_xlim(1968, 2011)
    ax.set_ylim(0, 100)
    ax.set_title(stem_cats[sp])
    ax.tick_params(bottom=False, top=False, left=False, right=False)

    if sp == 0:
        ax.text(2005, 87, "Men")
        ax.text(2002, 8, "Women")
    elif sp == 5:
        ax.text(2005, 62, "Men")
        ax.text(2001, 35, "Women")
plt.show()


# Next we'll look at the gender gap across all 17 degrees in our data set. The degree categories will be sorted in descending order by the percentage of degrees awarded to women.

stem_cats = [
    "Psychology",
    "Biology",
    "Math and Statistics",
    "Physical Sciences",
    "Computer Science",
    "Engineering",
]
lib_arts_cats = [
    "Foreign Languages",
    "English",
    "Communications and Journalism",
    "Art and Performance",
    "Social Sciences and History",
]
other_cats = [
    "Health Professions",
    "Public Administration",
    "Education",
    "Agriculture",
    "Business",
    "Architecture",
]

fig = plt.figure(figsize=(16, 20))

for sp in range(0, 6):
    ax = fig.add_subplot(6, 3, 3 * sp + 1)
    ax.plot(
        women_degrees["Year"],
        women_degrees[stem_cats[sp]],
        c=cb_dark_blue,
        label="Women",
        linewidth=3,
    )
    ax.plot(
        women_degrees["Year"],
        100 - women_degrees[stem_cats[sp]],
        c=cb_orange,
        label="Men",
        linewidth=3,
    )
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.set_xlim(1968, 2011)
    ax.set_ylim(0, 100)
    ax.set_title(stem_cats[sp])
    ax.tick_params(bottom=False, top=False, left=False, right=False)

    if sp == 0:
        ax.text(2005, 10, "Men")
        ax.text(2003, 85, "Women")
    elif sp == 5:
        ax.text(2005, 87, "Men")
        ax.text(2003, 7, "Women")

for sp in range(0, 5):
    ax = fig.add_subplot(6, 3, 3 * sp + 2)
    ax.plot(
        women_degrees["Year"],
        women_degrees[lib_arts_cats[sp]],
        c=cb_dark_blue,
        label="Women",
        linewidth=3,
    )
    ax.plot(
        women_degrees["Year"],
        100 - women_degrees[lib_arts_cats[sp]],
        c=cb_orange,
        label="Men",
        linewidth=3,
    )
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.set_xlim(1968, 2011)
    ax.set_ylim(0, 100)
    ax.set_title(lib_arts_cats[sp])
    ax.tick_params(bottom=False, top=False, left=False, right=False)

    if sp == 0:
        ax.text(2005, 18, "Men")
        ax.text(2003, 78, "Women")

for sp in range(0, 6):
    ax = fig.add_subplot(6, 3, 3 * sp + 3)
    ax.plot(
        women_degrees["Year"],
        women_degrees[other_cats[sp]],
        c=cb_dark_blue,
        label="Women",
        linewidth=3,
    )
    ax.plot(
        women_degrees["Year"],
        100 - women_degrees[other_cats[sp]],
        c=cb_orange,
        label="Men",
        linewidth=3,
    )
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.set_xlim(1968, 2011)
    ax.set_ylim(0, 100)
    ax.set_title(other_cats[sp])
    ax.tick_params(bottom=False, top=False, left=False, right=False)

    if sp == 0:
        ax.text(2005, 5, "Men")
        ax.text(2003, 90, "Women")
    elif sp == 5:
        ax.text(2005, 62, "Men")
        ax.text(2003, 30, "Women")

plt.show()

# The x-axis values nearly overlap with many plot titles. To fix this while also making the figure look less cluttered we will disable the x-axis values for all except the bottom-most plots.

fig = plt.figure(figsize=(16, 16))

for sp in range(0, 6):
    ax = fig.add_subplot(6, 3, 3 * sp + 1)
    ax.plot(
        women_degrees["Year"],
        women_degrees[stem_cats[sp]],
        c=cb_dark_blue,
        label="Women",
        linewidth=3,
    )
    ax.plot(
        women_degrees["Year"],
        100 - women_degrees[stem_cats[sp]],
        c=cb_orange,
        label="Men",
        linewidth=3,
    )
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.set_xlim(1968, 2011)
    ax.set_ylim(0, 100)
    ax.set_title(stem_cats[sp])
    ax.tick_params(bottom=False, top=False, left=False, right=False, labelbottom=False)

    if sp == 0:
        ax.text(2005, 10, "Men")
        ax.text(2003, 85, "Women")
    elif sp == 5:
        ax.text(2005, 87, "Men")
        ax.text(2003, 7, "Women")
        ax.tick_params(labelbottom=True)

for sp in range(0, 5):
    ax = fig.add_subplot(6, 3, 3 * sp + 2)
    ax.plot(
        women_degrees["Year"],
        women_degrees[lib_arts_cats[sp]],
        c=cb_dark_blue,
        label="Women",
        linewidth=3,
    )
    ax.plot(
        women_degrees["Year"],
        100 - women_degrees[lib_arts_cats[sp]],
        c=cb_orange,
        label="Men",
        linewidth=3,
    )
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.set_xlim(1968, 2011)
    ax.set_ylim(0, 100)
    ax.set_title(lib_arts_cats[sp])
    ax.tick_params(bottom=False, top=False, left=False, right=False, labelbottom=False)

    if sp == 0:
        ax.text(2005, 18, "Men")
        ax.text(2003, 78, "Women")
    elif sp == 4:
        ax.tick_params(labelbottom=True)

for sp in range(0, 6):
    ax = fig.add_subplot(6, 3, 3 * sp + 3)
    ax.plot(
        women_degrees["Year"],
        women_degrees[other_cats[sp]],
        c=cb_dark_blue,
        label="Women",
        linewidth=3,
    )
    ax.plot(
        women_degrees["Year"],
        100 - women_degrees[other_cats[sp]],
        c=cb_orange,
        label="Men",
        linewidth=3,
    )
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.set_xlim(1968, 2011)
    ax.set_ylim(0, 100)
    ax.set_title(other_cats[sp])
    ax.tick_params(bottom=False, top=False, left=False, right=False, labelbottom=False)

    if sp == 0:
        ax.text(2005, 5, "Men")
        ax.text(2003, 90, "Women")
    elif sp == 5:
        ax.text(2005, 62, "Men")
        ax.text(2003, 30, "Women")
        ax.tick_params(labelbottom=True)

plt.show()

# To further reduce clutter we will only show the y-axis values of 0 and 100


fig = plt.figure(figsize=(16, 16))

for sp in range(0, 6):
    ax = fig.add_subplot(6, 3, 3 * sp + 1)
    ax.plot(
        women_degrees["Year"],
        women_degrees[stem_cats[sp]],
        c=cb_dark_blue,
        label="Women",
        linewidth=3,
    )
    ax.plot(
        women_degrees["Year"],
        100 - women_degrees[stem_cats[sp]],
        c=cb_orange,
        label="Men",
        linewidth=3,
    )
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.set_xlim(1968, 2011)
    ax.set_ylim(0, 100)
    ax.set_yticks([0, 100])
    ax.set_title(stem_cats[sp])
    ax.tick_params(bottom=False, top=False, left=False, right=False, labelbottom=False)

    if sp == 0:
        ax.text(2005, 10, "Men")
        ax.text(2003, 85, "Women")
    elif sp == 5:
        ax.text(2005, 87, "Men")
        ax.text(2003, 7, "Women")
        ax.tick_params(labelbottom=True)

for sp in range(0, 5):
    ax = fig.add_subplot(6, 3, 3 * sp + 2)
    ax.plot(
        women_degrees["Year"],
        women_degrees[lib_arts_cats[sp]],
        c=cb_dark_blue,
        label="Women",
        linewidth=3,
    )
    ax.plot(
        women_degrees["Year"],
        100 - women_degrees[lib_arts_cats[sp]],
        c=cb_orange,
        label="Men",
        linewidth=3,
    )
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.set_xlim(1968, 2011)
    ax.set_ylim(0, 100)
    ax.set_yticks([0, 100])
    ax.set_title(lib_arts_cats[sp])
    ax.tick_params(bottom=False, top=False, left=False, right=False, labelbottom=False)

    if sp == 0:
        ax.text(2005, 18, "Men")
        ax.text(2003, 78, "Women")
    elif sp == 4:
        ax.tick_params(labelbottom=True)

for sp in range(0, 6):
    ax = fig.add_subplot(6, 3, 3 * sp + 3)
    ax.plot(
        women_degrees["Year"],
        women_degrees[other_cats[sp]],
        c=cb_dark_blue,
        label="Women",
        linewidth=3,
    )
    ax.plot(
        women_degrees["Year"],
        100 - women_degrees[other_cats[sp]],
        c=cb_orange,
        label="Men",
        linewidth=3,
    )
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.set_xlim(1968, 2011)
    ax.set_ylim(0, 100)
    ax.set_yticks([0, 100])
    ax.set_title(other_cats[sp])
    ax.tick_params(bottom=False, top=False, left=False, right=False, labelbottom=False)

    if sp == 0:
        ax.text(2005, 5, "Men")
        ax.text(2003, 90, "Women")
    elif sp == 5:
        ax.text(2005, 62, "Men")
        ax.text(2003, 30, "Women")
        ax.tick_params(labelbottom=True)

plt.show()

# To make it more obvious which degrees have close to 50-50 gendre breakdown we will add a horizontal line at 50% in every plot. Additionally we will increase its transparency and give it another color friendly to color-blind people.


fig = plt.figure(figsize=(16, 16))

for sp in range(0, 6):
    ax = fig.add_subplot(6, 3, 3 * sp + 1)
    ax.plot(
        women_degrees["Year"],
        women_degrees[stem_cats[sp]],
        c=cb_dark_blue,
        label="Women",
        linewidth=3,
    )
    ax.plot(
        women_degrees["Year"],
        100 - women_degrees[stem_cats[sp]],
        c=cb_orange,
        label="Men",
        linewidth=3,
    )
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.set_xlim(1968, 2011)
    ax.set_ylim(0, 100)
    ax.set_yticks([0, 100])
    ax.axhline(50, c=(171 / 255, 171 / 255, 171 / 255), alpha=0.3)
    ax.set_title(stem_cats[sp])
    ax.tick_params(bottom=False, top=False, left=False, right=False, labelbottom=False)

    if sp == 0:
        ax.text(2005, 10, "Men")
        ax.text(2003, 85, "Women")
    elif sp == 5:
        ax.text(2005, 87, "Men")
        ax.text(2003, 7, "Women")
        ax.tick_params(labelbottom=True)

for sp in range(0, 5):
    ax = fig.add_subplot(6, 3, 3 * sp + 2)
    ax.plot(
        women_degrees["Year"],
        women_degrees[lib_arts_cats[sp]],
        c=cb_dark_blue,
        label="Women",
        linewidth=3,
    )
    ax.plot(
        women_degrees["Year"],
        100 - women_degrees[lib_arts_cats[sp]],
        c=cb_orange,
        label="Men",
        linewidth=3,
    )
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.set_xlim(1968, 2011)
    ax.set_ylim(0, 100)
    ax.set_yticks([0, 100])
    ax.axhline(50, c=(171 / 255, 171 / 255, 171 / 255), alpha=0.3)
    ax.set_title(lib_arts_cats[sp])
    ax.tick_params(bottom=False, top=False, left=False, right=False, labelbottom=False)

    if sp == 0:
        ax.text(2005, 18, "Men")
        ax.text(2003, 78, "Women")
    elif sp == 4:
        ax.tick_params(labelbottom=True)

for sp in range(0, 6):
    ax = fig.add_subplot(6, 3, 3 * sp + 3)
    ax.plot(
        women_degrees["Year"],
        women_degrees[other_cats[sp]],
        c=cb_dark_blue,
        label="Women",
        linewidth=3,
    )
    ax.plot(
        women_degrees["Year"],
        100 - women_degrees[other_cats[sp]],
        c=cb_orange,
        label="Men",
        linewidth=3,
    )
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.set_xlim(1968, 2011)
    ax.set_ylim(0, 100)
    ax.set_yticks([0, 100])
    ax.axhline(50, c=(171 / 255, 171 / 255, 171 / 255), alpha=0.3)
    ax.set_title(other_cats[sp])
    ax.tick_params(bottom=False, top=False, left=False, right=False, labelbottom=False)

    if sp == 0:
        ax.text(2005, 5, "Men")
        ax.text(2003, 90, "Women")
    elif sp == 5:
        ax.text(2005, 62, "Men")
        ax.text(2003, 30, "Women")
        ax.tick_params(labelbottom=True)

plt.show()

# Finally, we will export and save the figure.

fig = plt.figure(figsize=(16, 16))

for sp in range(0, 6):
    ax = fig.add_subplot(6, 3, 3 * sp + 1)
    ax.plot(
        women_degrees["Year"],
        women_degrees[stem_cats[sp]],
        c=cb_dark_blue,
        label="Women",
        linewidth=3,
    )
    ax.plot(
        women_degrees["Year"],
        100 - women_degrees[stem_cats[sp]],
        c=cb_orange,
        label="Men",
        linewidth=3,
    )
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.set_xlim(1968, 2011)
    ax.set_ylim(0, 100)
    ax.set_yticks([0, 100])
    ax.axhline(50, c=(171 / 255, 171 / 255, 171 / 255), alpha=0.3)
    ax.set_title(stem_cats[sp])
    ax.tick_params(bottom=False, top=False, left=False, right=False, labelbottom=False)

    if sp == 0:
        ax.text(2005, 10, "Men")
        ax.text(2003, 85, "Women")
    elif sp == 5:
        ax.text(2005, 87, "Men")
        ax.text(2003, 7, "Women")
        ax.tick_params(labelbottom=True)

for sp in range(0, 5):
    ax = fig.add_subplot(6, 3, 3 * sp + 2)
    ax.plot(
        women_degrees["Year"],
        women_degrees[lib_arts_cats[sp]],
        c=cb_dark_blue,
        label="Women",
        linewidth=3,
    )
    ax.plot(
        women_degrees["Year"],
        100 - women_degrees[lib_arts_cats[sp]],
        c=cb_orange,
        label="Men",
        linewidth=3,
    )
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.set_xlim(1968, 2011)
    ax.set_ylim(0, 100)
    ax.set_yticks([0, 100])
    ax.axhline(50, c=(171 / 255, 171 / 255, 171 / 255), alpha=0.3)
    ax.set_title(lib_arts_cats[sp])
    ax.tick_params(bottom=False, top=False, left=False, right=False, labelbottom=False)

    if sp == 0:
        ax.text(2005, 18, "Men")
        ax.text(2003, 78, "Women")
    elif sp == 4:
        ax.tick_params(labelbottom=True)

for sp in range(0, 6):
    ax = fig.add_subplot(6, 3, 3 * sp + 3)
    ax.plot(
        women_degrees["Year"],
        women_degrees[other_cats[sp]],
        c=cb_dark_blue,
        label="Women",
        linewidth=3,
    )
    ax.plot(
        women_degrees["Year"],
        100 - women_degrees[other_cats[sp]],
        c=cb_orange,
        label="Men",
        linewidth=3,
    )
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.set_xlim(1968, 2011)
    ax.set_ylim(0, 100)
    ax.set_yticks([0, 100])
    ax.axhline(50, c=(171 / 255, 171 / 255, 171 / 255), alpha=0.3)
    ax.set_title(other_cats[sp])
    ax.tick_params(bottom=False, top=False, left=False, right=False, labelbottom=False)

    if sp == 0:
        ax.text(2005, 5, "Men")
        ax.text(2003, 90, "Women")
    elif sp == 5:
        ax.text(2005, 62, "Men")
        ax.text(2003, 30, "Women")
        ax.tick_params(labelbottom=True)

plt.savefig(get_path("gender_degrees.png"))
plt.show()
