from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^save_fish$', "api.views.save_fish"),
    url(r'^delete_fish$', "api.views.delete_fish"),
    url(r'^get_fish$', "api.views.get_fish"),
    url(r'^$', "api.views.load_frontend")
)
