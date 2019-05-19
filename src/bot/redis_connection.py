# -*- coding: UTF-8  -*-
import redis, json, pickle

class RedisConnection(object):

    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.connection = redis.from_url(self.connection_string)
        self.memes_key = "memes"
        self.images_key = "images"

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
        str_memes = self.get_value(self.memes_key)
        return json.loads(str_memes)

    def set_all_memes(self, value):
        """Sets memes to new value"""
        str_memes = json.dumps(value)
        self.set_value(self.memes_key, str_memes)

    def get_images_tree(self):
        """Returns bktree with all image hashes"""
        serialized_tree = self.get_value(self.images_key)
        return pickle.loads(serialized_tree)

    def set_images_tree(self, tree):
        """Sets image tree to new value"""
        serialized_tree = pickle.dumps(tree)
        self.set_value(self.images_key, serialized_tree)
