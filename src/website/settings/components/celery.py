# coding=utf-8

import logging

from celery.schedules import crontab

from . import core

log = logging.getLogger(__name__)

# Celery
# http://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html#configuration

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = 'Europe/Warsaw'
CELERY_ENABLE_UTC = True
CELERY_SEND_TASK_ERROR_EMAILS = True
CELERY_ALWAYS_EAGER = False
CELERY_EAGER_PROPAGATES_EXCEPTIONS = False

# http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html

CELERYBEAT_SCHEDULE = {
    'update-experience-stat': {
        'task': 'resume.tasks.update_all_counters',
        # 'schedule': crontab(hour=2, minute=30)
        # 'schedule': crontab(minute='*/15')  # Execute every 15 minutes
        'schedule': crontab(minute=0, hour=3, day_of_week=1)  # Execute weekly at 3 in the morning
    },
    'update-contry-stat': {
        'task': 'resume.tasks.country_counter_update_all',
        'schedule': crontab(minute=0, hour=8, day_of_week=1)
    },
}

CELERY_QUEUES = {
    "celery": {},
    "linkedin": {},
    "external_postings": {},
    "beats": {
        "queue_arguments": {'x-message-ttl': 120000}
    },
    "counters": {
        "queue_arguments": {'x-message-ttl': 120000}
    },
    "dictionaries": {
        "queue_arguments": {'x-message-ttl': 120000}
    },
    "github": {
        "queue_arguments": {}
    },
    "geocoding": {
        "queue_arguments": {}
    },
}

# Sync task testing
# http://docs.celeryproject.org/en/2.5/configuration.html?highlight=celery_always_eager#celery-always-eager

CELERY_ALWAYS_EAGER = core.env('CELERY_ALWAYS_EAGER', bool, default=False)
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

BROKER_URL = core.env("BROKER_URL", default=None) or core.env("CLOUDAMQP_URL")
