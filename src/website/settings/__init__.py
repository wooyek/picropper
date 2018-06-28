from __future__ import absolute_import

import logging
import os
import sys

# Loading here any other settings is a possibly a destructive operation
# as purposed settings modules can modify sys.environment
# leading to setting up configuration variables that should remain empty

if os.environ.get("DJANGO_SETTINGS_MODULE", None) == "website.settings":
    # We'll try to guess settings module when DJANGO_SETTINGS_MODULE to default (this module)
    # It's unusable as it is, we may as well try to correct this.
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        logging.info("Module website.settings is loading testing settings. Set DJANGO_SETTINGS_MODULE to override this.")
        from .testing import *  # noqa: F401, F403
    else:
        logging.info("Module website.settings is loading development settings. Set DJANGO_SETTINGS_MODULE to override this.")
        from .development import *  # noqa: F401, F403

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
# from ..celery import app as celery_app  # noqa


def context_processor(request):
    from django.conf import settings
    from django.utils import translation
    return {
        'intercom': {"app_id": settings.INTERCOM_APP_ID},
        'BASE_URL': settings.BASE_URL,
        'GOOGLE_ANALYTICS_TRACKING_CODE': settings.GOOGLE_ANALYTICS_TRACKING_CODE,
        'LANGUAGE_CODE': translation.get_language(),
        'ENVIRONMENT_NAME': settings.ENVIRONMENT_NAME,
    }
