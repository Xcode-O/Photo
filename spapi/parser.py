
# -*- coding: utf-8 -*-

import requests
import urllib.request
from bs4 import BeautifulSoup
#from urllib2_file import urlopen
from urllib.request import urlopen

class Parser (object):
    url = 'https://photolab.me/tag/'
    array_id = []

    def parse(self, tag):
        req_url = self.url + tag
        html_doc = urlopen(req_url).read()
        soup = BeautifulSoup(html_doc)

        for data_id in soup.find_all('div', 'combos-item'):
            self.array_id.append(data_id.get('data-id'))

        return (tag, self.array_id)