"""Pelikan website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.views.i18n import JavaScriptCatalog
from django_error_views.handlers import *  # noqa F401

from . import debug

sitemaps = {}

urlpatterns = [
    url(r'admin/', admin.site.urls),
    url(r'^err/', debug.ErrView.as_view(), name='err'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^', include('picropper.urls')),
]

if 'debug_toolbar' in settings.INSTALLED_APPS:
    if settings.DEBUG or 'SHOW_TOOLBAR_CALLBACK' in settings.DEBUG_TOOLBAR_CONFIG:
        import debug_toolbar  # noqa: F402

        urlpatterns += [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ]
