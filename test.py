import bs4
import requests
import random
import re

# url = "https://syzx.me/ons-bishoujo-mangekyou-1-norowareshi-densetsu-no-shoujo/"
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
baidu_disk_list = []
topic_list = []
basic_url = "https://syzx.me/?s="


def load_html(url: str):  # 请求html没什么好说的
    try:
        r = requests.get(url, headers={'user-agent': random.choice(user_agent_list)})
        r.encoding = 'utf-8'  # r.apparent_encoding
        r.raise_for_status()
        return r.text
    except:
        return print('爬取异常')


class syzx():
    def __init__(self, search_name: str):
        self.html = load_html(basic_url + search_name)
        self.soup = bs4.BeautifulSoup(self.html, "html.parser")

    def get_topic_url(self) -> list:
        head = self.soup.find_all("h3", class_="title")
        for h3 in head:
            a_tag = h3.find('a')
            href = a_tag.get("href")
            topic_list.append(href)
        return topic_list

    def get_names(self) -> list:
        # title_dict = {}
        title = re.findall(r'<h3 class="title"><a href=".*?">(.*?)</a></h3></div>', self.html)
        # for i in range(len(title)):
        #    title_dict[i] = title[i]
        return title

    def get_resourse(self, topic_url) -> list:
        html = load_html(topic_url)
        soup = bs4.BeautifulSoup(html, 'html.parser')
        a = soup.find_all("a", class_="download-button baidunetdisk rounded-left btn btn-primary")
        for link in a:
            href = link.get("href")
            baidu_disk_list.append(href)
        return baidu_disk_list

    def get_code(self, topic_url: str) -> list:
        html = load_html(topic_url)
        soup = bs4.BeautifulSoup(html, "html.parser")
        button1 = soup.find("button", class_="baidunetdisk-password click-to-copy text-light btn btn-success")
        button2 = soup.find("button", class_="unzip-password click-to-copy text-warning btn btn-info")
        extract_code = re.findall(r'<code>(.*?)</code>', str(button1))
        zip_code = re.findall(r'<code>(.*?)</code>', str(button2))
        return [extract_code, zip_code]


def main():
    key_word = input("input galgame's name which you wanna download:")
    search_url = basic_url + key_word
    try:
        """
        搜索模块
        可让用户先/gal.search (搜索关键词)
        返回搜索列表
        """
        sz = syzx(key_word)
        topic_list = sz.get_topic_url()
        topic_name = sz.get_names()
        print("搜索结果:", topic_name)
        # print("搜索结果:", end="")
        # for i in range(len(topic_name)):
        #    print(topic_name[i])
        search_Node = eval(input("input search node:"))

        """
        获得搜索列表后
        用户可根据列表先后顺序输入 /gal.get search_Node
        获得资源
        """
        baidu_disk_list = sz.get_resourse(topic_list[search_Node])
        extract_code = sz.get_code(topic_list[search_Node])[0]
        zip_code = sz.get_code(topic_list[search_Node])[1]
        print("网盘链接:", baidu_disk_list)
        print("网盘提取码:", extract_code)
        print("文件解压码:", zip_code)
    except IndexError:
        print("设置的资源节点超出已有资源范围,请把节点设小些")


def Gal_get_All_resourse(gal_name: str) -> str:
    sz = syzx(gal_name)
    topic_list = sz.get_topic_url()
    topic_name = sz.get_names()  # there is names list
    String = ''
    extract_code_list = []
    zip_code_list = []
    for link in topic_list:
        html = load_html(link)
        soup = bs4.BeautifulSoup(html, 'html.parser')
        a = soup.find("a", class_="download-button baidunetdisk rounded-left btn btn-primary")
        if a != None:
            baidu_disk_list.append(a.get('href'))
            button1 = soup.find("button", class_="baidunetdisk-password click-to-copy text-light btn btn-success")
            button2 = soup.find("button", class_="unzip-password click-to-copy text-warning btn btn-info")
            extract_code_list.append(re.findall(r'<code>(.*?)</code>', str(button1)))
            zip_code_list.append(re.findall(r'<code>(.*?)</code>', str(button2)))
        else:
            baidu_disk_list.append('这个不是资源')
            extract_code_list.append([])
            zip_code_list.append([])

    for i in range(len(topic_name)):
        String += topic_name[i] + ":" + baidu_disk_list[i] + "," + "提取码:" + str(
            extract_code_list[i]) + "," + "解压码:" + str(zip_code_list[i]) + "\n"

    return String


if __name__ == "__main__":
    keyword = input()
    print(Gal_get_All_resourse(keyword))
