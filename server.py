#!/usr/bin/env python
# -*- coding: utf8  -*-
'''
Created on 20190711
@author zhangsheng013
'''

import sys
import json
import logging
import ConfigParser

from flask import Flask, request
from gevent.pywsgi import WSGIServer
from gevent import monkey
monkey.patch_all()

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)

ERR_CODE = {0: 'success', -1: 'no_data', -2: 'illegal_params'}

@app.route('/stat', methods=['POST', 'GET'])
def stat():
    ret_dict = {'code': 0, 'msg': 'success', 'data': []}
    data = request.get_data()
    data = json.loads(data)

    return json.dumps(ret_dict)
    
if __name__ == '__main__':
    #port = int(sys.argv[1]) 
    logging.basicConfig(level=logging.INFO, \
        filename='./log/log.txt', \
        filemode='w', \
        datefmt='%Y-%m-%d %H:%M:%S', \
        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

    config = ConfigParser.ConfigParser()
    config.read("conf/env.conf")

    port = int(config.get("server", "port"))

    logging.info("start server port {}".format(port))
    http_server = WSGIServer(('0.0.0.0', port), app)
    http_server.serve_forever()
    loggin.info("end server")
