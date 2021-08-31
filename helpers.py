import json
from urllib.parse import urlsplit, urlunsplit, quote
import unicodedata
import re
import requests
import sys

def iri2uri(iri):
    """
    Convert an IRI to a URI (Python 3).
    """
    uri = ''
    if isinstance(iri, str):
        (scheme, netloc, path, query, fragment) = urlsplit(iri)
        scheme = quote(scheme)
        netloc = netloc.encode('idna').decode('utf-8')
        path = quote(path)
        query = quote(query)
        fragment = quote(fragment)
        uri = urlunsplit((scheme, netloc, path, query, fragment))

    return uri

def dumpJsonToFile(data, indent, path):
    json_str = json.dumps(data, ensure_ascii=False, indent=indent)
    file = open(path + "/data.json", "a")
    file.write(json_str + ",\n")
    file.close()
    print("KAYDEDİLDİ")
    
def errorLog(errorTitle, data):
    file = open("logs.log", "a")
    file.write(errorTitle + ": " + data + "\n")
    file.close()
    
def slugify(value):
    value = value.replace(u'\u0131', 'i')
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '-', value)


def downloadImage(url, path):
    img_data = requests.get(url).content
    with open(path, 'wb') as handler:
        handler.write(img_data)