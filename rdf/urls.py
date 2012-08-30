from django.conf.urls import patterns, include, url

urlpatterns = patterns('rdf.views',
    url(r'^$', 'home', name='home'),

    url('^twitter-oauth/request/$', 'twitter_oauth_request', name='twitter_oauth_request'),
    url('^twitter-oauth/verify/$', 'twitter_oauth_verify', name='twitter_oauth_verify'),
)
