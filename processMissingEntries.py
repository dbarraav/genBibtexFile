import requests
import os 

def read_existing_file(file_path):
    """
    Reads the existing text file and returns a list of lines.
    """
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
        return lines
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return []

def write_to_file(file_path, lines):
    """
    Writes the modified lines back to the text file.
    """
    with open(file_path, "w") as file:
        for line in lines:
            file.write(line)

def process_file(file_path, author_names):
    """
    Processes the text file, skipping lines with existing authors and DOIs,
    and adding new lines for authors not found.
    """
    existing_lines = read_existing_file(file_path)
    modified_lines = []
    missingDOIs = {}
    arxivDOIs = []
    arxivNames = []
    noDOIListNum = len(existing_lines)

    for line in existing_lines:
        parts = line.strip().split(",")
        if len(parts) >= 2:
            author_name, doi = parts[0].strip(), parts[1].strip()

            if author_name in author_names:
                
                # If DOI is missing, keep the line unchanged
                if doi:
                    # Keep the line unchanged
                    modified_lines.append(line)
                    if 'arXiv' in doi:
                        print('Yes this is a arxiv article: {}'.format(doi))
                        arxivDOIs.append(doi)
                        arxivNames.append(author_name)
                    else:
                        missingDOIs[author_name] = doi
                        noDOIListNum-=1
            elif (author_name not in author_names) and doi:
                # print('auhor is not in names and DOI exists')
                modified_lines.append(line)
                
                missingDOIs[author_name] = doi
            else:
                # print("author not in names, doi doesn't exist")
                # Add new line for authors not found
                modified_lines.append(f"{author_name},\n")
        else:
            # Invalid line format, keep it unchanged
            modified_lines.append(line)

    # Add new lines for authors not found
    for author_name in author_names:
        if author_name not in missingDOIs and author_name not in arxivNames:
            modified_lines.append(f"{author_name},\n")

    modified_lines.sort(key=lambda line: line.split(",")[0].strip())
    # Write the modified lines back to the file
    write_to_file(file_path, modified_lines)

    return arxivDOIs, missingDOIs, noDOIListNum

# # Example usage
# if __name__ == "__main__":
#     file_path = "your_text_file.txt"  # Replace with your actual file path
#     author_names = ["Author1", "Author2", "Author3"]  # Replace with your list of author names
#     process_file(file_path, author_names)

def processArXivDOIs(pdfDir, output_file, arxivDOIs):
    print('Processing bibtex for arXiv articles')
    bibtexEntriesPath = os.path.join(pdfDir, output_file)
    for arxivDOI in arxivDOIs:
        url = "https://arxiv.org/bibtex/{}".format(arxivDOI)
        response = requests.get(url)
        text = response.text
        # print(text)
        lines = text.split('\n')
        lines = [line.lstrip() for line in lines]

        bibtexEntryNoIndent = '\n'.join(lines)
        with open(bibtexEntriesPath, 'a') as file:
            file.write(bibtexEntryNoIndent)