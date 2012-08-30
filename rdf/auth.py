from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from tweepy import API, OAuthHandler

class TwitterBackend(ModelBackend):

    def authenticate(self, access_token_key='', access_token_secret='', consumer_key='', consumer_secret=''):
        handler = OAuthHandler(consumer_key, consumer_secret)
        handler.set_access_token(access_token_key, access_token_secret)

        api = API(handler)
        twitter_user = api.verify_credentials()

        try:
            twitter_id = twitter_user.id
        except AttributeError:
            user = None
        else:
            try:
                user = User.objects.get(username=twitter_id)
            except User.DoesNotExist:
                user = User.objects.create_user(twitter_id)

            profile = user.get_profile()

            profile.access_token_key = handler.access_token.key
            profile.access_token_secret = handler.access_token.secret

            profile.save()

        return user
