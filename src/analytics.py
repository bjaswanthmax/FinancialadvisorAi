import pandas as pd


def expenses_to_dataframe(expenses):
    if not expenses:
        return pd.DataFrame(
            columns=[
                "ID",
                "Merchant",
                "Amount",
                "Category",
                "Date",
                "Source"
            ]
        )

    data = []

    for item in expenses:
        data.append({
            "ID": item[0],
            "Merchant": item[1],
            "Amount": item[2],
            "Category": item[3],
            "Date": item[4],
            "Source": item[5]
        })

    df = pd.DataFrame(data)

    df["Amount"] = pd.to_numeric(
        df["Amount"],
        errors="coerce"
    )

    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

    return df


def total_spending(df):
    if df.empty:
        return 0.0

    return float(
        df["Amount"].sum()
    )


def average_expense(df):
    if df.empty:
        return 0.0

    return float(
        df["Amount"].mean()
    )


def highest_expense(df):
    if df.empty:
        return 0.0

    return float(
        df["Amount"].max()
    )


def transaction_count(df):
    return len(df)


def category_summary(df):
    if df.empty:
        return pd.DataFrame(
            columns=[
                "Category",
                "Amount"
            ]
        )

    summary = (
        df.groupby("Category")["Amount"]
        .sum()
        .reset_index()
        .sort_values(
            "Amount",
            ascending=False
        )
    )

    return summary


def merchant_summary(df):
    if df.empty:
        return pd.DataFrame(
            columns=[
                "Merchant",
                "Amount"
            ]
        )

    summary = (
        df.groupby("Merchant")["Amount"]
        .sum()
        .reset_index()
        .sort_values(
            "Amount",
            ascending=False
        )
    )

    return summary


def monthly_summary(df):
    if df.empty:
        return pd.DataFrame(
            columns=[
                "Month",
                "Amount"
            ]
        )

    temp_df = df.copy()

    temp_df["Month"] = (
        temp_df["Date"]
        .dt.to_period("M")
        .astype(str)
    )

    summary = (
        temp_df.groupby("Month")["Amount"]
        .sum()
        .reset_index()
        .sort_values("Month")
    )

    return summary


def source_summary(df):
    if df.empty:
        return pd.DataFrame(
            columns=[
                "Source",
                "Amount"
            ]
        )

    summary = (
        df.groupby("Source")["Amount"]
        .sum()
        .reset_index()
        .sort_values(
            "Amount",
            ascending=False
        )
    )

    return summary


def highest_spending_category(df):
    summary = category_summary(df)

    if summary.empty:
        return None

    return summary.iloc[0]["Category"]


def highest_spending_merchant(df):
    summary = merchant_summary(df)

    if summary.empty:
        return None

    return summary.iloc[0]["Merchant"]


def category_percentage(df, category):
    total = total_spending(df)

    if total == 0:
        return 0.0

    category_total = df.loc[
        df["Category"] == category,
        "Amount"
    ].sum()

    return float(
        (category_total / total) * 100
    )


def monthly_expenses(df, year, month):
    if df.empty:
        return df.copy()

    return df[
        (df["Date"].dt.year == year) &
        (df["Date"].dt.month == month)
    ].copy()