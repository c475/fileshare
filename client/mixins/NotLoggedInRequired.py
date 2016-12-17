from django.http import HttpResponseRedirect


class NotLoggedInRequired(object):
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_anonymous():
            return super(NotLoggedInRequired, self).dispatch(*args, **kwargs)
        else:
            return HttpResponseRedirect('/')
