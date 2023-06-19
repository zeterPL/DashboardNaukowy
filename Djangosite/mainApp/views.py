import random
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from .forms import EditProfileForm

# Charts
from .models import CitationCount, Collaboration, CollaborationImpact, FieldWeightedCitationImpact, OutputsInTopCitationPercentiles, PublicationsCountPerYear, PublicationsInTopJournalPercentiles, ScholarlyOutput, SubjectArea, University
import plotly.express as px
import plotly.graph_objs as go
from .forms import BenchmarkingForm, CitationDistributionForm, CitationsPerYearForm
from datetime import datetime
from django.db.models.functions import Coalesce
from django.forms.models import model_to_dict
from django.core import serializers
import pandas as pd

class Object:
    pass

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

    # Default data
    universities = ['Białystok University of Technology']
    metric = 'CitationCount'
    subjectArea = 'Computer Science'
    start = 2012
    end = 2021

    # From data
    if request.POST:
        universities = request.POST.getlist('university')
        metric = request.POST.get('metric')
        subjectArea = request.POST.get('subject_area')
        start = int(request.POST.get('start'))
        end = int(request.POST.get('end'))

    # Create dataset
    dataset = []

    metricModel = ''
    metricName = ''
    if (metric == 'CitationCount'):
        metricModel = CitationCount
        metricName = 'Liczba cytowań'

    if (metric == 'Collaboration'):
        metricModel = Collaboration
        metricName = 'Współpraca'

    if (metric == 'CollaborationImpact'):
        metricModel = CollaborationImpact
        metricName = 'Współpraca - impakt'

    if (metric == 'FieldWeightedCitationImpact'):
        metricModel = FieldWeightedCitationImpact
        metricName = 'Cytowania - impakt'

    if (metric == 'OutputsInTopCitationPercentiles'):
        metricModel = OutputsInTopCitationPercentiles
        metricName = 'OutputsInTopCitationPercentiles (?)'

    if (metric == 'PublicationsInTopJournalPercentiles'):
        metricModel = PublicationsInTopJournalPercentiles
        metricName = 'PublicationsInTopJournalPercentiles (?)'

    if (metric == 'ScholarlyOutput'):
        metricModel = ScholarlyOutput
        metricName = 'Liczba publikacji'

    subjectAreaObject = SubjectArea.objects.get(name=subjectArea)

    for university in universities:
        universityObject = University.objects.get(name=university)
        print(universityObject.id)
        for x in (range(start, end)):
            value = metricModel.objects.all().filter(
                year=x,
                universityId_id=universityObject.id,
                subjectAreaId_id=subjectAreaObject.id).first().value

            if value is None:
                value = 0

            entry = {
                "university": university,
                "year": x,
                "value": value
            }
            dataset.append(entry)

    # Create chart
    fig = px.line(
        dataset,
        x="year",
        y="value",
        color="university",
        color_discrete_sequence=px.colors.sequential.YlGnBu,
        markers=True)

    # Chart settings
    fig.update_layout(
        yaxis_title=metricName,
        xaxis_title='Rok',
        showlegend=True,
        autosize=True,
        height=575,
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font_color="rgba(255, 255, 255, 0.8)",
        legend_title_text="Uczelnia",
        legend=dict(
            orientation="v",
            entrywidth=20
        ),
        xaxis=dict(
            tickmode='linear',
            color="rgba(255, 255, 255, 0.75)",
            tick0=0,
            dtick=1,
        ),
        yaxis=dict(
            color="rgba(255, 255, 255, 0.75)",
            tick0=0,
        ),
        margin=dict(l=20, r=20, t=40, b=0),)

    fig.update_xaxes(
        gridcolor='rgba(0, 0, 0, 0.2)',
        zerolinecolor='rgba(0, 0, 0, 0.4)'
    )

    fig.update_yaxes(
        gridcolor='rgba(0, 0, 0, 0.2)',
        zerolinecolor='rgba(0, 0, 0, 0.4)'
    )

    # Convert chart object to html
    chart = fig.to_html()

    context = {
        'viewName': 'Główny dashboard',
        'link': 'home-link',
        'form': BenchmarkingForm(
            initial={
                'universities': universities,
                'metric': metric,
                'subject_area': subjectArea,
                'start': start,
                'end': end
            }
        ),
        'chart': chart
    }

    if request.user.is_authenticated:    
         return render(request, "mainApp/home.html", context)
    else:
        return redirect('welcome-page')



def benchmarking(request):
    context = {
        'viewName': 'Porównanie uczelni',
        'link': 'benchmarking-link'
    }
    return render(request, "mainApp/benchmarking.html", context)


def profile(request):
    context = {
        'viewName': 'Profil użytkownika',
        'link': 'profile-link'
    }
    return render(request, 'mainApp/profile.html', context)


def statistics(request):

    # Get the data from the database
    university = University.objects.get(id=327002)
    startDate = CitationCount.objects.all().values_list(
        'year', flat=True).distinct().first()
    endDate = CitationCount.objects.all().values_list(
        'year', flat=True).distinct().last()
    xData = CitationCount.objects.all().values_list('year', flat=True).distinct()
    yData = CitationCount.objects.filter(
        universityId=university.id, subjectAreaId=10).values_list('value', flat=True)

    # ---- Line chart ---- #
    # Get the data from the form
    start = request.GET.get('start')
    end = request.GET.get('end')
    selectedUniversity = request.GET.get('university')
    # selectedSubjectAera

    # Filter the data according to the form input
    if selectedUniversity:
        university = University.objects.all().filter(
            name=selectedUniversity).first()
    if start:
        startDate = start
        xData = CitationCount.objects.all().values_list(
            'year', flat=True).distinct().filter(year__gte=start)
        citations = CitationCount.objects.filter(
            universityId=university.id, subjectAreaId=10).values_list('value', flat=True).filter(year__gte=start).filter(year__lte=end)
        yData = [0 if citation is None else citation for citation in citations]

    if end:
        endDate = end
        xData = CitationCount.objects.all().values_list(
            'year', flat=True).distinct().filter(year__lte=end)
        citations = CitationCount.objects.filter(
            universityId=university.id, subjectAreaId=10).values_list('value', flat=True).filter(year__gte=start).filter(year__lte=end)
        yData = [0 if citation is None else citation for citation in citations]

    # Create a chart
    fig = px.line(
        x=xData,
        y=yData,
        title='Cytowania dla {university} w latach {startDate}-{endDate}'.format(
            university=university.name, startDate=startDate, endDate=endDate),
        labels={
            'x': 'Rok',
            'y': 'Liczba cytowań'
        },
    )

    fig.update_layout(
        autosize=True,
        height=250,
        title_pad=dict(l=-30, b=5),
        title_font_size=14,
        title_font_color='white',
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        xaxis=dict(
            tickmode='linear',
            color="rgba(255, 255, 255, 0.75)",
            tick0=0.5,
            dtick=0.75
        ),
        yaxis=dict(
            color="rgba(255, 255, 255, 0.75)",
            tick0=0,
        ),
        margin=dict(l=20, r=20, t=40, b=0),
    )

    fig.update_xaxes(
        gridcolor='rgba(0, 0, 0, 0.2)',
        zerolinecolor='rgba(0, 0, 0, 0.4)'
    )

    fig.update_yaxes(
        gridcolor='rgba(0, 0, 0, 0.2)',
        zerolinecolor='rgba(0, 0, 0, 0.4)'
    )

    fig.update_traces(
        line_color=' #00afa4'
    )

    chart = fig.to_html()

    # ---- Donut chart ---- #
    # Dla uczelni wyświetl analizę:
    #  - Liczba cytowań/wydział
    #  - Liczba publikacji/wydział

    # Get the data from the database
    #  - Uczelnie
    #  - Dziedziny naukowe
    #  - Cytowania danej uczelni

    # Z formularza wybierz:
    #  - rodzaj danych (cytowania, publikacje)
    #  - uczelnię
    #  - przedział czasowy

    # Get the data from the form
    dataType = request.GET.get('dataType')

    # Create dataset based on the form input
    dataSet = []
    subjectAreasIds = CitationCount.objects.all().filter(
        universityId=university.id).values_list('subjectAreaId',
                                                flat=True).distinct()
    subjectAreaNames = SubjectArea.objects.all(
    ).values_list('name', flat=True).distinct()

    if (dataType == 'citations'):
        for subjectAreaId in subjectAreasIds:
            citationCount = CitationCount.objects.all().filter(
                universityId=university.id,
                year=2012,
                subjectAreaId=subjectAreaId).values_list('value', flat=True)[0]
            print(citationCount)
            dataSet.append(citationCount)
            title = 'Dziedziny cytowań'
    else:
        for subjectAreaId in subjectAreasIds:
            publicationCount = ScholarlyOutput.objects.all().filter(
                universityId=university.id,
                year=2012,
                subjectAreaId=subjectAreaId).values_list('value', flat=True)[0]
            dataSet.append(publicationCount)
            title = 'Dziedziny publikacji'

    # Create chart
    x = 10
    y = 15
    print(dataSet)
    pull = [0.1 for _ in range(len(dataSet)+10)]
    pieChart = px.pie(values=dataSet[x: y],
                      names=subjectAreaNames[x: y],
                      hole=.8,
                      color_discrete_sequence=px.colors.sequential.Bluyl)

    # Chart settings
    pieChart.update_traces(
        textposition='inside',
        textinfo='percent+label')

    pieChart.update_layout(
        font_color="rgba(255, 255, 255, 0.8)",
        uniformtext_minsize=12,
        uniformtext_mode='hide',
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        legend=dict(
            orientation="h",
            entrywidth=70,
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ))

    pieChart.add_annotation(x=0.5, y=0.55,
                            text=title,
                            font=dict(size=18,
                                      color='rgba(255, 255, 255, 1)'),
                            showarrow=False)

    pieChart.add_annotation(x=0.5, y=0.45,
                            text=f'Lata {startDate}-{endDate}',
                            font=dict(size=14,
                                      color='rgba(255, 255, 255, 0.8)'),
                            showarrow=False)

    # Convert chart to HTML
    pieChartHTML = pieChart.to_html()

    context = {
        'viewName': 'Statystyki uczelni',
        'link': 'statistics-link',
        'publicationsPerYearChart': chart,
        'pieChart': pieChartHTML,
        'form': CitationsPerYearForm(initial={
            'university': university.name,
            'start': startDate,
            'end': endDate
        }),
        'donutChartForm': CitationDistributionForm(initial={
            'dataType': 'Liczba cytowań'
        })
    }

    if request.user.is_authenticated:    
         return render(request, 'mainApp/statistics.html', context)
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
