import sys
import os
import shutil
import re
from collections import defaultdict
import argparse


# Directory containing the initial text files
parser = argparse.ArgumentParser()
parser.add_argument("inputDir", type=str, help="convert pdf in input directory to bibtex file")
# parser.add_argument("-t", "--test", help="produce outfile for test", action="store_true")

args = parser.parse_args()
directory= args.inputDir 


# directory = sys.argv[1]
parentDir = os.path.dirname(directory)

# Dictionary to store the bibtex entries
bibtex_dict = defaultdict(list)

# Regular expression to match bibtex entries
pattern = re.compile(r'@(\w+){([^,]+),([^@]+)}', re.DOTALL)

# Iterate over each file in the directory
# for filename in os.listdir(directory):
#     if filename.endswith('.txt') and "bibtexEntries" in filename:

for root, dirs, files in os.walk(directory):
    for filename in files:
        if filename.endswith('.txt') and "bibtexEntries" in filename:
            with open(os.path.join(root, filename), 'r') as file:
                content = file.read()
                # Find all bibtex entries in the file
                matches = pattern.findall(content)
                for match in matches:
                    # Extract the citekey and the entry
                    entry_type, citekey, entry = match
                    # Store the entry in the dictionary
                    # bibtex_dict[citekey].append(f'@{entry_type}{{{citekey},\n{entry}}}')
                    bibtex_dict[citekey].append(f'@{entry_type}{{{citekey},\n{entry.strip()}}}')
                

# Dictionary to store the final bibtex entries
final_bibtex_dict = {}

# New dictionary to store entries by title
title_dict = defaultdict(list)

# Iterate over the bibtex entries
for citekey, entries in bibtex_dict.items():
    # If there are multiple entries with the same citekey
    if len(entries) > 1:
        for i, entry in enumerate(entries):
            title = re.search(r'title\s*=\s*{([^}]+)}', entry, re.IGNORECASE)

            if title:
                title = title.group(1)
                # If title already exists in title_dict
                if title in title_dict:
                    continue
                else:
                    # Add title in title_dict
                    title_dict[title].append(entry)
            # Add a letter to the citekey
            new_citekey = citekey + chr(97 + i)
            # Replace the old citekey with the new citekey in the entry
            new_entry = entry.replace(citekey, new_citekey, 1)
            # Store the new entry in the final dictionary
            final_bibtex_dict[new_citekey] = new_entry
    else:
        # Store the entry in the final dictionary
        final_bibtex_dict[citekey] = entries[0]

# Sort the bibtex entries by citekey
sorted_entries = sorted(final_bibtex_dict.items())

# Write the sorted entries to the final text file
bibtexFilePath = os.path.join(directory, 'finalBibtexEntries.txt')
with open(bibtexFilePath, 'w') as file:
    for citekey, entry in sorted_entries:
        file.write(entry + '\n\n')

print('Final Bibtex entries were written from all subdirectories in {}'.format(directory))
# shutil.copy(bibtexFilePath, os.path.join(directory, 'final_bibtex_entries.bib'))
shutil.copyfile(os.path.join(directory, 'finalBibtexEntries.txt'), os.path.join(directory, 'finalBibtexEntries.bib'))

# def copy_and_change_ext(src, dst, new_extension):
#     # Get the base name of the source file without the extension
#     base = os.path.splitext(src)[0]
#     # Add the new extension to the destination path
#     dst_with_new_ext = base + new_extension
#     # Copy the file
#     shutil.copy(src, dst_with_new_ext)
#     return dst_with_new_ext

# new_file = copy_and_change_ext(bibtexFilePath, dst, ".bib")