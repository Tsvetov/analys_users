# -*- coding: utf-8 -*-

from django.conf.urls import url

from analys_users.views import UsersView
from analys_users.views import res_view


urlpatterns = [
    url(r'^users_check/$', UsersView.as_view()),
    url(r'^res/$', res_view)
]
