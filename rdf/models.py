from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import BooleanField, CharField, DateTimeField, PositiveIntegerField, ManyToManyField, Model, OneToOneField

from rdf.constants import MAX_FREQUENCY, MIN_FREQUENCY, SECONDS_PER_DAY

class Retweet(Model):
    datetime = DateTimeField(default=datetime.utcnow)
    tweet_id = CharField(max_length=100)

    class Meta(object):
        ordering = ('-datetime',)

class Settings(Model):
    frequency = PositiveIntegerField(default=MIN_FREQUENCY, help_text='How many times to retweet per day', validators=[MaxValueValidator(MAX_FREQUENCY), MinValueValidator(MIN_FREQUENCY)])
    paused = BooleanField(help_text='Pause your account. You won\'t retweet whilst your account is paused')

class UserProfile(Model):
    access_token_key = CharField(max_length=100)
    access_token_secret = CharField(max_length=100)
    retweets = ManyToManyField('Retweet')
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
