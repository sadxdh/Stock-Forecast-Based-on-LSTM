# https://stock.finance.sina.com.cn/stock/go.php/vReport_List/kind/search/index.phtml?symbol=002415&t1=all&p=1
# 海康威视 近半年研究报告
import requests
from lxml import etree
import csv
import time

# 代理池
def getproxy():
    # proxypool_url = 'http://127.0.0.1:5555/random'
    # proxy = requests.get(proxypool_url).text.strip()
    # proxies = {'http': 'http://' + proxy}
    proxies = {'http': 'http://127.0.0.1:7890'}
    return proxies

def getNumPage(code):
    # https://stock.finance.sina.com.cn/stock/go.php/vReport_List/kind/search/index.phtml?symbol=002415&t1=all
    url = f"https://stock.finance.sina.com.cn/stock/go.php/vReport_List/kind/search/index.phtml?symbol={code}&t1=all"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.42',
    }
    resp = requests.get(url, headers=headers, proxies=getproxy())
    # print(resp.text)
    # page_count = 1
    page_count = etree.HTML(resp.text).xpath('//*[@id="_function_code_page"]/span[10]/a/@onclick')[0].split("'")[1]
    print(f"研究报告共{page_count}页")
    return page_count

# 被识别为爬虫会限制五分钟内拒绝访问 # 代理池默认不执行，需要请自行配置
def reports(stock,code, page):
    # https://stock.finance.sina.com.cn/stock/go.php/vReport_List/kind/search/index.phtml?symbol=002415&t1=all&p=16
    url = f"https://stock.finance.sina.com.cn/stock/go.php/vReport_List/kind/search/index.phtml?symbol={code}&t1=all&p={page}"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.42',
    }
    resp = requests.get(url, headers=headers, proxies=getproxy())
    # print(resp.text)
    page_html = etree.HTML(resp.text)
    trs = ['https:' + i for i in page_html.xpath('//td[@class="tal f14"]/a/@href')]
    # print(trs)
    csv_file = open('data//news_data//' + f'{stock}研究报告第{page}页.csv', 'w', newline='', encoding='utf-8')
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

def main():
    # f = open('target','r',encoding='utf-8')
    # stock_name = f.read().split('\n')
    # print(stock_name)
    # for s in stock_name:
    #     stock = s.split('（')[0]
    #     code = s.split('.')[-1].split('）')[0]
    #     print(stock)
    #     print(code)
    #     # 启动爬虫获取获取页数、页面响应
    #     page_count = getNumPage(code)
    #     print(page_count)
    #     # # 爬取内容
    for i in range(24, 27):
        reports('海康威视','002415', i)


if __name__ == '__main__':
    main()

# 海康威视（SZ.002415）
# 浦发银行（SH.600000）
# 东方智造（SZ.002175）
# 上海临港（SH.600848）
# 华工科技（SZ.000988）