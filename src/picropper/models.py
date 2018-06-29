# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from filer.fields.image import FilerImageField


class Image(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'), on_delete=models.CASCADE, blank=True, null=True)
    ts = models.DateTimeField(auto_now=True)
    file = FilerImageField(null=True, blank=True, related_name="logo_company", on_delete=models.CASCADE)

    class Meta:
        default_related_name = "images"
        verbose_name = _('image')
        verbose_name_plural = _('images')
