# Given text file with DOIs, output bibtex bib/txt file and excel file with specific information

import os
from habanero import cn
from habanero import Crossref
import re
from openpyxl import Workbook
import sys
from pypdf import PdfReader
import pandas as pd
from openpyxl.utils.dataframe import dataframe_to_rows


doisTextFile = sys.argv[1]
parentDir = os.path.dirname(doisTextFile)

output_file = os.path.join(parentDir, 'bibtexEntries.txt')
excel_file = os.path.join(parentDir, 'bibtexEntries.xlsx')
# pdf_folder = '/path/to/pdf/folder'

dois = open(doisTextFile, 'r').read().splitlines()
print(dois)

with open(output_file, 'w') as f:
    for j, doi in enumerate(dois):
        try:
            bibtexEntry = cn.content_negotiation(ids=doi, format="bibentry")
            # print(bibtexEntry)
            print(j)
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

        except:
            continue
        f.write("\n")
    


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

# # Write to an Excel file
# df.to_excel(excel_file, index=False, engine='openpyxl')

wb = Workbook()
ws = wb.active

# Write DataFrame to the sheet
for r in dataframe_to_rows(df, index=False, header=True):
    ws.append(r)

# Adjust column widths
for column in ws.columns:
    max_length = 0
    column = [cell for cell in column]
    for cell in column:
        try:
            if len(str(cell.value)) > max_length:
                max_length = len(cell.value)
        except:
            pass
    adjusted_width = (max_length + 2)
    ws.column_dimensions[column[0].column_letter].width = adjusted_width

# Save the workbook
wb.save(excel_file)

