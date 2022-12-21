def drawGraph():
    import main
    yearRange = main.yearRange
    data = main.yearRange


    years = []
    for i in range(yearRange-1, -1, -1):
        years.append(str(2021-i))
    print(years)
    valuesOverTheYears = []
    for i in range(yearRange):
        valuesOverTheYears.append(data[years[i]])
    print(valuesOverTheYears)

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
    app.run_server(debug=True)