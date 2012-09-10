from celery import task
from django.contrib.auth.models import User

from rdf.models import Retweet, UserProfile
from rdf.utils import user_api, retweet_random_favorite_tweet

@task
def retweet(user_name):
    profile = UserProfile.objects.get(user__username=user_name)

    api = user_api(profile)

    tweet = retweet_random_favorite_tweet(api)
    retweet_ = Retweet.objects.create_from_tweet(profile, tweet)

    return retweet_
