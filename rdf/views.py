from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import logout_then_login
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect, render
from tweepy import OAuthHandler, TweepError

def landing(request):
    if request.user.is_authenticated():
        return redirect(reverse('home'))

    return render(request, 'landing.html')

def home(request):
    return HttpResponse('Hi')

def twitter_oauth_request(request):
    callback = reverse('twitter_oauth_verify')
    callback = request.build_absolute_uri(callback)

    handler = OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET, callback)

    redirect_url = handler.get_authorization_url(signin_with_twitter=True)

    request.session['request_token_key'] = handler.request_token.key
    request.session['request_token_secret'] = handler.request_token.secret

    return redirect(redirect_url)	

def twitter_oauth_verify(request):
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

    return redirect(reverse('home'))

def log_out(request):
    return logout_then_login(request, reverse('landing'))

def log_in(request):
    return redirect(reverse('twitter_oauth_request'))
