from random import randrange

from django.conf import settings
from tweepy import API, OAuthHandler, TweepError

def _random_favorite_tweet(api):
    twitter_user = api.me()

    favorites_count = twitter_user.favourites_count

    page = randrange(favorites_count)

    tweet = api.favorites(count=1, page=page)
    tweet = tweet[0]

    return tweet

def retweet_random_favorite_tweet(api):
    retweeted = False

    while not retweeted:
        tweet = _random_favorite_tweet(api)

        try:
            tweet.retweet()
        except TweepError:
            pass
        else:
            retweeted = True

    return tweet

def user_api(user):
    profile = user.get_profile()

    handler = OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    handler.set_access_token(profile.access_token_key, profile.access_token_secret)

    api = API(handler)

    return api
