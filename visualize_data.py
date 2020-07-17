import argparse
import json
import sys
from collections import defaultdict, namedtuple
from datetime import datetime
from typing import Dict, DefaultDict, NamedTuple, List

import chartify
import pandas as pd

from lib.models import *

parser = argparse.ArgumentParser(description='Analyzes the output of parse_data.py and generates visualizations')
parser.add_argument('output_filename', help='filename for the generated chart')
parser.add_argument('-f', '--input-file', help='file to analyze; if omitted uses stdin')
parser.add_argument('-g', '--group-file', help='json file specifying a mapping from group to list of users')
parser.add_argument(
    '--goal', type=int, default=75, help='integer, from 0 to 100, representing the desired percent of on-time reviews'
)
parser.add_argument(
    '--min-reviews',
    type=int,
    default=10,
    help='integer, representing the min number of reviews a user must have to show up in the chart'
)
args = parser.parse_args()

if args.input_file:
    with open(args.input_file, 'r') as f:
        data = json.load(f)
else:
    data = json.load(sys.stdin)

if args.group_file:
    with open(args.group_file, 'r') as f:
        group_to_users = json.load(f)

# Create a `Reviews` object for each user
reviews_by_user: DefaultDict[str, Reviews] = defaultdict(lambda: Reviews())
for row in data:
    reviews = reviews_by_user[row['reviewer']]
    if row['status'] == ReviewStatus.ON_TIME:
        reviews.on_time += 1
    elif row['status'] == ReviewStatus.LATE:
        reviews.late += 1
    if row['status'] == ReviewStatus.NO_RESPONSE:
        reviews.no_response += 1

# create a data frame with a user, team, and on_time_ratio column
users, on_time_ratios = zip(
    *((k, v.on_time_ratio) for (k, v) in reviews_by_user.items() if v.total >= args.min_reviews)
)

user_to_group = {}
if args.group_file:
    for k, v in group_to_users.items():
        for x in v:
            user_to_group[x] = k
groups = [user_to_group.get(user, 'Other') for user in users]

data_frame = pd.DataFrame({
    'user': users,
    'on_time_ratio': on_time_ratios,
    'group': groups,
})

# create the chart of our results
ch = chartify.Chart(blank_labels=True, x_axis_type='categorical')
ch.set_title('On-time review rate')

ch.plot.bar(
    data_frame=data_frame,
    categorical_columns=(['group', 'user'] if args.group_file else ['user']),
    numeric_column='on_time_ratio',
    **({'color_column': 'group'} if args.group_file else {}),
).callout.line(
    args.goal / 100,
    line_dash='dashed',
)

ch.axes.set_yaxis_range(0, 1)
ch.axes.set_yaxis_tick_format('0%')
ch.axes.set_xaxis_tick_orientation(['diagonal', 'horizontal'])
ch.save(args.output_filename)
