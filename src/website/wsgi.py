"""
WSGI config for website project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""

# Print statements may help with gunicorn debugging

print("Importing: %s" % __file__)

import logging  # noqa: F402
import os  # noqa: F402

logging.basicConfig(format='%(asctime)s %(levelname)-7s %(thread)-5d %(filename)s:%(lineno)s | %(funcName)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logging.getLogger().setLevel(logging.DEBUG)
logging.disable(logging.NOTSET)
logging.info('Loading %s', __name__)

DJANGO_SETTINGS_MODULE = os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")
print("DJANGO_SETTINGS_MODULE=", DJANGO_SETTINGS_MODULE)
from django.conf import settings  # noqa: F402 isort:skip

# determine where is the single absolute path that
# will be used as a reference point for other directories
SITE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
logging.debug("SITE_ROOT: %s" % SITE_ROOT)
logging.debug("settings.DEBUG: %s" % settings.DEBUG)

# Obtain WSGIHandler
from django.core.wsgi import get_wsgi_application  # noqa: F402 isort:skip
from whitenoise.django import DjangoWhiteNoise  # noqa: F402 isort:skip
from raven.contrib.django.raven_compat.middleware.wsgi import Sentry  # noqa: F402 isort:skip

application = get_wsgi_application()
application = Sentry(application)
application = DjangoWhiteNoise(application)

logging.debug("application: %s" % application)
