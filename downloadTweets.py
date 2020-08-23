#!/usr/bin/env python3
""" 
    Build a small corpus of tweets collected with Twitter's API, calculate some statistics on the collected data, and store the corpus for later use.
    See <https://snlp2020.github.io/a1/>
    Jinghua Xu

"""

import tweepy
from tweepy import RateLimitError
from keys import Keys
from nltk.tokenize import TweetTokenizer
from statistics import mean
import json
from matplotlib import pyplot as plt
import matplotlib.backends.backend_pdf
import numpy as np
import gzip
import os
import argparse


def accepted_tweet(tweetDict):
    """
        A helper function of download_tweets(), determines if the tweet is accepted. An accepted tweets should be just a tweet, not responses or re-tweets,
        and in English.
        Parameters
        ----------
        tweetDict : dict()
            tweet._json
        Returns
        ------
        Boolean
            True if the tweet represented by tweet._json is accepted. An accepted tweets should be just a tweet, not responses or re-tweets,
            and it has to be in English. False otherwise.
    """
    if tweetDict['lang'] == 'en' and tweetDict['in_reply_to_status_id'] is None and 'retweeted_status' not in tweetDict.keys():
        return True
    else:
        return False


def download_tweets(screen_name, keys, max_tweets=None):
    """Download all tweets of Twitter user with given screen_name.
    Parameters:
    -----------
    screen_name:  The screen name of the twitter user
    keys:         An object (or package) with four members,
                    consumer_key, consumer_secret,
                    access_token, access_secret
                  each holding respective OAuth authorization key.
    max_tweets:   Maximum number of tweets to download. If None, all
                  tweets (as much as Twitter allows) should be
                  downloaded.
    Returns:
    ----------
    tweets:       A list of dictionaries containing all the information
                  downloaded from Twitter for each tweet.
    """
    # list of dictionaries containing all the information downloaded from Twitter for each tweet to be returned
    dicts = []

    # tweepy initialization
    auth = tweepy.OAuthHandler(keys.consumer_key, keys.consumer_secret)
    auth.set_access_token(keys.access_token, keys.access_secret)

    try:
        api = tweepy.API(auth, wait_on_rate_limit=True)

        if max_tweets is None:
            max_tweets = float('inf')

        tweets = api.user_timeline(
            screen_name=screen_name, tweet_mode='extended', count=200)

        # temporary list of tweets(dictionaries) storing all tweets including retweets and replies, the id of the last element in this list will be used for while-loop control
        tmp = []

        for tweet in tweets:
            tmp.append(tweet._json)
            if accepted_tweet(tweet._json):
                dicts.append(tweet._json)
                if len(dicts) >= max_tweets:
                    return dicts

        # save the id of the oldest tweet less one
        oldest = tmp[-1]['id'] - 1

        # keep grabbing tweets until no more left to grab or reaching max_tweets set by user
        while len(tweets) > 0:
            tweets = api.user_timeline(
                screen_name=screen_name, tweet_mode='extended', count=200, max_id=oldest)
            for tweet in tweets:
                tmp.append(tweet._json)
                if accepted_tweet(tweet._json):
                    dicts.append(tweet._json)
                    if len(dicts) >= max_tweets:
                        return dicts

            # update oldest
            oldest = tmp[-1]['id'] - 1

        return dicts

    except RateLimitError:
        print("A rate limits error occured!")


def print_statistics(tweets):
    """Print out some statistics about the collected tweets.
    See the assignment sheet for detailed instructions.
    Parameters:
    -----------
    tweets:     A list of dictionaries containing all the information
                downloaded from Twitter for each tweet. 
    Returns:    None
    """
    # The number of tweets
    num_tweets = len(tweets)
    print(f"The number of tweets is: {num_tweets}")

    # tokens
    tknzr = TweetTokenizer()
    # list of numbers of tokens of each tweet
    num_tks = []

    # list of number of meantions of each tweet
    num_mentions = []

    # list of numbers of hashtags of each tweet
    num_hashtags = []

    # list of number of retweets of each tweet
    num_retweets = []

    # list of number of times being favorited of each tweet
    num_favorites = []

    # list of times of tweets in UTC
    times = []

    for tweet in tweets:

        # tokens
        tks = tknzr.tokenize(tweet['full_text'])
        # number of tokens of each tweet
        num_tks.append(len(tks))

        # mentions
        num_mentions.append(len(tweet['entities']['user_mentions']))

        # hashtags
        num_hashtags.append(len(tweet['entities']['hashtags']))

        # retweets
        num_retweets.append(tweet['retweet_count'])

        # favorites
        num_favorites.append(tweet['favorite_count'])

        # times
        time = tweet['created_at'].split(' ')
        oclock = time[3].split(':')[0]
        times.append(int(oclock))

    # minimum number of tokens
    min_tks = min(num_tks)
    print(f"The minimum number of tokens is: {min_tks}")

    # maximum number of tokens
    max_tks = max(num_tks)
    print(f"The maximum number of tokens is: {max_tks}")

    # average number of tokens
    avg_tks = mean(num_tks)
    print(f"The average number of tokens is: {avg_tks}")

    # average number of mentions
    avg_mentions = mean(num_mentions)
    print(f"Average number of menions is: {avg_mentions}")

    # average number of hashtags
    avg_hashtags = mean(num_hashtags)
    print(f"Average number of hashtags is: {avg_hashtags}")

    # average number of retweets
    avg_retweets = mean(num_retweets)
    print(f"Average number of retweets is: {avg_retweets}")

    # average number of times the tweets were favorited
    avg_favorites = mean(num_favorites)
    print(
        f"Average number of times the tweets were favorited is: {avg_favorites}")

    # The date span of the tweets (dates of the first and the last tweets in the list)
    time_first_tweet = tweets[-1]['created_at']
    time_last_tweet = tweets[0]['created_at']
    print("The first tweet in the list was created at: " + time_first_tweet)
    print("The last tweet in the list was created at: " + time_last_tweet)

    # user name
    user_name = tweets[0]['user']['screen_name']

    # plot two histograms into a single PDF file called <user_name>-histograms.pdf
    filename = user_name + '-histograms.pdf'
    pdf = matplotlib.backends.backend_pdf.PdfPages(filename)

    # A histogram of number of tokens
    bins_tks = np.arange(min_tks - 5, max_tks + 5, 1)
    plt.hist(num_tks, bins=bins_tks, alpha=0.5)
    plt.title("A histogram of numbers of tokens in all tweets of @" + user_name)
    plt.xlabel('number of tokens')
    plt.ylabel('frequency')
    plt.savefig(pdf, format='pdf')
    plt.cla()

    # A histogram the times of tweets in UTC
    bins_times = np.arange(0, 24, 1)
    plt.hist(times, bins=bins_times, alpha=0.5)
    plt.title("A histogram the times(in UTC) of tweets of @" + user_name)
    plt.xlabel('time')
    plt.ylabel('frequency')
    plt.savefig(pdf, format='pdf')

    pdf.close()


def save_tweets(tweets, filename, compress=False):
    """Save the downloaded tweets to a JSON file.
    Parameters:
    -----------
    tweets:     A list of dictionaries containing all the information
                downloaded from Twitter for each tweet. 
    filename:   The filename to save the tweets. Overwrite it if file exists.
    compress:   If True, the file should be compressed using gzip algorithm.
    Returns:    None
    """

    with open(filename, 'w') as f:
        f.write(json.dumps(tweets, indent=4))

    if compress:
        with open(filename, 'rb') as f_in, gzip.open(filename+'.gz', 'wb') as f_out:
            f_out.writelines(f_in)

        # optional line of code: delete the original file after the gzip is done:
        os.unlink(filename)


if __name__ == "__main__":

    # the path to the json file stores the keys
    keys = Keys('/Users/xujinghua/TwitterCrawler/tokens.json')

    parser = argparse.ArgumentParser(description="Corpus collector")

    # the only required (positional) argument screen name
    parser.add_argument('screen_name', type=str, help='screen name')

    # The optional argument --stats should print out the statistics implemented in 1.3 to the standard output
    parser.add_argument("-s", "--stats", type=bool,
                        default=False, help='print stats?')

    args = parser.parse_args()

    # screen name
    screen_name = args.screen_name
    # bool
    print_stats = args.stats
    # store the downloaded tweets to
    filename = screen_name + '.json'

    tweets = download_tweets(screen_name, keys)
    save_tweets(tweets, filename)

    if print_stats:
        print_statistics(tweets)
