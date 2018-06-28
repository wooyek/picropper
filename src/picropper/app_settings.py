# coding=utf-8

from django.conf import settings

# This is an example
PICROPPER_SECRET = settings.SECRET_KEY[::4]
