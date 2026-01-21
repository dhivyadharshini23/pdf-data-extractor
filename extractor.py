import fitz
import re


def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""

    for page in doc:
        page_text = page.get_text()
        if page_text:
            text += page_text + "\n"

    return text


def extract_details(text):
    details = {}

    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z.-]+\.[a-z]{2,}"
    phone_pattern = r"\b[6-9]\d{9}\b"

    details["emails"] = list(set(re.findall(email_pattern, text)))
    details["phones"] = list(set(re.findall(phone_pattern, text)))

    lines = text.split("\n")
    for line in lines[:5]:
        if line.strip().istitle() and len(line.split()) <= 3:
            details["name"] = line.strip()
            break

    return details


if __name__ == "__main__":
    pdf_path = "sample.pdf"
    text = extract_text_from_pdf(pdf_path)
    details = extract_details(text)

    print("Extracted Details:")
    print(details)
