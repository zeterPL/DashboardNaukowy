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


class Abstractmetric(models.Model):
    year = models.CharField(max_length=10, verbose_name='Rok', help_text='Rok metryki')
    value = models.FloatField(null=True, blank=True, verbose_name='Wartość', help_text='Wartość danej metryki')
    universityId = models.ForeignKey(University, on_delete=models.CASCADE, verbose_name='Id Uczelni', help_text='Id uczelni. Id opowiada Id z Scival-a')
    subjectAreaId = models.ForeignKey(SubjectArea, on_delete=models.CASCADE, verbose_name='Id Dziedzina Naukowej', help_text='Id głównej dziedziny naukowej. Id opowiada Id z Scival-a')
    class Meta:
        abstract = True
class CitationCount(Abstractmetric):
    class Meta:
        verbose_name = "Metryka CitationCount"
        verbose_name_plural = "Metryki CitationCount"
class CitationsPerPublication(Abstractmetric):
    class Meta:
        verbose_name = "Metryka CitationsPerPublication"
        verbose_name_plural = "Metryki CitationsPerPublication"

class CitingPatentsCount(Abstractmetric):
    class Meta:
        verbose_name = "Metryka CitingPatentsCount"
        verbose_name_plural = "Metryki CitingPatentsCount"

class Collaboration(Abstractmetric):
    class Meta:
        verbose_name = "Metryka Collaboration"
        verbose_name_plural = "Metryki Collaboration"

class CollaborationImpact(Abstractmetric):
    class Meta:
        verbose_name = "Metryka CollaborationImpact"
        verbose_name_plural = "Metryki CollaborationImpact"

class FieldWeightedCitationImpact(Abstractmetric):
    class Meta:
        verbose_name = "Metryka FieldWeightedCitationImpact"
        verbose_name_plural = "Metryki FieldWeightedCitationImpact"

class Hindices(Abstractmetric):
    class Meta:
        verbose_name = "Metryka Hindices"
        verbose_name_plural = "Metryki Hindices"

class PatentCitationsCount(Abstractmetric):
    class Meta:
        verbose_name = "Metryka PatentCitationsCount"
        verbose_name_plural = "Metryki PatentCitationsCount"

class PatentCitationsPerScholarlyOutput(Abstractmetric):
    class Meta:
        verbose_name = "Metryka PatentCitationsPerScholarlyOutput"
        verbose_name_plural = "Metryki PatentCitationsPerScholarlyOutput"

class PatentCitedScholarlyOutput(Abstractmetric):
    class Meta:
        verbose_name = "Metryka PatentCitedScholarlyOutput"
        verbose_name_plural = "Metryki PatentCitedScholarlyOutput"

class PublicationsInTopJournalPercentiles(Abstractmetric):
    class Meta:
        verbose_name = "Metryka PublicationsInTopJournalPercentiles"
        verbose_name_plural = "Metryki PublicationsInTopJournalPercentiles"

class OutputsInTopCitationPercentiles(Abstractmetric):
    class Meta:
        verbose_name = "Metryka OutputsInTopCitationPercentiles"
        verbose_name_plural = "Metryki OutputsInTopCitationPercentiles"

class ScholarlyOutput(Abstractmetric):
    class Meta:
        verbose_name = "Metryka ScholaryOutput"
        verbose_name_plural = "Metryki ScholaryOutput"