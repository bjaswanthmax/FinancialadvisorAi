from PIL import Image
# pyrefly: ignore [missing-import]
import pytesseract


def extract_text_from_image(image):
    """
    Extract text from an uploaded image using Tesseract OCR.
    """

    if hasattr(image, "read"):
        image = Image.open(image)

    text = pytesseract.image_to_string(image)

    return text