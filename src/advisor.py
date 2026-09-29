from .financial_tools import (
    get_spending_summary,
    get_category_analysis,
    get_merchant_analysis,
    get_budget_analysis
)

from .indian_finance import (
    get_indian_finance_advice
)


def get_financial_advice(category, amount):

    if amount is None:
        amount = 0

    if category == "Food":
        return (
            f"You spent ₹{amount:.2f} on Food. "
            "Track your food expenses and avoid "
            "unplanned purchases."
        )

    elif category == "Shopping":
        return (
            f"You spent ₹{amount:.2f} on Shopping. "
            "Consider whether similar purchases are "
            "necessary before spending."
        )

    elif category == "Transport":
        return (
            f"You spent ₹{amount:.2f} on Transport. "
            "Monitor transportation expenses regularly."
        )

    elif category == "Bills":
        return (
            f"You spent ₹{amount:.2f} on Bills. "
            "Track recurring bills and monthly totals."
        )

    elif category == "Healthcare":
        return (
            f"You spent ₹{amount:.2f} on Healthcare. "
            "Keep healthcare expenses recorded for "
            "better financial planning."
        )

    elif category == "Education":
        return (
            f"You spent ₹{amount:.2f} on Education. "
            "Track education expenses separately."
        )

    elif category == "Entertainment":
        return (
            f"You spent ₹{amount:.2f} on Entertainment. "
            "Monitor entertainment spending as part "
            "of your overall budget."
        )

    else:
        return (
            f"You spent ₹{amount:.2f}. "
            "Keep tracking this expense to understand "
            "your spending pattern."
        )


def generate_financial_advice(
    df,
    budget=10000
):

    if df.empty:

        return [
            "No expenses are available yet.",
            "Add some expenses to generate financial insights."
        ]

    summary = get_spending_summary(
        df
    )

    total = summary[
        "total_spending"
    ]

    average = summary[
        "average_expense"
    ]

    highest = summary[
        "highest_expense"
    ]

    transactions = summary[
        "transaction_count"
    ]

    category = summary[
        "highest_category"
    ]

    merchant = summary[
        "highest_merchant"
    ]

    budget_data = get_budget_analysis(
        total,
        budget
    )

    advice = []

    advice.append(
        f"You have recorded ₹{total:.2f} "
        f"across {transactions} transactions."
    )

    advice.append(
        f"Your average expense is ₹{average:.2f}."
    )

    advice.append(
        f"Your highest single expense is ₹{highest:.2f}."
    )

    if category:

        advice.append(
            f"Your highest spending category is {category}."
        )

    if merchant:

        advice.append(
            f"Your highest spending merchant is {merchant}."
        )

    percentage = budget_data[
        "percentage"
    ]

    remaining = budget_data[
        "remaining"
    ]

    advice.append(
        f"You have used {percentage:.1f}% "
        f"of your ₹{budget:.2f} budget."
    )

    if remaining >= 0:

        advice.append(
            f"Your remaining budget is ₹{remaining:.2f}."
        )

    else:

        advice.append(
            f"Your spending is ₹{abs(remaining):.2f} "
            "above the budget."
        )

    return advice


def get_category_advice(df):

    if df.empty:

        return (
            "No category spending data available."
        )

    summary = get_category_analysis(
        df
    )

    if summary.empty:

        return (
            "No category spending data available."
        )

    top_category = summary.iloc[0][
        "Category"
    ]

    top_amount = summary.iloc[0][
        "Amount"
    ]

    return (
        f"{top_category} is currently your highest "
        f"spending category at ₹{top_amount:.2f}. "
        "Review this category regularly to understand "
        "your spending pattern."
    )


def get_merchant_advice(df):

    if df.empty:

        return (
            "No merchant spending data available."
        )

    summary = get_merchant_analysis(
        df
    )

    if summary.empty:

        return (
            "No merchant spending data available."
        )

    top_merchant = summary.iloc[0][
        "Merchant"
    ]

    top_amount = summary.iloc[0][
        "Amount"
    ]

    return (
        f"{top_merchant} has the highest recorded "
        f"spending at ₹{top_amount:.2f}. "
        "Review repeated transactions from this merchant."
    )


def generate_indian_advice(
    monthly_income,
    monthly_expenses,
    savings_goal=0
):

    return get_indian_finance_advice(
        monthly_income,
        monthly_expenses,
        savings_goal
    )