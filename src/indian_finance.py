def indian_finance_terms():
    return {
        "PPF": "Public Provident Fund",
        "SIP": "Systematic Investment Plan",
        "ELSS": "Equity Linked Savings Scheme",
        "NPS": "National Pension System",
        "FD": "Fixed Deposit",
        "RD": "Recurring Deposit"
    }


def get_indian_finance_advice(
    monthly_income,
    monthly_expenses,
    savings_goal=0
):
    advice = []

    if monthly_income <= 0:
        return [
            "Enter your monthly income to generate "
            "Indian personal finance insights."
        ]

    savings = monthly_income - monthly_expenses
    savings_percentage = (
        savings / monthly_income
    ) * 100

    advice.append(
        f"Monthly income: ₹{monthly_income:.2f}"
    )

    advice.append(
        f"Monthly expenses: ₹{monthly_expenses:.2f}"
    )

    advice.append(
        f"Current surplus/deficit: ₹{savings:.2f}"
    )

    advice.append(
        f"Current savings rate: "
        f"{savings_percentage:.1f}%."
    )

    if savings < 0:
        advice.append(
            "Recorded expenses are higher than income. "
            "Review your monthly spending."
        )
    elif savings_percentage < 20:
        advice.append(
            "Your recorded savings rate is below 20%. "
            "Consider reviewing recurring and discretionary "
            "expenses."
        )
    else:
        advice.append(
            "Your recorded savings rate is 20% or higher. "
            "Continue monitoring your monthly cash flow."
        )

    if savings_goal > 0:
        if savings >= savings_goal:
            advice.append(
                "Your current monthly surplus is at least "
                "the specified savings goal."
            )
        else:
            difference = savings_goal - savings
            advice.append(
                f"You would need approximately "
                f"₹{difference:.2f} more monthly surplus "
                "to reach the specified goal."
            )

    advice.append(
        "For Indian financial planning, commonly discussed "
        "options include PPF, SIP, ELSS, NPS, FD and RD. "
        "Suitability depends on individual circumstances."
    )

    return advice