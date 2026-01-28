import re
import os
from PyPDF2 import PdfReader
from docx import Document
import pytesseract
from PIL import Image
from pdf2image import convert_from_path

# Update path if needed
pytesseract.pytesseract.tesseract_cmd = r"G:\dd\pdf-data-extractor\TESSERACT\tesseract.exe"


def read_pdf(path):
    reader = PdfReader(path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    if len(text.strip()) < 50:
        text += ocr_pdf(path)

    return text


def ocr_pdf(path):
    text = ""
    images = convert_from_path(path, dpi=300)
    for img in images:
        text += pytesseract.image_to_string(img)
    return text


def read_image(path):
    img = Image.open(path)
    return pytesseract.image_to_string(img)


def read_docx(path):
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs)


def read_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def extract_key_info(text):
    extracted = {
        "email": None,
        "phone": None,
        "gstin": None,
        "invoice_no": None,
        "date": None,
        "total_amount": None
    }

    extracted["email"] = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    extracted["phone"] = re.search(r"\b[6-9]\d{9}\b", text)
    extracted["gstin"] = re.search(r"\b\d{2}[A-Z]{5}\d{4}[A-Z][A-Z\d]Z[A-Z\d]\b", text)

    for k in ["email", "phone", "gstin"]:
        extracted[k] = extracted[k].group() if extracted[k] else None

    for line in text.splitlines():
        lower = line.lower()

        if "invoice" in lower and "no" in lower:
            extracted["invoice_no"] = line.split()[-1]

        if "date" in lower:
            m = re.search(r"\d{2}[/-]\d{2}[/-]\d{4}", line)
            if m:
                extracted["date"] = m.group()

        if "total" in lower:
            m = re.search(r"₹?\s*([\d,]+\.\d{2})", line)
            if m:
                extracted["total_amount"] = m.group(1)

    return extracted


def extract_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        text = read_pdf(file_path)
    elif ext == ".docx":
        text = read_docx(file_path)
    elif ext == ".txt":
        text = read_txt(file_path)
    elif ext in [".png", ".jpg", ".jpeg"]:
        text = read_image(file_path)
    else:
        raise ValueError("Unsupported file type")

    return extract_key_info(text)
