from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

import nltk
from nltk.corpus import stopwords
from nltk import FreqDist
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
from textblob.classifiers import DecisionTreeClassifier

import pandas as pd
import os

sdgs = ['Poverty', 'Hunger', 'Health', 'Education','Gender Equality']
sdg_df = pd.DataFrame()

def convert(sdg,fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)
    infile = file('/Users/xiao/Dropbox/Text Analytics/PDF Files/' + sdg + '/'+ fname, 'rb')


    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text

def convert_test(sdg,fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)
    infile = file('/Users/xiao/Dropbox/Text Analytics/PDF Files/Test/' + sdg +'/'+ fname, 'rb')


    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text

def train_extractor(sdg_name):
    files = os.listdir('/Users/xiao/Dropbox/Text Analytics/PDF Files/' + sdg_name)
    for i in range(1,len(files)):
        sdg_df.set_value(i,'Content',convert(sdg_name,files[i]))
    sdg_df.to_csv(sdg_name + '.txt')


def test_extractor(sdg_name):
    files = os.listdir('/Users/xiao/Dropbox/Text Analytics/PDF Files/' + sdg_name)
    for i in range(1, len(files)):
        sdg_df.set_value(i, 'Content', convert(sdg_name, files[i]))
        sdg_df.to_csv(files[i] + '.txt')
# Stemmer
def stem(text):
    raw = text.decode('utf-8')
    raw = raw.replace('\n', ' ')
    tokens = nltk.word_tokenize(raw)
    mystopwords = stopwords.words('english')
    words = [w.lower() for w in tokens if w.isalpha() if w.lower() not in mystopwords]
    #porter = nltk.PorterStemmer()
    #stem = []
    #for i in range(0,len(words)):
    #    stem.append(porter.stem(words[i]))
    return words

# Training set
train = []
count = 0
for j in range(0,len(sdgs)):
    files = os.listdir('/Users/xiao/Dropbox/Text Analytics/PDF Files/' + sdgs[j])
    for i in range(1, len(files)):
        train.append([])
        train[count].append(stem(convert(sdgs[j],files[i])))
        train[count].append(sdgs[j])
        count = count + 1

# Testing set
test = []
count_test = 0
for j in range(0,len(sdgs)):
    files = os.listdir('/Users/xiao/Dropbox/Text Analytics/PDF Files/Test/' + sdgs[j])
    for i in range(1, len(files)):
        test.append([])
        test[count_test].append(stem(convert_test(sdgs[j],files[i])))
        test[count_test].append(sdgs[j])
        count_test = count_test + 1

#cl = NaiveBayesClassifier(train)
cl = NaiveBayesClassifier(train)
#sdg1_test = convert_test('5_Why-it-Matters_GenderEquality_2p.pdf').decode('utf-8')
#pdist=cl.prob_classify(sdg1_test)
#print('%.4f %.4f %.4f %.4f %.4f' % (pdist.prob('Poverty'), pdist.prob('Hunger'),pdist.prob('Health'),pdist.prob('Education'),pdist.prob('Gender Equality')))

print cl.show_informative_features(100)




#for pdist in classifier.prob_classify_many(test):
#    print('%.4f %.4f %.4f' % (pdist.prob('x'), pdist.prob('y'), pdist.prob('z')))