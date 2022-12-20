import json

apiKey = "7f59af901d2d86f78a1fd60c1bf9426a"

#Id politechniki białostockiej
institutionId = "327005"
numberOfYears = 10

getMetricUrl = "https://api.elsevier.com/analytics/scival/institution/metrics?metricTypes=ScholarlyOutput&institutionIds=" + institutionId + "&yearRange="+ str(numberOfYears) +"yrs&includeSelfCitations=true&byYear=true&includedDocs=AllPublicationTypes&journalImpactType=CiteScore&showAsFieldWeighted=false&apiKey=" + apiKey


def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    #print(text)
    return text