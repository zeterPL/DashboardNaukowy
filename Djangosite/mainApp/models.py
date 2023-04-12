from django.db import models

class University(models.Model):
    name = models.CharField(max_length=150, unique=True)
    country = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class SubjectArea(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150, unique=True)
    uri = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name

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