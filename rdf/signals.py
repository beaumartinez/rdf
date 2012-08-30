from django.contrib.messages import success
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from rdf.models import Settings, UserProfile

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

def create_settings(sender, instance, created, **kwargs):
    if created:
        settings = Settings.objects.create()

        instance.settings = settings
        instance.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(create_settings, sender=UserProfile)
