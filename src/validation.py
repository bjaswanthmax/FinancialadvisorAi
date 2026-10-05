from datetime import date


def validate_amount(amount):
    if amount is None:
        return False, "Amount is required."

    if amount <= 0:
        return False, "Amount must be greater than ₹0."

    if amount > 1000000:
        return False, "Amount is too large."

    return True, ""


def validate_merchant(merchant):
    if not merchant or not merchant.strip():
        return False, "Merchant name is required."

    if len(merchant.strip()) > 100:
        return False, "Merchant name is too long."

    return True, ""


def validate_budget(budget):
    if budget < 0:
        return False, "Budget cannot be negative."

    return True, ""


def validate_date(expense_date):
    if not expense_date:
        return False, "Expense date is required."

    if expense_date > date.today():
        return False, "Expense date cannot be in the future."

    return True, ""


def validate_expense(
    merchant,
    amount,
    expense_date
):
    valid, message = validate_merchant(
        merchant
    )

    if not valid:
        return False, message

    valid, message = validate_amount(
        amount
    )

    if not valid:
        return False, message

    valid, message = validate_date(
        expense_date
    )

    if not valid:
        return False, message

    return True, ""