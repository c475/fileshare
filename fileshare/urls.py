from django.conf.urls import url
from django.contrib.auth.views import logout
from client.views import *


urlpatterns = [
    url(r'^index/', Index),
    url(r'^register/', Register.as_view()),
    url(r'^logout/$', logout, {'next_page': '/'}),
    url(r'^login/$', custom_login),
]
