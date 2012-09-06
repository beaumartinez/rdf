from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import BooleanField, CharField, DateTimeField, ForeignKey, Manager, Model, OneToOneField, PositiveIntegerField

from rdf.constants import MAX_FREQUENCY, MIN_FREQUENCY, SECONDS_PER_DAY

class RetweetManager(Manager):

    def last_five(self):
        return self[:5]

# Models

class Retweet(Model):
    datetime = DateTimeField(default=datetime.utcnow)
    profile = ForeignKey('UserProfile', related_name='retweets')
    text = CharField(max_length=140)
    tweet_id = CharField(max_length=100)
    user_name = CharField(max_length=100)

    class Meta(object):
        ordering = ('-datetime',)

    objects = RetweetManager()

class Settings(Model):
    frequency = PositiveIntegerField(default=MIN_FREQUENCY, help_text='How many times to retweet per day', validators=[MaxValueValidator(MAX_FREQUENCY), MinValueValidator(MIN_FREQUENCY)])
    paused = BooleanField(help_text='Pause your account. You won\'t retweet whilst your account is paused')

class UserProfile(Model):
    access_token_key = CharField(max_length=100)
    access_token_secret = CharField(max_length=100)
    settings = OneToOneField('Settings', null=True)
    user = OneToOneField(User)

    @property
    def next_retweet(self):
        period = 1 / float(self.settings.frequency)
        seconds = SECONDS_PER_DAY * period

        retweets = self.retweets.all()

        try:
            last_retweet = retweets[0]
        except IndexError:
            next_retweet_ = datetime.utcnow()
        else:
            next_retweet_ = last_retweet.datetime + relativedelta(seconds=seconds)
        
        return next_retweet_

import rdf.signals
