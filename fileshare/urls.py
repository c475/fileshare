from django.conf.urls import url
from django.contrib.auth.views import logout
from client.views import *


urlpatterns = [
    url(r'^$', Index),
    url(r'^index/$', Index, name='index'),
    url(r'^register/$', Register.as_view(), name='register'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
    url(r'^login/$', custom_login, name='login'),
]
