## Twitter Crawler through Twitter's API 
_though there are issues with Twitter's API, view this [closed issue]() in Tweepy._
### to build a small corpus and print some statistics

## The functions

### 1.1 Downloading "timeline" of a twitter account
Download tweets of each given `user_name` through Twitter's API with `tweepy.API.user_timeline()`, `cursor()` can do here too.

### 1.2 Print out some statistics

The `print_statistics` function in the template,
prints out the following information about a list of tweets:

- The number of tweets.
- Minimum, maximum, and average number of tokens.
    Tokens can be obtained using [NLTK](https://www.nltk.org/)'s
    [TweetTokenizer](https://www.nltk.org/api/nltk.tokenize.html).
- Average number of 'mentions'
- Average number 'hash tags'
- Average number of retweets
- Average number of times the tweets were favorited
- The date span of the tweets
    (dates of the first and the last tweets in the list)

Plot two histograms into a single PDF file called `<user>-histograms.pdf`,
where `<user>` is the Twitter screen name of the person:
- A histogram of number of tokens.
- A histogram the times of tweets in UTC.

For plotting data, you can use the `mathplotlib` library.

### 1.3 Save the tweets

The `save_tweets` function a should save the given list of tweets as a JSON file.

### 1.4 A basic command line interface

Command-line specification for this script:

- The "screen\_name" of the person should be the only required
    (positional) argument. E.g., `python3 a1.py realDonaldTrump` should
    download tweets by screen name `realDonaldTrump`, and save them to
    the file `realDonaldTrump.joson`.
- The optional argument `--stats` should print out the statistics
    implemented in 1.2 to the standard output (screen, not to the data
    file).

## The `tweet` class
is to build an objectivized representaiton out of a dictionary representation