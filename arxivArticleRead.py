
import requests

arxivDOIs = ['arXiv:2401.01404v3', 'arXiv:2312.17306v1', ]

for arxivDOI in arxivDOIs:
    url = "https://arxiv.org/bibtex/{}".format(arxivDOI)
    response = requests.get(url)
    text = response.text
    print(text)