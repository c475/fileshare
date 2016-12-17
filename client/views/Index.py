from credentials import CROSSBAR_KEY
from django.shortcuts import render
from django.auth.decorators import login_required


def generate_key()


# Create your views here.
@login_required
def Index(request):
	render(request, "index.html", context=)
