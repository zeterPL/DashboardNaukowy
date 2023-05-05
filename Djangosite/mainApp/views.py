from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse


def welcome(request):
    return render(request, "mainApp/welcome.html")

def about(request):
    return render(request, "mainApp/about.html")

def contact(request):
    return render(request, "mainApp/contact.html")

def features(request):
    return render(request, "mainApp/features.html")

def login(request):
    return render(request, "mainApp/login.html")

def home(request):
    return render(request, "mainApp/home.html")

def benchmarking(request):
    return render(request, "mainApp/benchmarking.html")

def user(request):
    return render(request, "mainApp/profile.html")