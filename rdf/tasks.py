from celery import Task, task
from celery.task.control import revoke
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from rdf.models import Retweet, Settings, UserProfile
from rdf.utils import user_api, retweet_random_favorite_tweet

class RetweetTask(Task):

    abstract = True

    def after_return(self, *args, **kwargs):
        user_name = args[0]
        profile = UserProfile.objects.get(user__username=user_name)

        self.apply_async(args, eta=profile.next_retweet)

@task(base=RetweetTask)
def retweet(user_name):
    profile = UserProfile.objects.get(user__username=user_name)

    profile.retweet_task_id = retweet.request.id
    profile.save()

    api = user_api(profile)

    tweet = retweet_random_favorite_tweet(api)
    retweet_ = Retweet.objects.create_from_tweet(profile, tweet)

    return retweet_

def reset_retweet_task_id(profile):
    revoke(profile.retweet_task_id)

    if not profile.settings.paused:
        retweet.apply_async((profile.user.username,), eta=profile.next_retweet)

# Signals

def reset_retweet_task(sender, instance, created, **kwargs):
    reset_retweet_task_id(instance.profile)

post_save.connect(reset_retweet_task, sender=Settings)
