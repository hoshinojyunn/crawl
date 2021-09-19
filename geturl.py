from requests import *
import os


def GetHtml(url):  # 获取html 设置检查申请是否成功
    try:
        r = get(url=url, headers=headers, timeout=30)
        r.raise_for_status()  # 检测是否访问成功 若失败 则抛出异常
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return '产生异常'


# url='https://image.baidu.com/search/index?\
# tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&word=%E9%97%B4%E6%A1%90%E6%A8%B1'
# url='https://item.jd.com/100009077475.html'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1;WOW64;rv:46.0) Gecko/20100101 Firefox/46.0', }


# 'cookie':"hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; tracknick=tb331119425; t=b92fb454ee319cf37fa71bc97a117c6e; tk_trace=oTRxOWSBNwn9dPyorMJE%2FoPdY8zMG1aAN%2F0TkjYGZjkj6rrK3kv4LgxGhtlxvv2n251iRZBLi5%2BxLVnyk1ChK8pniqtYc5POJ13MpHFreiulwoaAZtxumg5KFvqGYOM5fQhGT2UbPZ8yZCnabKina0LudU2Gsu21qkwoGeFdhFd3%2Fi2nnWRXYoig8Pz54xs42uWOJpbTW666EFRTMatEmgsAd57V4AG6JPP7t2KkItJ8b53h7Qwre2aWHYycCB02s1D6BftoUvVoCq0ue%2BIuGJ4gl64XN%2FgbI66Z4PYehdWU9q3JNsQOKc%2BNx%2FmWYVq1vis53jA%2F0GH7zoM%2F6obNP2jOzwhM79JN7aJI05xGqi3U; _m_h5_tk=fffd0ef3065cea08b5cf22e369661384_1627665210692; _m_h5_tk_enc=cbcec54d17bc3d7472a4cb2c05f4de5d; xlly_s=1; _tb_token_=e7e651d361f37; mt=ci=5_1; cna=XIyqF+ksew0CAatvzxb6D+66; uc1=cookie15=Vq8l%2BKCLz3%2F65A%3D%3D&existShop=false&cookie21=UIHiLt3xTIkz&pas=0&cookie14=Uoe2ytPA5LRljA%3D%3D&cookie16=VT5L2FSpNgq6fDudInPRgavC%2BQ%3D%3D; csg=8cf52ff2; lgc=tb331119425; cancelledSubSites=empty; dnk=tb331119425; existShop=MTYyNzY1NzMxMg%3D%3D; _cc_=URm48syIZQ%3D%3D; _l_g_=Ug%3D%3D; sg=526; _nk_=tb331119425; isg=BMHBNGyURBTbcJYIffRkoXFq0w3b7jXgxvVqtyMWvkgnCuHcaz_PsJVI6P5MGc0Y; l=eBQmLZfqOrPXsIqsBOfahurza77OSIOYYuPzaNbMiOCPOM5B5CUCW6h-HhL6C31Vh6DBR3-8oQeJBeYBqQAonxvtIosM_Ckmn; tfstk=cO5dBR2eIlqhz4a6m9egF2i_Y9Ecw23pq2t-wyznnzxR5H1D6sfARnyBzFp0W"}#FireFox代理 也可直接用标准浏览器'Mozilla/5.0'
def getsearch(keyword):  # 搜索引擎
    try:
        kv = {'wd': keyword}
        r = get('http://www.baidu.com/s', params=kv, headers=headers)
        # print(r.request.url)
        r.raise_for_status()
        return r.request.url
    except:
        return print('爬取失败')


def downloadpics(url):  # 下载文件
    root = 'D://pics'
    path = root + '//' + url.split('/')[-1]  # 以url的最后一个目录作为文件名
    try:
        if not os.path.exists(root):  # 若写入的根目录不存在 则创建一个
            os.mkdir(root)
        if not os.path.exists(path):  # 若要下载的文件不存在此根目录 则进行下载
            r = get(url, headers=headers)
            r.raise_for_status()
            with open(path, 'wb') as w:  # 打开文件写入对象 若不存在该名字 则创建一个 wb表示该写入对象为二进制文件
                w.write(r.content)  # 写入r对象的二进制码
                w.close()
                print('文件下载成功')
        else:
            print('文件已存在')
    except:
        print('爬取失败')


# url='https://login.taobao.com/member/login.jhtml?spm=a21bo.21814703.754894437.1.5af911d969Bfuf&f=top&redirectURL=https%3A%2F%2Fwww.taobao.com%2F'
url = "https://s.taobao.com/search?q=书包&s=0"


def PrintTestInfo(url):
    r = GetHtml(url)
    print(r[:1000])
    head = get(url, headers=headers)
    print('初始头部信息为:', head.request.headers)


if __name__ == "__main__":
    keyword = input()
    print(getsearch(keyword))
