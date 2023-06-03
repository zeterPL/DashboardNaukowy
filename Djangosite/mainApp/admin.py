from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django.apps import apps
from .models import *

# Username: Admin
# email: admin@mail.com
# Pass: 123

#drugi admin dla leniwych
# Username: admin
# Pass: admin

class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('id','name','country')
    list_filter = ('country',)
    search_fields = ('name', 'country')
    ordering = ('name', 'country', 'id')
    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv),]
        return new_urls + urls
    def upload_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]
            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.replace('\r', '').split("\n")
            for x in csv_data:
                fields = x.split(";")
                if (len(fields) < 3):
                    countryX = 'Polska'
                else:
                    countryX = fields[2]
                created = University.objects.update_or_create(
                    id = fields[0],
                    name = fields[1],
                    country = countryX,
                )
            url = reverse('admin:mainApp_university_changelist')
            return HttpResponseRedirect(url)
        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/csv_upload.html", data)


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
    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv),]
        return new_urls + urls
    def upload_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]
            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.replace('\r','').split("\n")
            for x in csv_data:
                fields = x.split(";")
                if (len(fields) < 3):
                    uriFieldX = 'Class/ASJC/Code/' + fields[0]
                else:
                    uriFieldX = fields[2]
                created = SubjectArea.objects.update_or_create(
                    id = fields[0],
                    name = fields[1],
                    uri = uriFieldX,
                )
            url = reverse('admin:mainApp_subjectarea_changelist')
            return HttpResponseRedirect(url)
        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/csv_upload.html", data)

class FloatRangeFilter(admin.SimpleListFilter):
    title = 'Przedział wartości'
    parameter_name = 'Przedział wartości'
    def lookups(self, request, model_admin):
        return (
            ('0-50', '0-50'),
            ('50-100', '50-100'),
            ('100-200', '100-200'),
            ('200-500', '200-500'),
            ('500-1000', '500-1000'),
            ('1000-2000', '1000-2000'),
            ('2000-5000', '2000-5000'),
            ('5000-10000', '5000-10000'),
            ('10000+', '10000+'),
        )
    def queryset(self, request, queryset):
        if self.value() == '0-50':
            return queryset.filter(value__lt=50)
        elif self.value() == '50-100':
            return queryset.filter(Q(value__gte=50) & Q(value__lt=100))
        elif self.value() == '100-200':
            return queryset.filter(Q(value__gte=100) & Q(value__lt=200))
        elif self.value() == '200-500':
            return queryset.filter(Q(value__gte=200) & Q(value__lt=500))
        elif self.value() == '500-1000':
            return queryset.filter(Q(value__gte=500) & Q(value__lt=1000))
        elif self.value() == '1000-2000':
            return queryset.filter(Q(value__gte=1000) & Q(value__lt=2000))
        elif self.value() == '2000-5000':
            return queryset.filter(Q(value__gte=2000) & Q(value__lt=5000))
        elif self.value() == '5000-10000':
            return queryset.filter(Q(value__gte=5000) & Q(value__lt=10000))
        elif self.value() == '10000+':
            return queryset.filter(Q(value__gte=10000))


class AbstractMetricAdmin(admin.ModelAdmin):
    list_display = ('year', 'value', 'universityId', 'subjectAreaId')
    raw_id_fields = ('universityId', 'subjectAreaId')
    list_filter = ('year', FloatRangeFilter, 'universityId', 'subjectAreaId')
    search_fields = ('year', 'value', 'universityId', 'subjectAreaId')
    ordering = ('subjectAreaId', 'universityId', 'year', 'value')
    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv),]
        return new_urls + urls
        return urls
    def upload_csv(self, request, model_name):
        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]
            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.replace('\r', '').split("\n")
            for x in csv_data:
                fields = x.split(";")
                model = apps.get_model('mainApp', model_name)
                if (fields[3].lower() == 'none' or fields[3].lower() == 'null' or fields[3] == ''):
                    fields[3] = None;
                created = model.objects.update_or_create(
                    year=fields[0],
                    universityId=University.objects.get(id=fields[1]),
                    subjectAreaId=SubjectArea.objects.get(id=fields[2]),
                    value=fields[3],
                )
            url = reverse(f'admin:mainApp_{model_name.lower()}_changelist')
            return HttpResponseRedirect(url)
        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/csv_upload.html", data)

@admin.register(ScholarlyOutput)
class ScholaryOutputAdmin(AbstractMetricAdmin):
    def upload_csv(self, request):
        return super().upload_csv(request, 'ScholarlyOutput')

@admin.register(CitationCount)
class CitationCountAdmin(AbstractMetricAdmin):
    def upload_csv(self, request):
        return super().upload_csv(request, 'CitationCount')

@admin.register(CitationsPerPublication)
class CitationsPerPublicationAdmin(AbstractMetricAdmin):
    def upload_csv(self, request):
        return super().upload_csv(request, 'CitationsPerPublication')

@admin.register(Collaboration)
class CollaborationAdmin(AbstractMetricAdmin):
    def upload_csv(self, request):
        return super().upload_csv(request, 'Collaboration')

@admin.register(CollaborationImpact)
class CollaborationImpactAdmin(AbstractMetricAdmin):
    def upload_csv(self, request):
        return super().upload_csv(request, 'CollaborationImpact')

@admin.register(FieldWeightedCitationImpact)
class FieldWeightedCitationImpactAdmin(AbstractMetricAdmin):
    def upload_csv(self, request):
        return super().upload_csv(request, 'FieldWeightedCitationImpact')

@admin.register(PublicationsInTopJournalPercentiles)
class PublicationsInTopJournalPercentilesAdmin(AbstractMetricAdmin):
    def upload_csv(self, request):
        return super().upload_csv(request, 'PublicationsInTopJournalPercentiles')

@admin.register(OutputsInTopCitationPercentiles)
class OutputsInTopCitationPercentilesAdmin(AbstractMetricAdmin):
    def upload_csv(self, request):
        return super().upload_csv(request, 'OutputsInTopCitationPercentiles')


