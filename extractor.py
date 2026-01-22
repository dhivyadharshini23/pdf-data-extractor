import fitz  # PyMuPDF
import re


def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""

    for page in doc:
        page_text = page.get_text()
        if page_text:
            text += page_text + "\n"

    return text


def extract_school_percentages(text):
    result = {}
    lines = text.split("\n")

    for line in lines:
        lower_line = line.lower()
        match = re.search(r"\b(\d{2,3})\s*%", line)

        if match:
            percent = match.group(1)

            if "10th" in lower_line or "sslc" in lower_line or "secondary" in lower_line:
                result["10th_percentage"] = percent

            elif "12th" in lower_line or "hsc" in lower_line or "higher secondary" in lower_line:
                result["12th_percentage"] = percent

    return result


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

    
    cgpa_match = re.search(r"\bCGPA[:\s]*([0-9]\.\d{1,2})", text, re.IGNORECASE)
    if cgpa_match:
        details["cgpa"] = cgpa_match.group(1)

    
    for line in lines:
        if "college" in line.lower() or "engineering" in line.lower():
            details["college"] = line.strip()
            break

    
    skill_keywords = [
        "python", "c", "c++", "java", "sql", "git",
        "machine learning", "iot", "arduino",
        "html", "css", "javascript"
    ]

    found_skills = set()
    lower_text = text.lower()

    for skill in skill_keywords:
        if skill in lower_text:
            found_skills.add(skill)

    details["skills"] = list(found_skills)

   
    school_percentages = extract_school_percentages(text)
    details.update(school_percentages)

    return details

if __name__ == "__main__":
    pdf_path = "sample.pdf"   
    text = extract_text_from_pdf(pdf_path)
    details = extract_details(text)

    print("\nExtracted Details:")
    for key, value in details.items():
        print(f"{key}: {value}")
