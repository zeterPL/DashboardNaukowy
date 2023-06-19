from django.db import models
from django.db.models.functions import Concat
from django.contrib.auth.models import AbstractUser

# Do formularzy dla wykresów


# Modele danych przekazywanych do wykresów
class PublicationsCountPerYear(models.Model):
    publicationsCount = models.IntegerField()
    year = models.IntegerField()

    class Meta:
        ordering = ('year',)


class University(models.Model):
    id = models.IntegerField(
        primary_key=True, help_text='Id uczelni. Id opowiada Id z Scival-a')
    name = models.CharField(max_length=150, unique=True,
                            verbose_name='Uczelnia', help_text='Nazwa uczelni')
    country = models.CharField(max_length=150, default="Polska", verbose_name='Kraj',
                               help_text='Kraj w którym znajduje się dana uczelnia')

    def __str__(self):
        return self.name
        # return "University id={}, name={}, country={}".format(self.id, self.name, self.country)

    class Meta:
        verbose_name = "Uczelnia"
        verbose_name_plural = "Uczelnie"


class SubjectArea(models.Model):
    id = models.IntegerField(
        primary_key=True, help_text='Id głównej dziedziny naukowej. Id opowiada Id z Scival-a')
    name = models.CharField(max_length=150, unique=True, verbose_name='Dziedzina Naukowa',
                            help_text='Nazwa głównej dziedziny naukowej')
    uri = models.CharField(max_length=150, unique=True, default='', blank=True,
                           help_text='Uri głównej dziedziny naukowej. Uri jest parametrem filtrującym zapytanie z Scival-a')

    def save(self, *args, **kwargs):
        if not self.uri:
            self.uri = 'Class/ASJC/Code/' + str(self.id)
        super(SubjectArea, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
        # return "SubjectArea id={}, name={}, uri={}".format(self.id, self.name, self.uri)

    class Meta:
        verbose_name = "Dziedzina naukowa"
        verbose_name_plural = "Dziedziny naukowe"


metric_names = [
    {'EnglishName': 'CitationCount', 'PolishName': 'Liczba cytowan'},
    {'EnglishName': 'CitationsPerPublication',
        'PolishName': 'Liczba cytowan na publikacje'},
    {'EnglishName': 'Collaboration', 'PolishName': 'Kolaboracje'},
    {'EnglishName': 'CollaborationImpact', 'PolishName': 'Impakt kolaboracji'},
    {'EnglishName': 'FieldWeightedCitationImpact',
        'PolishName': 'Waga impaktu cytowan'},
    {'EnglishName': 'PublicationsInTopJournalPercentiles',
        'PolishName': 'Procent publikacji w topowych dziennikach'},
    {'EnglishName': 'OutputsInTopCitationPercentiles',
        'PolishName': 'Wyniki w najwyższych percentylach cytowań'},
    {'EnglishName': 'ScholaryOutput', 'PolishName': 'Wyniki naukowe'}
]


def getEnglishNameReturnPolishName(english_name):
    for metric in metric_names:
        if metric['EnglishName'] == english_name:
            return metric['PolishName']
    return "Brak nazwy"




class AbstractMetric(models.Model):
    year = models.CharField(
        max_length=10, verbose_name='Rok', help_text='Rok metryki')
    universityId = models.ForeignKey(University, on_delete=models.CASCADE,
                                     verbose_name='Id Uczelni', help_text='Id uczelni. Id opowiada Id z Scival-a')
    subjectAreaId = models.ForeignKey(SubjectArea, on_delete=models.CASCADE, verbose_name='Id Dziedzina Naukowej',
                                      help_text='Id głównej dziedziny naukowej. Id opowiada Id z Scival-a')

    def __str__(self):
        return "year={}, universityId={}, subjectAreaId={}".format(self.year, self.universityId, self.subjectAreaId)

    class Meta:
        abstract = True


class AbstractMetricOneValue(AbstractMetric):
    value = models.FloatField(
        null=True, blank=True, verbose_name='Wartość', help_text='Wartość danej metryki')

    def __str__(self):
        return "{} {} value={}".format(self.__class__.__name__, super().__str__(), self.value)

    class Meta:
        abstract = True


# class CollaborationImpact(Abstractmetric):

class ScholarlyOutput(AbstractMetricOneValue):
    class Meta:
        verbose_name = getEnglishNameReturnPolishName("ScholaryOutput")
        verbose_name_plural = getEnglishNameReturnPolishName("ScholaryOutput")

class CitationCount(AbstractMetricOneValue):
    class Meta:
        verbose_name = getEnglishNameReturnPolishName("CitationCount")
        verbose_name_plural = getEnglishNameReturnPolishName("CitationCount")


class CitationsPerPublication(AbstractMetricOneValue):
    class Meta:
        verbose_name = getEnglishNameReturnPolishName(
            "CitationsPerPublication")
        verbose_name_plural = getEnglishNameReturnPolishName(
            "CitationsPerPublication")

class FieldWeightedCitationImpact(AbstractMetricOneValue):
    class Meta:
        verbose_name = getEnglishNameReturnPolishName(
            "FieldWeightedCitationImpact")
        verbose_name_plural = getEnglishNameReturnPolishName(
            "FieldWeightedCitationImpact")

class AbstractMetricCollaborationType(AbstractMetric):
    InstitutionalValue = models.FloatField(
        null=True, blank=True, verbose_name='Wartość calkowita', help_text='Wartość calkowita kolaboracji')
    InternationalValue = models.FloatField(
        null=True, blank=True, verbose_name='Wartość miedzynarodowa', help_text='Wartość miedzynarodowa kolaboracji')
    NationalValue = models.FloatField(
        null=True, blank=True, verbose_name='Wartość narodowa', help_text='Wartość narodowa kolaboracji')
    SingleAuthorshipValue = models.FloatField(
        null=True, blank=True, verbose_name='Wartość pojedynczego autorstwa', help_text='Wartość pojedynczego autorstwa kolaboracji')

    def __str__(self):
        return "{} {}, InstitutionalValue={}, InternationalValue={}, NationalValue={}, SingleAuthorshipValue={}".format(self.__class__.__name__, super().__str__(), self.InstitutionalValue, self.InternationalValue, self.NationalValue, self.SingleAuthorshipValue)

    class Meta:
        abstract = True



class Collaboration(AbstractMetricCollaborationType):
    InstitutionalPercentageValue = models.FloatField(
        null=True, blank=True, verbose_name='Procentowa wartość calkowita', help_text='Procentowa wartość calkowita kolaboracji')
    InternationalPercentageValue = models.FloatField(
        null=True, blank=True, verbose_name='Procentowa wartość miedzynarodowa', help_text='Procentowa wartość miedzynarodowa kolaboracji')
    NationalPercentageValue = models.FloatField(
        null=True, blank=True, verbose_name='Procentowa wartość narodowa', help_text='Procentowa wartość narodowa kolaboracji')
    SingleAuthorshipPercentageValue = models.FloatField(
        null=True, blank=True, verbose_name='Procentowa wartość pojedynczego autorstwa', help_text='Procentowa wartość pojedynczego autorstwa kolaboracji')

    def __str__(self):
        return "{} InstitutionalPercentageValue={} InternationalPercentageValue={} NationalPercentageValue={} SingleAuthorshipPercentageValue={}".format(super().__str__(), self.InstitutionalPercentageValue, self.InternationalPercentageValue, self.NationalPercentageValue, self.SingleAuthorshipPercentageValue)
    class Meta:
        verbose_name = getEnglishNameReturnPolishName("Collaboration")
        verbose_name_plural = getEnglishNameReturnPolishName("Collaboration")


class CollaborationImpact(AbstractMetricCollaborationType):
    class Meta:
        verbose_name = getEnglishNameReturnPolishName("CollaborationImpact")
        verbose_name_plural = getEnglishNameReturnPolishName(
            "CollaborationImpact")

# class OutputsInTopCitationPercentiles(Abstractmetric):

class AbstractMetricTopPercentiles(AbstractMetric):
    threshold1Value = models.FloatField(
        null=True, blank=True, verbose_name='Wartość threshold1', help_text='Wartość threshold1')
    threshold1PercentageValue = models.FloatField(
        null=True, blank=True, verbose_name='Procentowa wartość threshold1', help_text='Procentowa wartość threshold1')
    threshold5Value = models.FloatField(
        null=True, blank=True, verbose_name='Wartość threshold5', help_text='Wartość threshold5')
    threshold5PercentageValue = models.FloatField(
        null=True, blank=True, verbose_name='Procentowa wartość threshold5', help_text='Procentowa wartość threshold5')
    threshold10Value = models.FloatField(
        null=True, blank=True, verbose_name='Wartość threshold10', help_text='Wartość threshold10')
    threshold10PercentageValue = models.FloatField(
        null=True, blank=True, verbose_name='Procentowa wartość threshold10', help_text='Procentowa wartość threshold10')
    threshold25Value = models.FloatField(
        null=True, blank=True, verbose_name='Wartość threshold25', help_text='Wartość threshold25')
    threshold25PercentageValue = models.FloatField(
        null=True, blank=True, verbose_name='Procentowa wartość threshold25', help_text='Procentowa wartość threshold25')

    def __str__(self):
        return "{} {}, threshold1Value={} threshold1PercentageValue={} threshold5Value={} threshold5PercentageValue={} threshold10Value={} threshold10PercentageValue={} threshold25Value={} threshold25PercentageValue={}".format(self.__class__.__name__, super().__str__(), self.threshold1Value, self.threshold1PercentageValue, self.threshold5Value, self.threshold5PercentageValue, self.threshold10Value, self.threshold10PercentageValue, self.threshold25Value, self.threshold25PercentageValue)

    class Meta:
        abstract = True

class PublicationsInTopJournalPercentiles(AbstractMetricTopPercentiles):
    class Meta:
        verbose_name = getEnglishNameReturnPolishName(
            "PublicationsInTopJournalPercentiles")
        verbose_name_plural = getEnglishNameReturnPolishName(
            "PublicationsInTopJournalPercentiles")



class OutputsInTopCitationPercentiles(AbstractMetricTopPercentiles):
    class Meta:
        verbose_name = getEnglishNameReturnPolishName(
            "OutputsInTopCitationPercentiles")
        verbose_name_plural = getEnglishNameReturnPolishName(
            "OutputsInTopCitationPercentiles")

