import json
import pandas as pd
from elsapy.utils import recast_df



# nasz API_KEY = "c16459404285717f102391e3e8008be0"
# default API_KEY = "7f59af901d2d86f78a1fd60c1bf9426a"


class ElsSearch:
    """Represents a search to one of the search indexes accessible
         through api.elsevier.com. Returns True if successful; else, False."""

    # static / class variables
    _base_url = u'https://api.elsevier.com/analytics/scival/institution/metrics?metricTypes='

    def __init__(self, query, apiKey):
        """Initializes a search object with a query and target index."""
        self.query = query
        self._uri = self._base_url + self.query + "&apiKey=" + apiKey
        self.results_df = pd.DataFrame()

    # properties
    @property
    def query(self):
        """Gets the search query"""
        return self._query

    @query.setter
    def query(self, query):
        """Sets the search query"""
        self._query = query

    @property
    def results(self):
        """Gets the results for the search"""
        return self._results

    @property
    def tot_num_res(self):
        """Gets the total number of results that exist in the index for
            this query. This number might be larger than can be retrieved
            and stored in a single ElsSearch object (i.e. 5,000)."""
        return self._tot_num_res

    @property
    def num_res(self):
        """Gets the number of results for this query that are stored in the
            search object. This number might be smaller than the number of
            results that exist in the index for the query."""
        return len(self.results)

    @property
    def uri(self):
        """Gets the request uri for the search"""
        return self._uri

    def execute(
            self,
            els_client=None,
            get_all=True
    ):
        url = self._uri
        api_response = els_client.exec_request(url)
        self._tot_num_res = int(len(api_response['results']))
        self._results = api_response['results']
        if get_all is True:
            while self.num_res < self.tot_num_res:
                for e in api_response['results']['link']:
                    if e['@ref'] == 'next':
                        next_url = e['@href']
                api_response = els_client.exec_request(next_url)
                self._results += api_response['results']['entry']
        with open('dump.json', 'w') as f:
            f.write(json.dumps(self._results))
        self.results_df = recast_df(pd.DataFrame(self._results))


