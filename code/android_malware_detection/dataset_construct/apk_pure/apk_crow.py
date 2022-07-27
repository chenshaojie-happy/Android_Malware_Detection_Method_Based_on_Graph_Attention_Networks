# -*- coding:utf-8-*-

import requests
import urllib
import re
import os
from bs4 import BeautifulSoup as bs


# return name_url_list  [apk_name,apk_url,info_url]
def first_crawl(value, page_number):
    proxies = {
        'https': 'https://127.0.0.1:1080',
        'http': 'http://127.0.0.1:1080'
    }

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',

    }
    name_url_list = []
    for i in range(page_number):

        url = 'https://apkpure.com/cn/' + value + '?page=' + str(i + 1) + '&ajax=1'

        response = requests.get(url, headers=headers, proxies=proxies)

        soup = bs(response.text.encode('utf-8'), 'html.parser')

        result = soup.find_all('li')

        for item in result:
            url_back = item.find('a', attrs={'rel': 'nofollow'})['href']
            # 这里获取apk第一层下载地址
            apk_url = 'https://apkpure.com' + url_back

            _blank = item.find_all('a', attrs={'target': '_blank'})
            # 这里或取apk的介绍链接
            info_url_back = _blank[0]['href']

            info_url = 'https://apkpure.com' + info_url_back
            # 这里获取apk的名字
            apk_name = _blank[1].string.strip().encode('utf-8')

            print(apk_name)
            print(apk_url)
            print(info_url)
            name_url_list.append([apk_name, apk_url, info_url])

    return name_url_list


# return google_url
def getgoogleurl_crawl(info_url):
    proxies = {
        'https': 'https://127.0.0.1:1080',
        'http': 'http://127.0.0.1:1080'
    }

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',

    }

    response = requests.get(info_url, headers=headers, proxies=proxies)

    soup = bs(response.text.encode('utf-8'), 'html.parser')

    google_url = soup.find_all('a', attrs={'rel': 'nofollow', 'target': '_blank'})[2]['href']

    return google_url


# 获取国内和国外下载地址，并且下载apk，无return
def download(apk_name, apk_url, path):
    proxies = {
        'https': 'https://127.0.0.1:1080',
        'http': 'http://127.0.0.1:1080'
    }

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',

    }

    response = requests.get(apk_url, headers=headers, proxies=proxies)

    soup = bs(response.text.encode('utf-8'), "html.parser")

    overseas_url = soup.find_all('a', attrs={'id': 'download_link'})[0]['href']
    # 国外下载地址
    print(overseas_url)

    response = requests.get(overseas_url, headers=headers, proxies=proxies, allow_redirects=False)
    # 国内下载地址
    domestic_url = response.headers['location']
    print(domestic_url)

    try:
        with open(path + 'overseas_url.txt', 'w') as f:
            f.write(overseas_url)
    except:
        print("overseas_url写入失败")

    try:
        with open(path + 'domestic_url.txt', 'w') as f:
            f.write(domestic_url)
    except:
        print("domestic_url写入失败")


# #下载apk文件
# headers = {
# 		'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'

# }
# response = requests.get(overseas_url,headers = headers,proxies=proxies)

# try:
# 	with open(path+apk_name+'.apk','wb') as apk:
# 		apk.write(response.content)
# except:
# 	print "下载失败!"

# google商店的部分，获取简介、隐私政策链接、和权限信息
def google_crawl(google_url, path):
    package_name = re.search(r'\?id=(.*)', google_url).group(1)
    url = r'''[[["xdSrCf","[[null,[\"%s\",7],[]]]",null,"IZBjA:0|TA"]]]&''' % (package_name)
    url = 'https://play.google.com/_/PlayStoreUi/data/batchexecute?f.req=' + urllib.quote(url)
    print(url)
    proxies = {
        'https': 'https://127.0.0.1:1080',
        'http': 'http://127.0.0.1:1080'
    }
    headers = {
        # 'Host':'play.google.com',
        # 'Connection': 'close',
        # 'Content-Length': '0',
        # 'X-Same-Domain': '1',
        # 'Origin':'https://play.google.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE',
        # 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        # 'Accept': '*/*',
        # 'Referer': 'https://play.google.com/',
        # 'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        # 'Cookie': '_ga=GA1.3.257569943.1553177649; _gid=GA1.3.1516440743.1553506688; OTZ=4853379_24_24__24_; NID=164=e6I-2byGG665RbH4GvgQfDz1Mdfu6YPXtw8MZYgZfdn1F4I0X0P6jvx-O5mL4MYhTqXFvKlDaYnwqNRggeWdliijvkoDJoUo1X70utbYp279eOojNAtdcRWPAFcDERJiMxyQedOb9n2F1wQbIGpdrei-pRgsSEZM3ajHTiEhqqM; 1P_JAR=2019-3-26-3; _gat_UA199959031=1',

    }

    text = requests.post(url, headers=headers, proxies=proxies).text.encode('utf-8')
    # print text
    text = re.search(r'''(\[.+\])''', text).group(1)[1:]
    # print text
    list_2 = eval(text.replace('null', '1'))
    # print list_2
    list_3 = eval(list_2[2])
    with open(path + 'access permission.txt', 'w') as f:
        # 有用的第一层信息
        try:
            list_4 = eval(str(list_3[0]))
            if list_4 != 1:
                for i in list_4:
                    if i:
                        list_5 = eval(str(i))
                        # print '类别：' + str(list_5[0])
                        for j in list_5[2]:
                            list_6 = eval(str(j))
                            # print list_6[1]
                            f.write(list_6[1] + '\n')
        except:
            print('无第一层权限信息！')
        print('2')
        # 有用的第二层信息
        try:
            list_4 = eval(str(list_3[1]))
            for index in range(len(list_4)):
                list_5 = eval(str(list_4[index]))
                list_6 = eval(str(list_5[2]))
                for i in list_6:
                    print(eval(str(i))[1] + '\n')
                    f.write(str(eval(str(i))[1]) + '\n')
        except:
            print('无第二层权限信息！')
        print('3')
        # 有用的第三层信息
        try:
            list_4 = eval(str(list_3[2]))
            list_5 = eval(str(list_4))
            for i in list_5:
                print(eval(str(i))[1] + '\n')
                f.write(str(eval(str(i))[1]) + '\n')
        except:
            print('无第三层权限信息！')
    proxies = {
        'https': 'https://127.0.0.1:1080',
        'http': 'http://127.0.0.1:1080'
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': 'NID=164=RqR1s86eZ4-wtl2_5n3vGZ5dah45_ZKX3CdxTNYddGTQfihDL2QwXuwNojNOnpUALnV1EzAHSzIpDA1qBDpu9DRvhnNFvu5SVXrUPzHiJxmoW3hB7u6ihj43rU80lBpNqf2mXtMC499Y2R3fyhlImhbFiLYBIVIHyHzyBjvnxsg; _ga=GA1.3.257569943.1553177649; 1P_JAR=2019-3-25-9; _gid=GA1.3.1516440743.1553506688; _gat_UA199959031=1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
    }

    response = requests.get(google_url, headers=headers, proxies=proxies)

    soup = bs(response.text.encode('utf-8'), "html.parser")
    info = ''
    for i in soup.find_all('div', attrs={'jsname': 'sngebd'})[0].strings:
        info = info + i + '\n'
    # print info.encode('utf-8')
    with open(path + 'info.txt', 'w') as f:
        f.write(info.encode('utf-8'))

    # print soup.find_all('a',text = "隐私权政策")[0]['href']
    with open(path + 'Privacy policy.txt', 'w') as f:
        f.write(soup.find_all('a', text="隐私权政策")[0]['href'])


if __name__ == '__main__':
    # https://apkpure.com/cn 该网站的应用分类
    url_first = {
        'game_casual': 1,
        # 'game_role_playing':2,
        # 'game_simulation':2
    }

    appname_url_list = []

    # for item in url_first:
    # 	appname_url_dict.update(first_crawl(item))
    for key, number in url_first.items():
        print('请求类别：' + key + '页数：' + str(number))
        # print first_crawl(value = key, page_number = number)
        # print len(first_crawl(value = key, page_number = number))
        appname_url_list += first_crawl(value=key, page_number=number)
        for item in appname_url_list:
            print('------------------')
            print(item[0])
            try:
                path = './all_type/%s/%s/' % (key, str(item[0]))
                print(path)
                folder = os.path.exists(path.decode('utf-8', 'ignore').encode('gbk'))
                if not folder:
                    os.makedirs(path.decode('utf-8', 'ignore').encode('gbk'))
            # with open(path + '/%s.txt'%(name), 'w') as f:
            # 	f.write(url)

            except:
                print('app名字错误')
            # google_url = getgoogleurl_crawl(item[2])
            google_url = "https://play.google.com/store/apps/details?id=" + re.search(r'//.*/cn/.*/(.*)',
                                                                                      item[2]).group(1)
            print('google的网址为：%s' % (google_url.encode('utf-8')))
            download(item[0], item[1], path.decode('utf-8', 'ignore').encode('gbk'))
            try:
                google_crawl(google_url, path.decode('utf-8', 'ignore').encode('gbk'))
            except:
                print('google play 无此应用！')
    print('共收集到%d个app信息' % (len(appname_url_list)))