# PDF Data Extractor

This project extracts essential details like email and phone numbers
from uploaded PDF files.

## Features
- Text-based PDF parsing
- Fast extraction using PyMuPDF
- Regex-based detail extraction

## Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

## Run
python extractor.py sample.pdf