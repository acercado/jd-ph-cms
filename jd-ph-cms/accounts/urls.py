# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    # URL pattern for the UserListView
    url(
        regex=r'^$',
        view=views.index,
        name='account_index'
    ),
    url(
        regex=r'^edit/(?P<pk>[0-9]+)$',
        view=views.edit,
        name='edit'
    ),

]
