import fitz  # PyMuPDF
import re
import os
import argparse
from habanero import cn

import processMissingEntries

def extract_doi(pdf_path, doiPatternCounter=0):
    # Open the PDF file
    doc = fitz.open(pdf_path)

    # Define the regular expression pattern for a DOI
    # pattern = r"/^10.\d{4,9}/[-._;()/:A-Z0-9]+$/i"
    # pattern = r"\b10\.\d+/[\w.]+\b"
    if doiPatternCounter==0:
        pattern = r"\b10\.\d+\/[\w.-]+\b" # given edited RE from AI
    elif doiPatternCounter==1:
        # print('DOI 1 needs to be used')
        pattern = r"\b10\.\d+\/[\w.-]+\w+\b" # second edited RE given by AI
    elif doiPatternCounter==2:
        # print('DOI 2 needs to be used')
        pattern = r"\b10\.\d+\/[\w.-]*\w\b" # 3rd RE given by AI
    elif doiPatternCounter==3:
        # print('DOI 3 needs to be used')
        pattern = r"\b10\.\d+\/[\w.-]*\/\w+\b" # 4th RE given by AI
    else:
        # print('DOI 4 needs to be used')
        pattern = r"/^10.\d{4,9}/[-._;()/:A-Za-z0-9]+$/i"#given by edited RE by AI
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

    if doiPatternCounter <=3:
        doiPatternCounter=doiPatternCounter+1
        extract_doi(pdf_path, doiPatternCounter)
    else:
        return None

def get_dois_from_directory(directory_path):
    dois = {}
    missingEntries= []

    pdf_count = sum(1 for file in os.listdir(directory_path) if file.lower().endswith('.pdf'))
    # print('This directory has {} PDF files.'.format(pdf_count))

    for filename in os.listdir(directory_path):
        if filename.endswith('.pdf'):
            # print(filename)
            pdf_path = os.path.join(directory_path, filename)
            doi = extract_doi(pdf_path)
            if doi:
                dois[filename] = doi
            else:
                missingEntries.append(filename)

    
    return missingEntries, dois

# Usage:
parser = argparse.ArgumentParser()
parser.add_argument("inputDir", type=str, help="convert pdf in input directory to bibtex file")
parser.add_argument("-s", "--single", help="single directory input path", action="store_true")
parser.add_argument("-t", "--test", help="produce outfile for test", action="store_true")

args = parser.parse_args()
pdfDir = args.inputDir 
singleDir = args.single

if args.test:
    output_file = 'Tests/bibtexEntries.txt'
    excel_file = 'Tests/bibtexEntries.xlsx'
else:
    output_file = 'bibtexEntries.txt'
    # excel_file = os.path.join(pdfDir, 'bibtexEntries.xlsx')

def writeBibtex(pdfDir, output_file, dois):
    outputFilePath = os.path.join(pdfDir, output_file)
    counter = 0
    pdf_count = sum(1 for file in os.listdir(pdfDir) if file.lower().endswith('.pdf'))
    # print('writing bibtex')
    # print(len(dois.items()))
    missingHabaneroDOIs = []
    # dois = {key: dois[key] for key in sorted(dois.items())}

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

                # print('{}:{} was found.'.format(filename, doi))
            except:
                # print('{}:{} was not found.'.format(filename, doi))
                missingHabaneroDOIs.append(filename)
                continue
            f.write("\n")

    print("{} DOIs from {} articles were found, but only {}/{} have bibtex in directory '{}'.".format(len(dois.items()), pdf_count, counter, len(dois.items()), os.path.basename(os.path.normpath(pdfDir))))
    
    return missingHabaneroDOIs

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

if singleDir:
    missingEntries, dois = get_dois_from_directory(pdfDir)
    missingEntriesFilePath = "missingDOIs.txt"
    if not os.path.exists(os.path.join(pdfDir, missingEntriesFilePath)):
        open(os.path.join(pdfDir, missingEntriesFilePath), "w").close()
        print('Creating missing entries file.')

    # print(missingEntries)
    # print(dois['Tevlek2024.pdf'])
    missingDOIs = processMissingEntries.process_file(os.path.join(pdfDir, missingEntriesFilePath), missingEntries)
    if len(missingDOIs.items())!=0:
        # dois.update(missingDOIs)
        dois = {**dois, **missingDOIs}
    # print(dois['Tevlek2024.pdf'])
    # print('DOIs obtained from PDFs and read from missingEntries')
    missingHabaneroDOIs = writeBibtex(pdfDir, output_file, dois)
    # print('Bibtex entries written to file')
    missingEntries = sorted(missingEntries+missingHabaneroDOIs)
    missingDOIs = processMissingEntries.process_file(os.path.join(pdfDir, missingEntriesFilePath), missingEntries)

    # print(missingEntries)
    print('Directory has bibtex file.')

else:
    subDirs = get_subdirectories(pdfDir)
    # print(subDirs)
    for counter1, subDir in enumerate(subDirs):
        # if counter1 in [0, 1, 2, 3, 4, 5, 6, 7]:
        #     continue
        missingEntries, dois = get_dois_from_directory(subDir)
        missingEntriesFilePath = "missingDOIs.txt"
        if not os.path.exists(os.path.join(subDir, missingEntriesFilePath)):
            open(os.path.join(subDir, missingEntriesFilePath), "w").close()
            print('Creating missing entries file.')

        missingDOIs = processMissingEntries.process_file(os.path.join(subDir, missingEntriesFilePath), missingEntries)
        if len(missingDOIs.items())!=0:
            # dois.update(missingDOIs)
            dois = {**dois, **missingDOIs}

        missingHabaneroDOIs = writeBibtex(subDir, output_file, dois)
        missingEntries = sorted(missingEntries+missingHabaneroDOIs)
        missingDOIs = processMissingEntries.process_file(os.path.join(subDir, missingEntriesFilePath), missingEntries)
        print('Directory {} has bibtex file'.format(counter1))
# NOTE: if OneDrive is open and syncing is on, it may cause a TimeOut error. Make sure to stop syncing OneDrive to avoid this issue
