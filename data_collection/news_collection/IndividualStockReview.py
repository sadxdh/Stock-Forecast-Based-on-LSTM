# https://finance.sina.com.cn/roll/index.d.html?cid=56588&page=1
# 海康威视 近两个月个股点评
import requests
from lxml import etree
from urllib import parse
import csv
import time

# 被识别为爬虫会限制五分钟内拒绝访问 # 代理池默认不执行，需要请自行配置
def reports(page):
    url = f"https://finance.sina.com.cn/roll/index.d.html?cid=56588&page={page}"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.42',
    }
    resp = requests.get(url, headers=headers) # , proxies=getproxy()
    # print(resp.text)
    page_html = etree.HTML(resp.text)
    trs = [i for i in page_html.xpath('//*[@id="Main"]/div[3]/ul/li/a/@href')]
    # print(trs)
    csv_file = open('data//news_data//' + f'个股点评第{page}页.csv', 'w', newline='', encoding='utf-8')
    f = csv.writer(csv_file)
    for tr in range(len(trs)):
        # print(requests.get(tr, headers=headers).text)
        html = etree.HTML(requests.get(trs[tr], headers=headers).text)
        title = html.xpath('/html/body/div[2]/h1/text()')
        title = [parse.unquote(t.encode('unicode_escape').decode('utf-8').replace('\\x', '%')) for t in title]
        content = html.xpath('//*[@id="artibody"]/p/text()')
        content = [parse.unquote(c.encode('unicode_escape').decode('utf-8').replace('\\x', '%')) for c in content]
        # print(title)
        # print(content)
        f.writerow([title, ''.join(content).strip()])
    csv_file.close()

def main():
    page_count = 6
    for i in range(1, int(page_count)+1):
        reports(i)
    time.time(2000)


if __name__ == '__main__':
    main()
