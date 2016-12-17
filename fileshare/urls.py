from django.conf.urls import url
from client.views import *


urlpatterns = [
    url(r'^index/', Index),
    url(r'^register/', Register.as_view()),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^login/$', Login.custom_login),
]
