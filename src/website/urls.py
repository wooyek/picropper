"""Picropper website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
"""
from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path
from django.views.i18n import JavaScriptCatalog
from django_error_views.handlers import *  # noqa F401

from .misc import debug

sitemaps = {}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('err/', debug.ErrView.as_view(), name='err'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('picropper.urls')),
]

if 'debug_toolbar' in settings.INSTALLED_APPS:
    if settings.DEBUG or 'SHOW_TOOLBAR_CALLBACK' in settings.DEBUG_TOOLBAR_CONFIG:
        import debug_toolbar  # noqa: F402

        urlpatterns += [
            path('__debug__/', include(debug_toolbar.urls)),
        ]
