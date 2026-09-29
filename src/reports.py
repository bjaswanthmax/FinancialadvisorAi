from .analytics import (
    total_spending,
    average_expense,
    highest_expense,
    transaction_count,
    category_summary,
    merchant_summary,
    monthly_summary
)


def generate_report(df):
    if df.empty:
        return {
            "total_spending": 0.0,
            "average_expense": 0.0,
            "highest_expense": 0.0,
            "transaction_count": 0,
            "category_summary": [],
            "merchant_summary": [],
            "monthly_summary": []
        }

    return {
        "total_spending": total_spending(df),
        "average_expense": average_expense(df),
        "highest_expense": highest_expense(df),
        "transaction_count": transaction_count(df),
        "category_summary": category_summary(
            df
        ).to_dict("records"),
        "merchant_summary": merchant_summary(
            df
        ).to_dict("records"),
        "monthly_summary": monthly_summary(
            df
        ).to_dict("records")
    }