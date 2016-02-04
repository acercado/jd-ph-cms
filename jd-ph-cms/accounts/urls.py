# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

# app_name = 'accounts'
urlpatterns = [
    url(
        regex=r'^$',
        view=views.index,
        name='account_index'
    ),
    url(
        regex=r'^something/$',
        view=views.something,
        name='account_something'
    ),
    url(
        regex=r'^edit/(?P<pk>[0-9]+)/$',
        view=views.edit,
        name='edit'
    ),

]
