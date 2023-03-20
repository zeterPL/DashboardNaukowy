import pandas as pd
class DataSchema2:
    YEAR = "year"
    UNIVERSITYID = "universityId"
    SUBJECTAREAID = "subjectAreaId"
    SUBJECTID = "subjectId"
    AMOUNT = "amount"

def load_transaction_data(path: str) -> pd.DataFrame:
    # load the data from the CSV file
    data = pd.read_csv(
        path,
        dtype={
            DataSchema2.YEAR: str,
            DataSchema2.UNIVERSITYID: str,
            DataSchema2.SUBJECTAREAID: str,
            DataSchema2.SUBJECTID: str,
            DataSchema2.AMOUNT: int,
        },
        encoding="utf-8"
    )
    return data