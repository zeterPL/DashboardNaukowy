class Query:

    # Query constructor. Institutions as table of IDs (IDs as strings), other fields as strings
    def __init__(self, institutions, metric="ScholarlyOutput", yearRange="5yrs", includeSelfCitations="true",
                 byYear="true", includedDocs="AllPublicationTypes", journalImpactType="CiteScore",
                 showAsFieldWeighted="false", subjectAreaFilterURI=None):
        self.institutions = institutions
        self.metric = metric
        self.yearRange = yearRange
        self.includeSelfCitations = includeSelfCitations
        self.byYear = byYear
        self.includedDocs = includedDocs
        self.journalImpactType = journalImpactType
        self.showAsFieldWeighted = showAsFieldWeighted
        if subjectAreaFilterURI:
            self.subjectAreaFilterURI = subjectAreaFilterURI.replace("/", "%2F")
        else:
            self.subjectAreaFilterURI = None

    def parse_url(self):
        result = self.metric + "&institutionIds="
        for i in self.institutions:
            result += str(i)
            if i != self.institutions[len(self.institutions) - 1]:
                result += "%2C"
            else:
                result += "&"
        result += "yearRange=" + self.yearRange + "&"
        if self.subjectAreaFilterURI:
            result += "subjectAreaFilterURI=" + self.subjectAreaFilterURI + "&"
        result += "includeSelfCitations=" + self.includeSelfCitations + "&"
        result += "byYear=" + self.byYear + "&"
        result += "includedDocs=" + self.includedDocs + "&"
        result += "journalImpactType=" + self.journalImpactType + "&"
        result += "showAsFieldWeighted=" + self.showAsFieldWeighted

        return result

