import fitz  # PyMuPDF
import re
import os
import argparse
from habanero import cn
import subprocess
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

    foundDOIsPathFile = os.path.join(directory_path, 'foundDOIs.txt')
    foundArticleDOIs = {}
    if os.path.exists(foundDOIsPathFile):
        with open(foundDOIsPathFile, "r") as file:
            for line in file:
                foundArticle, foundDOI = line.strip().split(',')
                foundArticleDOIs[foundArticle] = foundDOI
        
    for filename in os.listdir(directory_path):
        
        if filename.endswith('.pdf'):
            # print(filename)
            if filename in foundArticleDOIs.keys():
                continue
            pdf_path = os.path.join(directory_path, filename)
            doi = extract_doi(pdf_path)
            if doi:
                dois[filename] = doi
            else:
                missingEntries.append(filename)

    foundArticleDOIsfinal = {**foundArticleDOIs, **dois}
    if not os.path.exists(foundDOIsPathFile):
        if len(foundArticleDOIsfinal) != 0:
            with open(foundDOIsPathFile, "a") as file:
                for key in sorted(foundArticleDOIsfinal):
                    file.write(f'{key}, {foundArticleDOIsfinal[key]}\n')

    return missingEntries, dois, foundArticleDOIs

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

    # print("{} DOIs from {} articles were found, but only {}/{} have bibtex in directory '{}'.".format(len(dois.items()), pdf_count, counter, len(dois.items()), os.path.basename(os.path.normpath(pdfDir))))
    
    return missingHabaneroDOIs

def get_subdirectories(path):
    return [os.path.join(path, o) for o in os.listdir(path) 
            if os.path.isdir(os.path.join(path, o))]


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

if singleDir:
    missingEntries, dois, foundArticleDOIs = get_dois_from_directory(pdfDir)
    missingEntriesFilePath = os.path.join(pdfDir, "missingDOIs.txt")
    if not os.path.exists(missingEntriesFilePath):
        open(missingEntriesFilePath, "w").close()
        print('Created missing entries file.')

    # print(missingEntries)
    # print(dois['Tevlek2024.pdf'])
    arxivDOIs, missingDOIs, noDOIListNum = processMissingEntries.process_file(missingEntriesFilePath, missingEntries)
    # print(missingEntries, arxivDOIs)

    with open(missingEntriesFilePath, "r") as file:
            lines = file.readlines()
            print(lines)

    if len(missingDOIs.items())!=0:
        # dois.update(missingDOIs)
        dois = {**dois, **missingDOIs}
    # print(dois['Tevlek2024.pdf'])
    # print('DOIs obtained from PDFs and read from missingEntries')
    missingHabaneroDOIs = writeBibtex(pdfDir, output_file, dois)
    # print('Bibtex entries written to file')
    missingEntries = sorted(missingEntries+missingHabaneroDOIs)
    arxivDOIs, missingDOIs, noDOIListNum = processMissingEntries.process_file(missingEntriesFilePath, missingEntries)
    # print(missingEntries, arxivDOIs)

    with open(missingEntriesFilePath, "r") as file:
        lines = file.readlines()
    # print(missingEntries)
    processMissingEntries.processArXivDOIs(pdfDir, output_file, arxivDOIs)

    # numPDFFiles = len([file for file in os.listdir(pdfDir) if file.endswith('.pdf')])
    # numBibtexFound = len(arxivDOIs) + len(foundArticleDOIs)
    # print("{} DOIs from {} articles were found, but only {}/{} have bibtex in directory '{}'.".format(numBibtexFound, numPDFFiles, numPDFFiles-noDOIListNum, numPDFFiles, os.path.basename(os.path.normpath(pdfDir))))

    print('Directory "{}" has bibtex file'.format(os.path.basename(os.path.normpath(pdfDir))))

else:
    subDirs = get_subdirectories(pdfDir)
    # print(subDirs)
    for counter1, subDir in enumerate(subDirs):
        # if counter1 in [0, 1, 2, 3, 4, 5, 6, 7]:
        #     continue
        missingEntries, dois, foundArticleDOIs = get_dois_from_directory(subDir)
        missingEntriesFilePath = os.path.join(subDir, "missingDOIs.txt")
        if not os.path.exists(missingEntriesFilePath):
            open(missingEntriesFilePath, "w").close()
            print('Created missing entries file.')

        arxivDOIs, missingDOIs, noDOIListNum = processMissingEntries.process_file(missingEntriesFilePath, missingEntries)
        # print(missingEntries, arxivDOIs)

        if len(missingDOIs.items())!=0:
            # dois.update(missingDOIs)
            dois = {**dois, **missingDOIs}

        missingHabaneroDOIs = writeBibtex(subDir, output_file, dois)
        missingEntries = sorted(missingEntries+missingHabaneroDOIs)
        arxivDOIs, missingDOIs, noDOIListNum = processMissingEntries.process_file(missingEntriesFilePath, missingEntries)
        # print(missingEntries, arxivDOIs)

        # numPDFFiles = len([file for file in os.listdir(subDir) if file.endswith('.pdf')])
        # numBibtexFound = len(arxivDOIs) + len(foundArticleDOIs)
        # print("{} DOIs from {} articles were found, but only {}/{} have bibtex in directory '{}'.".format(numBibtexFound, numPDFFiles, numPDFFiles-noDOIListNum, numPDFFiles, os.path.basename(os.path.normpath(subDir))))

        processMissingEntries.processArXivDOIs(subDir, output_file, arxivDOIs)
        print('Directory "{}" has bibtex file'.format(os.path.basename(os.path.normpath(subDir))))

    subprocess.call(['python', 'bibtexCombine.py', pdfDir])

# NOTE: if OneDrive is open and syncing is on, it may cause a TimeOut error. Make sure to stop syncing OneDrive to avoid this issue
