# https://stock.finance.sina.com.cn/stock/go.php/vReport_List/kind/search/index.phtml?symbol=002415&t1=all&p=1
# 海康威视 近半年研究报告
import requests
from lxml import etree
import csv


# 代理池
def getproxy():
    proxypool_url = 'http://127.0.0.1:5555/random'
    proxy = requests.get(proxypool_url).text.strip()
    proxies = {'http': 'http://' + proxy}
    return proxies


# 被识别为爬虫会限制五分钟内拒绝访问 # 代理池默认不执行，需要请自行配置
def reports(code, page):
    url = f"https://stock.finance.sina.com.cn/stock/go.php/vReport_List/kind/search/index.phtml?symbol={code}&t1=all&p={page}"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.42',
    }
    resp = requests.get(url, headers=headers, proxies=getproxy())
    # print(resp.text)
    page_html = etree.HTML(resp.text)
    trs = ['https:' + i for i in page_html.xpath('//td[@class="tal f14"]/a/@href')]
    # print(trs)
    csv_file = open('data//' + f'浦发银行研究报告第{page}页.csv', 'w', newline='', encoding='utf-8')
    f = csv.writer(csv_file)
    for tr in trs:
        # print(requests.get(tr, headers=headers).text)
        html = etree.HTML(requests.get(tr, headers=headers).text)
        title = html.xpath('//div[@class="content"]/h1/text()')
        category = html.xpath('//div[@class="content"]/div[1]/span[1]/text()')
        institution = html.xpath('//div[@class="content"]/div[1]/span[2]/a/text()')
        researcher = html.xpath('//div[@class="content"]/div[1]/span[3]/a/text()')
        date = html.xpath('//div[@class="content"]/div[1]/span[4]/text()')
        content = html.xpath('//div[@class="content"]/div[2]/p/text()')
        f.writerow([title[0], category[0][3:], institution[0], researcher[0], date[0][3:], ''.join(content).strip()])
        print([title[0], category[0][3:], institution[0], researcher[0], date[0][3:], ''.join(content).strip()])
    csv_file.close()


if __name__ == '__main__':
    code = '002415'  # 海康威视
    page = 1  # 爬取第几页
    reports(code, page)
