import fitz  # PyMuPDF
import re
import os
import argparse
from habanero import cn

def extract_doi(pdf_path):
    # Open the PDF file
    doc = fitz.open(pdf_path)

    # Define the regular expression pattern for a DOI
    # pattern = r"/^10.\d{4,9}/[-._;()/:A-Z0-9]+$/i"
    # pattern = r"\b10\.\d+/[\w.]+\b"
    pattern = r"\b10\.\d+\/[\w.-]+\b" # given edited RE from AI
    # pattern = r"\b10\.\d+\/[\w.-]+\w+\b" # second edited RE given by AI
    # pattern = r"\b10\.\d+\/[\w.-]*\w\b" # 3rd RE given by AI
    # pattern = r"\b10\.\d+\/[\w.-]*\/\w+\b" # 4th RE given by AI
    # pattern = r"/^10.\d{4,9}/[-._;()/:A-Za-z0-9]+$/i"#given by edited RE by AI
    # Create a regular expression object
    regex = re.compile(pattern, re.IGNORECASE)

    # Load the first page
    for i in range(3):
        page = doc.load_page(i)  # zero-based index
        text = page.get_text()  # get the text content

        # Search for the DOI
        match = regex.search(text)
        if match:
            return match.group()

    return None

def get_dois_from_directory(directory_path):
    dois = {}
    for filename in os.listdir(directory_path):
        if filename.endswith('.pdf'):
            # print(filename)
            pdf_path = os.path.join(directory_path, filename)
            doi = extract_doi(pdf_path)
            if doi:
                dois[filename] = doi
    return dois

# Usage:
parser = argparse.ArgumentParser()
parser.add_argument("inputDir", type=str, help="convert pdf in input directory to bibtex file")
parser.add_argument("-t", "--test", help="produce outfile for test", action="store_true")

args = parser.parse_args()
pdfDir = args.inputDir 

if args.test:
    output_file = 'Tests/bibtexEntries.txt'
    excel_file = 'Tests/bibtexEntries.xlsx'
else:
    output_file = 'bibtexEntries.txt'
    # excel_file = os.path.join(pdfDir, 'bibtexEntries.xlsx')
       
def writeBibtex(pdfDir, output_file, dois):
    outputFilePath = os.path.join(pdfDir, output_file)
    counter = 0
    # print('writing bibtex')
    # print(len(dois.items()))
    with open(outputFilePath, 'w') as f:
        for filename, doi in dois.items():
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
                counter+=1
            except:
                continue
            f.write("\n")

    print("{} DOIs from {} articles were found in directory '{}'.".format(counter, len(dois.items()), pdfDir))

def get_subdirectories(path):
    return [os.path.join(path, o) for o in os.listdir(path) 
            if os.path.isdir(os.path.join(path, o))]

# Following code is for one directory containing PDF files
# dois = get_dois_from_directory(pdfDir)
# writeBibtex(output_file, dois)
# print(dois)
# counter = 0
# for filename, doi in dois.items():
#     try:
#         bibtexEntry = cn.content_negotiation(ids=doi, format="bibentry")
#         print(f"Found bibtex entry for DOI {doi} in file {filename}")
#         counter+=1
#     except:
#         print(f"Bibtex entry not found for DOI {doi} in file {filename}")

# print("{} DOIs out of {} articles were found.".format(counter, len(dois.items())))

# Following code is for one directory that has subdirectories containing PDF files

subDirs = get_subdirectories(pdfDir)
# print(subDirs)
for subDir in subDirs:
    dois = get_dois_from_directory(subDir)
    writeBibtex(subDir, output_file, dois)
