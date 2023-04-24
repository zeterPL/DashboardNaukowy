import json

from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP

from src.components.layout import create_layout
from src.data.loader import load_transaction_data

from api.requests import *

DATA_PATH = "./data/data.txt"

def saveMetricsData():
    print("Pobranie i zapisanie głównych danych")
    downloadAndSaveMainData()

def changeNullTo0():
    metricTypes = ["OutputsInTopCitationPercentiles", "PublicationsInTopJournalPercentiles", "ScholarlyOutput","FieldWeightedCitationImpact", "CollaborationImpact", "CitationsPerPublication", "CitationCount","Collaboration"]
    for metricType in metricTypes:
        text = ""
        with open('./data/metrics/' + metricType + '.txt', 'r', encoding="utf-8") as file:
            for line in file:
                elements = line.strip().split(',')
                value_in_4_column = elements[3]
                if value_in_4_column == 'None':
                    elements[3] = '0'
                    line_corrected = ','.join(elements)+'\n'
                else:
                    line_corrected = line
                text += line_corrected

        with open('./data/metrics/' + metricType + '.txt', 'w', encoding="utf-8") as file:
            file.write(text)


def main() -> None:
    #pobranie i zapisanie w plikach wszystkich danych z API
    #saveMetricsData()
    #changeNullTo0()

    # load the data and create the data manager
    data = load_transaction_data(DATA_PATH)
    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = "NAUKOWY Dashboard"
    app.layout = create_layout(app, data)
    app.run()

if __name__ == "__main__":
    main()
