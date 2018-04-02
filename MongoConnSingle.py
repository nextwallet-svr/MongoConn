# -*- coding: utf-8 -*-
import pymongo
import sys
import traceback
# import ServerConfig
from ServerConfig import *

class Singleton(object):
    # 单例模式写法,参考：http://ghostfromheaven.iteye.com/blog/1562618
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls)
        return cls._instance
  

class MongoConn(Singleton):    
    def __init__(self, DB_CONFIG):
        # connect db
        try:
            self.conn = pymongo.MongoClient(DB_CONFIG['host'], DB_CONFIG['port'])
            self.db = self.conn[DB_CONFIG['db_name']]  # connect db
            self.username=DB_CONFIG['username']
            self.password=DB_CONFIG['password']  
            if self.username and self.password:
                self.connected = self.db.authenticate(self.username, self.password)
            else:
                self.connected = True
        except Exception:
            traceback.print_exc()
            print ('Connect Statics Database Fail.')
            sys.exit(1)


class BtcMongoConn(Singleton):    
    def __init__(self):
        # connect db
        try:
            self.conn = pymongo.MongoClient(BTC_MONGODB_CONFIG['host'], BTC_MONGODB_CONFIG['port'])
            self.db = self.conn[BTC_MONGODB_CONFIG['db_name']]  # connect db
            self.username=BTC_MONGODB_CONFIG['username']
            self.password=BTC_MONGODB_CONFIG['password']  
            if self.username and self.password:
                self.connected = self.db.authenticate(self.username, self.password)
            else:
                self.connected = True
        except Exception:
            traceback.print_exc()
            print ('Connect Statics Database Fail.')
            sys.exit(1)