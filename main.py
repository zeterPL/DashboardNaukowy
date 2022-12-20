import requests
import ApiConfig as apiconfig

if __name__ == '__main__':
    response = requests.get(apiconfig.getMetricUrl)
    apiconfig.jprint(response.json())
    results = response.json()['results'];
    metrics = results[0]['metrics']
    yearsValues = metrics[0]['valueByYear']
    x = apiconfig.jprint(yearsValues);

import json
data = json.loads(x)

years = []
for i in range(apiconfig.yearRange-1, -1, -1):
    years.append(str(2021-i))
#print(years)
valuesOverTheYears = []
for i in range(apiconfig.yearRange):
    valuesOverTheYears.append(data[years[i]])
#print(valuesOverTheYears)

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

df = pd.DataFrame({
    "Rok": years,
    "Ilosc publikacji czy czegos tam": valuesOverTheYears
})

fig = px.bar(df, x="Rok", y="Ilosc publikacji czy czegos tam", title="Tytul diagramu1")

app.layout = html.Div(children=[
    html.H1(children='Wykres'),

    html.Div(children='''
        Opis diagramu
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),
    dcc.Graph(
        id='example-graph2',
        figure={
                "data": [
                    {
                        "x": years,
                        "y": valuesOverTheYears,
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Tytul diagramu2"},
        },
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
