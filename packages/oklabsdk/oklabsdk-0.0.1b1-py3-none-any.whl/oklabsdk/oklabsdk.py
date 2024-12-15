#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyPDF2 import PdfReader # type: ignore

from dotenv import load_dotenv
load_dotenv()


def load_pdf(file_path):
    """Returns the content of a PDF file as a string."""
    text = ""
    with open(file_path, "rb") as file:
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n" 
    return text.strip()

