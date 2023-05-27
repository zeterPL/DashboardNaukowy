from elsapy.elsclient import ElsClient
from .components.data_getter import ElsSearch
from .components.query_class import Query
from .models import *


# Interface class used to connect database with API. Internal classes shouldn't be accessed directly
class API_Interface:

    # nasz API_KEY = "c16459404285717f102391e3e8008be0"
    # default API_KEY = "7f59af901d2d86f78a1fd60c1bf9426a"

    def __init__(self, apiKey="7f59af901d2d86f78a1fd60c1bf9426a"):
        inst = list(University.objects.all().values('id'))
        unis = []
        for uni in inst:
            unis.append(uni['id'])
        self.apiKey = apiKey
        self.client = ElsClient(apiKey)
        self.institutions = unis
        self.metrics = ["CitationCount", "CollaborationImpact", "CitationsPerPublication", "Collaboration",
                        "FieldWeightedCitationImpact", "PublicationsInTopJournalPercentiles",
                        "OutputsInTopCitationPercentiles", "ScholarlyOutput"]
        self.subjectAreas = SubjectArea.objects.all()

    # not for use, API limits will be violated
    def db_fill(self):
        for metric in self.metrics:
            for s in self.subjectAreas:
                search = ElsSearch(
                    Query(institutions=self.institutions, metric=metric,
                          subjectAreaFilterURI=s.uri).parse_url(),
                    self.apiKey)
                search.execute(self.client, get_all=True)

                # Data Frame from json response
                for i in range(len(search.results_df['metrics'])):
                    result = search.results_df['metrics'][i]
                    result = result[0]['valueByYear']
                    institution = search.results_df['institution'][i]
                    institution = institution['id']
                    result_keys = result.keys()

                    for year in result_keys:
                        if metric == "CitationCount":
                            record = CitationCount(year=year, value=result[year], universityId=University.objects.get(id = institution),
                                        subjectAreaId=SubjectArea.objects.get(id = s.id))
                            record.save()
                        if metric == "CollaborationImpact":
                            record = CollaborationImpact(year=year, value=result[year], universityId=University.objects.get(id = institution),
                                        subjectAreaId=SubjectArea.objects.get(id = s.id))
                            record.save()
                        if metric == "CitationsPerPublication":
                            record = CitationsPerPublication(year=year, value=result[year], universityId=University.objects.get(id = institution),
                                        subjectAreaId=SubjectArea.objects.get(id = s.id))
                            record.save()
                        if metric == "Collaboration":
                            record = Collaboration(year=year, value=result[year], universityId=University.objects.get(id = institution),
                                        subjectAreaId=SubjectArea.objects.get(id = s.id))
                            record.save()
                        if metric == "FieldWeightedCitationImpact":
                            record = FieldWeightedCitationImpact(year=year, value=result[year],
                                                                 universityId=University.objects.get(id=institution),
                                                                 subjectAreaId=SubjectArea.objects.get(id=s.id))
                            record.save()
                        if metric == "PublicationsInTopJournalPercentiles":
                            record = PublicationsInTopJournalPercentiles(year=year, value=result[year],
                                                                         universityId=University.objects.get(
                                                                             id=institution),
                                                                         subjectAreaId=SubjectArea.objects.get(id=s.id))
                            record.save()
                        if metric == "OutputsInTopCitationPercentiles":
                            record = OutputsInTopCitationPercentiles(year=year, value=result[year],
                                                                     universityId=University.objects.get(
                                                                         id=institution),
                                                                     subjectAreaId=SubjectArea.objects.get(id=s.id))
                            record.save()
                        if metric == "ScholarlyOutput":
                            record = ScholarlyOutput(year=year, value=result[year], universityId=University.objects.get(id = institution),
                                        subjectAreaId=SubjectArea.objects.get(id = s.id))
                            record.save()

    # Update given metrics or given uni or given SubjectArea
    def db_update_metric(self, metric: Abstractmetric):
        try:
            metric.objects.all().delete()

        except:
            print("Niepowodzenie")

        else:
            for s in self.subjectAreas:
                search = ElsSearch(
                    Query(institutions=self.institutions, metric=metric.__str__(self),
                          subjectAreaFilterURI=s.uri).parse_url(),
                    self.apiKey)
                search.execute(self.client, get_all=True)

                # Data Frame from json response
                for i in range(len(search.results_df['metrics'])):
                    result = search.results_df['metrics'][i]
                    result = result[0]['valueByYear']
                    institution = search.results_df['institution'][i]
                    institution = institution['id']
                    result_keys = result.keys()

                    for year in result_keys:
                        record = metric(year=year, value=result[year], universityId=University.objects.get(id = institution),
                                        subjectAreaId=SubjectArea.objects.get(id = s.id))
                        record.save()

    def db_update_uni(self, uni: University):
        try:
            CitationCount.objects.filter(universityId=uni.id).delete()
            CollaborationImpact.objects.filter(universityId=uni.id).delete()
            CitationsPerPublication.objects.filter(universityId=uni.id).delete()
            Collaboration.objects.filter(universityId=uni.id).delete()
            FieldWeightedCitationImpact.objects.filter(universityId=uni.id).delete()
            PublicationsInTopJournalPercentiles.objects.filter(universityId=uni.id).delete()
            OutputsInTopCitationPercentiles.objects.filter(universityId=uni.id).delete()
            ScholarlyOutput.objects.filter(universityId=uni.id).delete()

        except:
            print("Niepowodzenie")

        else:
            for metric in self.metrics:
                for s in self.subjectAreas:
                    search = ElsSearch(
                        Query(institutions=[uni.id], metric=metric, subjectAreaFilterURI=s.uri).parse_url(),
                        self.apiKey)
                    search.execute(self.client, get_all=True)

                    # Data Frame from json response
                    result = search.results_df['metrics'][0]
                    result = result[0]['valueByYear']
                    result_keys = result.keys()

                    for year in result_keys:
                        if metric == "CitationCount":
                            record = CitationCount(year=year, value=result[year], universityId=uni.id,
                                                   subjectAreaId=s.id)
                            record.save()
                        if metric == "CollaborationImpact":
                            record = CollaborationImpact(year=year, value=result[year], universityId=University.objects.get(id = uni.id),
                                        subjectAreaId=SubjectArea.objects.get(id = s.id))
                            record.save()
                        if metric == "CitationsPerPublication":
                            record = CitationsPerPublication(year=year, value=result[year], universityId=University.objects.get(id = uni.id),
                                        subjectAreaId=SubjectArea.objects.get(id = s.id))
                            record.save()
                        if metric == "Collaboration":
                            record = Collaboration(year=year, value=result[year], universityId=University.objects.get(id = uni.id),
                                        subjectAreaId=SubjectArea.objects.get(id = s.id))
                            record.save()
                        if metric == "FieldWeightedCitationImpact":
                            record = FieldWeightedCitationImpact(year=year, value=result[year],
                                                                 universityId=University.objects.get(id=uni.id),
                                                                 subjectAreaId=SubjectArea.objects.get(id=s.id))
                            record.save()
                        if metric == "PublicationsInTopJournalPercentiles":
                            record = PublicationsInTopJournalPercentiles(year=year, value=result[year],
                                                                         universityId=University.objects.get(id=uni.id),
                                                                         subjectAreaId=SubjectArea.objects.get(id=s.id))
                            record.save()
                        if metric == "OutputsInTopCitationPercentiles":
                            record = OutputsInTopCitationPercentiles(year=year, value=result[year],
                                                                     universityId=University.objects.get(id=uni.id),
                                                                     subjectAreaId=SubjectArea.objects.get(id=s.id))
                            record.save()
                        if metric == "ScholarlyOutput":
                            record = ScholarlyOutput(year=year, value=result[year], uuniversityId=University.objects.get(id = uni.id),
                                        subjectAreaId=SubjectArea.objects.get(id = s.id))
                            record.save()

    def db_update_subjectArea(self, s: SubjectArea):
        try:
            CitationCount.objects.filter(subjectAreaId=s.id).delete()
            CollaborationImpact.objects.filter(subjectAreaId=s.id).delete()
            CitationsPerPublication.objects.filter(subjectAreaId=s.id).delete()
            Collaboration.objects.filter(subjectAreaId=s.id).delete()
            FieldWeightedCitationImpact.objects.filter(subjectAreaId=s.id).delete()
            PublicationsInTopJournalPercentiles.objects.filter(subjectAreaId=s.id).delete()
            OutputsInTopCitationPercentiles.objects.filter(subjectAreaId=s.id).delete()
            ScholarlyOutput.objects.filter(subjectAreaId=s.id).delete()

        except:
            print("Niepowodzenie")

        else:
            for metric in self.metrics:
                for i in self.institutions:
                    search = ElsSearch(
                        Query(institutions=[i.id], metric=metric, subjectAreaFilterURI=s.uri).parse_url(),
                        self.apiKey)
                    search.execute(self.client, get_all=True)

                    for j in range(len(search.results_df['metrics'])):
                        result = search.results_df['institution'][j]
                        result = result[0]['valueByYear']
                        institution = search.results_df['institution'][j]
                        institution = institution['id']
                        result_keys = result.keys()

                        for year in result_keys:
                            if metric == "CitationCount":
                                record = CitationCount(year=year, value=result[year], universityId=University.objects.get(id = institution),
                                        subjectAreaId=SubjectArea.objects.get(id = s.id))
                                record.save()
                            if metric == "CollaborationImpact":
                                record = CollaborationImpact(year=year, value=result[year], universityId=University.objects.get(id = institution),
                                        subjectAreaId=SubjectArea.objects.get(id = s.id))
                                record.save()
                            if metric == "CitationsPerPublication":
                                record = CitationsPerPublication(year=year, value=result[year], universityId=University.objects.get(id = institution),
                                        subjectAreaId=SubjectArea.objects.get(id = s.id))
                                record.save()
                            if metric == "Collaboration":
                                record = Collaboration(year=year, value=result[year], universityId=University.objects.get(id = institution),
                                        subjectAreaId=SubjectArea.objects.get(id = s.id))
                                record.save()
                            if metric == "FieldWeightedCitationImpact":
                                record = FieldWeightedCitationImpact(year=year, value=result[year],
                                                                 universityId=University.objects.get(id = institution),
                                        subjectAreaId=SubjectArea.objects.get(id = s.id))
                                record.save()
                            if metric == "PublicationsInTopJournalPercentiles":
                                record = PublicationsInTopJournalPercentiles(year=year, value=result[year],
                                                                         universityId=University.objects.get(id = institution),
                                        subjectAreaId=SubjectArea.objects.get(id = s.id))
                                record.save()
                            if metric == "OutputsInTopCitationPercentiles":
                                record = OutputsInTopCitationPercentiles(year=year, value=result[year],
                                                                     universityId=University.objects.get(id = institution),
                                        subjectAreaId=SubjectArea.objects.get(id = s.id))
                                record.save()
                            if metric == "ScholarlyOutput":
                                record = ScholarlyOutput(year=year, value=result[year], universityId=University.objects.get(id = institution),
                                        subjectAreaId=SubjectArea.objects.get(id = s.id))
                                record.save()
