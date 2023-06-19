from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import SubjectArea, University, CitationCount



class BenchmarkingForm(forms.Form):
    # Multiselect dla uczelni
    university = forms.ModelMultipleChoiceField(
        queryset=University.objects.all().values_list('name', flat=True),
        widget=forms.CheckboxSelectMultiple
    )
    # Dropdown dla metryki
    METRICS = (
        ('CitationCount', 'Liczba cytowań'),
        ('Collaboration', 'Współpraca'),
        ('CollaborationImpact', 'Współpraca - impakt'),
        ('FieldWeightedCitationImpact', 'Cytowania - impakt'),
        ('OutputsInTopCitationPercentiles', 'Top citation percentile'),
        ('PublicationsInTopJournalPercentiles', 'Publications in top journals'),
        ('ScholarlyOutput', 'Liczba publikacji'),
    )
    metric = forms.ChoiceField(choices=METRICS)

    # Dropdown dla dziedziny
    subject_area = forms.ModelChoiceField(
        queryset=SubjectArea.objects.all().values_list('name', flat=True),
    )
    # Start year
    start = forms.ModelChoiceField(
        queryset=CitationCount.objects.all().values_list('year', flat=True).distinct(),
    )
    # End year
    end = forms.ModelChoiceField(
        queryset=CitationCount.objects.all().values_list('year', flat=True).distinct(),
    )


class CitationDistributionForm(forms.Form):
    DATATYPE_CHOICES = (
        ('citations', 'Liczba cytowań'),
        ('publications', 'Liczba publikacji')
    )

    dataType = forms.CharField(
        label='Select data type', widget=forms.Select(choices=DATATYPE_CHOICES))


class CitationsPerYearForm(forms.Form):
    university = forms.ModelChoiceField(
        queryset=University.objects.all().values_list('name', flat=True),
        # initial=University(name='Białystok University of Technology')
    )
    start = forms.ModelChoiceField(
        queryset=CitationCount.objects.all().values_list('year', flat=True).distinct(),
        # initial=CitationCount.objects.all().values_list('year', flat=True).distinct().first()
    )
    end = forms.ModelChoiceField(
        queryset=CitationCount.objects.all().values_list('year', flat=True).distinct(),
        # initial=CitationCount.objects.all().values_list('year', flat=True).distinct().last()
    )

    # class Meta:
    #     fields = ('university', 'start', 'end')
    #     labels = {
    #         'university': 'Uczelnia',
    #         'start': 'Od',
    #         'end': 'Do'
    #     }


class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
        )
        exclude = ('password',)
