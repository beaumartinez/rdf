from django.conf.urls import patterns, include, url

urlpatterns = patterns('rdf.views',
    url(r'^$', 'home', name='home'),
)
