#!/usr/bin/env python
# -*- coding: utf8  -*-
'''
Created on 20190701
@author zhangsheng013
'''

import sys
import json
import logging
import ConfigParser
import requests
from requests.adapters import HTTPAdapter
import pandas as pd

reload(sys)
sys.setdefaultencoding('utf-8')
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=3))
s.mount('https://', HTTPAdapter(max_retries=3))
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

def read_file(name, sp='\t', is_dict=False):
    columns = []
    with open(name) as f:
        for line in f:
            line = line.strip("\n").split(sp)
            if is_dict:
                if len(columns) == 0:
                    columns = line
                    continue
                line = dict(zip(columns, line))
            yield line

def post(url, data):
    try:
        r = requests.post(url, data, headers=headers)
        return json.loads(r.text)['data']
    except Exception,e:
        server_app.logger.info("post {} error {}".format(url, e))
        return None

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, \
        filename='./log/log.txt', \
        filemode='w', \
        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

    conf_file = "conf/env.conf"
    config.read(conf_file)

    columns = []
    name = ""
    df = pd.DataFrame(data, columns = columns)
    df.to_excel(name, index=False)
