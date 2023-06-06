from django.contrib import admin
from django.urls import path
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django.apps import apps
from .models import *

from django.shortcuts import render, redirect
import requests

API_KEY = '7f59af901d2d86f78a1fd60c1bf9426a'


# Username: Admin
# email: admin@mail.com
# Pass: 123

# drugi admin dla leniwych
# Username: admin
# Pass: admin

class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()

def get_model_columns(model_name):
    model = apps.get_model(app_label='mainApp', model_name=model_name)
    if model:
        return [field.name for field in model._meta.get_fields()]

import os
import csv
def save_to_csv(modeladmin, request, queryset):
    print()
save_to_csv.short_description = "Save selected records to CSV file"


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country')
    list_filter = ('country',)
    search_fields = ('name', 'country')
    ordering = ('name', 'country', 'id')
    actions = [save_to_csv]

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-textFile/', self.upload_textFile), ]
        return new_urls + urls

    def upload_textFile(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]
            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.replace('\r', '').split("\n")
            for x in csv_data:
                fields = x.split(";")
                if len(fields) < 3:
                    countryX = 'Polska'
                else:
                    countryX = fields[2]
                created = University.objects.update_or_create(
                    id=fields[0],
                    name=fields[1],
                    country=countryX,
                )
            url = reverse('admin:mainApp_university_changelist')
            return HttpResponseRedirect(url)
        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/textFile_upload.html", data)


opis = "Domyślnie Uri jest tworzone 'Class/ASJC/Code/id' ale można zdefiniować własne"


@admin.register(SubjectArea)
class SubjectAreaAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Wymagane:', {
            'fields': ('id', 'name',),
        }),
        ('Dodatkowe', {
            'fields': ('uri',),
            'description': '%s' % opis,
            'classes': ('collapse',),
        }),
    )
    list_display = ('id', 'name', 'uri')
    list_filter = ('name',)
    search_fields = ('id', 'name', 'uri')
    ordering = ('name', 'id', 'uri')
    actions = [save_to_csv]

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-textFile/', self.upload_textFile), ]
        return new_urls + urls

    def upload_textFile(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]
            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.replace('\r', '').split("\n")
            for x in csv_data:
                fields = x.split(";")
                if len(fields) < 3:
                    uriFieldX = 'Class/ASJC/Code/' + fields[0]
                else:
                    uriFieldX = fields[2]
                created = SubjectArea.objects.update_or_create(
                    id=fields[0],
                    name=fields[1],
                    uri=uriFieldX,
                )
            url = reverse('admin:mainApp_subjectarea_changelist')
            return HttpResponseRedirect(url)
        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/textFile_upload.html", data)

class AbstractRangeFilter(admin.SimpleListFilter):

    def lookups(self, request, model_admin):
        return (
            ('0-10', '0-10'),
            ('10-50', '10-50'),
            ('50-100', '50-100'),
            ('100-200', '100-200'),
            ('200-500', '200-500'),
            ('500-1000', '500-1000'),
            ('1000+', '1000+'),
        )

    def queryset(self, request, queryset):
        if self.value() == '0-10':
            return queryset.filter(**{f'{self.parameter_name}__lt': 10})
        elif self.value() == '10-50':
            return queryset.filter(**{f'{self.parameter_name}__gte': 10, f'{self.parameter_name}__lt': 50})
        elif self.value() == '50-100':
            return queryset.filter(**{f'{self.parameter_name}__gte': 50, f'{self.parameter_name}__lt': 100})
        elif self.value() == '100-200':
            return queryset.filter(**{f'{self.parameter_name}__gte': 100, f'{self.parameter_name}__lt': 200})
        elif self.value() == '200-500':
            return queryset.filter(**{f'{self.parameter_name}__gte': 200, f'{self.parameter_name}__lt': 500})
        elif self.value() == '500-1000':
            return queryset.filter(**{f'{self.parameter_name}__gte': 500, f'{self.parameter_name}__lt': 1000})
        elif self.value() == '1000+':
            return queryset.filter(**{f'{self.parameter_name}__gte': 1000})
class ValueRangeFilter(AbstractRangeFilter):
    columnName = 'value'
    title, parameter_name = 'przedzial wartosci', columnName
class InstitutionalValueRangeFilter(AbstractRangeFilter):
    columnName = 'InstitutionalValue'
    title, parameter_name = 'przedzial wartosci {}'.format(AbstractMetricCollaborationType._meta.get_field(columnName).help_text), columnName
class InstitutionalPercentageValueRangeFilter(AbstractRangeFilter):
    columnName = 'InstitutionalPercentageValue'
    title, parameter_name = 'przedzial wartosci {}'.format(Collaboration._meta.get_field(columnName).help_text), columnName
class InternationalValueRangeFilter(AbstractRangeFilter):
    columnName = 'InternationalValue'
    title, parameter_name = 'przedzial wartosci {}'.format(AbstractMetricCollaborationType._meta.get_field(columnName).help_text), columnName
class InternationalPercentageValueRangeFilter(AbstractRangeFilter):
    columnName = 'InternationalPercentageValue'
    title, parameter_name = 'przedzial wartosci {}'.format(Collaboration._meta.get_field(columnName).help_text), columnName
class NationalValueRangeFilter(AbstractRangeFilter):
    columnName = 'NationalValue'
    title, parameter_name = 'przedzial wartosci {}'.format(AbstractMetricCollaborationType._meta.get_field(columnName).help_text), columnName
class NationalPercentageValueRangeFilter(AbstractRangeFilter):
    columnName = 'NationalPercentageValue'
    title, parameter_name = 'przedzial wartosci {}'.format(Collaboration._meta.get_field(columnName).help_text), columnName
class SingleAuthorshipValueRangeFilter(AbstractRangeFilter):
    columnName = 'SingleAuthorshipValue'
    title, parameter_name = 'przedzial wartosci {}'.format(AbstractMetricCollaborationType._meta.get_field(columnName).help_text), columnName
class SingleAuthorshipPercentageValueRangeFilter(AbstractRangeFilter):
    columnName = 'SingleAuthorshipPercentageValue'
    title, parameter_name = 'przedzial wartosci {}'.format(Collaboration._meta.get_field(columnName).help_text), columnName
class Threshold1ValueRangeFilter(AbstractRangeFilter):
    columnName = 'threshold1Value'
    title, parameter_name = 'przedzial wartosci {}'.format(AbstractMetricTopPercentiles._meta.get_field(columnName).help_text), columnName
class Threshold5ValueRangeFilter(AbstractRangeFilter):
    columnName = 'threshold5Value'
    title, parameter_name = 'przedzial wartosci {}'.format(AbstractMetricTopPercentiles._meta.get_field(columnName).help_text), columnName
class Threshold10ValueRangeFilter(AbstractRangeFilter):
    columnName = 'threshold10Value'
    title, parameter_name = 'przedzial wartosci {}'.format(AbstractMetricTopPercentiles._meta.get_field(columnName).help_text), columnName
class Threshold25ValueRangeFilter(AbstractRangeFilter):
    columnName = 'threshold25Value'
    title, parameter_name = 'przedzial wartosci {}'.format(AbstractMetricTopPercentiles._meta.get_field(columnName).help_text), columnName
class Threshold1PercentageValueRangeFilter(AbstractRangeFilter):
    columnName = 'threshold1PercentageValue'
    title, parameter_name = 'przedzial wartosci {}'.format(AbstractMetricTopPercentiles._meta.get_field(columnName).help_text), columnName
class Threshold5PercentageValueRangeFilter(AbstractRangeFilter):
    columnName = 'threshold5PercentageValue'
    title, parameter_name = 'przedzial wartosci {}'.format(AbstractMetricTopPercentiles._meta.get_field(columnName).help_text), columnName
class Threshold10PercentageValueRangeFilter(AbstractRangeFilter):
    columnName = 'threshold10PercentageValue'
    title, parameter_name = 'przedzial wartosci {}'.format(AbstractMetricTopPercentiles._meta.get_field(columnName).help_text), columnName
class Threshold25PercentageValueRangeFilter(AbstractRangeFilter):
    columnName = 'threshold25PercentageValue'
    title, parameter_name = 'przedzial wartosci {}'.format(AbstractMetricTopPercentiles._meta.get_field(columnName).help_text), columnName

class AbstractMetricAdmin(admin.ModelAdmin):
    list_display = ('year', 'value', 'universityId', 'subjectAreaId')
    raw_id_fields = ('universityId', 'subjectAreaId')
    list_filter = ('year', ValueRangeFilter, 'universityId', 'subjectAreaId')
    search_fields = ('year', 'value', 'universityId', 'subjectAreaId')
    ordering = ('subjectAreaId', 'universityId', 'year', 'value')
    actions = [save_to_csv]

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-textFile/', self.upload_textFile), ]
        return new_urls + urls

    def upload_textFile(self, request, model_name):
        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]
            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.replace('\r', '').split("\n")
            for x in csv_data:
                fields = x.split(";")
                model = apps.get_model('mainApp', model_name)
                if fields[3].lower() == 'none' or fields[3].lower() == 'null' or fields[3] == '':
                    fields[3] = None
                try:
                    metric = model.objects.get(year=fields[0], universityId=University.objects.get(id=fields[1]),
                                               subjectAreaId=SubjectArea.objects.get(id=fields[2]))
                    metric.value = fields[3]
                    metric.save()
                except model.DoesNotExist:
                    model.objects.create(year=fields[0], value=fields[3],
                                         universityId=University.objects.get(id=fields[1]),
                                         subjectAreaId=SubjectArea.objects.get(id=fields[2]))
            url = reverse(f'admin:mainApp_{model_name.lower()}_changelist')
            return HttpResponseRedirect(url)
        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/textFile_upload.html", data)


@admin.register(ScholarlyOutput)
class ScholarlyOutputAdmin(AbstractMetricAdmin):
    def upload_textFile(self, request, model_name='ScholarlyOutput'):
        return super().upload_textFile(request, model_name)


@admin.register(CitationCount)
class CitationCountAdmin(AbstractMetricAdmin):
    def upload_textFile(self, request, model_name='CitationCount'):
        return super().upload_textFile(request, model_name)


@admin.register(CitationsPerPublication)
class CitationsPerPublicationAdmin(AbstractMetricAdmin):
    def upload_textFile(self, request, model_name='CitationsPerPublication'):
        return super().upload_textFile(request, model_name)


@admin.register(FieldWeightedCitationImpact)
class FieldWeightedCitationImpactAdmin(AbstractMetricAdmin):
    def upload_textFile(self, request, model_name='FieldWeightedCitationImpact'):
        return super().upload_textFile(request, model_name)


class AbstractCollaborationMetricAdmin(admin.ModelAdmin):
    raw_id_fields = ('universityId', 'subjectAreaId')
    search_fields = ('year', 'universityId', 'subjectAreaId')
    ordering = ('subjectAreaId', 'universityId', 'year')
    actions = [save_to_csv]

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-textFile/', self.upload_textFile), ]
        return new_urls + urls

    def upload_textFile(self, request, model_name):
        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]
            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.replace('\r', '').split("\n")
            for x in csv_data:
                fields = x.split(";")
                model = apps.get_model('mainApp', model_name)
                for i in range(3, len(fields)):
                    if fields[i] and (fields[i].lower() == 'none' or fields[i].lower() == 'null' or fields[i] == ''):
                        fields[i] = None
                try:
                    metric = model.objects.get(year=fields[0], universityId=University.objects.get(id=fields[1]),
                                               subjectAreaId=SubjectArea.objects.get(id=fields[2]))
                    metric.InstitutionalValue = fields[3]
                    metric.InternationalValue = fields[4]
                    metric.NationalValue = fields[5]
                    metric.SingleAuthorshipValue = fields[6]
                    if model_name == "Collaboration":
                        metric.InstitutionalPercentageValue = fields[7]
                        metric.InternationalPercentageValue = fields[8]
                        metric.NationalPercentageValue = fields[9]
                        metric.SingleAuthorshipPercentageValue = fields[10]
                    metric.save()
                except model.DoesNotExist:
                    if model_name == "Collaboration":
                        model.objects.create(year=fields[0], universityId=University.objects.get(id=fields[1]),
                                             subjectAreaId=SubjectArea.objects.get(id=fields[2]),
                                             InstitutionalValue=fields[3], InternationalValue=fields[4],
                                             NationalValue=fields[5], SingleAuthorshipValue=fields[6],
                                             InstitutionalPercentageValue=fields[7],
                                             InternationalPercentageValue=fields[8], NationalPercentageValue=fields[9],
                                             SingleAuthorshipPercentageValue=fields[10])
                    else:
                        model.objects.create(year=fields[0], universityId=University.objects.get(id=fields[1]),
                                             subjectAreaId=SubjectArea.objects.get(id=fields[2]),
                                             InstitutionalValue=fields[3], InternationalValue=fields[4],
                                             NationalValue=fields[5], SingleAuthorshipValue=fields[6])
            url = reverse(f'admin:mainApp_{model_name.lower()}_changelist')
            return HttpResponseRedirect(url)
        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/textFile_upload.html", data)


@admin.register(Collaboration)
class CollaborationAdmin(AbstractCollaborationMetricAdmin):
    list_display = (
        'year', 'universityId', 'subjectAreaId', 'InstitutionalValue', 'InstitutionalPercentageValue',
        'InternationalValue', 'InternationalPercentageValue', 'NationalValue', 'NationalPercentageValue',
        'SingleAuthorshipValue', 'SingleAuthorshipPercentageValue')
    list_filter = ('year', 'universityId', 'subjectAreaId', InstitutionalValueRangeFilter, InstitutionalPercentageValueRangeFilter,
                   InternationalValueRangeFilter, InternationalPercentageValueRangeFilter,
                   NationalValueRangeFilter, NationalPercentageValueRangeFilter,
                   SingleAuthorshipValueRangeFilter, SingleAuthorshipPercentageValueRangeFilter)

    def upload_textFile(self, request, model_name='Collaboration'):
        return super().upload_textFile(request, model_name)


@admin.register(CollaborationImpact)
class CollaborationImpactAdmin(AbstractCollaborationMetricAdmin):
    list_display = (
        'year', 'universityId', 'subjectAreaId', 'InstitutionalValue', 'InternationalValue', 'NationalValue',
        'SingleAuthorshipValue')
    list_filter = ('year', 'universityId', 'subjectAreaId', InstitutionalValueRangeFilter,
                   InternationalValueRangeFilter, NationalValueRangeFilter, SingleAuthorshipValueRangeFilter)

    def upload_textFile(self, request, model_name='CollaborationImpact'):
        return super().upload_textFile(request, model_name)


class AbstractTopPercentilesMetricAdmin(admin.ModelAdmin):
    list_display = (
        'year', 'universityId', 'subjectAreaId', 'threshold1Value', 'threshold1PercentageValue', 'threshold5Value',
        'threshold5PercentageValue', 'threshold10Value', 'threshold10PercentageValue', 'threshold25Value',
        'threshold25PercentageValue')
    raw_id_fields = ('universityId', 'subjectAreaId')
    list_filter = ('year', 'universityId', 'subjectAreaId', Threshold1ValueRangeFilter, Threshold1PercentageValueRangeFilter, Threshold5ValueRangeFilter, Threshold5PercentageValueRangeFilter, Threshold10ValueRangeFilter, Threshold10PercentageValueRangeFilter, Threshold25ValueRangeFilter, Threshold25PercentageValueRangeFilter)
    search_fields = ('year', 'universityId', 'subjectAreaId')
    ordering = ('subjectAreaId', 'universityId', 'year')
    actions = [save_to_csv]

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-textFile/', self.upload_textFile), ]
        return new_urls + urls

    def upload_textFile(self, request, model_name):
        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]
            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.replace('\r', '').split("\n")
            for x in csv_data:
                fields = x.split(";")
                model = apps.get_model('mainApp', model_name)
                for i in range(3, len(fields)):
                    if fields[i] and (fields[i].lower() == 'none' or fields[i].lower() == 'null' or fields[i] == ''):
                        fields[i] = None
                try:
                    metric = model.objects.get(year=fields[0], universityId=University.objects.get(id=fields[1]),
                                               subjectAreaId=SubjectArea.objects.get(id=fields[2]))
                    metric.threshold1Value = fields[3]
                    metric.threshold1PercentageValue = fields[4]
                    metric.threshold5Value = fields[5]
                    metric.threshold5PercentageValue = fields[6]
                    metric.threshold10Value = fields[7]
                    metric.threshold10PercentageValue = fields[8]
                    metric.threshold25Value = fields[9]
                    metric.threshold25PercentageValue = fields[10]
                    metric.save()
                except model.DoesNotExist:
                    model.objects.create(year=fields[0], universityId=University.objects.get(id=fields[1]),
                                         subjectAreaId=SubjectArea.objects.get(id=fields[2]),
                                         threshold1Value=fields[3], threshold1PercentageValue=fields[4],
                                         threshold5Value=fields[5], threshold5PercentageValue=fields[6],
                                         threshold10Value=fields[7], threshold10PercentageValue=fields[8],
                                         threshold25Value=fields[9], threshold25PercentageValue=fields[10])
            url = reverse(f'admin:mainApp_{model_name.lower()}_changelist')
            return HttpResponseRedirect(url)
        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/textFile_upload.html", data)


@admin.register(PublicationsInTopJournalPercentiles)
class PublicationsInTopJournalPercentilesAdmin(AbstractTopPercentilesMetricAdmin):
    def upload_textFile(self, request, model_name='PublicationsInTopJournalPercentiles'):
        return super().upload_textFile(request, model_name)


@admin.register(OutputsInTopCitationPercentiles)
class OutputsInTopCitationPercentilesAdmin(AbstractTopPercentilesMetricAdmin):
    def upload_textFile(self, request, model_name='OutputsInTopCitationPercentiles'):
        return super().upload_textFile(request, model_name)


# Function to update all database from API
def updateDatabaseByApi(request):
    metricTypes = ["OutputsInTopCitationPercentiles", "PublicationsInTopJournalPercentiles", "ScholarlyOutput",
                   "FieldWeightedCitationImpact", "CollaborationImpact", "CitationsPerPublication", "CitationCount",
                   "Collaboration"]
    for metricType in metricTypes:
        #globals()[metricType].objects.all().delete() #usuwanie wszystkich rekordow z danej tabeli
        print("\nMetricType =", metricType)
        updateTableByApi(request, metricType, True)
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    else:
        return redirect('/admin/mainApp')


# Function to update concrect table from API
def updateTableByApi(request, metric_name, updateAllDatabase=False):
    # model_obj = globals()[metric_name]
    # model_obj.objects.all().delete() #usuwanie wszystkich rekordow z danej tabeli
    universityList = University.objects.values_list('id', flat=True)
    mainSubjectsList = SubjectArea.objects.values_list('id', flat=True)
    if metric_name in {"ScholarlyOutput", "FieldWeightedCitationImpact", "CitationsPerPublication", "CitationCount"}:
        updateTableByApiSimpleType(metric_name, universityList, mainSubjectsList)
    elif metric_name in {"Collaboration", "CollaborationImpact"}:
        updateTableByApiCollaborationType(metric_name, universityList, mainSubjectsList)
    elif metric_name in {"PublicationsInTopJournalPercentiles", "OutputsInTopCitationPercentiles"}:
        updateTableByApiTopPercentileType(metric_name, universityList, mainSubjectsList)
    else:
        print("\nNie ma takiej metryki\n")
    if updateAllDatabase is False:
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        else:
            return redirect('/admin/mainApp')


# Functions used to updated simple table with only one value
def getValuesFromSimpleType(values, valuesNew):
    years = list(values[0]['valueByYear'].keys())
    values = list(values[0]['valueByYear'].values())
    yearsNew = list(valuesNew[0]['valueByYear'].keys())[-2:]
    valuesNew = list(valuesNew[0]['valueByYear'].values())[-2:]
    years.extend(yearsNew)
    values.extend(valuesNew)
    return values, years

def updateTableByApiSimpleType(metricType, universityList, mainSubjectsList):
    model_obj = globals()[metricType]
    # model_obj.objects.all().delete() #usuwanie wszystkich rekordow z danej tabeli
    for university in universityList:
        universityId = University.objects.get(id=university)
        for subject in mainSubjectsList:
            subjectAreaId = SubjectArea.objects.get(id=subject)
            requestURL = "https://api.elsevier.com/analytics/scival/institution/metrics?metricTypes=" + metricType + "&institutionIds=" + str(
                university) + "&yearRange=10yrs&subjectAreaFilterURI=Class%2FASJC%2FCode%2F" + str(
                subject) + "&includeSelfCitations=true&byYear=true&includedDocs=AllPublicationTypes&journalImpactType=CiteScore&showAsFieldWeighted=false&apiKey=" + API_KEY
            requestURL2 = "https://api.elsevier.com/analytics/scival/institution/metrics?metricTypes=" + metricType + "&institutionIds=" + str(
                university) + "&yearRange=3yrsAndCurrentAndFuture&subjectAreaFilterURI=Class%2FASJC%2FCode%2F" + str(
                subject) + "&includeSelfCitations=true&byYear=true&includedDocs=AllPublicationTypes&journalImpactType=CiteScore&showAsFieldWeighted=false&apiKey=" + API_KEY
            response = requests.get(requestURL)
            response2 = requests.get(requestURL2)
            amountInYear, years = getValuesFromSimpleType(response.json()['results'][0]['metrics'], response2.json()['results'][0]['metrics'])
            for indx, y in enumerate(years):
                # model_obj.objects.create(year=y, value=amountInYear[indx], universityId=University.objects.get(id=university), subjectAreaId=SubjectArea.objects.get(id=subject)) #wersja z usuwaniem wszystkich rekordow
                try:
                    metric = model_obj.objects.get(year=y, universityId=universityId, subjectAreaId=subjectAreaId)
                    metric.value = amountInYear[indx]
                    metric.save()
                except model_obj.DoesNotExist:
                    model_obj.objects.create(year=y, value=amountInYear[indx], universityId=universityId,
                                             subjectAreaId=subjectAreaId)


# Functions used to updated collaboration type table
def saveToDatabaseCollaboration(model_obj, metricType, universityID, subjectAreaID, InstitutionalValues, InternationalValues, NationalValues, SingleAuthorshipValues, InstitutionalPercentageValues=None, InternationalPercentageValues=None, NationalPercentageValues=None, SingleAuthorshipPercentageValues=None):
    for year, InstitutionalValue in InstitutionalValues.items():
        InternationalValue = InternationalValues.get(year)
        NationalValue = NationalValues.get(year)
        SingleAuthorshipValue = SingleAuthorshipValues.get(year)
        if metricType == "Collaboration":
            institutionalPercentageValue = InstitutionalPercentageValues.get(year)
            internationalPercentageValue = InternationalPercentageValues.get(year)
            nationalPercentageValue = NationalPercentageValues.get(year)
            singleAuthorshipPercentageValue = SingleAuthorshipPercentageValues.get(year)
        try:
            metric = model_obj.objects.get(year=year, universityId=universityID, subjectAreaId=subjectAreaID)
            metric.InstitutionalValue = InstitutionalValue
            metric.InternationalValue = InternationalValue
            metric.NationalValue = NationalValue
            metric.SingleAuthorshipValue = SingleAuthorshipValue
            if metricType == "Collaboration":
                metric.InstitutionalPercentageValue = institutionalPercentageValue
                metric.InternationalPercentageValue = internationalPercentageValue
                metric.NationalPercentageValue = nationalPercentageValue
                metric.SingleAuthorshipPercentageValue = singleAuthorshipPercentageValue
            metric.save()
        except model_obj.DoesNotExist:
            if metricType == "Collaboration":
                model_obj.objects.create(year=year, universityId=universityID, subjectAreaId=subjectAreaID,
                                         InstitutionalValue=InstitutionalValue,
                                         InternationalValue=InternationalValue, NationalValue=NationalValue,
                                         SingleAuthorshipValue=SingleAuthorshipValue,
                                         InstitutionalPercentageValue=institutionalPercentageValue,
                                         InternationalPercentageValue=internationalPercentageValue,
                                         NationalPercentageValue=nationalPercentageValue,
                                         SingleAuthorshipPercentageValue=singleAuthorshipPercentageValue)
            else:
                model_obj.objects.create(year=year, universityId=universityID, subjectAreaId=subjectAreaID,
                                         InstitutionalValue=InstitutionalValue,
                                         InternationalValue=InternationalValue, NationalValue=NationalValue,
                                         SingleAuthorshipValue=SingleAuthorshipValue)


def getValuesFromCollabType(values, valuesNew, collabType, metricType):
    dict10yearsValues = next(item for item in values if item['collabType'] == collabType)
    dict5lastYearsValues = next(item for item in valuesNew if item['collabType'] == collabType)
    last_two_records_value = list(dict5lastYearsValues['valueByYear'].keys())[-2:]
    dict10yearsValues['valueByYear'].update(
        {key: value for key, value in dict5lastYearsValues['valueByYear'].items() if key in last_two_records_value})
    if metricType == "Collaboration":
        last_two_records_percentage = list(dict5lastYearsValues['percentageByYear'].keys())[-2:]
        dict10yearsValues['percentageByYear'].update(
            {key: value for key, value in dict5lastYearsValues['percentageByYear'].items() if key in last_two_records_percentage})
        return dict10yearsValues['valueByYear'], dict10yearsValues['percentageByYear']
    else:
        return dict10yearsValues['valueByYear']


def updateTableByApiCollaborationType(metricType, universityList, mainSubjectsList):
    model_obj = globals()[metricType]
    # model_obj.objects.all().delete() #usuwanie wszystkich rekordow z danej tabeli
    for university in universityList:
        universityId = University.objects.get(id=university)
        for subject in mainSubjectsList:
            subjectAreaId = SubjectArea.objects.get(id=subject)
            requestURL = "https://api.elsevier.com/analytics/scival/institution/metrics?metricTypes=" + metricType + "&institutionIds=" + str(
                university) + "&yearRange=10yrs&subjectAreaFilterURI=Class%2FASJC%2FCode%2F" + str(
                subject) + "&includeSelfCitations=true&byYear=true&includedDocs=AllPublicationTypes&journalImpactType=CiteScore&showAsFieldWeighted=false&apiKey=" + API_KEY
            requestURL2 = "https://api.elsevier.com/analytics/scival/institution/metrics?metricTypes=" + metricType + "&institutionIds=" + str(
                university) + "&yearRange=3yrsAndCurrentAndFuture&subjectAreaFilterURI=Class%2FASJC%2FCode%2F" + str(
                subject) + "&includeSelfCitations=true&byYear=true&includedDocs=AllPublicationTypes&journalImpactType=CiteScore&showAsFieldWeighted=false&apiKey=" + API_KEY
            response = requests.get(requestURL)
            response2 = requests.get(requestURL2)
            valuesFromLast10years = response.json()['results'][0]['metrics'][0]['values']
            valuesFromLast3yearsAndFuture = response2.json()['results'][0]['metrics'][0]['values']
            if metricType == "Collaboration":
                valueInstitutional, percentagevalueInstitutional = getValuesFromCollabType(valuesFromLast10years,
                                                                                           valuesFromLast3yearsAndFuture,
                                                                                           'Institutional collaboration',
                                                                                           metricType)
                valueInternational, percentagevalueInternational = getValuesFromCollabType(valuesFromLast10years,
                                                                                           valuesFromLast3yearsAndFuture,
                                                                                           'International collaboration',
                                                                                           metricType)
                valueNational, percentagevalueNational = getValuesFromCollabType(valuesFromLast10years,
                                                                                 valuesFromLast3yearsAndFuture,
                                                                                 'National collaboration', metricType)
                valueSingleAuthorship, percentagevalueSingleAuthorship = getValuesFromCollabType(valuesFromLast10years,
                                                                                                 valuesFromLast3yearsAndFuture,
                                                                                                 'Single authorship',
                                                                                                 metricType)
                saveToDatabaseCollaboration(model_obj, metricType, universityId, subjectAreaId, valueInstitutional,
                                            valueInternational, valueNational, valueSingleAuthorship,
                                            percentagevalueInstitutional, percentagevalueInternational,
                                            percentagevalueNational, percentagevalueSingleAuthorship)
            else:
                valueInstitutional = getValuesFromCollabType(valuesFromLast10years, valuesFromLast3yearsAndFuture,
                                                             'Institutional collaboration', metricType)
                valueInternational = getValuesFromCollabType(valuesFromLast10years, valuesFromLast3yearsAndFuture,
                                                             'International collaboration', metricType)
                valueNational = getValuesFromCollabType(valuesFromLast10years, valuesFromLast3yearsAndFuture,
                                                        'National collaboration', metricType)
                valueSingleAuthorship = getValuesFromCollabType(valuesFromLast10years, valuesFromLast3yearsAndFuture,
                                                                'Single authorship', metricType)
                saveToDatabaseCollaboration(model_obj, metricType, universityId, subjectAreaId, valueInstitutional,
                                            valueInternational, valueNational, valueSingleAuthorship)


# Functions used to updated top percentile type table
def saveToDatabaseTopPercentile(model_obj, universityID, subjectAreaID, valuesThreshold1, percentageValuesThreshold1, valuesThreshold5, percentageValuesThreshold5, valuesThreshold10, percentageValuesThreshold10, valuesThreshold25, percentageValuesThreshold25):
    for year, threshold1Value in valuesThreshold1.items():
        threshold1PercentageValue = percentageValuesThreshold1.get(year)
        threshold5Value = valuesThreshold5.get(year)
        threshold5PercentageValue = percentageValuesThreshold5.get(year)
        threshold10Value = valuesThreshold10.get(year)
        threshold10PercentageValue = percentageValuesThreshold10.get(year)
        threshold25Value = valuesThreshold25.get(year)
        threshold25PercentageValue = percentageValuesThreshold25.get(year)
        try:
            metric = model_obj.objects.get(year=year, universityId=universityID, subjectAreaId=subjectAreaID)
            metric.threshold1Value = threshold1Value
            metric.threshold1PercentageValue = threshold1PercentageValue
            metric.threshold5Value = threshold5Value
            metric.threshold5PercentageValue = threshold5PercentageValue
            metric.threshold10Value = threshold10Value
            metric.threshold10PercentageValue = threshold10PercentageValue
            metric.threshold25Value = threshold25Value
            metric.threshold25PercentageValue = threshold25PercentageValue
            metric.save()
        except model_obj.DoesNotExist:
            model_obj.objects.create(year=year, universityId=universityID, subjectAreaId=subjectAreaID,
                                     threshold1Value=threshold1Value,
                                     threshold1PercentageValue=threshold1PercentageValue,
                                     threshold5Value=threshold5Value,
                                     threshold5PercentageValue=threshold5PercentageValue,
                                     threshold10Value=threshold10Value,
                                     threshold10PercentageValue=threshold10PercentageValue,
                                     threshold25Value=threshold25Value,
                                     threshold25PercentageValue=threshold25PercentageValue)


def getValuesFromThresholdType(values, valuesNew, threshold):
    dict10yearsValues = next(item for item in values if item['threshold'] == threshold)
    dict5lastYearsValues = next(item for item in valuesNew if item['threshold'] == threshold)
    last_two_records_value = list(dict5lastYearsValues['valueByYear'].keys())[-2:]
    dict10yearsValues['valueByYear'].update(
        {key: value for key, value in dict5lastYearsValues['valueByYear'].items() if key in last_two_records_value})
    last_two_records_percentage = list(dict5lastYearsValues['percentageByYear'].keys())[-2:]
    dict10yearsValues['percentageByYear'].update(
        {key: value for key, value in dict5lastYearsValues['percentageByYear'].items() if key in last_two_records_percentage})
    return dict10yearsValues['valueByYear'], dict10yearsValues['percentageByYear']


def updateTableByApiTopPercentileType(metricType, universityList, mainSubjectsList):
    model_obj = globals()[metricType]
    # model_obj.objects.all().delete() #usuwanie wszystkich rekordow z danej tabeli
    for university in universityList:
        universityId = University.objects.get(id=university)
        for subject in mainSubjectsList:
            subjectAreaId = SubjectArea.objects.get(id=subject)
            requestURL = "https://api.elsevier.com/analytics/scival/institution/metrics?metricTypes=" + metricType + "&institutionIds=" + str(
                university) + "&yearRange=10yrs&subjectAreaFilterURI=Class%2FASJC%2FCode%2F" + str(
                subject) + "&includeSelfCitations=true&byYear=true&includedDocs=AllPublicationTypes&journalImpactType=CiteScore&showAsFieldWeighted=false&apiKey=" + API_KEY
            requestURL2 = "https://api.elsevier.com/analytics/scival/institution/metrics?metricTypes=" + metricType + "&institutionIds=" + str(
                university) + "&yearRange=3yrsAndCurrentAndFuture&subjectAreaFilterURI=Class%2FASJC%2FCode%2F" + str(
                subject) + "&includeSelfCitations=true&byYear=true&includedDocs=AllPublicationTypes&journalImpactType=CiteScore&showAsFieldWeighted=false&apiKey=" + API_KEY
            response = requests.get(requestURL)
            response2 = requests.get(requestURL2)
            valuesFromLast10years = response.json()['results'][0]['metrics'][0]['values']
            valuesFromLast3yearsAndFuture = response2.json()['results'][0]['metrics'][0]['values']
            valueThreshold1, percentagevalueThreshold1 = getValuesFromThresholdType(valuesFromLast10years,
                                                                                    valuesFromLast3yearsAndFuture, 1)
            valueThreshold5, percentagevalueThreshold5 = getValuesFromThresholdType(valuesFromLast10years,
                                                                                    valuesFromLast3yearsAndFuture, 5)
            valueThreshold10, percentagevalueThreshold10 = getValuesFromThresholdType(valuesFromLast10years,
                                                                                      valuesFromLast3yearsAndFuture, 10)
            valueThreshold25, percentagevalueThreshold25 = getValuesFromThresholdType(valuesFromLast10years,
                                                                                      valuesFromLast3yearsAndFuture, 25)
            saveToDatabaseTopPercentile(model_obj, universityId, subjectAreaId, valueThreshold1,
                                        percentagevalueThreshold1, valueThreshold5, percentagevalueThreshold5,
                                        valueThreshold10, percentagevalueThreshold10, valueThreshold25,
                                        percentagevalueThreshold25)
