# -*- coding: UTF-8  -*-
import os
import redis
r = redis.from_url(os.environ.get("REDIS_URL"))

#r = redis.from_url(
#     "redis://h:pb0a1e45ad71a25e3604d6f1f3837618c11cdc9b6e70ca9dcbbbe437b1333ba38@ec2-54-172-241-93.compute-1.amazonaws.com:7109")

def get_all_values():
    """Returns all keys and values from redis as dictionary"""
    key_value = {}
    for key in r.scan_iter():
        values = r.lrange(key, 0,-1)
        key_value[key.decode(
            'utf-8')] = [values[0].decode('utf-8'), values[1].decode('utf-8')]
    return key_value

def set_value(key, value):
    """Sets the value of key to value"""
    r.rpush(key, *value)

def get_value(key):
    """Gets value of a key"""
    return r.lrange(key,0, -1)

def delete(key):
    """Deletes value by key"""
    r.delete(key)
