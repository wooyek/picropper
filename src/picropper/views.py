# -*- coding: utf-8 -*-
from django.shortcuts import resolve_url
from django_powerbank.views.auth import AbstractAuthorizedView, AuthenticatedView
from filer.models import Image
from pascal_templates import ListView
from pascal_templates.views import CreateView, DetailView

from . import models


class ImageList(AuthenticatedView, ListView):
    template_name = "picropper/Image/list.html"
    model = Image
    paginate_by = 50


class ImageCreate(AuthenticatedView, CreateView):
    model = Image
    fields = ('name',)

    def get_success_url(self):
        return resolve_url("picropper:SampleDetail", self.object.pk)


class ImageDetail(AuthenticatedView, DetailView):
    template_name = "picropper/Image/detail.html"
    model = Image

    def get_context_data(self, **kwargs):
        from filer.models import ThumbnailOption
        options = ThumbnailOption.objects.all()
        # thumbnailer = self.object.file.easy_thumbnails_thumbnailer
        thumbnailer = self.object.easy_thumbnails_thumbnailer
        versions = [(option.name, thumbnailer.get_thumbnail(option.as_dict)) for option in options]
        return super().get_context_data(versions=versions, **kwargs)

