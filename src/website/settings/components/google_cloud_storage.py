# coding=utf-8
# Copyright 2015 Brave Labs sp. z o.o.
# All rights reserved.
#
# This source code and all resulting intermediate files are CONFIDENTIAL and
# PROPRIETY TRADE SECRETS of Brave Labs sp. z o.o.
# Use is subject to license terms. See NOTICE file of this project for details.

import logging

from google.oauth2 import service_account

from . import core
from website.settings import env

log = logging.getLogger(__name__)

core.INSTALLED_APPS += (
    'storages',
)

DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_PROJECT_ID = env('GOOGLE_STORAGE_ID')

GS_CREDENTIALS = service_account.Credentials.from_service_account_info({
    'token_uri': 'https://accounts.google.com/o/oauth2/token',
    'client_email': env('GOOGLE_STORAGE_USER'),
    'private_key_id': env('GOOGLE_STORAGE_ID'),
    'private_key': env('GOOGLE_STORAGE_KEY', lambda s: bytes(s, 'UTF-8').decode('unicode_escape')),
})
GS_BUCKET_NAME = env('GOOGLE_STORAGE_BUCKET')
