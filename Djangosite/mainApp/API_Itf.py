from elsapy.elsclient import ElsClient
from .components.data_getter import ElsSearch
from .components.query_class import Query
from .models import *

# Interface class used to connect database with API. Internal classes shouldn't be accessed directly
class API_Interface:

    # nasz API_KEY = "c16459404285717f102391e3e8008be0"
    # default API_KEY = "7f59af901d2d86f78a1fd60c1bf9426a"

    def __init__(self, apiKey="7f59af901d2d86f78a1fd60c1bf9426a"):
        self.apiKey = apiKey
        self.client = ElsClient(apiKey)
        self.institutions = University.objects.all()
        self.metrics = Abstractmetric.objects.all()
        self.subjectAreas = SubjectArea.objects.all()

    def db_fill(self):

        try:
            for metric in self.metrics:
                metric.objects.all().delete()

        except:
            print("Niepowodzenie")

        else:
            for metric in self.metrics:
                for i in self.institutions:
                    for s in self.subjectAreas:
                        search = ElsSearch(
                            Query(institutions=[i.id], metric=metric.__str__(), subjectAreaFilterURI=s.uri).parse_url(),self.apiKey)
                        search.execute(self.client, get_all=True)

                        # Data Frame from json response
                        result = search.results_df['metrics'][0]
                        result = result[0]['valueByYear']
                        result_keys = result.keys()

                        for year in result_keys:
                            record = metric(year=year, value=result[year], universityId=i.id, subjectAreaId=s.id)
                            record.save()

    # Update given metrics or given uni or given SubjectArea
    def db_update_metric(self, metric: Abstractmetric):
        try:
            metric.objects.all().delete()

        except:
            print("Niepowodzenie")

        else:
            for i in self.institutions:
                for s in self.subjectAreas:
                    search = ElsSearch(
                        Query(institutions=[i.id], metric=metric.__str__(), subjectAreaFilterURI=s.uri).parse_url(), self.apiKey)
                    search.execute(self.client, get_all=True)

                    # Data Frame from json response
                    result = search.results_df['metrics'][0]
                    result = result[0]['valueByYear']
                    result_keys = result.keys()

                    for year in result_keys:
                        if year == '2013':
                            record = metric(year=year, value=result[year], universityId=i.id, subjectAreaId=s.id)
                            record.save()

    def db_update_uni(self, uni: University):
        try:
            for metric in self.metrics:
                metric.objects.filter(universityId=uni.id).delete()

        except:
            print("Niepowodzenie")

        else:
            for metric in self.metrics:
                for s in self.subjectAreas:
                    search = ElsSearch(
                        Query(institutions=[uni.id], metric=metric.__str__(), subjectAreaFilterURI=s.uri).parse_url(), self.apiKey)
                    search.execute(self.client, get_all=True)

                    # Data Frame from json response
                    result = search.results_df['metrics'][0]
                    result = result[0]['valueByYear']
                    result_keys = result.keys()

                    for year in result_keys:
                        record = metric(year=year, value=result[year], universityId=uni.id, subjectAreaId=s.id)
                        record.save()

    def db_update_subjectArea(self, sA: SubjectArea):
        try:
            for metric in self.metrics:
                metric.objects.filter(subjectAreaId=sA.id).delete()

        except:
            print("Niepowodzenie")

        else:
            for metric in self.metrics:
                for i in self.institutions:
                    search = ElsSearch(
                        Query(institutions=[i.id], metric=metric.__str__(), subjectAreaFilterURI=sA.uri).parse_url(), self.apiKey)
                    search.execute(self.client, get_all=True)

                    # Data Frame from json response
                    result = search.results_df['metrics'][0]
                    result = result[0]['valueByYear']
                    result_keys = result.keys()

                    for year in result_keys:
                        record = metric(year=year, value=result[year], universityId=i.id, subjectAreaId=sA.id)
                        record.save()
