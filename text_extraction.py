from pypdf import PdfReader
import pypandoc
import re

def file_to_text(file_name : str):
    """Extracts all text from a .pdf or .docx file and outputs a .txt file"""
    if file_name.endswith('.pdf'):
        text_file = PdfReader(file_name)
    elif file_name.endswith('.docx'):
        text_file = pypandoc.convert_file(file_name, 'plain', outputfile = "file_name.txt")

def text_extraction(file_name : str, new_file_name : str):
    """Extracts all non-numerical text from a plain text file"""
    with open(file_name, 'r') as f:
        text = re.findall("[^\d]*", f.read())
    return open(f"{new_file_name}.txt", text)