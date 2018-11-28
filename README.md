Calculates the ratio of reviews by a user that are 'on-time' in a given GitHub repository.

## Setup:
0. Prereqs: Python 3.6+
1. `pip install -r requirements.txt`
2. [Get a GitHub API token][get-token]
3. Set a `GH_API_TOKEN` environment variable with the value from step two

## Simple usage:

```
python download_data.py microsoft typescript -o data/msftRawData.json
python transform_data.py -f data/msftRawData.json -o data/msftData.json
python visualize_data.py -f data/msftData.json output/msftChart.html
```

Output:
![microsoft-typescript-on-time-reviews](output/msftChart.png?raw=true)

#### Customize output chart:

```
python visualize_data.py -f data/msftParsedData.json -g data/groups.json --min-reviews 20 --goal 50 output/msftChartWithGroups.html
```

Output:
![microsoft-typescript-on-time-reviews-with-groups](output/msftChartWithGroups.png?raw=true)


## FAQ:

**What is an on-time review?**
If a review is requested before 2pm in the local time zone, a review is ontime if it's finished by 6pm that day.
If a review is requested after 2pm, a review is on-time if it's finished before 2pm the next business day.

**I don't like your definition of on-time.**
That's okay! Feel free to change the defintion of `get_due_time` in `lib/date_utils`.
Also we'd be happy to take a PR making the definition more customizable.

## API Reference:

**download_data.py**:
```
usage: download_data.py [-h] [-n NUM_PRS] [--prs-per-batch PRS_PER_BATCH]
                        [-o OUTPUT_FILE]
                        repo_owner repo_name

Downloads PR review data from GitHub for a given repo

positional arguments:
  repo_owner            the owner of a GitHub repo. For
                        'https://github.com/Microsoft/TypeScript' would be
                        'Microsoft'
  repo_name             the name of a GitHub repo of the above owner. For
                        'https://github.com/Microsoft/TypeScript' would be
                        'TypeScript'

optional arguments:
  -h, --help            show this help message and exit
  -n NUM_PRS, --num-prs NUM_PRS
                        the total number of PRs to download from the repo
  --prs-per-batch PRS_PER_BATCH
                        the number of PRs to download per request
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        file to output; if omitted uses stdout
```

**transform_data.py**:
```
usage: transform_data.py [-h] [-f INPUT_FILE] [-o OUTPUT_FILE] [-tz TZ]

Parses the output of download_data.py into a list of reviews and their status,
either 'on_time', 'late', or 'no_response'

optional arguments:
  -h, --help            show this help message and exit
  -f INPUT_FILE, --input-file INPUT_FILE
                        file to parse; if omitted uses stdin
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        file to output; if omitted uses stdout
  -tz TZ                timezone to use for calculating business hours for
                        review status
```

**visualize_data.py**:
```
usage: visualize_data.py [-h] [-f INPUT_FILE] [-g GROUP_FILE] [--goal GOAL]
                         [--min-reviews MIN_REVIEWS]
                         output_filename

Analyzes the output of parse_data.py and generates visualizations

positional arguments:
  output_filename       filename for the generated chart

optional arguments:
  -h, --help            show this help message and exit
  -f INPUT_FILE, --input-file INPUT_FILE
                        file to analyze; if omitted uses stdin
  -g GROUP_FILE, --group-file GROUP_FILE
                        json file specifying a mapping from group to list of
                        users
  --goal GOAL           integer, from 0 to 100, representing the desired
                        percent of on-time reviews
  --min-reviews MIN_REVIEWS
                        integer, representing the min number of reviews a user
                        must have to show up in the chart
```

[get-token]: https://help.github.com/articles/creating-an-access-token-for-command-line-use/


