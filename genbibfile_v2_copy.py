import os
from habanero import cn
import re
from openpyxl import Workbook
import sys
from pypdf import PdfReader
import pandas as pd

pdf_dir = sys.argv[1]
output_file = 'bibtexEntries2.txt'
excel_file = 'bibtexEntries.xlsx'
# pdf_folder = '/path/to/pdf/folder'


pdf_files = [os.path.join(pdf_dir, f) for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
print('There are a total of {} articles in PDF format'.format(len(pdf_files)))
# doi_re = re.compile(r'10\.\d{4,9}/[-._;()/:A-Z0-9]+', re.IGNORECASE)
# r'\b(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?![\"&\'<>])\S)+)\b'

# doi_re = re.compile(r'\b(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?![\"&\'<>])\S)+)\b', re.IGNORECASE)
doi_re = re.compile(r'10\.\d{4,9}/[-._;()/:A-Z0-9]+', re.IGNORECASE)

dois = []

for pdf_file in pdf_files:
    with open(pdf_file, 'rb') as f:
        pdf = PdfReader(f)
        first_page = pdf.pages[0]
        text = first_page.extract_text()
        doi_match = doi_re.search(text)
        if doi_match:
            doi = doi_match.group()
            print(doi)
            dois.append(doi)

print('There are a total of {} DOIs found from articles'.format(len(dois)))

# with open(output_file, 'w') as f:
#     for doi in dois:
#         bibtexEntry = cn.content_negotiation(ids=doi, format="bibentry")

#         f.write(bibtexEntry)


with open(output_file, 'w') as f:
    for j, doi in enumerate(dois):
        try:
            bibtexEntry = cn.content_negotiation(ids=doi, format="bibentry")
            f.write(bibtexEntry + '\n')
            print(j)
        except:
            f.write('\n')
