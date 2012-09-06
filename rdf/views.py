# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login
from django.contrib.messages import error, success
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect, render
from tweepy import OAuthHandler, TweepError

from rdf.decorators import save_to_session
from rdf.forms import SettingsForm
from rdf.utils import user_api

@save_to_session('next')
def landing(request):
    if request.user.is_authenticated():
        return redirect(reverse('home'))

    return render(request, 'landing.html')

@login_required
def home(request):
    api = user_api(request.user)
    twitter_user = api.me()

    profile = request.user.get_profile()

    return render(request, 'home.html', {
        'profile': profile,
        'twitter_user': twitter_user, 
    })

@login_required
def retweets(request):
    api = user_api(request.user)
    twitter_user = api.me()

    profile = request.user.get_profile()

    return render(request, 'retweets.html', {
        'profile': profile,
        'twitter_user': twitter_user, 
    })

@login_required
def settings_view(request):
    api = user_api(request.user)
    twitter_user = api.me()

    profile = request.user.get_profile()

    form = SettingsForm(request.POST or None, instance=profile.settings)

    if form.is_valid():
        form.save()
        success(request, 'Updated settings')

        return redirect(reverse('home'))
    elif request.POST:
        error(request, 'Couldn\'t update settings—the form has errors')

    return render(request, 'settings.html', {
        'form': form,
        'twitter_user': twitter_user, 
    })

def twitter_oauth_request(request):
    callback = reverse('twitter_oauth_verify')
    callback = request.build_absolute_uri(callback)

    handler = OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET, callback)

    redirect_url = handler.get_authorization_url(signin_with_twitter=True)

    request.session['request_token_key'] = handler.request_token.key
    request.session['request_token_secret'] = handler.request_token.secret

    return redirect(redirect_url)	

def twitter_oauth_verify(request):
    redirect_url = reverse('landing')

    request_token_key = request.session.pop('request_token_key', '')
    request_token_secret = request.session.pop('request_token_secret', '')

    handler = OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    handler.set_request_token(request_token_key, request_token_secret)

    verifier = request.GET.get('oauth_verifier', '')

    try:
        handler.get_access_token(verifier)
    except TweepError:
        pass
    else:
        user = authenticate(access_token_key=handler.access_token.key, access_token_secret=handler.access_token.secret, consumer_key=settings.CONSUMER_KEY, consumer_secret=settings.CONSUMER_SECRET)
        login(request, user)

        redirect_url = request.session.pop('next', redirect_url)

    return redirect(redirect_url)

def log_out(request):
    return logout_then_login(request, reverse('landing'))

def log_in(request):
    return redirect(reverse('twitter_oauth_request'))
