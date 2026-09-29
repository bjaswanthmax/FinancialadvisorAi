def budget_percentage(spending, budget):
    if budget <= 0:
        return 0.0

    return (spending / budget) * 100


def remaining_budget(spending, budget):
    return budget - spending


def budget_status(spending, budget):
    if budget <= 0:
        return "No budget set"

    percentage = budget_percentage(
        spending,
        budget
    )

    if percentage < 50:
        return "Healthy"

    elif percentage < 80:
        return "Moderate"

    elif percentage <= 100:
        return "Warning"

    else:
        return "Exceeded"


def category_budget_status(
    spending,
    budget,
    category
):
    if budget <= 0:
        return {
            "category": category,
            "spending": spending,
            "budget": budget,
            "percentage": 0.0,
            "remaining": budget,
            "status": "No budget set"
        }

    percentage = budget_percentage(
        spending,
        budget
    )

    remaining = remaining_budget(
        spending,
        budget
    )

    return {
        "category": category,
        "spending": spending,
        "budget": budget,
        "percentage": percentage,
        "remaining": remaining,
        "status": budget_status(
            spending,
            budget
        )
    }


def analyze_budget(spending, budget):
    percentage = budget_percentage(
        spending,
        budget
    )

    remaining = remaining_budget(
        spending,
        budget
    )

    status = budget_status(
        spending,
        budget
    )

    return {
        "spending": spending,
        "budget": budget,
        "percentage": percentage,
        "remaining": remaining,
        "status": status
    }