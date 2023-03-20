import pandas as pd
from dash import Dash, html
from piotr.src.components import (
    bar_chart,
    line_chart,
    category_dropdown,
    institution_dropdown,
    year_dropdown,
    searchNewData,
)


def create_layout(app: Dash, data: pd.DataFrame) -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title),
            html.Hr(),
            html.Div(
                className="dropdown-container",
                children=[
                    year_dropdown.render(app, data),
                    institution_dropdown.render(app, data),
                    category_dropdown.render(app, data),
                ],
            ),
            bar_chart.render(app, data),
            line_chart.render(app, data),
            # html.H1("Dodawanie nowych danych do bazy danych: "),
            # html.Div(
            #     className="inputs-container",
            #     children=[
            #         searchNewData.render(app),
            #     ],
            # ),
        ],
    )
