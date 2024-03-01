import re
import collections
import argparse
import os

def parse_bibtex(file):
    with open(file, 'r') as f:
        content = f.read()
    entries = content.split('@')[1:]
    parsed_entries = {}
    for entry in entries:
        title_search = re.search(r'title\s*=\s*{([^}]*)}', entry)
        citekey_search = re.search(r'([^\s{]*)\s*{', entry)
        year_search = re.search(r'year\s*=\s*{([^}]*)}', entry)
        month_search = re.search(r'month\s*=\s*{([^}]*)}', entry)
        if title_search and citekey_search and year_search and month_search:
            title = title_search.group(1)
            citekey = citekey_search.group(1)
            year = year_search.group(1)
            month = month_search.group(1)
            if title not in parsed_entries:
                parsed_entries[title] = {'entry': '@' + entry, 'citekey': citekey, 'year': year, 'month': month}
    return parsed_entries

def relabel_citekeys(entries):
    citekeys = collections.defaultdict(list)
    for title, info in entries.items():
        citekeys[info['citekey']].append((info['year'], info['month'], title))
    for citekey, infos in citekeys.items():
        if len(infos) > 1:
            infos.sort()
            for i, info in enumerate(infos):
                entries[info[2]]['citekey'] = citekey + chr(ord('a') + i)
    return entries

def write_bibtex(entries, file):
    with open(file, 'w') as f:
        for info in entries.values():
            f.write(info['entry'].replace(info['citekey'], info['citekey'], 1))


parser = argparse.ArgumentParser()
parser.add_argument("inputFile", type=str, help="convert pdf in input directory to bibtex file")
# parser.add_argument("-t", "--test", help="produce outfile for test", action="store_true")

args = parser.parse_args()
bibtexFile= args.inputFile 

entries = parse_bibtex(bibtexFile)
entries = relabel_citekeys(entries)

parentDir = os.path.dirname(bibtexFile)
outputFile = os.path.join(parentDir, 'combRelabelBibtex.txt')
write_bibtex(entries, outputFile)
