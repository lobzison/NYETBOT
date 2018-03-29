import requests
from yandex_translate import YandexTranslate


class BotHandler:
    """Generic class for any bot using long pooling"""
	api_url = 'https://api.telegram.org/bot{}/'.format(token)

    def __init__(self, token):
        self.token = token
        self.offset = None
		self.commands = {}
		self.response_types = set(['text'])
		self.message_types = set(['message', 'edited_message'])

    # API part
    def send_message(self, chat, message):
        """Send message to the chat."""""
        method = 'sendMessage'
        params = {"chat_id": chat, "text": message}
        response = requests.post(api_url + method, params)
        return response

    def get_updates(self, timeout=30):
        """Gets json of messages"""
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': self.offset}
        response = requests.get(api_url + method, params)
        result_json = response.json()['result']
        return result_json

    # /API part

    # setters
    def set_offset(self, offset):
        """Setter for offset"""
        self.offset = offset

    #/ setters

    # getters
    def get_text(self, message):
        """Gets text part of message"""
        return message['text']

    def get_msg_type(self, message):
        """Returns type of message"""
        for typ in self.response_types:
            if typ in message:
                return typ

    def get_meta(self, message):
        """Returns metadata of message"""
        meta = []
        chat_id = message['chat']['id']
        meta.append(chat_id)
        return meta

    def get_response(self, text):
        """Responce for a text. Should be owerritter in child if you want to get any response"""
        return None

    def get_command(self, text):
        """Checks if text contains commans
        If yes - returns first, if no - returns None"""
		words = map(str.split(), text)
		for command in words:
		    if command in self.commands.values():
			    return command

    #/ getters

    def strip_update(self, update):
        """Retuns message part of update, 
        sets offset to the update_id of message + 1"""
        self.set_offset(update['update_id'] + 1)
		for message_type in self.message_types:
		    if message_type in update:
			    return update[message_type]
		return []

	def execute_command(self, command, chat_id):
        """Executes appropriate action for a command"""
		self.commands[command](chat_id)

#   main part

    def handle_updates(self, updates):
        """Hanles the update set and responses accordingly"""
        if not updates:
            pass
        for update in updates[-1:]:
            # print(update)
            message = self.strip_update(update)
            typ = self.get_msg_type(message)
            if not typ:
			    pass
            meta = self.get_meta(message)
            text = self.get_text(message)
            command = self.get_command(text)
            if command:
                self.execute_command(command, meta[0])
            else:
                response = self.get_response(text)
                if response: self.send_message(meta[0], response)
			
			
class PshekBot(BotHandler):
    """ Simple translation """
	
	def __init__(self, token, translate_key):
	    super(PshekBot, self).__init__(token)
	    self.translate_key = translate_key
		self.language = {"from": "ru", "to": "pl"}
        self.commands = {'/pshek': self.change_language}
		
	def change_language(self, chat_id):
        """Changes the language back and forth"""
        lng_to = self.language["to"]
        lng_from = self.language["from"]
        self.language["to"] = lng_from
        self.language["from"] = lng_to
		response = "Now translating from {} to {}".format(
                self.language["from"].upper(),
                self.language["to"].upper())
        self.send_message(chat_id, response)
		
	def get_translation(self, text):
        """Translates text"""
        translate = YandexTranslate(self.translate_key)
        text = translate.translate(
            text, '{}-{}'.format(self.language["from"], self.language["to"]))
        return text["text"]
		
	def get_response(self, text):
        """Response for a text. Should be owerritter in child if you want to get any response"""
        return self.get_translation(text)
		
import json
import os
import random

class NyetBot(BotHandler):
    """Parse all messages, posm memes, save memes, random fuck you"""
	
    def __init__(self, token):
	    super(PshekBot, self).__init__(token)
		self.commands = {'/add_meme': self.add_meme,
                   		'/del_meme': self.del_meme,
						'/show_memes': self.show_memes}
		self.memes_file = "dicpics.json"
		self.average_message_per_fuck = 300
		self.fucks = ['pishov nahui']
		with open(self.memes_file) as f:
            self.memes = json.load(f)
		
	def get_response(self, text):
        """Responce for a text. Should be owerritter in child if you want to get any response"""
        return None
		
	def set_memes(self, memes):
	    """Setter for a meme object"""
		self.memes = memes
		
	# TODO multiple names for same meme without generating same line again
	def add_meme(self, meme_name, pic_addres):
	    """Adds meme with picture addres to file"""
        with open(self.memes_file,"r+b") as f:
            data = json.load(f)
            data[meme_name] = pic_addres
			self.set_memes(data)
            f.seek(0) # need to work on windows
            json.dump(data, f, indent=4, separators=(',', ': '))

	def del_meme(self, meme_name):
	    """Delete meme from frile"""
        with open(self.memes_file,"r+b") as f:
            data = json.load(f)
            data.pop(meme_name, None)
			self.set_memes(data)
            f.seek(0) # need to work on windows
            json.dump(data, f, indent=4, separators=(',', ': '))
			
	def show_memes(self, chat_id):
	    """Shows avalibale commands"""
		memes_list = 'Avaliable memes:'
		for meme in self.memes.keys():
		    memes_list += '\n' + meme
		self.send_message(chat_id, memes_list)
	
	def random_fuck_you(self, chat_id, user_id, message_id):
	    """Randomly fuck-offs the user"""
		roll = random.randint(1, self.average_message_per_fuck)
		if roll == 1:
		    fuck = random.choise(fucks)
			# TODO not just message but a reply
			self.send_message(chat_id, fuck)
	# TODO wrappers for add and delete funcs for user interactions
	# TODO recieve and send pictures
	# TODO add and delete in different thread
