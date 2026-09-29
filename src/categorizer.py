def categorize_expense(text):
    """
    Categorize an expense using OCR text.
    """

    text = text.lower()

    food = [
        "swiggy", "zomato", "kfc", "dominos",
        "mcdonald", "restaurant", "food", "cafe"
    ]

    shopping = [
        "amazon", "flipkart", "myntra", "shopping"
    ]

    transport = [
        "uber", "ola", "rapido", "petrol", "fuel"
    ]

    bills = [
        "airtel", "jio", "vi", "electricity",
        "water", "internet", "recharge"
    ]

    healthcare = [
        "apollo", "hospital", "pharmacy", "medical"
    ]

    education = [
        "college", "school", "udemy", "coursera"
    ]

    entertainment = [
        "netflix", "spotify", "cinema", "movie"
    ]

    if any(word in text for word in food):
        return "Food"

    if any(word in text for word in shopping):
        return "Shopping"

    if any(word in text for word in transport):
        return "Transport"

    if any(word in text for word in bills):
        return "Bills"

    if any(word in text for word in healthcare):
        return "Healthcare"

    if any(word in text for word in education):
        return "Education"

    if any(word in text for word in entertainment):
        return "Entertainment"

    return "Other"