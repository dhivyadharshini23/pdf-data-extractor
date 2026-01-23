import re
import os
from PyPDF2 import PdfReader
from docx import Document



def read_pdf(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def read_docx(path):
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs)


def read_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def extract_key_info(text):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
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

    extracted["email"] = extracted["email"].group() if extracted["email"] else None
    extracted["phone"] = extracted["phone"].group() if extracted["phone"] else None
    extracted["gstin"] = extracted["gstin"].group() if extracted["gstin"] else None

   
    for line in lines:
        lower = line.lower()

        if "invoice" in lower and "no" in lower:
            extracted["invoice_no"] = line.split()[-1]

        elif "date" in lower:
            m = re.search(r"\d{2}[/-]\d{2}[/-]\d{4}", line)
            if m:
                extracted["date"] = m.group()

        elif "total" in lower:
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
    else:
        raise ValueError("Unsupported file format")

    return extract_key_info(text)




if __name__ == "__main__":
    file_path = "sample_invoice.docx"  
    result = extract_from_file(file_path)

    print("Extracted Information:")
    for k, v in result.items():
        print(f"{k.upper():12}: {v}")
