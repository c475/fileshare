from django.http import HttpResponseRedirect
from django.contrib.auth.views import login
from client.mixins import NotLoggedInRequired


def custom_login(request, **kwargs):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")
    else:
        return login(request, **kwargs)


class Login(NotLoggedInRequired, TemplateView):
    template_name = 'login.html'
