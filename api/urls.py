from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^get_poke$', "api.views.get_poke"),
    url(r'^$', "api.views.load_frontend")
)
