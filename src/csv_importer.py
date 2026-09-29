import pandas as pd


REQUIRED_COLUMNS = [
    "Merchant",
    "Amount",
    "Category",
    "Date"
]


def validate_csv(df):
    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    return missing_columns


def prepare_csv(df):
    missing_columns = validate_csv(df)

    if missing_columns:
        raise ValueError(
            "Missing columns: "
            + ", ".join(missing_columns)
        )

    result = df.copy()

    result["Amount"] = pd.to_numeric(
        result["Amount"],
        errors="coerce"
    )

    result["Date"] = pd.to_datetime(
        result["Date"],
        errors="coerce"
    )

    result = result.dropna(
        subset=[
            "Merchant",
            "Amount",
            "Date"
        ]
    )

    if "Category" not in result:
        result["Category"] = "Other"

    result["Source"] = "CSV"

    return result


def csv_preview(df):
    prepared = prepare_csv(df)

    return prepared[
        [
            "Merchant",
            "Amount",
            "Category",
            "Date",
            "Source"
        ]
    ]