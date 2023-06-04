from django.db import models
from django.db.models.functions import Concat

class University(models.Model):
    id = models.IntegerField(primary_key=True, help_text='Id uczelni. Id opowiada Id z Scival-a')
    name = models.CharField(max_length=150, unique=True, verbose_name='Uczelnia', help_text='Nazwa uczelni')
    country = models.CharField(max_length=150, default="Polska", verbose_name='Kraj', help_text='Kraj w którym znajduje się dana uczelnia')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Uczelnia"
        verbose_name_plural = "Uczelnie"

class SubjectArea(models.Model):
    id = models.IntegerField(primary_key=True, help_text='Id głównej dziedziny naukowej. Id opowiada Id z Scival-a')
    name = models.CharField(max_length=150, unique=True, verbose_name='Dziedzina Naukowa', help_text='Nazwa głównej dziedziny naukowej')
    uri = models.CharField(max_length=150, unique=True, default='', blank=True, help_text='Uri głównej dziedziny naukowej. Uri jest parametrem filtrującym zapytanie z Scival-a')
    def save(self, *args, **kwargs):
        if not self.uri:
            self.uri = 'Class/ASJC/Code/' + str(self.id)
        super(SubjectArea, self).save(*args, **kwargs)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Dziedzina naukowa"
        verbose_name_plural = "Dziedziny naukowe"

metric_names = [
    {'EnglishName': 'CitationCount', 'PolishName': 'Liczba cytowan'},
    {'EnglishName': 'CitationsPerPublication', 'PolishName': 'Liczba cytowan na publikacje'},
    {'EnglishName': 'Collaboration', 'PolishName': 'Kolaboracje'},
    {'EnglishName': 'CollaborationImpact', 'PolishName': 'Impakt kolaboracji'},
    {'EnglishName': 'FieldWeightedCitationImpact', 'PolishName': 'Waga impaktu cytowan'},
    {'EnglishName': 'PublicationsInTopJournalPercentiles', 'PolishName': 'Procent publikacji w topowych dziennikach'},
    {'EnglishName': 'OutputsInTopCitationPercentiles', 'PolishName': 'Wyniki w najwyższych percentylach cytowań'},
    {'EnglishName': 'ScholaryOutput', 'PolishName': 'Wyniki naukowe'}
]
def getEnglishNameReturnPolishName(english_name):
    for metric in metric_names:
        if metric['EnglishName'] == english_name:
            return metric['PolishName']
    return "Brak nazwy"

class Abstractmetric(models.Model):
    year = models.CharField(max_length=10, verbose_name='Rok', help_text='Rok metryki')
    universityId = models.ForeignKey(University, on_delete=models.CASCADE, verbose_name='Id Uczelni', help_text='Id uczelni. Id opowiada Id z Scival-a')
    subjectAreaId = models.ForeignKey(SubjectArea, on_delete=models.CASCADE, verbose_name='Id Dziedzina Naukowej', help_text='Id głównej dziedziny naukowej. Id opowiada Id z Scival-a')
    class Meta:
        abstract = True

class ScholarlyOutput(Abstractmetric):
    value = models.FloatField(null=True, blank=True, verbose_name='Wartość', help_text='Wartość danej metryki')
    class Meta:
        verbose_name = getEnglishNameReturnPolishName("ScholaryOutput")
        verbose_name_plural = getEnglishNameReturnPolishName("ScholaryOutput")
class CitationCount(Abstractmetric):
    value = models.FloatField(null=True, blank=True, verbose_name='Wartość', help_text='Wartość danej metryki')
    class Meta:
        verbose_name = getEnglishNameReturnPolishName("CitationCount")
        verbose_name_plural = getEnglishNameReturnPolishName("CitationCount")
class CitationsPerPublication(Abstractmetric):
    value = models.FloatField(null=True, blank=True, verbose_name='Wartość', help_text='Wartość danej metryki')
    class Meta:
        verbose_name =getEnglishNameReturnPolishName( "CitationsPerPublication")
        verbose_name_plural = getEnglishNameReturnPolishName("CitationsPerPublication")
class FieldWeightedCitationImpact(Abstractmetric):
    value = models.FloatField(null=True, blank=True, verbose_name='Wartość', help_text='Wartość danej metryki')
    class Meta:
        verbose_name = getEnglishNameReturnPolishName("FieldWeightedCitationImpact")
        verbose_name_plural = getEnglishNameReturnPolishName("FieldWeightedCitationImpact")
class Collaboration(Abstractmetric):
    InstitutionalValue = models.FloatField(null=True, blank=True, verbose_name='Wartość calkowita', help_text='Wartość calkowita kolaboracji')
    InternationalValue = models.FloatField(null=True, blank=True, verbose_name='Wartość miedzynarodowa', help_text='Wartość miedzynarodowa kolaboracji')
    NationalValue = models.FloatField(null=True, blank=True, verbose_name='Wartość narodowa', help_text='Wartość narodowa kolaboracji')
    SingleAuthorshipValue = models.FloatField(null=True, blank=True, verbose_name='Wartość pojedynczego autorstwa', help_text='Wartość pojedynczego autorstwa kolaboracji')
    InstitutionalPercentageValue = models.FloatField(null=True, blank=True, verbose_name='Procentowa wartość calkowita', help_text='Procentowa wartość calkowita kolaboracji')
    InternationalPercentageValue = models.FloatField(null=True, blank=True, verbose_name='Procentowa wartość miedzynarodowa', help_text='Procentowa wartość miedzynarodowa kolaboracji')
    NationalPercentageValue = models.FloatField(null=True, blank=True, verbose_name='Procentowa wartość narodowa', help_text='Procentowa wartość narodowa kolaboracji')
    SingleAuthorshipPercentageValue = models.FloatField(null=True, blank=True, verbose_name='Procentowa wartość pojedynczego autorstwa', help_text='Procentowa wartość pojedynczego autorstwa kolaboracji')
    class Meta:
        verbose_name = getEnglishNameReturnPolishName("Collaboration")
        verbose_name_plural = getEnglishNameReturnPolishName("Collaboration")
class CollaborationImpact(Abstractmetric):
    InstitutionalValue = models.FloatField(null=True, blank=True, verbose_name='Wartość calkowita', help_text='Wartość calkowita impaktu kolaboracji')
    InternationalValue = models.FloatField(null=True, blank=True, verbose_name='Wartość miedzynarodowa', help_text='Wartość miedzynarodowa impaktu kolaboracji')
    NationalValue = models.FloatField(null=True, blank=True, verbose_name='Wartość narodowa', help_text='Wartość narodowa impaktu kolaboracji')
    SingleAuthorshipValue = models.FloatField(null=True, blank=True, verbose_name='Wartość pojedynczego autorstwa', help_text='Wartość pojedynczego autorstwa impaktu kolaboracji')
    class Meta:
        verbose_name = getEnglishNameReturnPolishName("CollaborationImpact")
        verbose_name_plural = getEnglishNameReturnPolishName("CollaborationImpact")
class PublicationsInTopJournalPercentiles(Abstractmetric):
    value = models.FloatField(null=True, blank=True, verbose_name='Wartość', help_text='Wartość danej metryki')  # kiedys moze sie zmieni na prawidlowe :P
    class Meta:
        verbose_name = getEnglishNameReturnPolishName("PublicationsInTopJournalPercentiles")
        verbose_name_plural = getEnglishNameReturnPolishName("PublicationsInTopJournalPercentiles")

class OutputsInTopCitationPercentiles(Abstractmetric):
    value = models.FloatField(null=True, blank=True, verbose_name='Wartość', help_text='Wartość danej metryki') # kiedys moze sie zmieni na prawidlowe :P
    class Meta:
        verbose_name = getEnglishNameReturnPolishName("OutputsInTopCitationPercentiles")
        verbose_name_plural = getEnglishNameReturnPolishName("OutputsInTopCitationPercentiles")