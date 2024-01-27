import os
from habanero import cn
from habanero import Crossref
import re
from openpyxl import Workbook
import sys
from pypdf import PdfReader
import pandas as pd

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument


pdf_dir = sys.argv[1]
output_file = 'bibtexEntries_title.txt'
excel_file = 'bibtexEntries_title.xlsx'
# pdf_folder = '/path/to/pdf/folder'


pdf_files = [os.path.join(pdf_dir, f) for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
print('There are a total of {} articles in PDF format'.format(len(pdf_files)))
# doi_re = re.compile(r'10\.\d{4,9}/[-._;()/:A-Z0-9]+', re.IGNORECASE)
# r'\b(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?![\"&\'<>])\S)+)\b'

# doi_re = re.compile(r'\b(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?![\"&\'<>])\S)+)\b', re.IGNORECASE)
# doi_re = re.compile(r'10\.\d{4,9}/[-._;()/:A-Z0-9]+', re.IGNORECASE)
# dois = []
titles_pypdf = {}
titles_pdfminer = {}
# for num, pdf_file in enumerate(pdf_files):
#     with open(pdf_file, 'rb') as f:
#         pdf = PdfReader(f)
#         title = pdf.metadata.title
#         titles_pypdf[num] = title

#         parser = PDFParser(f)
#         document = PDFDocument(parser)
#         titles_pdfminer[num] = document.info[0]['Title']
# print('There are a total of {} titles found from articles'.format(len(titles_pypdf)))

for num, pdf_file in enumerate(pdf_files):
    with open(pdf_file, 'rb') as f:
        parser = PDFParser(f)
        document = PDFDocument(parser)
        titles_pdfminer[num] = document.info[0]['Title']

        try:
            print(document.info[0]['doi'])
        except:
            print(document.info[0]['Title'])
        # if num==0:
        #     print(document.info[0].items())
# print('There are a total of {} titles found from articles'.format(len(titles_pypdf)))



# with open(output_file, 'w') as f:
#     for key, title in titles.items():
#         cr = Crossref()
#         works = cr.works(query = title, limit = 1)
#         if works['message']['items']:   
#             if works['message']['items'][0]['title'][0] == title:
#                 print('Title #{} found'.format(key))
#                 doi = works['message']['items'][0]['DOI']
#                 bibtexEntry = cn.content_negotiation(ids = doi, format= "bibentry")

#                 fields = re.split(r',(?=\s\w+=)', bibtexEntry)
#                 for i, field in enumerate(fields):
#                         field = field.strip()
#                         if i != len(fields)-1:
#                             field += ','
#                         f.write(field + '\n')
            
#             else:
#                 print("No BibTeX entry for title #{}".format(key))
#         else:
#             print("No results for title #{}".format(key))

# for key, title in titles_pypdf.items():
#     print(title)

# for key, title in titles_pdfminer.items():
#     print(title)

    # cr = Crossref()
    # works = cr.works(query = title, limit = 1)
    # if key <=0:
    #     if works['message']['items']:   
    #         print(works['message']['items'][0].keys())
    # if len(works['message']['items'])!=0:
    #     print(works['message']['items'][0]['title'])

#------------------------------------------------------------------------------------
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


