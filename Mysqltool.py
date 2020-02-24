#!/usr/bin/env python
# -*- coding: utf8  -*-
'''
Created on 20190823
@author zhangsheng013
'''

import MySQLdb
import traceback
import logging
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class MysqlConnect:
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
        self._conn = None
        self._connect()
        self._cursor = self._conn.cursor()

        logging.info("mysql init end!!")

    def _connect(self):
        try:
            self._conn = MySQLdb.Connection(**self.config_mysql)
            return True
        except:
            return False
    
    def query(self, sql):
        try:
            result = self._cursor.execute(sql)
        except MySQLdb.Error, e:
            print e
            result = False
        return result

    def select(self, table, column='*', condition=''):
        condition = ' where ' + condition if condition else None
        if condition:
            sql = "select %s from %s %s" % (column,table,condition)
        else:
            sql = "select %s from %s" % (column,table)
        self.query(sql)
        return self._cursor.fetchall()

    def insert(self, table, tdict):
        column = ''
        value = ''
        for key in tdict:
            column += ',' + key
            value += "','" + tdict[key]
        column = column[1:]
        value = value[2:] + "'"
        sql = "insert into %s(%s) values(%s)" % (table,column,value)
        self._cursor.execute(sql)
        self._conn.commit() 
        return self._cursor.lastrowid #返回最后的id

    def update(self, table, tdict, condition=''):
        if not condition:
            print "must have id"
            exit()
        else:
            condition = 'where ' + condition
        value = ''
        for key in tdict:
            value += ",%s='%s'" % (key,tdict[key])
        value = value[1:]
        sql = "update %s set %s %s" % (table,value,condition)
        self._cursor.execute(sql)
        return self.affected_num() #返回受影响行数

    def delete(self, table, condition=''):
        condition = 'where ' + condition if condition else None
        sql = "delete from %s %s" % (table,condition)
        # print sql
        self._cursor.execute(sql)
        self._conn.commit()
        return self.affected_num() #返回受影响行数

    def rollback(self):
        self._conn.rollback()

    def affected_num(self):
        return self._cursor.rowcount

    def __del__(self):
        try:
            self._cursor.close()
            self._conn.close()
        except:
            pass

    def close(self):
        self.__del__()

if __name__ == '__main__':
    dbconfig = {
        'host':'',
        'port':,
        'user':'python',
        'passwd':'123456',
        'dbname':'python',
        'charset':'utf8'
    }
    db = mysql(dbconfig)

    # print db.select('msg','id,ip,domain')
    # print db.select('msg','id,ip,domain','id>2')
    # print db.affected_num()

    # tdict = {
    #     'ip':'111.13.100.91',
    #     'domain':'baidu.com'
    # }
    # print db.insert('msg', tdict)
    
    # tdict = {
    #     'ip':'111.13.100.91',
    #     'domain':'aaaaa.com'
    # }
    # print db.update('msg', tdict, 'id=5')

    # print db.delete('msg', 'id>3')

    db.close()
