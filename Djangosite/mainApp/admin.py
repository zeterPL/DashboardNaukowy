from django.contrib import admin
#from .models import University, SubjectArea
from .models import *
# Register your models here.

#tutaj będą modele które admin może edytować
# Username: Admin
# email: admin@mail.com
# Pass: 123

#drugi admin dla leniwych
# Username: admin
# Pass: admin

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('id','name','country')
    list_filter = ('country',)
    search_fields = ('name', 'country')
    ordering = ('id', 'name', 'country')

opis = "Domyślnie Uri jest tworzone 'Class/ASJC/Code/id' ale można zdefiniować własne"
@admin.register(SubjectArea)
class SubjectAreaAdmin(admin.ModelAdmin):
    #fields = ('id', 'name')
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
    ordering = ('id', 'name', 'uri')

@admin.register(ScholarlyOutput)
class ScholaryOutputAdmin(admin.ModelAdmin):
    list_display = ('year', 'value')
    raw_id_fields = ('universityId', 'subjectAreaId')

# class CitationCountInline(admin.TabularInline):
#     model = CitationCount
#
# class CitationsPerPublicationInline(admin.TabularInline):
#     model = CitationsPerPublication
# @admin.register(CitationCount)
# class DateAdmin(admin.ModelAdmin):
#     inlines = [CitationCountInline,
#                CitationsPerPublicationInline]
#     list_display = ('year', 'value', 'universityId', 'subjectAreaId')
