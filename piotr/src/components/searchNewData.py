import json

import pandas as pd
from dash import Dash, dcc, html, ctx
from dash.dependencies import Input, Output, State

from . import ids
from piotr.api.requests import *
DATA_PATH = "./data/bazaDanych.txt"
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
            print("Update Search Input1 = "+input1+" Input2 = "+input2)
            institutionId, institutionName = getInstitutionId(input1)
            subjectUri, findedSubjectName = getSubjectUri(input2)
            print("Update Search InstitutionName = "+institutionName+" SubjectName = "+findedSubjectName)
        except:
            return "Can't find anything from this data", ""
        print("Przed returnem = {}, {}".format(institutionName,findedSubjectName))
        return u'''Finded Institution is "{}" and Finded subject is "{}"'''.format(institutionName, findedSubjectName), ""

    def submit_to_Database(input1, input2):
        if (input1 == "" or input2 == ""):
            return "","Cant submit to database, because Input1 or INput2 is empty"
        try:
            #institutionName = input1 #stara wersja
            #subjectName = input2 #stara wersja
            print("Submit Input1 = " + input1 + " Input2 = " + input2)
            institutionId, institutionName = getInstitutionId(input1)
            subjectUri, subjectName = getSubjectUri(input2)
            print("Submit to Database InstitutionName = " + institutionName + " SubjectName = " + subjectName)
            jsonData, subjectName, instuitionName = getData(institutionName, subjectName)
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