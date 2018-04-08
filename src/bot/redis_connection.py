# -*- coding: UTF-8  -*-
import redis
import json

class RedisConnection(object):

    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.connection = redis.from_url(self.connection_string)

    def set_value(self, key, value):
        """Sets the value of key to value"""
        self.connection.set(key, value)

    def get_value(self, key):
        """Gets value of a key"""
        return self.connection.get(key)

    def delete(self, key):
        """Deletes value by key"""
        self.connection.delete(key)

    def get_all_memes(self):
        """Returns all keys and values from redis as dictionary"""
        str_memes = self.get_value('memes')
        return json.loads(str_memes)

    def set_all_memes(self, value):
        """Sets memes to new value"""
        str_memes = json.dumps(value)
        self.set_value('memes', str_memes)