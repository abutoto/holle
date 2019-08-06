#!/usr/bin/env python
# -*- coding: utf8  -*-
'''
Created on 20190802
@author zhangsheng013
'''

import MySQLdb
import traceback
import logging
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class Mysqltool:
    def __init__(self, config):
        logging.info("mysql init start!!")

        from_mysql = "mysql"
        host = config.get(from_mysql, "host")
        port = int(config.get(from_mysql, "port"))
        user = config.get(from_mysql, "user")
        passwd = config.get(from_mysql, "passwd")
        db = config.get(from_mysql, "db")
        charset = config.get(from_mysql, "charset")

        self.config_mysql = { 
            'host': host,
            'port': int(port),
            'user': user,
            'passwd': passwd,
            'db': db, 
            'charset': charset
        }   
        self.conn = None
        self.__conn()
        self.__cur = None

        logging.info("mysql init end!!")

    def __conn(self):
        try:
            self.conn = MySQLdb.Connection(**self.config_mysql)
            return True
        except :
            return False

    def __conn(self):
        try:
            self.conn = MySQLdb.Connection(**self.config_mysql)
            return True
        except :
            return False

    def __reConn(self, num = 28800,stime = 3): #重试连接总次数为1天,这里根据实际情况自己设置,如果服务器宕机1天都没发现就......
        _number = 0
        _status = True
        while _status and _number <= num:
            try:
                self.conn.ping()       #cping 校验连接是否异常
                _status = False
            except:
                if self.__conn()==True: #重新连接,成功退出
                    _status = False
                    break
                _number +=1
                time.sleep(stime)      #连接不成功,休眠3秒钟,继续循环，知道成功或重试次数结束 

    def execute(self, sql, param=None):
        try:
            self.__reConn()
            self.__cur = self.conn.cursor()
            self.__cur.execute(sql, param)
            self.conn.commit()
            return int(self.__cur.rowcount)
        except Exception,e:
            logging.error('execute error:' + str(e))   # traceback.format_exc()
            self.conn.rollback()
            return 0
