# https://stock.finance.sina.com.cn/stock/go.php/vReport_List/kind/search/index.phtml?symbol=002415&t1=all&p=1
# 海康威视 近半年研究报告
import requests
from lxml import etree
import csv
import time
import fake_useragent
import redis
import json
import random
from requests.exceptions import ProxyError
ua = fake_useragent.UserAgent()


# 代理池
def getproxy():
    # 连接到本地Redis数据库
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    # 获取所有键名为"use_proxy"的键的值
    all_values = redis_client.hvals('use_proxy')
    # 从值中筛选出"last_status": true的键
    filtered_keys = []
    for value in all_values:
        data = json.loads(value.decode('utf-8'))
        if data.get('last_status') is True:
            filtered_keys.append(data)
    # 从筛选后的键中随机选择一个键
    proxy = random.choice(filtered_keys)['proxy']
    # print(proxy)
    proxies = {'http': f'http://{proxy}', 'https': f'https://{proxy}'}
    return proxies


def getNumPage(code):
    # https://stock.finance.sina.com.cn/stock/go.php/vReport_List/kind/search/index.phtml?symbol=002415&t1=all
    url = f"https://stock.finance.sina.com.cn/stock/go.php/vReport_List/kind/search/index.phtml?symbol={code}&t1=all"
    resp = requests.get(url, headers={'User-Agent': ua.firefox}, proxies=getproxy())
    # print(resp.text)
    # page_count = 1
    page_count = etree.HTML(resp.text).xpath('//*[@id="_function_code_page"]/span[10]/a/@onclick')[0].split("'")[1]
    print(f"研究报告共{page_count}页")
    return page_count


# 被识别为爬虫会限制五分钟内拒绝访问
def reports(stock, code, page):
    global resp, htmlpage
    print(f"{stock}研究报告第{page}页")
    # https://stock.finance.sina.com.cn/stock/go.php/vReport_List/kind/search/index.phtml?symbol=600000&t1=all&p=8
    url = f"https://stock.finance.sina.com.cn/stock/go.php/vReport_List/kind/search/index.phtml?symbol={code}&t1=all&p={page}"
    print(url)
    while True:
        try:
            resp = requests.get(url, headers={'User-Agent': ua.firefox}, proxies=getproxy(), verify=False)
        except ProxyError:
            print(f'{ProxyError},IP失效，标题页面内容无法获取，正在更换IP。。。。')
        else:
            # print(resp.text)
            page_html = etree.HTML(resp.text)
            trs = ['https:' + i for i in page_html.xpath('//td[@class="tal f14"]/a/@href')]
            print(trs)
            csv_file = open('data//news_data//' + f'{stock}研究报告第{page}页.csv', 'w', newline='', encoding='utf-8')
            f = csv.writer(csv_file)
            for tr in trs:
                time.sleep(2)
                while True:
                    try:
                        htmlpage = requests.get(tr, headers={'User-Agent': ua.firefox}, proxies=getproxy(),
                                                verify=False)
                    except ProxyError:
                        print(f'{ProxyError},IP失效，研究报告页面内容无法获取，正在更换IP。。。。')
                    else:
                        # print(htmlpage.text)
                        html = etree.HTML(htmlpage.text)
                        title = html.xpath('//div[@class="content"]/h1/text()')
                        category = html.xpath('//div[@class="content"]/div[1]/span[1]/text()')
                        institution = html.xpath('//div[@class="content"]/div[1]/span[2]/a/text()')
                        researcher = html.xpath('//div[@class="content"]/div[1]/span[3]/a/text()')
                        date = html.xpath('//div[@class="content"]/div[1]/span[4]/text()')
                        content = html.xpath('//div[@class="content"]/div[2]/p/text()')
                        print([title[0], category[0][3:], institution[0], researcher[0], date[0][3:],
                               ''.join(content).strip()])
                        f.writerow([title[0], category[0][3:], institution[0], researcher[0], date[0][3:],
                                    ''.join(content).strip()])
            csv_file.close()


def main():
    f = open('target', 'r', encoding='utf-8')
    stock_name = f.read().split('\n')
    print(stock_name)
    for s in stock_name:
        stock = s.split('（')[0]
        code = s.split('.')[-1].split('）')[0]
        print(stock)
        print(code)
        # 启动爬虫获取获取页数、页面响应
        page_count = getNumPage(code)
        print(page_count)
        # # 爬取内容
        for i in range(1, int(page_count)+1):
            reports(stock, code, i)
        time.sleep(2)


if __name__ == '__main__':
    main()
