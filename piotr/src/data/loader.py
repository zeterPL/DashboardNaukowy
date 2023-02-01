import pandas as pd


class DataSchema:
    AMOUNT = "amount"
    CATEGORY = "category"
    DATE = "date"
    # MONTH = "month"
    INSTITUTION = "institution"
    YEAR = "year"


def load_transaction_data(path: str) -> pd.DataFrame:
    # load the data from the CSV file
    data = pd.read_csv(
        path,
        dtype={
            DataSchema.AMOUNT: float,
            DataSchema.CATEGORY: str,
            DataSchema.YEAR: str,
            DataSchema.INSTITUTION: str,
        },
    )
    return data
