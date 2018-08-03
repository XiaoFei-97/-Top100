#!/usr/bin/env python
# coding=utf-8

import re
import json
import requests
from requests.exceptions import RequestException
from multiprocessing import Pool

def get_one_page(url, headers):
    """
        作用：获取一页的源码
        url:请求地址
        headers：请求头
    """
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    """
        作用：解析一页的源码
        html：网页源码
    """
    pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name"><a.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>', re.S)
    items = pattern.findall(html)
    # print(items)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5]+item[6]
        }
    
def write_to_file(item):
    """
        作用：往文件中写入内容
        item：处理后的单个电影信息
    """
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(item + '\n')

def maoyan_Spider(offset):
    """
        作用：猫眼电影调度器
        offset:get的页码参数
    """
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'}
    html = get_one_page(url, headers)
    # print(html)
    for item in parse_one_page(html):
        # print(item)
        item_str = json.dumps(item, ensure_ascii=False)
        write_to_file(item_str)

if __name__ == "__main__":
    # for i in range(10):
    #    maoyan_Spider(i*10)

    pool = Pool()
    pool.map(maoyan_Spider, [i*10 for i in range(10)])


