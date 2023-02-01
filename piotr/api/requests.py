import json

import requests

API_KEY  = '7f59af901d2d86f78a1fd60c1bf9426a'

# Data that needs to be fetched:

def getInstitutionId(institutionName):
    # if(institutionName == ""):
    #     institutionName = "Białystok University of technology"
    requestURL = "https://api.elsevier.com/analytics/scival/institution/search?query=name("+institutionName+")&limit=1&offset=0&apiKey=7f59af901d2d86f78a1fd60c1bf9426a"
    responseInstitutionId = requests.get(requestURL)
    resultInstitutionData = responseInstitutionId.json()['results']
    resultId = resultInstitutionData[0]['id']
    print("InstitutionId = ",resultId, "\nInstitution researched name = ", resultInstitutionData[0]['name'])
    return resultId, resultInstitutionData[0]['name']


def getSubjectUri(subjectName):
    if(subjectName == ""):
        return ""
    requestURL = "https://api.elsevier.com/analytics/scival/subjectArea/search?query=name("+subjectName+")%20AND%20classification(ASJC)&limit=1&offset=0&apiKey=7f59af901d2d86f78a1fd60c1bf9426a"
    responseSubjectUri = requests.get(requestURL)
    resultSubjectUri = responseSubjectUri.json()['results']
    subjectUri = resultSubjectUri[0]['uri']
    print("SubjectId = ",resultSubjectUri[0]['id'],"\nSubjectName=", resultSubjectUri[0]['name'], "\nZwracane uri funkcji: ", subjectUri)
    return subjectUri, resultSubjectUri[0]['name']

#PB institutionId="327005"
def getInstitutionMetrics(institutionId="", subjectAreaFilterURI="", yearRange="10", includedDocs="AllPublicationTypes", metricTypes="ScholarlyOutput&institutionIds"):
    apiKey = API_KEY
    getMetricUrl = "https://api.elsevier.com/analytics/scival/institution/metrics?metricTypes="+str(metricTypes)+"="+str(institutionId)+"&yearRange="+str(yearRange)+"yrs&subjectAreaFilterURI="+str(subjectAreaFilterURI)+"&includeSelfCitations=true&byYear=true&includedDocs="+str(includedDocs)+"&journalImpactType=CiteScore&showAsFieldWeighted=false&apiKey="+str(apiKey)
    response = requests.get(getMetricUrl)
    jprint(response.json())
    results = response.json()['results'];
    metrics = results[0]['metrics']
    yearsValues = metrics[0]['valueByYear']
    return jprint(yearsValues);

def getData(institutionName, subjectName):
    print(institutionName)
    institutionId, institutionNameFound = getInstitutionId(institutionName)
    subjectAreaFilterURI, subjectNameFound = getSubjectUri(subjectName)
    yearRange = 10
    return getInstitutionMetrics(institutionId, subjectAreaFilterURI, yearRange), subjectNameFound, institutionNameFound


def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    #print(text)
    return text









# Get all institutions
# Get institution id by name

#nie działa, bo scival ma ograniczenie do 100 instytucji
def getAllInstitutions():
    url = "https://api.elsevier.com/analytics/scival/institution"
    response = requests.get(url, headers={
        'Accept':'application/json',
        'X-ELS-APIKey': '7f59af901d2d86f78a1fd60c1bf9426a'
        }).json()
    print(response)

#nie uzywane juz
def getImportantDataByInputs():
    print('PODAJ nazwe uczelni (domyślnie PB):')
    institutionName = input()
    institutionId = getInstitutionId(institutionName)

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