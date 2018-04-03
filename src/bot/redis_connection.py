# -*- coding: UTF-8  -*-
import os
import redis
r = redis.from_url(os.environ.get("REDIS_URL"))

def get_all_values():
    """Returns all keys and values from redis as dictionary"""
    key_value = {}
    for key in r.scan_iter():
       key_value[key] = r.get(key)
    return key_value

def set_value(key, value):
    """Sets the value of key to value"""
    r.set(key, value)

def get_value(key):
    """Gets value of a key"""
    return r.get(key)

def delete(key):
    """Deletes value by key"""
    r.delete(key)