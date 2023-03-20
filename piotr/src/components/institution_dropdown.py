import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output


from . import ids
from ..data.loader import DataSchema2
from piotr.src.data.loader import *
from piotr.api.requests import *

def render(app: Dash, data: pd.DataFrame) -> html.Div:
    all_institutions: list[str] = data[DataSchema2.UNIVERSITYID].tolist()
    unique_institutions: list[str] = sorted(set(all_institutions))

    @app.callback(
        Output(ids.INSTITUTION_DROPDOWN, "value"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.SELECT_ALL_INSTITUTIONS_BUTTON, "n_clicks"),
        ],
    )
    def select_all_institutions(years: list[str], _: int) -> list[str]:
        filtered_data = data.query("year in @years")
        return sorted(set(filtered_data[DataSchema2.UNIVERSITYID].tolist()))


    return html.Div(
        children=[
            html.H6("Institution"),
            dcc.Dropdown(
                id=ids.INSTITUTION_DROPDOWN,
                options=[{"label": universityDictionary[institution], "value": institution} for institution in unique_institutions],
                value=unique_institutions,
                multi=True,
            ),
            html.Button(
                className="dropdown-button",
                children=["Select All"],
                id=ids.SELECT_ALL_INSTITUTIONS_BUTTON,
                n_clicks=0,
            ),
        ]
    )

