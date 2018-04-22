#coding=utf-8
from .MongoConnSingle import MongoConn
import traceback

import functools
import pymongo
import logging
import time

MAX_AUTO_RECONNECT_ATTEMPTS = 5
my_conn = None

def graceful_auto_reconnect(mongo_op_func):
  """Gracefully handle a reconnection event."""
  @functools.wraps(mongo_op_func)
  def wrapper(*args, **kwargs):
    for attempt in range(MAX_AUTO_RECONNECT_ATTEMPTS):
      try:
        return mongo_op_func(*args, **kwargs)
      except pymongo.errors.AutoReconnect as e:
        wait_t = 0.5 * pow(2, attempt) # exponential back off
        logging.warning("PyMongo auto-reconnecting... %s. Waiting %.1f seconds.", str(e), wait_t)
        time.sleep(wait_t)

  return wrapper


def init_conn(DB_CONFIG):
    global my_conn
    my_conn = MongoConn(DB_CONFIG)


def get_conn():
    global my_conn
    return my_conn

def close_conn():
    global my_conn
    my_conn.conn.close()

@graceful_auto_reconnect
def remove(table):
    global my_conn
    my_conn.db[table].remove()

@graceful_auto_reconnect
def save(table, value):
    # 一次操作一条记录，根据‘_id’是否存在，决定插入或更新记录
    try:
        global my_conn
        my_conn.db[table].save(value)
    except Exception:
        traceback.print_exc()
        raise

@graceful_auto_reconnect
def insert(table, value):
    # 可以使用insert直接一次性向mongoDB插入整个列表，也可以插入单条记录，但是'_id'重复会报错
    try:
        global my_conn
        my_conn.db[table].insert(value, continue_on_error=True)
    except (Exception) as e:
        print("insert: ", e)
        raise
        # print(value)

@graceful_auto_reconnect
def update(table, conditions, value, s_upsert=False, s_multi=False):
    try:
        global my_conn
        my_conn.db[table].update(conditions, value, upsert=s_upsert, multi=s_multi)
    except (Exception) as e:
        print("update: ", e)
        raise
        # print(value)

@graceful_auto_reconnect
def upsert_mary(table, datas):
    #批量更新插入，根据‘_id’更新或插入多条记录。
    #把'_id'值不存在的记录，插入数据库。'_id'值存在，则更新记录。
    #如果更新的字段在mongo中不存在，则直接新增一个字段
    try:
        global my_conn
        bulk = my_conn.db[table].initialize_ordered_bulk_op()
        for data in datas:
            _id=data['_id']
            bulk.find({'_id': _id}).upsert().update({'$set': data})
        bulk.execute()
    except Exception:
        traceback.print_exc()
        raise

@graceful_auto_reconnect
def upsert_one(table, data):
    #更新插入，根据‘_id’更新一条记录，如果‘_id’的值不存在，则插入一条记录
    try:
        global my_conn
        query = {'_id': data.get('_id','')}
        if not my_conn.db[table].find_one(query):
            my_conn.db[table].insert(data)
        else:
            data.pop('_id') #删除'_id'键
            my_conn.db[table].update(query, {'$set': data})
    except Exception:
        traceback.print_exc()
        raise

@graceful_auto_reconnect
def find_one(table, value):
    #根据条件进行查询，返回一条记录
    try:
        global my_conn
        return my_conn.db[table].find_one(value, max_time_ms=5000)
    except Exception:
        traceback.print_exc()
        raise

@graceful_auto_reconnect
def find(table, value):
    #根据条件进行查询，返回所有记录
    try:
        global my_conn
        return my_conn.db[table].find(value, max_time_ms=5000)
    except Exception:
        traceback.print_exc()
        raise

@graceful_auto_reconnect
def select_colum(table, value, colum):
    #查询指定列的所有值
    try:
        global my_conn
        return my_conn.db[table].find(value, {colum:1})
    except Exception:
        traceback.print_exc()
        raise
