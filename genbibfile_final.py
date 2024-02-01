import os
from habanero import cn
from habanero import Crossref
import re
from openpyxl import Workbook
import sys
from pypdf import PdfReader
# import pandas as pd
import argparse


# pdf_dir = sys.argv[1]
parser = argparse.ArgumentParser()
parser.add_argument("inputDir", type=str, help="convert pdf in input directory to bibtex file")
parser.add_argument("-t", "--test", help="produce outfile for test", action="store_true")

args = parser.parse_args()
pdfDir = args.inputDir 

if args.test:
    output_file = 'Tests/bibtexEntries.txt'
    excel_file = 'Tests/bibtexEntries.xlsx'
else:

    output_file = os.path.join(pdfDir, 'bibtexEntries.txt')
    excel_file = os.path.join(pdfDir, 'bibtexEntries.xlsx')
                        
# pdf_folder = '/path/to/pdf/folder'


pdf_files = [os.path.join(pdfDir, f) for f in os.listdir(pdfDir) if f.endswith('.pdf')]
print('There are a total of {} articles in PDF format'.format(len(pdf_files)))
# doi_re = re.compile(r'10\.\d{4,9}/[-._;()/:A-Z0-9]+', re.IGNORECASE)
# r'\b(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?![\"&\'<>])\S)+)\b'

# doi_re = re.compile(r'\b(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?![\"&\'<>])\S)+)\b', re.IGNORECASE)
doi_re = re.compile(r'10\.\d{4,9}/[-._;()/:A-Z0-9]+', re.IGNORECASE)
dois = []
titles = []
for pdf_file in pdf_files:
    with open(pdf_file, 'rb') as f:
        pdf = PdfReader(f)
        
        first_page = pdf.pages[0]
        text = first_page.extract_text()
        doi_match = doi_re.search(text)

        title = pdf.metadata.title
        
        if doi_match:
            doi = doi_match.group()
            # print(doi)
            dois.append(doi)
        else:
            titles.append(title)

print('There are a total of {} DOIs found from articles'.format(len(dois)))
print('There are a total of {} titles found from articles'.format(len(titles)))

# with open(output_file, 'w') as f:
#     for filename in os.listdir(pdf_dir):
#         if filename.endswith('.pdf'):
#             pdf_path = os.path.join(pdf_dir, filename)
#             bib_entries = habanero.cn.content_negotiation(ids=dois, format="bibentry")
#             f.write(bib_entries + '\n\n')

with open(output_file, 'w') as f:
    for j, doi in enumerate(dois):
        try:
            bibtexEntry = cn.content_negotiation(ids=doi, format="bibentry")
            # print(bibtexEntry)
            
            # Split the string into lines
            fields = re.split(r',(?=\s\w+=)', bibtexEntry)

            for i, field in enumerate(fields):
                    # Remove leading and trailing spaces
                    field = field.strip()
                    
                    # Add a comma at the end of the line if it's not the last line
                    if i != len(fields)-1:
                        # print(field)
                        field += ','

                    # Write the field to the file
                    f.write(field + '\n')
            if j%5==0:
                print(j)
        except:
            continue
        f.write("\n")
    


# def parse_bibtex(file):
#     with open(file, 'r') as f:
#         content = f.read()
#     entries = content.split('\n@')

#     data = []
#     for entry in entries:
#         title = re.search(r'title={([^}]*)}', entry)
#         author = re.search(r'author={([^}]*)}', entry)
#         year = re.search(r'year={([^}]*)}', entry)
#         doi = re.search(r'DOI={([^}]*)}', entry)

#         data.append({
#             'title': title.group(1) if title else None,
#             'author': author.group(1) if author else None,
#             'year': year.group(1) if year else None,
#             'DOI': doi.group(1) if doi else None
#         })

#     return data


# # Parse the BibTeX entries
# data = parse_bibtex(output_file)

# # Create a DataFrame
# df = pd.DataFrame(data)

# # Write to an Excel file
# df.to_excel(excel_file, index=False, engine='openpyxl')


