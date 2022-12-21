import json

apiKey = "7f59af901d2d86f78a1fd60c1bf9426a"

# #Id politechniki białostockiej
# institutionId = "327005"
# yearRange = 10
# metricTypes = "ScholarlyOutput&institutionIds"
# includedDocs = "AllPublicationTypes"
# subjectAreaFilterURI = "Class%2FASJC%2FCode%2F26" # filtr do publikacji dotyczacych matematyki
#
# getMetricUrl = "https://api.elsevier.com/analytics/scival/institution/metrics?metricTypes="+metricTypes+"=" + institutionId + "&yearRange="+ str(yearRange) +"yrs&subjectAreaFilterURI="+subjectAreaFilterURI+"&includeSelfCitations=true&byYear=true&includedDocs="+includedDocs+"&journalImpactType=CiteScore&showAsFieldWeighted=false&apiKey=" + apiKey


def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)
    return text