# -*- coding: utf-8 -*-

import json
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import time


def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
	soup = BeautifulSoup(html, 'lxml')
	for item in soup.find_all(class_='item'):
		index = item.find(name='em').string.split()[0]
		name = item.find(class_='title').string.strip()
		score = item.find(class_='rating_num').string.strip()
		quote = item.find(class_='inq').string.strip()
		yield '%3s\t%-20s %-5s %-20s\n' % (index, name, score, quote)

def write_to_file(content):
	with open('result.txt', 'a', encoding='utf-8') as f:
		f.write(content)
		print(content)

def main(offset):
	url = 'https://movie.douban.com/top250?start={}&filter='.format(offset)
	html = get_one_page(url)
	for item in parse_one_page(html):
		write_to_file(item)


if __name__ == '__main__':
    for i in range(6):
        main(offset=i * 25)
        time.sleep(1)
