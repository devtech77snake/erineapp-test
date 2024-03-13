from .bus_views import *
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


# Create your views here.
def hello(request):
    template = loader.get_template("hello.html")
    return HttpResponse(template.render())
    # return HttpResponse("hello world")
