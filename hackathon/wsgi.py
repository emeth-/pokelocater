"""
WSGI config for hackathon project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hackathon.settings")


application = get_wsgi_application()

if os.environ.get('IS_HEROKU_SERVER', False): # $ heroku config:add IS_HEROKU_SERVER='1'
    from whitenoise.django import DjangoWhiteNoise
    application = DjangoWhiteNoise(application)
else:
    from dj_static import Cling
    application = Cling(application)