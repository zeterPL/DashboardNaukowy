import json

import pandas as pd
from dash import Dash, dcc, html, ctx
from dash.dependencies import Input, Output, State

from . import ids
from piotr.api.requests import getSubjectUri, getData
from piotr.api.requests import getInstitutionId

def render(app: Dash) -> html.Div:
    @app.callback([Output(ids.INPUT_DATA, 'children'),
                  Output(ids.SUBMIT_RESULT_MESSAGE, 'children')],
                  Input(ids.SEARCH_INPUT_BUTTON, 'n_clicks'),
                  Input(ids.SUBMIT_BUTTON_NEW_QUERRY_DATABASE, 'n_clicks'),
                  State('input-1-state', 'value'),
                  State('input-2-state', 'value'))

    def update_output(search_clicks, submit_clicks, input1, input2):
        #print("Update output is working XD")
        if ids.SEARCH_INPUT_BUTTON == ctx.triggered_id:
            return update_search(input1, input2)
        if ids.SUBMIT_BUTTON_NEW_QUERRY_DATABASE == ctx.triggered_id:
            return submit_to_Database(input1, input2)
        # institutionId, institutionName = getInstitutionId(input1)
        # subjectUri, findedSubjectName = getSubjectUri(input2)
        # return u'''Finded Institution is "{}" and Finded subject is "{}"'''.format(institutionName, findedSubjectName)

    def update_search(input1, input2):
        if(input1 == "" or input2 == ""):
            return "Input1 or INput2 is empty", ""
        try:
            institutionId, institutionName = getInstitutionId(input1)
            subjectUri, findedSubjectName = getSubjectUri(input2)
        except:
            return "Can't find anything from this data", ""
        return u'''Finded Institution is "{}" and Finded subject is "{}"'''.format(institutionName, findedSubjectName), ""

    def submit_to_Database(input1, input2):
        if (input1 == "" or input2 == ""):
            return "","Cant submit to database, because Input1 or INput2 is empty"
        try:
            instuitionName = input1
            subjectName = input2
            jsonData, subjectName, instuitionName = getData(instuitionName, subjectName)
            dataFromApi = json.loads(jsonData)
            print("Data from API: ",dataFromApi)
            valuesOverTheYears, years = extractDataFromJsonToArrays(dataFromApi)
            saveDataToFile(DATA_PATH, valuesOverTheYears, years, instuitionName, subjectName)
        except:
            return "", "Submit failed"
        return "","Submit successful"


    return html.Div([
    html.Span("Nazwa Instytucji i nazwa przedmiotu: "),
    html.Br(),
    dcc.Input(id='input-1-state', type='text', value=''),
    dcc.Input(id='input-2-state', type='text', value=''),
    html.Button(name="Search button",id=ids.SEARCH_INPUT_BUTTON, n_clicks=0, children='Search'),
    html.Div(id=ids.INPUT_DATA, className="SearchDiv"),
    html.Br(),
    html.Button(name="Submit button",id=ids.SUBMIT_BUTTON_NEW_QUERRY_DATABASE, n_clicks=0, children="Submit to Database"),
    html.Div(id=ids.SUBMIT_RESULT_MESSAGE, className="SubmitMessageDiv"),
])


DATA_PATH = "./data/bazaDanych.txt"
def saveDataToFile(path, valuesOverTheYears, years, instuitionName, subjectName):
    f = open(path, "a")
    for i in range(len(valuesOverTheYears)):
        dataArray = [years[i], valuesOverTheYears[i], instuitionName, subjectName]
        f.write(str(dataArray[0]) + "," + str(dataArray[1]) + "," + str(dataArray[2]) + "," + str(dataArray[3]) + "\n")
    f.close()

def extractDataFromJsonToArrays(dataFromApi):
    yearRange = 0
    for i in dataFromApi:
        yearRange += 1
    years = []
    for i in range(yearRange - 1, -1, -1):
        years.append(str(2021 - i))
    print(years)
    valuesOverTheYears = []
    for i in range(yearRange):
        valuesOverTheYears.append(dataFromApi[years[i]])
    print(valuesOverTheYears)
    return valuesOverTheYears, years