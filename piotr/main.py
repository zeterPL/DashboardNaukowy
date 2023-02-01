import json

from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP

from src.components.layout import create_layout
from src.data.loader import load_transaction_data

from api.requests import getData

DATA_PATH = "./data/bazaDanych.txt"


def main() -> None:

    path = "data/bazaDanych.txt"

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

    # instuitionName = "Warsaw University"
    # subjectName = "mathematic"
    # jsonData, subjectName, instuitionName = getData(instuitionName, subjectName)
    # dataFromApi = json.loads(jsonData)
    # print(dataFromApi)
    # valuesOverTheYears, years = extractDataFromJsonToArrays(dataFromApi)
    # saveDataToFile(path, valuesOverTheYears, years, instuitionName, subjectName)
    #
    #

    # load the data and create the data manager
    data = load_transaction_data(DATA_PATH)

    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = "NAUKOWY Dashboard"
    app.layout = create_layout(app, data)
    app.run()


if __name__ == "__main__":
    main()
