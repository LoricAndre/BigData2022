from bs4 import BeautifulSoup
import pandas as pd
import requests

def search(query, lang="fr"):
    url = 'https://%s.wikipedia.org/w/api.php' % lang
    params = {
        'action': 'query',
        'format': 'json',
        'list': 'search',
        'utf8': 1,
        'srsearch': query
    }

    data = requests.get(url, params=params).json()
    for i in data['query']['search']:
        subject = i["pageid"]
        url = 'https://%s.wikipedia.org/w/api.php' % lang
        params = {
            'action': 'parse',
            'prop': 'text',
            'format': 'json',
            'pageid': subject,
            'section': 0,
            'redirects': ''
        }
        data = requests.get(url, params=params).json()
        soup = BeautifulSoup(data['parse']['text']['*'], 'html.parser')
        infoboxes = soup.select('.taxobox_classification')
        if infoboxes != None and len(infoboxes) > 0:
            return infoboxes[-1].b.text
