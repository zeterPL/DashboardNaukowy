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

class CitationCount(models.Model):
    year = models.CharField(max_length=10)
    value = models.FloatField()
    universityId = models.ForeignKey(University, on_delete=models.CASCADE)
    subjectAreaId = models.ForeignKey(SubjectArea, on_delete=models.CASCADE)

class CitationsPerPublication(models.Model):
    year = models.CharField(max_length=10)
    value = models.FloatField()
    universityId = models.ForeignKey(University, on_delete=models.CASCADE)
    subjectAreaId = models.ForeignKey(SubjectArea, on_delete=models.CASCADE)

class CitingPatentsCount(models.Model):
    year = models.CharField(max_length=10)
    value = models.FloatField()
    universityId = models.ForeignKey(University, on_delete=models.CASCADE)
    subjectAreaId = models.ForeignKey(SubjectArea, on_delete=models.CASCADE)

class Collaboration(models.Model):
    year = models.CharField(max_length=10)
    value = models.FloatField()
    universityId = models.ForeignKey(University, on_delete=models.CASCADE)
    subjectAreaId = models.ForeignKey(SubjectArea, on_delete=models.CASCADE)

class CollaborationImpact(models.Model):
    year = models.CharField(max_length=10)
    value = models.FloatField()
    universityId = models.ForeignKey(University, on_delete=models.CASCADE)
    subjectAreaId = models.ForeignKey(SubjectArea, on_delete=models.CASCADE)

class FieldWeightedCitationImpact(models.Model):
    year = models.CharField(max_length=10)
    value = models.FloatField()
    universityId = models.ForeignKey(University, on_delete=models.CASCADE)
    subjectAreaId = models.ForeignKey(SubjectArea, on_delete=models.CASCADE)

class Hindices(models.Model):
    year = models.CharField(max_length=10)
    value = models.FloatField()
    universityId = models.ForeignKey(University, on_delete=models.CASCADE)
    subjectAreaId = models.ForeignKey(SubjectArea, on_delete=models.CASCADE)

class PatentCitationsCount(models.Model):
    year = models.CharField(max_length=10)
    value = models.FloatField()
    universityId = models.ForeignKey(University, on_delete=models.CASCADE)
    subjectAreaId = models.ForeignKey(SubjectArea, on_delete=models.CASCADE)

class PatentCitationsPerScholarlyOutput(models.Model):
    year = models.CharField(max_length=10)
    value = models.FloatField()
    universityId = models.ForeignKey(University, on_delete=models.CASCADE)
    subjectAreaId = models.ForeignKey(SubjectArea, on_delete=models.CASCADE)

class PatentCitedScholarlyOutput(models.Model):
    year = models.CharField(max_length=10)
    value = models.FloatField()
    universityId = models.ForeignKey(University, on_delete=models.CASCADE)
    subjectAreaId = models.ForeignKey(SubjectArea, on_delete=models.CASCADE)

class PublicationsInTopJournalPercentiles(models.Model):
    year = models.CharField(max_length=10)
    value = models.FloatField()
    universityId = models.ForeignKey(University, on_delete=models.CASCADE)
    subjectAreaId = models.ForeignKey(SubjectArea, on_delete=models.CASCADE)

class OutputsInTopCitationPercentiles(models.Model):
    year = models.CharField(max_length=10)
    value = models.FloatField()
    universityId = models.ForeignKey(University, on_delete=models.CASCADE)
    subjectAreaId = models.ForeignKey(SubjectArea, on_delete=models.CASCADE)

class ScholarlyOutput(models.Model):
    year = models.CharField(max_length=10)
    value = models.FloatField()
    universityId = models.ForeignKey(University, on_delete=models.CASCADE)
    subjectAreaId = models.ForeignKey(SubjectArea, on_delete=models.CASCADE)
    class Meta:
        verbose_name = "Metryka ScholaryOutput"
        verbose_name_plural = "Metryki ScholaryOutput"