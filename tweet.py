
# get relevant information(e.g. lanaguage, retweeted, favorated count...) of each 'tweet object'
# Jinghua Xu

# this now may seem liek a dumb idea, if one study the json file well enough, creating an object each time and get information through this approach can be erdandunt???

""" the Tweepy documentation does not provide an intuitive way to obatain relevant information of each 'tweet object'
Tweet class is to enable represent each tweet and enable getting relevant information directly from each 'tweet object' """

import tweepy
from tweepy import RateLimitError
from keys import Keys

tweepy.debug(True)


class tweet:
    """ a tweet class represents a tweet, use this class to obatain information of each tweet """

    def __init__(self, t):
        '''pass a 'tweet object' to the constructor'''
        self._tweet = t

    @property
    def json(self):
        '''return a dictionary representation of a tweet'''
        return self._json

    @property
    def language(self):
        '''return the language of a tweet'''
        return self.json['lang']

    @property
    def retweeted(self):
        '''return True if the tweet is retweeted, False otherwise'''
        if self.json['retweeted']:
            return True
        else:
            return False

    @property
    def favorited(self):
        '''return True if the tweet was favourated, False otherwise'''
        if self.json['favorited']:
            return True
        else:
            return False

    @property
    def favorite_count(self):
        '''return the count of favourate'''
        return self.json['favorite_count']

    @property
    def retweet_count(self):
        '''return the count of retweets'''
        return self.json['retweet_count']

    @property
    def is_quote_status(self):
        '''return true if the tweet is quoted. False otherwise'''
        if self.json['is_quote_status']:
            return True
        else:
            return False

    @property
    def contributors(self):
        '''return contributors of the tweet'''
        return self.json['contributors']

    @property
    def place(self):
        '''return the place of a tweet'''
        return self.json['place']

    @property
    def coordinates(self):
        '''return coordinates of a tweet'''
        return self.json['coordinates']

    @property
    def geo(self):
        '''return geo of a tweet'''
        return self.json['geo']

    # informatiom about user



'''
# little testing part
   
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

        for tweet in tweets:
            d = tweet._json
            for it in d.items():
                print(it)
                
            break

    except RateLimitError:
        print("A rate limits error occured!")



if __name__ == "__main__":

    # the path to the json file stores the keys
    keys = Keys('/Users/xujinghua/TwitterCrawler/tokens.json')
    screen_name = 'tim_cook'

    download_tweets(screen_name, keys)
