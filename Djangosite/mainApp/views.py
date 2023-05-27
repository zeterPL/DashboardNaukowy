from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth

from .API_Itf import API_Interface
from .models import *
from django.template import loader

from django.contrib.auth.models import User, auth
from .forms import EditProfileForm

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
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home-page')
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('login')
    else:
        return render(request, "mainApp/login.html")


def logout(request):
    auth.logout(request)
    return redirect('welcome-page')


def home(request):
    if request.user.is_authenticated:    
         return render(request, 'mainApp/home.html')
    else:
        return redirect('welcome-page')


def benchmarking(request):
    return render(request, "mainApp/benchmarking.html")


def profile(request):
    if request.user.is_authenticated:    
         return render(request, 'mainApp/profile.html')
    else:
        return redirect('welcome-page')



def roboczy_view_do_testowania_bazy(request):
    interface = API_Interface()
    # interface.db_update_metric(CitationCount)
    cc = CitationCount.objects.all().values()
    template = loader.get_template('view.html')
    context = {
        'cc': cc,
    }
    return HttpResponse(template.render(context, request))
    


def edit(request):
    if request.user.is_authenticated:    
         if request.method == 'POST':
            form = EditProfileForm(request.POST, instance=request.user)
            if form.is_valid:
                 form.save()
                 return redirect('profile-page')
            else:
                #TODO
                return render(request, 'mainApp/edit.html', form)
         else:
            form = EditProfileForm(instance=request.user)
            args = {
            'form': form,
            }
            return render(request, 'mainApp/edit.html', args)
           
    else:
        return redirect('welcome-page')
