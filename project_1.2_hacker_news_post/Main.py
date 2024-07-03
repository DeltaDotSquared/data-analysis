# In this project we're interested in the average number of comments on posts on the news website "Hacker News". This website has so-called "Ask HN" and "Show HN" posts, which are posts where the community is asked a specific question or shown something by the creator of that post. We want to find out a) if these kinds of posts receive more comments on average and b) if posts created at certain time receive more comments.

import os
from csv import reader
import datetime as dt


def get_path(path):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(dir_path, path)


opened_file = open(get_path("hacker_news.csv"))
read_file = reader(opened_file)
hn = list(read_file)

# The first list contains the column headers. We will separate thse from the rest of the data.
headers, hn = hn[0], hn[1:]

# We will now separate the "Ask HN" and "Show HN" posts from the others.
ask_posts = []
show_posts = []
other_posts = []
for post in hn:
    title = post[1]
    title = title.lower()
    if title.startswith("ask hn"):
        ask_posts.append(post)
    if title.startswith("show hn"):
        show_posts.append(post)
    else:
        other_posts.append(post)

# print(len(ask_posts))
# print(len(show_posts))
# print(len(other_posts))

# Let us calculate the average number of comments for "Ask HN" and "Show HN" posts.
total_ask_comments = 0
total_show_comments = 0

for post in ask_posts:
    ask_comments = post[4]
    total_ask_comments += int(ask_comments)

for post in show_posts:
    show_comments = post[4]
    total_show_comments += int(show_comments)

avg_ask_comments = total_ask_comments / len(ask_posts)
avg_show_comments = total_show_comments / len(show_posts)

# "Ask HN" posts get 14 comments per post on average versus. 10 comments for "Show HN" posts. For that reason the focus of our second question will be on "Ask HN" posts.
# print(avg_ask_comments, avg_show_comments)

result_list = []
for post in ask_posts:
    created_at = post[6]
    ask_comments = int(post[4])
    result_list.append([created_at, ask_comments])

counts_by_hour = {}
comments_by_hour = {}
for row in result_list:
    date = dt.datetime.strptime(row[0], "%m/%d/%Y %H:%M")
    hour = date.strftime("%H")
    if hour not in counts_by_hour:
        counts_by_hour[hour] = 1
        comments_by_hour[hour] = row[1]
    else:
        counts_by_hour[hour] += 1
        comments_by_hour[hour] += row[1]

# print(counts_by_hour, comments_by_hour)

avg_by_hour = []
for hour in comments_by_hour:
    avg_by_hour.append([hour, (comments_by_hour[hour] / counts_by_hour[hour])])

swap_avg_by_hour = []
for val in avg_by_hour:
    temp_list = [val[1], val[0]]
    swap_avg_by_hour.append(temp_list)

sorted_swap = sorted(swap_avg_by_hour, reverse=True)
# print(*sorted_swap, sep="\n")

print("Top 5 Hours for Ask Posts Comments (Timezone: EST)")
for val in sorted_swap[:5]:
    print("{h}:00 {avg:.2f} average comments per post".format(h=val[1], avg=val[0]))
