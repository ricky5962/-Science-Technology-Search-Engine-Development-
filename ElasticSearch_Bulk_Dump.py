import urllib2
import urllib
from stripogram import html2text
import pandas as pd
import json

from elasticsearch import Elasticsearch
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

# An instance of Elasticsearch, node 1
es = Elasticsearch(hosts=['localhost:9200'])


def pdf_to_txt(url):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    # Open the url provided as an argument to the function and read the content
    f = urllib2.urlopen(urllib2.Request(url)).read()
    # Cast to StringIO object
    fp = StringIO(f)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()
    for page in PDFPage.get_pages(fp,
                                  pagenos,
                                  maxpages=maxpages,
                                  password=password,
                                  caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str

def html_to_text(url):
    myurl = urllib.urlopen(url)
    html_string = myurl.read()
    text = html2text(html_string)
    return text

# process the output url text file, and output a array that contains all the urls
def process_url(path, file):
    with open(path + file, "r") as ins:
        array = []
        for line in ins:
            array.append(line)
    return array

#print(process_url("/Users/xiao/PycharmProjects/S&T Project/", "File Processing Result.txt"))

def es_put(url):

    content = html_to_text(url)
    content = unicode(content, errors='ignore')
    content.decode('utf-8')
    es.index(index='st', doc_type='webpages', body={
        'url': url,
        'content': content
    })

#es_put("https://www.un.org/")
urls = process_url('/Users/xiao/PycharmProjects/S&T Project/','File Processing Result.txt')
for url in urls:
    es_put(url)
