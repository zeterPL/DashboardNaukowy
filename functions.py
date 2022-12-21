import requests

import ApiConfig


def getIdInstitutionId(institutionName):
    if(institutionName == ""):
        institutionName = "Białystok University of technology"
    requestURL = "https://api.elsevier.com/analytics/scival/institution/search?query=name("+institutionName+")&limit=1&offset=0&apiKey=7f59af901d2d86f78a1fd60c1bf9426a"
    responseInstitutionId = requests.get(requestURL)
    resultInstitutionData = responseInstitutionId.json()['results']
    resultId = resultInstitutionData[0]['id']
    #print("Id",institutionName,"=",resultId)
    return resultId


def getSubjectUri(subjectName):
    if(subjectName == ""):
        return ""
    requestURL = "https://api.elsevier.com/analytics/scival/subjectArea/search?query=name("+subjectName+")%20AND%20classification(ASJC)&limit=1&offset=0&apiKey=7f59af901d2d86f78a1fd60c1bf9426a"
    responseSubjectUri = requests.get(requestURL)
    resultSubjectUri = responseSubjectUri.json()['results']
    subjectUri = resultSubjectUri[0]['uri']
    #print("Id",subjectName,"=",subjectUri)
    return subjectUri

def getInstitutionMetrics(institutionId="327005", subjectAreaFilterURI="", yearRange="10", includedDocs="AllPublicationTypes", metricTypes="ScholarlyOutput&institutionIds"):
    apiKey = ApiConfig.apiKey
    getMetricUrl = "https://api.elsevier.com/analytics/scival/institution/metrics?metricTypes="+str(metricTypes)+"="+str(institutionId)+"&yearRange="+str(yearRange)+"yrs&subjectAreaFilterURI="+str(subjectAreaFilterURI)+"&includeSelfCitations=true&byYear=true&includedDocs="+str(includedDocs)+"&journalImpactType=CiteScore&showAsFieldWeighted=false&apiKey="+str(apiKey)
    response = requests.get(getMetricUrl)
    ApiConfig.jprint(response.json())
    results = response.json()['results'];
    metrics = results[0]['metrics']
    yearsValues = metrics[0]['valueByYear']
    return ApiConfig.jprint(yearsValues);
def getImportantData():
    print('PODAJ nazwe uczelni (domyślnie PB):')
    institutionName = input()
    institutionId = getIdInstitutionId(institutionName)

    print('PODAJ filtr przedmiotu (domyślnie brak):')
    subjectName = input()
    subjectAreaFilterURI = getSubjectUri(subjectName)

    print('PODAJ liczbę lat (domyślnie 10):')
    yearRange = input()
    if(yearRange):
        yearRange = int(yearRange)
    else:
        yearRange = 10
    return institutionId, subjectAreaFilterURI, yearRange;