import requests
import random
from bs4 import BeautifulSoup
import os

user_agent_list = [  # 设多个user-agent防止爬多了被封 （@-@）
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"]


def load_html(url):  # 请求html没什么好说的
    try:
        r = requests.get(url, headers={'user-agent': random.choice(user_agent_list)})
        r.encoding = 'utf-8'  # r.apparent_encoding
        r.raise_for_status()
        return r.text
    except:
        return print('爬取异常')


search_url = 'https://search.bilibili.com/article?keyword='  # b站专栏搜索url


def get_topicURL(keyword, depth) -> list:  # 将各个专栏的地址加到pic_url_list中
    topic_url_list = []
    for i in range(1, depth + 1):
        serchurl = search_url + keyword + '&page={}'.format(i)
        html = load_html(serchurl)
        soup = BeautifulSoup(html, 'html.parser')
        a = soup.find_all('a', class_='poster')
        for link in a:
            href = link.get('href')
            list1 = href.split('/')
            if len(list1[-1]) != 20 and len(list1[-1]) != 21 and len(list1[-1]) != 22:  # url末尾 别问 问就是我一个一个数的
                continue
            else:
                topic_url_list.append('https:' + href)
    return topic_url_list


def getpicsURL_from_topic(topic_url) -> list:  # 返回图片url
    img_url = []
    for topic in topic_url:
        html = load_html(topic)
        soup = BeautifulSoup(html, 'html.parser')
        for picture in soup.find_all('figure', class_='img-box'):
            for img in picture:
                if img.get('data-src') != None:
                    img_url.append('https:' + img.get('data-src'))
    return img_url


def download_pics(img_url, keyword):  # 下载 色图 oh~~nice 下载一页的图
    root = 'D://topicPics'  # 此处修改根目录下保存的文件夹
    load = 0
    picnum = 0
    for url in img_url:
        try:
            picnum += 1
            path = root + '//' + keyword + str(picnum) + '.jpg'
            if not os.path.exists(root):
                os.mkdir(root)
            if not os.path.exists(path):
                r = requests.get(url, headers={'user-agent': random.choice(user_agent_list)})
                r.raise_for_status()
                with open(path, 'wb') as f:
                    f.write(r.content)
                    load += 1
                    print('\r当前进度:{}%'.format(load * 100 / len(img_url)), end='')
                    f.close()
                    print('文件下载成功')
            else:
                load += 1
                print('\r当前进度:{}%'.format(load * 100 / len(img_url)), end='')
                # print("文件已存在")
        except:
            load += 1
            print('\r当前进度:{}%'.format(load * 100 / len(img_url)), end='')
            # print('爬取异常')
            continue


if __name__ == '__main__':
    key = input('输入搜索关键词:')
    depth = eval(input('设置搜索深度:'))
    topicurl = get_topicURL(key, depth)  # topocurl列表中是各专栏的url
    imgurl = getpicsURL_from_topic(topicurl)  # 图片url列表
    download_pics(imgurl, key)  # 下载
