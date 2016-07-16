from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    # Examples:
    # url(r'^$', 'hackathon.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('api.urls')),
]


#https://docs.djangoproject.com/en/dev/howto/static-files/#serving-static-files-during-development
#This helper function works only in debug mode and only if the given prefix is local (e.g. /static/)
from django.conf.urls.static import static
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
