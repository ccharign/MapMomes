# -*- coding:utf-8 -*-
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path("recherche/", views.recherche, name="recherche")
    ]
