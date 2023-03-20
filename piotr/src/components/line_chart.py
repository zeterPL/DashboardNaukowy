import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from ..data.loader import DataSchema2
from . import ids
from piotr.api.requests import *

def render(app: Dash, data: pd.DataFrame) -> html.Div:
    @app.callback(
        Output(ids.LINE_CHART, "children"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.INSTITUTION_DROPDOWN, "value"),
            Input(ids.CATEGORY_DROPDOWN, "value"),
        ],
    )
    def update_line_chart(
        years: list[str], universityIds: list[str], subjectAreaIds: list[str]
    ) -> html.Div:
        filtered_data = data.query(
            "year in @years and universityId in @universityIds and subjectAreaId in @subjectAreaIds"
        )

        if filtered_data.shape[0] == 0:
            return html.Div("No data selected.", id=ids.LINE_CHART)
        def changeIndxToName(indx):
                return universityDictionary[indx]
        def create_table() -> pd.DataFrame:
            pt = filtered_data.pivot_table(
                values=DataSchema2.AMOUNT,
                index=[DataSchema2.YEAR, DataSchema2.UNIVERSITYID],
                aggfunc="sum",
                fill_value=0,
                dropna=False,
            )
            dataTable = pt.reset_index().sort_values(DataSchema2.YEAR, ascending=True)
            dataTable.columns = ['Rok', 'Uczelnia', 'Ilosc publikacji']
            dataTable["Uczelnia"] = dataTable[["Uczelnia"]].applymap(changeIndxToName)
            return dataTable

        fig = px.line(
            create_table(),
            x='Rok',
            y='Ilosc publikacji',
            color='Uczelnia',
            markers=True,
            text='Ilosc publikacji',
            title="Diagram liniowy",
        )
        fig.update_traces(textposition="bottom right")

        return html.Div(dcc.Graph(figure=fig), id=ids.LINE_CHART)

    return html.Div(id=ids.LINE_CHART)
