from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from .forms import EditProfileForm

from .models import *
import json
import requests
API_KEY  = '7f59af901d2d86f78a1fd60c1bf9426a'
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

def extractDataFromJsonToArrays(dataFromApi, dataFromApi2):
    yearRange = len(dataFromApi) + len(dataFromApi2) - 3
    years = []
    for i in range(yearRange - 1, -1, -1):
        years.append(str(2023 - i))
    #print(years)
    valuesOverTheYears = []
    for i in range(len(dataFromApi)):
        valuesOverTheYears.append(dataFromApi[years[i]])
    for i in range(len(dataFromApi), len(dataFromApi)+2):
        valuesOverTheYears.append(dataFromApi2[years[i]])
    #print(valuesOverTheYears)
    return valuesOverTheYears, years

def updateDatabaseByApi(request):
    metricTypes = ["OutputsInTopCitationPercentiles", "PublicationsInTopJournalPercentiles", "ScholarlyOutput", "FieldWeightedCitationImpact", "CollaborationImpact", "CitationsPerPublication", "CitationCount", "Collaboration"]
    universityList = University.objects.values_list('id', flat=True)
    mainSubjectsList = SubjectArea.objects.values_list('id', flat=True)
    for metricType in metricTypes:
        model_obj = globals()[metricType]
        #model_obj.objects.all().delete()
        for university in universityList:
            for subject in mainSubjectsList:
                requestURL = "https://api.elsevier.com/analytics/scival/institution/metrics?metricTypes=" + metricType + "&institutionIds=" + str(university) + "&yearRange=10yrs&subjectAreaFilterURI=Class%2FASJC%2FCode%2F" + str(subject) + "&includeSelfCitations=true&byYear=true&includedDocs=AllPublicationTypes&journalImpactType=CiteScore&showAsFieldWeighted=false&apiKey=" + API_KEY
                requestURL2 = "https://api.elsevier.com/analytics/scival/institution/metrics?metricTypes=" + metricType + "&institutionIds=" + str(university) + "&yearRange=3yrsAndCurrentAndFuture&subjectAreaFilterURI=Class%2FASJC%2FCode%2F" + str(subject) + "&includeSelfCitations=true&byYear=true&includedDocs=AllPublicationTypes&journalImpactType=CiteScore&showAsFieldWeighted=false&apiKey=" + API_KEY
                response = requests.get(requestURL)
                response2 = requests.get(requestURL2)
                if (metricType in {"ScholarlyOutput", "FieldWeightedCitationImpact", "CitationsPerPublication", "CitationCount"}):
                    valuesFromLast10years = response.json()['results'][0]['metrics'][0]['valueByYear']
                    valuesFromLast3yearsAndFuture = response2.json()['results'][0]['metrics'][0]['valueByYear']
                else:
                     valuesFromLast10years = response.json()['results'][0]['metrics'][0]['values'][0]['valueByYear']
                     valuesFromLast3yearsAndFuture = response2.json()['results'][0]['metrics'][0]['values'][0]['valueByYear']
                amountInYear, years = extractDataFromJsonToArrays(valuesFromLast10years, valuesFromLast3yearsAndFuture)
                for indx, y in enumerate(years):
                    #model_obj.objects.create(year=y, value=amountInYear[indx], universityId=University.objects.get(id=university), subjectAreaId=SubjectArea.objects.get(id=subject))
                    metric, created = model_obj.objects.get_or_create(year=y, universityId=University.objects.get(id=university), subjectAreaId=SubjectArea.objects.get(id=subject))
                    if not created:
                        metric.value = amountInYear[indx]
                        metric.save()
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    else:
        return redirect('/admin/mainApp')