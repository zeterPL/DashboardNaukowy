import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from ..data.loader import DataSchema
from . import ids


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    @app.callback(
        Output(ids.BAR_CHART, "children"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            # Input(ids.MONTH_DROPDOWN, "value"),
            Input(ids.INSTITUTION_DROPDOWN, "value"),
            Input(ids.CATEGORY_DROPDOWN, "value"),
        ],
    )
    def update_bar_chart(
        years: list[str], institutions: list[str], categories: list[str]
    ) -> html.Div:
        filtered_data = data.query(
            "year in @years and institution in @institutions and category in @categories"
        )

        if filtered_data.shape[0] == 0:
            return html.Div("No data selected.", id=ids.BAR_CHART)

        def create_pivot_table() -> pd.DataFrame:
            pt = filtered_data.pivot_table(
                values=DataSchema.AMOUNT,
                # index=[DataSchema.CATEGORY],
                index=[DataSchema.YEAR],
                aggfunc="sum",
                fill_value=0,
                dropna=False,
            )
            return pt.reset_index().sort_values(DataSchema.YEAR, ascending=True)

        def create_table() -> pd.DataFrame:
            pt = filtered_data.pivot_table(
                values=DataSchema.AMOUNT,
                index=[DataSchema.YEAR, DataSchema.INSTITUTION],
                aggfunc="sum",
                fill_value=0,
                dropna=False,
            )
            return pt.reset_index().sort_values(DataSchema.YEAR, ascending=True)

        fig = px.bar(
            create_table(),
            # filtered_data,
            #create_pivot_table(),
            x=DataSchema.YEAR,
            y=DataSchema.AMOUNT,
            #color=DataSchema.YEAR,
            color=DataSchema.INSTITUTION,
            barmode="group",
            text_auto=True,
            title="Diagram barowy",
        )
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
        return html.Div(dcc.Graph(figure=fig), id=ids.BAR_CHART)

    return html.Div(id=ids.BAR_CHART)
