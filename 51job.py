# -*- coding:utf-8 -*-
"""
 @Time: 2018/11/20 14:21
 @Author: Mr.Wang 
                                                  
"""
import requests
from lxml import etree
import csv
import time
import random

fp = open('51job.csv','wt',newline='',encoding='GBK',errors='ignore')
writer = csv.writer(fp)
'''title,salary,company,place,exp,edu,num,time,comment,url'''
writer.writerow(('职位','薪水','公司','地区','经验','学历','数量','时间','要求','url'))

def parseInfo(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
    }
    res = requests.get(url, headers=headers)
    selector = etree.HTML(res.text)
    # normalize-space空格处理
    title = selector.xpath('normalize-space(//*[@class="cn"]/h1/text())')
    salary = selector.xpath('normalize-space(//*[@class="cn"]/strong/text())')
    company = selector.xpath('normalize-space(//*[@class="cname"]/a[last()-1]/text())')
    place = selector.xpath('normalize-space(//*[@class="msg ltype"]/text()[1])')
    exp = selector.xpath('normalize-space(//*[@class="msg ltype"]/text()[2])')
    edu = selector.xpath('normalize-space(//*[@class="msg ltype"]/text()[3])')
    num = selector.xpath('normalize-space(//*[@class="msg ltype"]/text()[4])')
    time = selector.xpath('normalize-space(//*[@class="msg ltype"]/text()[5])')
    comment = selector.xpath('normalize-space(//*[@class="bmsg job_msg inbox"]/p/text())')
    url = res.url

    print(title,salary,company,place,exp,edu,num,time,comment,url)
    writer.writerow((title,salary,company,place,exp,edu,num,time,comment,url))

def getUrl(url):
    print(url)
    res = requests.get(url)
    res.encoding = 'GBK'
    if res.status_code == requests.codes.ok:
        selector = etree.HTML(res.text)
        urls = selector.xpath('//*[@id="resultList"]/div/p/span/a/@href')
        for url in urls:
            parseInfo(url)
            time.sleep(random.randrange(1, 2))


if __name__ == '__main__':
    key = 'Java'
    #  页数
    urls = ['https://search.51job.com/list/200200,000000,0000,00,9,99,'+key+',2,{}.html'.format(i) for i in range(1,3)]
    for url in urls:
        getUrl(url)