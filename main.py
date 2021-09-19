from geturl import *
import re


# 解析网页 将网页商品信息加入infolist中
def parsePage(infolist, html):
    try:
        pricelist = re.findall(r'"view_price":"[\d.]*"', html)
        titlelist = re.findall(r'"raw_title":".*?"', html)
        for i in range(len(pricelist)):
            price = eval(pricelist[i].split(':')[1])  # 返回view_price:price的第二个内容 即price
            title = titlelist[i].split(':')[1]
            infolist.append([price, title])
    except:
        print('解析失败')


# 打印商品信息表格
def printGoodslist(list):
    template = '{:4}\t{:8}\t{:16}'
    print(template.format('序号', '价格', '商品名称'))
    num = 0
    for i in list:
        num += 1
        print(template.format(num, i[0], i[1]))  # 输出表格


def FromTaoBaoSearchGoodsPrice():
    good = '书包'
    depth = 2  # 设置搜索深度
    search_url = 'https://s.taobao.com/search?q=' + good
    infoList = []
    for i in range(depth):
        try:
            url = search_url + '&s=' + str(i * 44)  # 淘宝每个页面有44个商品
            html = GetHtml(url)
            parsePage(infoList, html)
        except:
            continue  # 爬取失败则继续 确保不会影响后续操作
    printGoodslist(infoList)


FromTaoBaoSearchGoodsPrice()
