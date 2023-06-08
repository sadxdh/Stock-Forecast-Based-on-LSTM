# https://stock.finance.sina.com.cn/stock/go.php/vReport_List/kind/search/index.phtml?symbol=600000&t1=all&p=1
import requests
from lxml import etree
import fake_useragent
import threading
import json
import csv
import random
import redis
ua = fake_useragent.UserAgent()
headers = {
    'Referer': 'https://stock.finance.sina.com.cn/stock/go.php/vReport_List/kind/search/index.phtml?symbol=600000&t1=all&p=1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.37',
}
urls = [
    f'https://stock.finance.sina.com.cn/stock/go.php/vReport_List/kind/search/index.phtml?symbol=002175&t1=all&p={p}'
    for p in range(1, 30+1)
]

# 返回单页面所有url
def getProxy():
    target_url = "http://httpbin.org/ip"
    proxy_host = 'http-short.xiaoxiangdaili.com'
    proxy_port = 10010
    proxy_username = '984115141711122432'
    proxy_pwd = '7OBgVZuU'

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxy_host,
        "port": proxy_port,
        "user": proxy_username,
        "pass": proxy_pwd,
    }

    proxies = {
        'http': proxyMeta,
        'https': proxyMeta,
    }

    # try:
    #     resp = requests.get(url=target_url, proxies=proxies)
    #     print(resp.text)
    # except Exception as e:
    #     print(e)
    return proxies

def urlcrawl(url):
    pagetext = requests.get(url, headers={'User-Agent': ua.msie}, proxies=getProxy())  # 可能报错//获取不到页面
    print(pagetext.status_code)
    html = etree.HTML(pagetext.text)
    pageurllist = html.xpath('.//td[@class="tal f14"]/a/@href')
    pageurllist = ['https:'+url for url in pageurllist]
    print(pageurllist)
    return pageurllist

# 单独页
def reachcrawl(stackname,pageurllist,i):
    csv_file = open('data//news_data//' + f'{stackname}研究报告第{i}页.csv', 'w', newline='', encoding='utf-8')
    f = csv.writer(csv_file)
    for url in pageurllist:
        htmltext = requests.get(url, headers={'User-Agent': ua.msie}, proxies=getProxy())
        html = etree.HTML(htmltext.text)
        title = html.xpath('//div[@class="content"]/h1/text()')
        category = html.xpath('//div[@class="content"]/div[1]/span[1]/text()')
        institution = html.xpath('//div[@class="content"]/div[1]/span[2]/a/text()')
        researcher = html.xpath('//div[@class="content"]/div[1]/span[3]/a/text()')
        date = html.xpath('//div[@class="content"]/div[1]/span[4]/text()')
        content = html.xpath('//div[@class="content"]/div[2]/p/text()')
        print([title[0], category[0][3:], institution[0], researcher[0], date[0][3:], ''.join(content).strip()])
        f.writerow([title[0], category[0][3:], institution[0], researcher[0], date[0][3:], ''.join(content).strip()])
    csv_file.close()

def main():
    stockname = '东方智造'
    for url in urls:
        reachcrawl(stockname, urlcrawl(url), url.split('=')[-1])
# 多线程
def multi_thread():
    stockname = '东方智造'
    threads = []    # 线程列表
    for url in urls:
        print(url)
        threads.append(  # 添加线程
            threading.Thread(target=reachcrawl, args=(stockname, urlcrawl(url), url.split('=')[-1]))   # 参数为元组类型，此处不加逗号则为字符串，加逗号使其表示为元组
        )
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()   # 等待结束

# 东方智造（SZ.002175）
if __name__ == '__main__':
    # multi_thread()
    main()