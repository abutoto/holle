#!/usr/bin/env python
# -*- coding: utf8  -*-
'''
Created on 20190701
@author zhangsheng013
'''

import sys
import time
import datetime
import json
import logging
import ConfigParser

reload(sys)
sys.setdefaultencoding('utf-8')

def read_file(name, sp='\t'):
    with open(name) as f:
        for line in f:
            line = line.strip("\n").split(sp)
            yield line

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, filename='./log/log.txt', filemode='w', format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

    conf_file = "conf/env.conf"
    config.read(conf_file)
