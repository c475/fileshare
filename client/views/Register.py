from client.models import User
from client.forms import UserCreationForm
from client.mixins import NotLoggedInRequired
from django.views.generic.edit import CreateView
from django.contrib.auth import (
    login,
    authenticate
)


class Register(NotLoggedInRequired, CreateView):
    model = User
    template_name = 'registration/register.html'
    success_url = '/'
    form_class = UserCreationForm

    def get_success_url(self):
        new_user = authenticate(
            username=self.request.POST.get("username", None),
            password=self.request.POST.get("password1", None)
        )

        if new_user is not None:
            login(self.request, new_user)

        return super(Register, self).get_success_url()
