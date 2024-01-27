import sys
import os
import re
from collections import defaultdict

# Directory containing the initial text files
directory = sys.argv[1]
parentDir = os.path.dirname(directory)

# Dictionary to store the bibtex entries
bibtex_dict = defaultdict(list)

# Regular expression to match bibtex entries
pattern = re.compile(r'@(\w+){([^,]+),([^@]+)}', re.DOTALL)

# Iterate over each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        with open(os.path.join(directory, filename), 'r') as file:
            content = file.read()
            # Find all bibtex entries in the file
            matches = pattern.findall(content)
            for match in matches:
                # Extract the citekey and the entry
                entry_type, citekey, entry = match
                # Store the entry in the dictionary
                bibtex_dict[citekey].append(f'@{entry_type}{{\n{citekey},\n{entry}}}')

# Dictionary to store the final bibtex entries
final_bibtex_dict = {}

# Iterate over the bibtex entries
for citekey, entries in bibtex_dict.items():
    # If there are multiple entries with the same citekey
    if len(entries) > 1:
        for i, entry in enumerate(entries):
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
with open(os.path.join(directory, 'final_bibtex_entries.txt'), 'w') as file:
    for citekey, entry in sorted_entries:
        file.write(entry + '\n\n')
