from django.shortcuts import render
from django.auth.decorators import login_required


# Create your views here.
@login_required
def Index(request):
	render(request, "index.html", context={
		'user': request.user
	})
