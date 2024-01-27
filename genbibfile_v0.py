import os
# from pybtex.database.input import bibtex
# import pdf2bib
import habanero
import pandas as pd
import re
import sys

# Directory containing the PDF files
pdf_dir = sys.argv[1]

# List to store the BibTeX entries
bibtex_entries_pybtex = []
# bibtex_entries_pdf2bib = []
bibtex_entries_habanero = []

# Loop over all PDF files in the directory
for filename in os.listdir(pdf_dir):
    if filename.endswith('.pdf'):
        # Extract the BibTeX entries from the PDF file using pybtex
        parser = bibtex.Parser()
        bib_data = parser.parse_file(os.path.join(pdf_dir, filename))

        # Append each BibTeX entry as a list of strings to the bibtex_entries list
        for key in bib_data.entries:
            entry = str(bib_data.entries[key])
            entry_lines = entry.split('\n')
            bibtex_entries_pybtex.append(entry_lines)

        # # Extract the BibTeX entries from the PDF file using pdf2bib
        # output = pdf2bib.extract(os.path.join(pdf_dir, filename))
        # output_lines = output.split('\n')
        # for entry_lines in output_lines:
        #     if entry_lines:
        #         bibtex_entries_pdf2bib.append(entry_lines.split('\n'))

        # Extract the BibTeX entries from the PDF file using habanero
        output = habanero.cn.content_negotiation(
            ids='doi:', format="bibentry", url=os.path.join(pdf_dir, filename))
        output_lines = output.split('\n')
        for entry_lines in output_lines:
            if entry_lines:
                bibtex_entries_habanero.append(entry_lines.split('\n'))

print(bibtex_entries_pybtex)
# print(bibtex_entries_pdf2bib)
print(bibtex_entries_habanero)

# # Extract specific information from each BibTeX entry and write it to an Excel file
# data = []
# for entry_lines in bibtex_entries:
#     entry = ''.join(entry_lines)
#     title = re.search(r'title\s*=\s*{([^}]*)}', entry)
#     doi = re.search(r'doi\s*=\s*{([^}]*)}', entry)
#     authors = re.search(r'author\s*=\s*{([^}]*)}', entry)
#     year = re.search(r'year\s*=\s*{([^}]*)}', entry)
#     data.append({
#         'Title': title.group(1) if title else '',
#         'DOI': doi.group(1) if doi else '',
#         'Authors': authors.group(1) if authors else '',
#         'Publication Year': year.group(1) if year else ''
#     })

# df = pd.DataFrame(data)
# df.to_excel('articles.xlsx', index=False)
