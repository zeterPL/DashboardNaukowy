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

def updateTableByApi(request, metric_name):
    universityList = University.objects.values_list('id', flat=True)
    mainSubjectsList = SubjectArea.objects.values_list('id', flat=True)
    if(metric_name in {"ScholarlyOutput", "FieldWeightedCitationImpact", "CitationsPerPublication","CitationCount"}):
        updateTableByApiSimpleType(metric_name, universityList, mainSubjectsList)
    elif(metric_name in {"Collaboration", "CollaborationImpact"}):
        updateTableByApiCollaborationType(metric_name, universityList, mainSubjectsList)
    else:
        print("\nNot implemented yet\n")
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    else:
        return redirect('/admin/mainApp')

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

def updateTableByApiSimpleType(metricType, universityList, mainSubjectsList):
    model_obj = globals()[metricType]
    #model_obj.objects.all().delete() #usuwanie wszystkich rekordow z danej tabeli
    for university in universityList:
        for subject in mainSubjectsList:
            requestURL = "https://api.elsevier.com/analytics/scival/institution/metrics?metricTypes=" + metricType + "&institutionIds=" + str(university) + "&yearRange=10yrs&subjectAreaFilterURI=Class%2FASJC%2FCode%2F" + str(subject) + "&includeSelfCitations=true&byYear=true&includedDocs=AllPublicationTypes&journalImpactType=CiteScore&showAsFieldWeighted=false&apiKey=" + API_KEY
            requestURL2 = "https://api.elsevier.com/analytics/scival/institution/metrics?metricTypes=" + metricType + "&institutionIds=" + str(university) + "&yearRange=3yrsAndCurrentAndFuture&subjectAreaFilterURI=Class%2FASJC%2FCode%2F" + str(subject) + "&includeSelfCitations=true&byYear=true&includedDocs=AllPublicationTypes&journalImpactType=CiteScore&showAsFieldWeighted=false&apiKey=" + API_KEY
            response = requests.get(requestURL)
            response2 = requests.get(requestURL2)
            valuesFromLast10years = response.json()['results'][0]['metrics'][0]['valueByYear']
            valuesFromLast3yearsAndFuture = response2.json()['results'][0]['metrics'][0]['valueByYear']
            amountInYear, years = extractDataFromJsonToArrays(valuesFromLast10years, valuesFromLast3yearsAndFuture)
            for indx, y in enumerate(years):
                # model_obj.objects.create(year=y, value=amountInYear[indx], universityId=University.objects.get(id=university), subjectAreaId=SubjectArea.objects.get(id=subject)) #wersja z usuwaniem wszystkich rekordow
                try:
                    metric = model_obj.objects.get(year=y, universityId=University.objects.get(id=university), subjectAreaId=SubjectArea.objects.get(id=subject))
                    metric.value = amountInYear[indx]
                    metric.save()
                except model_obj.DoesNotExist:
                    model_obj.objects.create(year=y, value=amountInYear[indx], universityId=University.objects.get(id=university), subjectAreaId=SubjectArea.objects.get(id=subject))

def saveToDatabaseCollaboration(model_obj, metricType, universityID, subjectAreaID, InstitutionalValues, InternationalValues, NationalValues, SingleAuthorshipValues, InstitutionalPercentageValues=None, InternationalPercentageValues=None, NationalPercentageValues=None, SingleAuthorshipPercentageValues=None):
    for year, InstitutionalValue in InstitutionalValues.items():
        InternationalValue = InternationalValues.get(year)
        NationalValue = NationalValues.get(year)
        SingleAuthorshipValue = SingleAuthorshipValues.get(year)
        if (metricType == "Collaboration"):
            InstitutionalPercentageValue = InstitutionalPercentageValues.get(year)
            InternationalPercentageValue = InternationalPercentageValues.get(year)
            NationalPercentageValue = NationalPercentageValues.get(year)
            SingleAuthorshipPercentageValue = SingleAuthorshipPercentageValues.get(year)
        try:
            metric = model_obj.objects.get(year=year, universityId=universityID, subjectAreaId=subjectAreaID)
            metric.InstitutionalValue = InstitutionalValue
            metric.InternationalValue = InternationalValue
            metric.NationalValue = NationalValue
            metric.SingleAuthorshipValue = SingleAuthorshipValue
            if(metricType == "Collaboration"):
                metric.InstitutionalPercentageValue = InstitutionalPercentageValue
                metric.InternationalPercentageValue = InternationalPercentageValue
                metric.NationalPercentageValue = NationalPercentageValue
                metric.SingleAuthorshipPercentageValue = SingleAuthorshipPercentageValue
            metric.save()
        except model_obj.DoesNotExist:
            if (metricType == "Collaboration"):
                model_obj.objects.create(year=year, universityId=universityID, subjectAreaId=subjectAreaID, InstitutionalValue=InstitutionalValue,
                                     InternationalValue=InternationalValue, NationalValue=NationalValue, SingleAuthorshipValue=SingleAuthorshipValue, InstitutionalPercentageValue=InstitutionalPercentageValue,
                                     InternationalPercentageValue=InternationalPercentageValue, NationalPercentageValue=NationalPercentageValue, SingleAuthorshipPercentageValue=SingleAuthorshipPercentageValue)
            else:
                model_obj.objects.create(year=year, universityId=universityID, subjectAreaId=subjectAreaID, InstitutionalValue=InstitutionalValue,
                                         InternationalValue=InternationalValue, NationalValue=NationalValue, SingleAuthorshipValue=SingleAuthorshipValue)

def getValuesFromCollabType(values, valuesNew, collabType, metricType):
    dict = next(item for item in values if item['collabType'] == collabType)
    dict2 = next(item for item in valuesNew if item['collabType'] == collabType)
    last_two_records_value = list(dict2['valueByYear'].keys())[-2:]
    dict['valueByYear'].update({key: value for key, value in dict2['valueByYear'].items() if key in last_two_records_value})
    if(metricType == "Collaboration"):
        last_two_records_percentage = list(dict2['percentageByYear'].keys())[-2:]
        dict['percentageByYear'].update({key: value for key, value in dict2['percentageByYear'].items() if key in last_two_records_percentage})
        return dict['valueByYear'], dict['percentageByYear']
    else:
        return dict['valueByYear']

def updateTableByApiCollaborationType(metricType, universityList, mainSubjectsList):
    model_obj = globals()[metricType]
    #model_obj.objects.all().delete() #usuwanie wszystkich rekordow z danej tabeli
    for university in universityList:
        for subject in mainSubjectsList:
            requestURL = "https://api.elsevier.com/analytics/scival/institution/metrics?metricTypes=" + metricType + "&institutionIds=" + str(university) + "&yearRange=10yrs&subjectAreaFilterURI=Class%2FASJC%2FCode%2F" + str(subject) + "&includeSelfCitations=true&byYear=true&includedDocs=AllPublicationTypes&journalImpactType=CiteScore&showAsFieldWeighted=false&apiKey=" + API_KEY
            requestURL2 = "https://api.elsevier.com/analytics/scival/institution/metrics?metricTypes=" + metricType + "&institutionIds=" + str(university) + "&yearRange=3yrsAndCurrentAndFuture&subjectAreaFilterURI=Class%2FASJC%2FCode%2F" + str(subject) + "&includeSelfCitations=true&byYear=true&includedDocs=AllPublicationTypes&journalImpactType=CiteScore&showAsFieldWeighted=false&apiKey=" + API_KEY
            response = requests.get(requestURL)
            response2 = requests.get(requestURL2)
            valuesFromLast10years = response.json()['results'][0]['metrics'][0]['values']
            valuesFromLast3yearsAndFuture = response2.json()['results'][0]['metrics'][0]['values']
            universityId = University.objects.get(id=university)
            subjectAreaId = SubjectArea.objects.get(id=subject)
            if(metricType == "Collaboration"):
                valueInstitutional, percentagevalueInstitutional = getValuesFromCollabType(valuesFromLast10years,valuesFromLast3yearsAndFuture, 'Institutional collaboration', metricType)
                valueInternational, percentagevalueInternational = getValuesFromCollabType(valuesFromLast10years, valuesFromLast3yearsAndFuture, 'International collaboration', metricType)
                valueNational, percentagevalueNational = getValuesFromCollabType(valuesFromLast10years, valuesFromLast3yearsAndFuture, 'National collaboration', metricType)
                valueSingleAuthorship, percentagevalueSingleAuthorship = getValuesFromCollabType(valuesFromLast10years, valuesFromLast3yearsAndFuture, 'Single authorship', metricType)
                saveToDatabaseCollaboration(model_obj, metricType, universityId, subjectAreaId, valueInstitutional, valueInternational, valueNational, valueSingleAuthorship, percentagevalueInstitutional, percentagevalueInternational, percentagevalueNational, percentagevalueSingleAuthorship)
            else:
                valueInstitutional = getValuesFromCollabType(valuesFromLast10years, valuesFromLast3yearsAndFuture, 'Institutional collaboration', metricType)
                valueInternational = getValuesFromCollabType(valuesFromLast10years, valuesFromLast3yearsAndFuture, 'International collaboration', metricType)
                valueNational = getValuesFromCollabType(valuesFromLast10years, valuesFromLast3yearsAndFuture, 'National collaboration', metricType)
                valueSingleAuthorship = getValuesFromCollabType(valuesFromLast10years, valuesFromLast3yearsAndFuture, 'Single authorship', metricType)
                saveToDatabaseCollaboration(model_obj, metricType, universityId, subjectAreaId, valueInstitutional, valueInternational, valueNational, valueSingleAuthorship)

# def updateDatabaseByApi(request):
#     metricTypes = ["OutputsInTopCitationPercentiles", "PublicationsInTopJournalPercentiles", "ScholarlyOutput", "FieldWeightedCitationImpact", "CollaborationImpact", "CitationsPerPublication", "CitationCount", "Collaboration"]
#     universityList = University.objects.values_list('id', flat=True)
#     mainSubjectsList = SubjectArea.objects.values_list('id', flat=True)
#     for metricType in metricTypes:
#         updateTableByApi(metricType, universityList, mainSubjectsList)
#     referer = request.META.get('HTTP_REFERER')
#     if referer:
#         return redirect(referer)
#     else:
#         return redirect('/admin/mainApp')

# def updateTableByApiSimpleType(metricType, universityList, mainSubjectsList):
#     model_obj = globals()[metricType]
#     #model_obj.objects.all().delete() #usuwanie wszystkich rekordow z danej tabeli
#     for university in universityList:
#         for subject in mainSubjectsList:
#             requestURL = "https://api.elsevier.com/analytics/scival/institution/metrics?metricTypes=" + metricType + "&institutionIds=" + str(university) + "&yearRange=10yrs&subjectAreaFilterURI=Class%2FASJC%2FCode%2F" + str(subject) + "&includeSelfCitations=true&byYear=true&includedDocs=AllPublicationTypes&journalImpactType=CiteScore&showAsFieldWeighted=false&apiKey=" + API_KEY
#             requestURL2 = "https://api.elsevier.com/analytics/scival/institution/metrics?metricTypes=" + metricType + "&institutionIds=" + str(university) + "&yearRange=3yrsAndCurrentAndFuture&subjectAreaFilterURI=Class%2FASJC%2FCode%2F" + str(subject) + "&includeSelfCitations=true&byYear=true&includedDocs=AllPublicationTypes&journalImpactType=CiteScore&showAsFieldWeighted=false&apiKey=" + API_KEY
#             response = requests.get(requestURL)
#             response2 = requests.get(requestURL2)
#             if (metricType in {"ScholarlyOutput", "FieldWeightedCitationImpact", "CitationsPerPublication","CitationCount"}):
#                 valuesFromLast10years = response.json()['results'][0]['metrics'][0]['valueByYear']
#                 valuesFromLast3yearsAndFuture = response2.json()['results'][0]['metrics'][0]['valueByYear']
#             else:
#                 valuesFromLast10years = response.json()['results'][0]['metrics'][0]['values'][0]['valueByYear']
#                 valuesFromLast3yearsAndFuture = response2.json()['results'][0]['metrics'][0]['values'][0]['valueByYear']
#             amountInYear, years = extractDataFromJsonToArrays(valuesFromLast10years, valuesFromLast3yearsAndFuture)
#             for indx, y in enumerate(years):
#                 # model_obj.objects.create(year=y, value=amountInYear[indx], universityId=University.objects.get(id=university), subjectAreaId=SubjectArea.objects.get(id=subject)) #wersja z usuwaniem wszystkich rekordow
#                 try:
#                     metric = model_obj.objects.get(year=y, universityId=University.objects.get(id=university), subjectAreaId=SubjectArea.objects.get(id=subject))
#                     metric.value = amountInYear[indx]
#                     metric.save()
#                 except model_obj.DoesNotExist:
#                     model_obj.objects.create(year=y, value=amountInYear[indx], universityId=University.objects.get(id=university), subjectAreaId=SubjectArea.objects.get(id=subject))