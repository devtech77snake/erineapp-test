from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def bus_list(request):
    return HttpResponse("this is bus list")


def reserve_seat(request):
    return HttpResponse("this is reserve seat")


def unreserve_seat(request):
    return HttpResponse("this is unreserve seat")
