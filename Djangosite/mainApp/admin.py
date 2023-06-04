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
                try:
                    metric = model.objects.get(year=fields[0], universityId=University.objects.get(id=fields[1]), subjectAreaId=SubjectArea.objects.get(id=fields[2]))
                    metric.value = fields[3]
                    metric.save()
                except model.DoesNotExist:
                    model.objects.create(year=fields[0], value=fields[3], universityId=University.objects.get(id=fields[1]), subjectAreaId=SubjectArea.objects.get(id=fields[2]))
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

@admin.register(FieldWeightedCitationImpact)
class FieldWeightedCitationImpactAdmin(AbstractMetricAdmin):
    def upload_csv(self, request):
        return super().upload_csv(request, 'FieldWeightedCitationImpact')


class AbstractCollaborationMetricAdmin(admin.ModelAdmin):
    raw_id_fields = ('universityId', 'subjectAreaId')
    list_filter = ('year', 'universityId', 'subjectAreaId')
    search_fields = ('year', 'universityId', 'subjectAreaId')
    ordering = ('subjectAreaId', 'universityId', 'year')
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
                for i in range(3, len(fields)):
                    if (fields[i] and (fields[i].lower() == 'none' or fields[i].lower() == 'null' or fields[i] == '')):
                        fields[i] = None;
                try:
                    metric = model.objects.get(year=fields[0], universityId=University.objects.get(id=fields[1]), subjectAreaId=SubjectArea.objects.get(id=fields[2]))
                    metric.InstitutionalValue = fields[3]
                    metric.InternationalValue = fields[4]
                    metric.NationalValue = fields[5]
                    metric.SingleAuthorshipValue = fields[6]
                    if(model_name == "Collaboration"):
                        metric.InstitutionalPercentageValue = fields[7]
                        metric.InternationalPercentageValue = fields[8]
                        metric.NationalPercentageValue = fields[9]
                        metric.SingleAuthorshipPercentageValue = fields[10]
                    metric.save()
                except model.DoesNotExist:
                    if (model_name == "Collaboration"):
                        model.objects.create(year=fields[0], universityId=University.objects.get(id=fields[1]), subjectAreaId=SubjectArea.objects.get(id=fields[2]),
                                             InstitutionalValue=fields[3], InternationalValue=fields[4], NationalValue=fields[5], SingleAuthorshipValue=fields[6],
                                             InstitutionalPercentageValue=fields[7], InternationalPercentageValue=fields[8], NationalPercentageValue=fields[9], SingleAuthorshipPercentageValue=fields[10])
                    else:
                        model.objects.create(year=fields[0], universityId=University.objects.get(id=fields[1]), subjectAreaId=SubjectArea.objects.get(id=fields[2]),
                                                 InstitutionalValue=fields[3], InternationalValue=fields[4], NationalValue=fields[5], SingleAuthorshipValue=fields[6])
            url = reverse(f'admin:mainApp_{model_name.lower()}_changelist')
            return HttpResponseRedirect(url)
        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/csv_upload.html", data)

@admin.register(Collaboration)
class CollaborationAdmin(AbstractCollaborationMetricAdmin):
    list_display = ('year', 'universityId', 'subjectAreaId', 'InstitutionalValue', 'InstitutionalPercentageValue', 'InternationalValue', 'InternationalPercentageValue', 'NationalValue', 'NationalPercentageValue', 'SingleAuthorshipValue', 'SingleAuthorshipPercentageValue')
    def upload_csv(self, request):
        return super().upload_csv(request, 'Collaboration')

@admin.register(CollaborationImpact)
class CollaborationImpactAdmin(AbstractCollaborationMetricAdmin):
    list_display = ('year', 'universityId', 'subjectAreaId', 'InstitutionalValue',  'InternationalValue', 'NationalValue', 'SingleAuthorshipValue')
    def upload_csv(self, request):
        return super().upload_csv(request, 'CollaborationImpact')


class AbstractTopPercentilesMetricAdmin(admin.ModelAdmin):
    raw_id_fields = ('universityId', 'subjectAreaId')
    list_filter = ('year', 'universityId', 'subjectAreaId')
    search_fields = ('year', 'universityId', 'subjectAreaId')
    ordering = ('subjectAreaId', 'universityId', 'year')
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
                for i in range(3, len(fields)):
                    if (fields[i] and (fields[i].lower() == 'none' or fields[i].lower() == 'null' or fields[i] == '')):
                        fields[i] = None;
                try:
                    metric = model.objects.get(year=fields[0], universityId=University.objects.get(id=fields[1]), subjectAreaId=SubjectArea.objects.get(id=fields[2]))
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
                    model.objects.create(year=fields[0], universityId=University.objects.get(id=fields[1]), subjectAreaId=SubjectArea.objects.get(id=fields[2]),
                                         threshold1Value=fields[3], threshold1PercentageValue=fields[4], threshold5Value=fields[5], threshold5PercentageValue=fields[6],
                                         threshold10Value=fields[7], threshold10PercentageValue=fields[8], threshold25Value=fields[9], threshold25PercentageValue=fields[10])
            url = reverse(f'admin:mainApp_{model_name.lower()}_changelist')
            return HttpResponseRedirect(url)
        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/csv_upload.html", data)

@admin.register(PublicationsInTopJournalPercentiles)
class PublicationsInTopJournalPercentilesAdmin(AbstractTopPercentilesMetricAdmin):
    list_display = ('year', 'universityId', 'subjectAreaId', 'threshold1Value', 'threshold1PercentageValue', 'threshold5Value', 'threshold5PercentageValue', 'threshold10Value', 'threshold10PercentageValue', 'threshold25Value', 'threshold25PercentageValue')
    def upload_csv(self, request):
        return super().upload_csv(request, 'PublicationsInTopJournalPercentiles')

@admin.register(OutputsInTopCitationPercentiles)
class OutputsInTopCitationPercentilesAdmin(AbstractTopPercentilesMetricAdmin):
    list_display = ('year', 'universityId', 'subjectAreaId', 'threshold1Value', 'threshold1PercentageValue', 'threshold5Value', 'threshold5PercentageValue', 'threshold10Value', 'threshold10PercentageValue', 'threshold25Value', 'threshold25PercentageValue')
    def upload_csv(self, request):
        return super().upload_csv(request, 'OutputsInTopCitationPercentiles')