from celery import task
from django.contrib.auth.models import User

from rdf.models import Retweet
from rdf.utils import user_api, retweet_random_favorite_tweet

@task
def retweet(user_name):
    user = User.objects.get(username=user_name)
    profile = user.get_profile()

    api = user_api(user)

    tweet = retweet_random_favorite_tweet(api)
    retweet = Retweet.objects.create_from_tweet(profile, tweet)

    return retweet
