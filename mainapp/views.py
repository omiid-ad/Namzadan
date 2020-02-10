from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return HttpResponse("landing page")


def contact_us(request):
    return HttpResponse("contact us page")


def candidates(request):
    return HttpResponse("candidates page")

# search views
