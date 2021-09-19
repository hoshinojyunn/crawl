from geturl import *
from MakeSoup import *

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1;WOW64;rv:46.0) Gecko/20100101 Firefox/46.0'}
# url='http://www.iqiyi.com/v_li28o9z88c.html'
# PrintTestInfo()
# print(getsearch('间桐樱'))
# downloadpics(url)
# demo=GetHtml('http://baike.baidu.com/item/间桐樱/778771?fr=aladdin')
# soup=Soup(demo)
# soup.downtraverse()
url = 'http://www.nmc.cn/rest/weather'
soup = Soup(GetHtml(url))
list1 = []
# soup._find(list1)
r = get(url=url, headers=headers, timeout=30, params={'stationid': '54511'}).json()


def get_value_from_json(keyword, json, res_list):
    if not isinstance(json, dict):
        return json + 'is no a dict'
    elif keyword in json.keys():
        res_list.append(json[keyword])
    else:
        for value in json.values():
            if isinstance(value, dict):
                get_value_from_json(keyword, value, res_list)
            elif isinstance(value, (list, tuple)):
                get_value(keyword, value, res_list)
    return res_list


def get_value(keyword, content, res_list):
    for value in content:
        if isinstance(value, (list, tuple)):
            get_value(keyword, value, res_list)
        elif isinstance(value, dict):
            get_value_from_json(keyword, value, res_list)


print(r)
get_value_from_json('city', r, list1)
print(list1)
