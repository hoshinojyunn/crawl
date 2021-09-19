import geturl
from bs4 import BeautifulSoup
import re


def getStocklist(stocklist, url):
    html = geturl.GetHtml(url)
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find_all('a')
    for i in a:
        try:
            href = i.attrs['href']
            stocklist.append(re.findall(r'[s][zh]\w\d{6}', href))
        except:
            continue


def getStockInfo():
    return ''
