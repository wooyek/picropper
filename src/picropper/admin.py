# coding=utf-8
from django.contrib import admin
from import_export.admin import ImportExportMixin

from . import models


@admin.register(models.Image)
class ImageAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('name', )
    list_filter = ('name', )
    date_hierarchy = 'ts'
