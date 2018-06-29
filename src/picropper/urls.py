# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.urls import path
from django.views.generic import TemplateView

from . import views as v

app_name = 'picropper'

urlpatterns = [
    path('', TemplateView.as_view(template_name="picropper/base.html")),
    path('image/list', v.ImageList.as_view(), name='ImageList'),
    path('image/create', v.ImageCreate.as_view(), name='ImageCreate'),
    path('image/<int:pk>/', v.ImageDetail.as_view(), name='ImageDetail'),
]
