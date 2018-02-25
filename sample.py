import requests
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import urllib

#a = pdf.coinmarketcap("marketcap.csv")


def search(string):
    string.replace(' ','%20')
    string.replace(':', '%3A')
    bing_search = "https://www.bing.com/search?q=" + string
    r = requests.get(bing_search)
    if r is not None:
        soup = BeautifulSoup(r.text, "html.parser")
        # print(soup)
        if soup is not None:
            link = soup.find('cite').text
        return link

def many_search(strings_list):
    links_list = []
    counter = 0
    for each in strings_list:
        url = search(each)
        links_list.append(url)
        counter += 1
        print(counter)
    return links_list

def files(links_list):
    for link in links_list:
        r = requests.get(link)
        print(r.content.decode('utf-8', 'ignore'))
        # print(r.content.decode('utf-8','ignore'))

        # urllib.request.urlretrieve(url,"newpdfs/")
        # print(z)
    # print("H!")
        # f = urllib.request.urlopen(url)
        # data = f.read()
        # print(data)
        # with open(data, "wb") as code:
        #     code.write(data)
        # urllib.request.urlretrieve(url, "code.zip")
            
        # webFile = urllib2.urlopen(url)
        # pdfFile = open(url.split('/')[-1], 'w')
        # pdfFile.write(webFile.read())
        # webFile.close()
        # pdfFile.close()
