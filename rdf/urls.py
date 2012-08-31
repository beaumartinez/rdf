from django.conf.urls import patterns, include, url

urlpatterns = patterns('rdf.views',
    url(r'^$', 'landing', name='landing'),

    url(r'^home/$', 'home', name='home'),
    url(r'^settings/$', 'settings_view', name='settings'),

    url('^log-out/$', 'log_out', name='log_out'),
    url('^log-in/$', 'log_in', name='log_in'),

    url('^twitter-oauth/request/$', 'twitter_oauth_request', name='twitter_oauth_request'),
    url('^twitter-oauth/verify/$', 'twitter_oauth_verify', name='twitter_oauth_verify'),
)
