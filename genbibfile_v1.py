import os
import habanero
import re
import sys

def get_bibtex(pdf_file):
    # Get DOI from PDF file
    doi = habanero.content_negotiation(ids=[pdf_file], format="citeproc-json")["message"][pdf_file]["DOI"]

    # Get BibTeX entry from DOI
    bib = habanero.biblio.works(doi=doi, format="bibtex")

    return bib

def write_bibtex_to_file(pdf_dir, output_file):
    # Open output file for writing
    with open(output_file, "w") as f:
        # Loop through PDF files in directory
        for pdf_file in os.listdir(pdf_dir):
            if pdf_file.endswith(".pdf"):
                # Get BibTeX entry for PDF file
                bib = get_bibtex(os.path.join(pdf_dir, pdf_file))

                # Write BibTeX entry to file
                f.write(bib + "\n\n")

def write_metadata_to_file(pdf_dir, output_file):
    # Open output file for writing
    with open(output_file, "w") as f:
        # Loop through PDF files in directory
        for pdf_file in os.listdir(pdf_dir):
            if pdf_file.endswith(".pdf"):
                # Get DOI from PDF file
                doi = habanero.content_negotiation(ids=[os.path.join(pdf_dir, pdf_file)], format="citeproc-json")["message"][os.path.join(pdf_dir, pdf_file)]["DOI"]

                # Get metadata from DOI
                metadata = habanero.works.doi(doi=doi)

                # Write metadata to file
                title = metadata['title'][0]
                authors = ', '.join([author['given'] + ' ' + author['family'] for author in metadata['author']])
                year = metadata['issued']['date-parts'][0][0]
                doi = metadata['DOI']
                f.write(f"{title}, {authors}, {year}, {doi}\n")

# Example usage
pdf_dir = sys.argv[1]
output_file = "bibtex_test1.txt"

# Write BibTeX entries to file
write_bibtex_to_file(pdf_dir, output_file)

# Write metadata to file
metadata_file = "/path/to/metadata/file.txt"
write_metadata_to_file(pdf_dir, metadata_file)



