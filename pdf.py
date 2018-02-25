import PyPDF2, re, os, sys, csv
from textblob import TextBlob
from urllib.request import urlretrieve
import requests
from bs4 import BeautifulSoup
import numpy as np
from nltk.tokenize import RegexpTokenizer
from os import listdir
from os.path import isfile, join
import pandas as pd

def searching(search_list):
    save_list = []
    for each in search_list:
        print(type(each)) 
        print(each)
        g = pygoogle(each)
        g.pages = 1
        # print '*Found %s results*'%(g.get_result_count())
        z = g.get_urls()
        save = z[0] 
        save_list.append(save)
    return save_list

def coinmarketcap(filepath):
    df = pd.read_csv(filepath)
    # print(df)
    name_list = []
    search_list = []
    for each in df['Name']:
        name = each.split()[2]
        name_list.append(name)
    for every in name_list:
        every += " whitepaper filetype:pdf"
        search_list.append(every)
    return search_list


        # for row in csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE):
        #     stops_list += row
        # return stops_list
    # r = requests.get("https://coinmarketcap.com/all/views/all/")
    # soup = BeautifulSoup(r.content, "html5lib")
    # print(soup)


def get_list_files(mypath):
    onlyfiles = [mypath + f for f in listdir(mypath) if isfile(join(mypath, f))]
    return onlyfiles

def convert(file):
    os.system('pdftotext ' +  file)

def list_convert(file_list):
    path_list = []
    for each in file_list:
        # convert(each)
        if os.system('pdftotext ' + each):
            path = each[:-3] + "txt"
            path_list.append(path)
            os.system('pdftotext ' + each)
    clean_path_list = []
    for each in path_list:
        if each[-4:] == ".txt":
            clean_path_list.append(each)
    return clean_path_list

# def text(string_thing):

#     blob = TextBlob(string_thing)
#     return blob.sentiment
def stops():
    with open(r'stops.csv') as f:
        stops_list = []
        for row in csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE):
            stops_list += row
        return stops_list

def text(file):
    with open(file, 'rb') as f:
        contents = f.read()
    contents.strip()
    z=contents.decode('utf-8','ignore')
    # print(z)
    # print(type(z))
    y= z.replace('\n', ' ')
    # print(y)
    blob = TextBlob(z)
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(z)
    # print(tokens)
    length = len(tokens)
    defaultdict = {}
    count = {}
    freq_dict = {}
    freq_list = []
    char_count = 0
    for word in tokens:
        z= len(word)
        char_count += z
        if z > 2:
            if word.lower() not in stops():
                if word.lower() not in count:
                    count[word.lower()] = 1
                else:
                    count[word.lower()] += 1
    for word, ct in count.items():
        freq_dict[word] = float(ct) * 100.0 / float(length)
        if freq_dict[word] > 0.25:
            freq_list.append(word)
    return blob, freq_list, length, char_count

def nltk(file):
    run = text(file)
    blob = run[0]
    freq_list = run[1]
    word_len = run[2]
    char_count = run[3]

    b = blob.sentences
    sent_num = len(b)
    c = blob.sentiment
    words = blob.tags
    sent_len_char = []
    for each in b:
        sent_len_char.append(len(each))
    avg_sent_len = np.mean(sent_len_char)
    return freq_list, blob.sentiment, word_len, char_count, avg_sent_len
    # return b, c, len(words)

def nltk_papers(file_list):
    paper_dict = {}
    for each in file_list:
        coin = each.split("/", -1)[-1][:-4]
        # print(paper_dict)
        paper_dict[coin] = nltk(each)
    return paper_dict
        

def extract(file):
    pdfFileObj = open(file,'rb')     #'rb' for read binary mode
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    pages = pdfReader.numPages
    full_file = ""
    for i in range(pages):
        pageObj = pdfReader.getPage(i)          #'i' is the page number
        z = pageObj.extractText()
        full_file += z
    # print(full_file)
    regex = r'\w+'

    list1=re.findall(regex,full_file)
    print(list1)
    word_count = len(list1)
    cleaned_string = ""
    for each in list1:
        cleaned_string += each + " "
    # print(cleaned_string)
    blob = TextBlob(full_file)
    # a = opinion.sentiment
    # blob = TextBlob(cleaned_string)
    return blob
    # return cleaned_string, blob, pages, word_count 

def gits(file):
    rsrcmgr = PDFResourceManager()
    sio = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, sio, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    fp = open(file, 'rb')
    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
        fp.close()
        text = sio.getvalue()
        text=text.replace(chr(272)," ")
        print(type(text))




def extract_nostring(file):
    #returns pages, words, sentimate_object
    return extract(file)[1:]

# def buzzwords(file):


def multifile(files_list):
    files_list - []
    for each in files_list:
        file_and_pages = extract(each)
        files_list.append(file_and_pages)
    return files_list

