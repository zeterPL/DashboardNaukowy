import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from ..data.loader import DataSchema2
from . import ids
from piotr.api.requests import *
def render(app: Dash, data: pd.DataFrame) -> html.Div:
    all_subjectAreas: list[str] = data[DataSchema2.SUBJECTAREAID].tolist()
    unique_subjectAreas: list[str] = sorted(set(all_subjectAreas))

    @app.callback(
        Output(ids.CATEGORY_DROPDOWN, "value"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            #Input(ids.INSTITUTION_DROPDOWN, "value"),
            Input(ids.SELECT_ALL_CATEGORIES_BUTTON, "n_clicks"),
        ],
    )
    def select_all_categories(years: list[str], _: int) -> list[str]:
        filtered_data = data.query("year in @years")
        return sorted(set(filtered_data[DataSchema2.SUBJECTAREAID].tolist()))

    return html.Div(
        children=[
            html.H6("Subject Area"),
            dcc.Dropdown(
                id=ids.CATEGORY_DROPDOWN,
                options=[
                    {"label": subjectAreaDisctionary[category], "value": category}
                    for category in unique_subjectAreas
                ],
                value=unique_subjectAreas,
                multi=False,
                placeholder="Select",
                clearable=False,
            ),
            html.Button(
                className="dropdown-button",
                children=["Select All"],
                id=ids.SELECT_ALL_CATEGORIES_BUTTON,
                n_clicks=0,
            ),
        ],
    )
