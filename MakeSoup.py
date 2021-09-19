from bs4 import *
import re

"""
说实话 
这个类有点蠢
"""
# url='http://www.iqiyi.com/v_li28o9z88c.html'
# demo=GetUrl(url)
# soup=BeautifulSoup(demo,'html.parser')#第一个变量为html或xml格式的文本 第二个变量为对应文本的解释器
# tag=soup.title
# print(tag.string)
# print(soup.prettify())
class Soup(object):  # 该Soup对象用get返回的text来构建
    def __init__(self, html):
        self.text = html

    def downtraverse(self):  # 下行遍历
        soup = BeautifulSoup(self.text, 'html.parser')
        for child in soup.body.children:  # 遍历某一节点的儿子节点 .contents返回列表类型 .children返回迭代类型且有选择器
            print(child)

    def uptraverse(self):  # 上行遍历
        soup = BeautifulSoup(self.text, 'html.parser')
        for parent in soup.a.parents:  # 遍历某一节点的父亲节点 .parents返回迭代类型 只能用于for in结构
            if parent is None:  # 进行上行遍历时会遍历到最大的html本身 而本身没有名字
                print(parent)
            else:
                print(parent.name)  # 输出父亲节点名字

    def paralleltraverse(self):  # 平行遍历
        soup = BeautifulSoup(self.text, 'html.parser')
        for sibling in soup.a.previous_siblings:  # .previous_siblings返回某节点之前的所有的平行节点 是迭代类型 只能用于for in结构
            print(sibling)
        for sibling in soup.a.next_siblings:  # .next_siblings返回某节点之后的所有的平行节点 是迭代类型 只能用于for in结构
            print(sibling)

    def find_url(self):
        soup = BeautifulSoup(self.text, 'html.parser')
        for link in soup.find_all('a'):  # find_all返回一个列表类型
            print(link.get('href'))

    def _find(self, list):
        soup = BeautifulSoup(self.text, 'html.parser')
        temp = []
        time = []
        for i in soup.find_all(id=re.compile('day')):
            print(i)
            # temp.append(i.find(re.compile('tmp_lte_')))
            # time.append(i.find(re.compile('hour')))
        # for i in range(len(time)):
        #    list.append([time[i],temp[i]])
