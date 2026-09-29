import re


def extract_amount(text):
    """
    Extract the most likely payment amount from OCR text.
    """

    # Normalize OCR text
    text = text.replace("₹", "Rs ")
    text = text.replace("I", "1")

    patterns = [
        r"Rs\.?\s*([0-9][0-9,]*(?:\.[0-9]{1,2})?)",
        r"INR\s*([0-9][0-9,]*(?:\.[0-9]{1,2})?)",
        r"(?:total|amount|paid|price)\s*[:\-]?\s*([0-9][0-9,]*(?:\.[0-9]{1,2})?)",
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)

        if matches:
            amounts = []

            for value in matches:
                try:
                    amounts.append(float(value.replace(",", "")))
                except ValueError:
                    pass

            if amounts:
                return max(amounts)

    # Last fallback: find standalone numbers
    numbers = re.findall(
        r"\b[0-9][0-9,]*(?:\.[0-9]{1,2})?\b",
        text
    )

    possible_amounts = []

    for number in numbers:
        try:
            value = float(number.replace(",", ""))

            # Ignore very small numbers and years
            if 10 <= value <= 100000:
                possible_amounts.append(value)

        except ValueError:
            pass

    if possible_amounts:
        return max(possible_amounts)

    return None


def extract_merchant(text):
    """
    Identify common merchants from OCR text.
    """

    text_lower = text.lower()

    known_merchants = {
        "swiggy": "Swiggy",
        "zomato": "Zomato",
        "amazon": "Amazon",
        "flipkart": "Flipkart",
        "myntra": "Myntra",
        "uber": "Uber",
        "ola": "Ola",
        "rapido": "Rapido",
        "netflix": "Netflix",
        "spotify": "Spotify",
        "airtel": "Airtel",
        "jio": "Jio",
        "apollo": "Apollo",
        "kfc": "KFC",
        "dominos": "Dominos",
        "mcdonald": "McDonald's",
    }

    for keyword, merchant in known_merchants.items():

        if keyword in text_lower:
            return merchant

    # Try payment phrases
    patterns = [
        r"paid\s+to\s+([A-Za-z0-9 &.-]+)",
        r"payment\s+to\s+([A-Za-z0-9 &.-]+)",
        r"sent\s+to\s+([A-Za-z0-9 &.-]+)",
        r"merchant\s*[:\-]\s*([A-Za-z0-9 &.-]+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1).strip()

    return "Unknown"


def parse_expense(text):
    """
    Extract expense information from OCR text.
    """

    merchant = extract_merchant(text)
    amount = extract_amount(text)

    return {
        "merchant": merchant,
        "amount": amount,
        "raw_text": text
    }