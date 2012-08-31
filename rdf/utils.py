from django.conf import settings
from tweepy import API, OAuthHandler

def user_api(user):
    profile = user.get_profile()

    handler = OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    handler.set_access_token(profile.access_token_key, profile.access_token_secret)

    api = API(handler)

    return api
