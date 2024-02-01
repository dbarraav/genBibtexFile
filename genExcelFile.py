import os
from habanero import cn
from habanero import Crossref
import re
from openpyxl import Workbook
import sys
from pypdf import PdfReader
import pandas as pd

pdf_dir = sys.argv[1]
output_file = 'Tests/bibtexEntries.txt'
excel_file = 'Tests/bibtexEntries.xlsx'

def parse_bibtex(file):
    with open(file, 'r') as f:
        content = f.read()
    entries = content.split('\n@')

    data = []
    for entry in entries:
        title = re.search(r'title={([^}]*)}', entry)
        author = re.search(r'author={([^}]*)}', entry)
        year = re.search(r'year={([^}]*)}', entry)
        doi = re.search(r'DOI={([^}]*)}', entry)

        data.append({
            'title': title.group(1) if title else None,
            'author': author.group(1) if author else None,
            'year': year.group(1) if year else None,
            'DOI': doi.group(1) if doi else None
        })

    return data


# Parse the BibTeX entries
data = parse_bibtex(output_file)

# Create a DataFrame
df = pd.DataFrame(data)

# Write to an Excel file
df.to_excel(excel_file, index=False, engine='openpyxl')