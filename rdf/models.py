from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import BooleanField, CharField, DateTimeField, ForeignKey, Manager, Model, OneToOneField, PositiveIntegerField

from rdf.constants import MAX_FREQUENCY, MIN_FREQUENCY, SECONDS_PER_DAY

class RetweetManager(Manager):

    def create_from_tweet(self, profile, tweet):
        return self.create(
            profile=profile,
            text=tweet.text,
            tweet_id=tweet.id,
            user_name=tweet.user.screen_name
        )

# Models

class Retweet(Model):
    datetime = DateTimeField(default=datetime.utcnow)
    profile = ForeignKey('UserProfile', related_name='retweets')
    text = CharField(max_length=140)
    tweet_id = CharField(max_length=100)
    user_name = CharField(max_length=100)

    class Meta(object):
        get_latest_by = 'datetime'
        ordering = ('-datetime',)

    objects = RetweetManager()

class Settings(Model):
    frequency = PositiveIntegerField(default=MIN_FREQUENCY, help_text='How many times to retweet per day', validators=[MaxValueValidator(MAX_FREQUENCY), MinValueValidator(MIN_FREQUENCY)])
    paused = BooleanField(help_text='Pause your account. You won\'t retweet whilst your account is paused')
    profile = OneToOneField('UserProfile')

class UserProfile(Model):
    access_token_key = CharField(max_length=100)
    access_token_secret = CharField(max_length=100)
    retweet_task_id = CharField(max_length=100)
    user = OneToOneField(User)

    @property
    def next_retweet(self):
        period = 1 / float(self.settings.frequency)
        seconds = SECONDS_PER_DAY * period

        try:
            last_retweet = self.retweets.latest()
        except Retweet.DoesNotExist:
            next_retweet_ = datetime.utcnow()
        else:
            next_retweet_ = last_retweet.datetime + relativedelta(seconds=seconds)
        
        return next_retweet_

import rdf.signals
import rdf.tasks
