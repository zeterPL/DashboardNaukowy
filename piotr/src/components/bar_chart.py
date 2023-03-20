import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from . import ids
from piotr.src.data.loader import *
#from ..data.loader import DataSchema2
from piotr.api.requests import *

def render(app: Dash, data: pd.DataFrame) -> html.Div:

    @app.callback(
        Output(ids.BAR_CHART, "children"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.INSTITUTION_DROPDOWN, "value"),
            Input(ids.CATEGORY_DROPDOWN, "value"),
        ],
    )
    def update_bar_chart(
        years: list[str], universityIds: list[str], subjectAreaIds: list[str]
    ) -> html.Div:
        filtered_data = data.query(
            "year in @years and universityId in @universityIds and subjectAreaId in @subjectAreaIds"
        )

        if filtered_data.shape[0] == 0:
            return html.Div("No data selected.", id=ids.BAR_CHART)
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

        fig = px.bar(
            create_table(),
            x='Rok',
            y='Ilosc publikacji',
            color='Uczelnia',
            barmode="group",
            text_auto=True,
            title="Diagram barowy",
        )
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
        return html.Div(dcc.Graph(figure=fig), id=ids.BAR_CHART)

    return html.Div(id=ids.BAR_CHART)
