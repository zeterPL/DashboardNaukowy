import json

import requests

import pandas as pd

API_KEY  = '7f59af901d2d86f78a1fd60c1bf9426a'

def load_text_data(path: str):
    list = []
    with open(path, 'r', encoding="utf-8") as file:
        for line in file:
            line = line.strip().split(';')
            list.append(line)
    return list
universityData = load_text_data("./data/university.txt")
universityDictionary = {x[0]: x[1] for x in universityData}
subjectAreaData = load_text_data("./data/subjectAreas.txt")
subjectAreaDisctionary = {x[0]: x[1] for x in subjectAreaData}
def saveDataToFile(path, valuesOverTheYears, years, instuitionName, subjectName):
    f = open(path, "a", encoding="utf-8")
    for i in range(len(valuesOverTheYears)):
        dataArray = [years[i], valuesOverTheYears[i], instuitionName, subjectName]
        print("SAVE DATA TO FILE inst: "+instuitionName)
        f.write(str(dataArray[0]) + "," + str(dataArray[1]) + "," + str(dataArray[2]) + "," + str(dataArray[3]) + "\n")
    f.close()

def extractDataFromJsonToArrays(dataFromApi):
    yearRange = len(dataFromApi)
    years = []
    for i in range(yearRange - 1, -1, -1):
        years.append(str(2021 - i))
    #print(years)
    valuesOverTheYears = []
    for i in range(yearRange):
        valuesOverTheYears.append(dataFromApi[years[i]])
    #print(valuesOverTheYears)
    return valuesOverTheYears, years

def getInstitutionId(institutionName):
    # if(institutionName == ""):
    #     institutionName = "Białystok University of technology"
    requestURL = "https://api.elsevier.com/analytics/scival/institution/search?query=name("+institutionName+")&limit=1&offset=0&apiKey="+API_KEY
    responseInstitutionId = requests.get(requestURL)
    resultInstitutionData = responseInstitutionId.json()['results']
    resultId = resultInstitutionData[0]['id']
    print("InstitutionId = ",resultId, "\nInstitution researched name = ", resultInstitutionData[0]['name'])
    return resultId, resultInstitutionData[0]['name']


def getSubjectUri(subjectName):
    if(subjectName == ""):
        return ""
    requestURL = "https://api.elsevier.com/analytics/scival/subjectArea/search?query=name("+subjectName+")%20AND%20classification(ASJC)&limit=1&offset=0&apiKey="+API_KEY
    responseSubjectUri = requests.get(requestURL)
    resultSubjectUri = responseSubjectUri.json()['results']
    subjectUri = resultSubjectUri[0]['uri']
    print("SubjectId = ",resultSubjectUri[0]['id'],"\nSubjectName=", resultSubjectUri[0]['name'], "\nZwracane uri funkcji: ", subjectUri)
    return subjectUri, resultSubjectUri[0]['name']

#PB institutionId="327005"
def getInstitutionMetrics(institutionId="", subjectAreaFilterURI="", yearRange="10", includedDocs="AllPublicationTypes", metricTypes="ScholarlyOutput&institutionIds"):
    getMetricUrl = "https://api.elsevier.com/analytics/scival/institution/metrics?metricTypes="+str(metricTypes)+"="+str(institutionId)+"&yearRange="+str(yearRange)+"yrs&subjectAreaFilterURI="+str(subjectAreaFilterURI)+"&includeSelfCitations=true&byYear=true&includedDocs="+str(includedDocs)+"&journalImpactType=CiteScore&showAsFieldWeighted=false&apiKey="+API_KEY
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

#uzyte tylko raz do wygenerowania listy dziedzin naukowych
def getMainSubjectAreas():
    mainSubjectsList = []
    for i in range(10, 37):
        requestUrl = "https://api.elsevier.com/analytics/scival/subjectArea/"+str(i)+"?classificationType=ASJC&apiKey="+API_KEY
        response = requests.get(requestUrl)
        subjectName = response.json()['subjectArea']['name']
        #print(subjectName)
        mainSubjectsList.append(subjectName)
    return mainSubjectsList

#uzyte tylko raz do pobrania i zapisania glownych danych
def getMainData():
    mainData = []
    universityList = []
    with open('./data/university.txt', 'r', encoding="utf-8") as file:
        for line in file:
            line = line.strip().split(';')
            universityList.append(line)
    #print(universityList)
    mainSubjectsList = []
    with open('./data/subjectAreas.txt', 'r', encoding="utf-8") as file:
        for line in file:
            line = line.strip().split(';')
            mainSubjectsList.append(line)
    #print(mainSubjectsList)
    with open('./data/data.txt', 'a', encoding="utf-8") as file:
        for univers in universityList:
            for subject in mainSubjectsList:
                requestURL = "https://api.elsevier.com/analytics/scival/institution/metrics?metricTypes=ScholarlyOutput&institutionIds="+univers[0]+"&yearRange=10yrs&subjectAreaFilterURI=Class%2FASJC%2FCode%2F"+subject[0]+"&includeSelfCitations=true&byYear=true&includedDocs=AllPublicationTypes&journalImpactType=CiteScore&showAsFieldWeighted=false&apiKey="+API_KEY
                response = requests.get(requestURL)
                yearsValues = response.json()['results'][0]['metrics'][0]['valueByYear']
                amountInYear, years = extractDataFromJsonToArrays(yearsValues)
                for i in range(len(years)):
                    file.write(str(years[i])+ "," + str(univers[0]) + "," + str(subject[0]) + "," + str(subject[0]) + "," + str(amountInYear[i]) + "\n")
