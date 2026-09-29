from .analytics import (
    total_spending,
    average_expense,
    highest_expense,
    transaction_count,
    category_summary,
    merchant_summary,
    monthly_summary,
    source_summary,
    highest_spending_category,
    highest_spending_merchant
)

from .budget import (
    budget_percentage,
    remaining_budget,
    budget_status,
    analyze_budget,
    category_budget_status
)

from .reports import generate_report


def get_spending_summary(df):
    return {
        "total_spending": total_spending(df),
        "average_expense": average_expense(df),
        "highest_expense": highest_expense(df),
        "transaction_count": transaction_count(df),
        "highest_category": highest_spending_category(df),
        "highest_merchant": highest_spending_merchant(df)
    }


def get_category_analysis(df):
    return category_summary(df)


def get_merchant_analysis(df):
    return merchant_summary(df)


def get_monthly_analysis(df):
    return monthly_summary(df)


def get_source_analysis(df):
    return source_summary(df)


def get_budget_analysis(spending, budget):
    return analyze_budget(
        spending,
        budget
    )


def get_category_budget_analysis(
    spending,
    budget,
    category
):
    return category_budget_status(
        spending,
        budget,
        category
    )


def get_budget_percentage(
    spending,
    budget
):
    return budget_percentage(
        spending,
        budget
    )


def get_remaining_budget(
    spending,
    budget
):
    return remaining_budget(
        spending,
        budget
    )


def get_budget_status(
    spending,
    budget
):
    return budget_status(
        spending,
        budget
    )


def get_financial_report(df):
    return generate_report(df)