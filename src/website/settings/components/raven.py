# coding=utf-8
# Copyright 2015 Brave Labs sp. z o.o.
# All rights reserved.
#
# This source code and all resulting intermediate files are CONFIDENTIAL and
# PROPRIETY TRADE SECRETS of Brave Labs sp. z o.o.
# Use is subject to license terms. See NOTICE file of this project for details.

import logging

from . import core
from website import __version__

log = logging.getLogger(__name__)

core.INSTALLED_APPS += (
    'raven.contrib.django.raven_compat',
)

core.LOGGING['loggers']['raven'] = {
    'level': 'INFO',
    'handlers': ['console'],
    'propagate': False,
}

core.LOGGING['handlers']['sentry'] = {
    'level': 'ERROR',  # To capture more than ERROR, change to WARNING, INFO, etc.
    'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
    'tags': {'custom-tag': 'x'},
}

if core.env("RAVEN_DISABLE_MAIL_ADMINS", default=True):
    if core.LOGGING['loggers']['django.request']['handlers'] == 'mail_admins':
        # This duplicates sentry functionality
        del core.LOGGING['loggers']['django.request']

core.MIDDLEWARE = ('raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',) + core.MIDDLEWARE

RAVEN_CONFIG = {
    'dsn': core.env("RAVEN_CONFIG_DSN"),
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': __version__
}
