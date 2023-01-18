import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from ..data.loader import DataSchema
from . import ids


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    @app.callback(
        Output(ids.LINE_CHART, "children"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            # Input(ids.MONTH_DROPDOWN, "value"),
            Input(ids.INSTITUTION_DROPDOWN, "value"),
            Input(ids.CATEGORY_DROPDOWN, "value"),
        ],
    )
    def update_line_chart(
        years: list[str], institutions: list[str], categories: list[str]
    ) -> html.Div:
        filtered_data = data.query(
            "year in @years and institution in @institutions and category in @categories"
        )

        if filtered_data.shape[0] == 0:
            return html.Div("No data selected.", id=ids.LINE_CHART)

        def create_table() -> pd.DataFrame:
            pt = filtered_data.pivot_table(
                values=DataSchema.AMOUNT,
                index=[DataSchema.YEAR, DataSchema.INSTITUTION],
                aggfunc="sum",
                fill_value=0,
                dropna=False,
            )
            return pt.reset_index().sort_values(DataSchema.YEAR, ascending=True)

        fig = px.line(
            create_table(),
            x=DataSchema.YEAR,
            y=DataSchema.AMOUNT,
            color=DataSchema.INSTITUTION,
            markers=True,
            text="amount",
            title="Diagram liniowy",
        )
        fig.update_traces(textposition="bottom right")

        return html.Div(dcc.Graph(figure=fig), id=ids.LINE_CHART)

    return html.Div(id=ids.LINE_CHART)
