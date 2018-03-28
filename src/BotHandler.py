import requests
from yandex_translate import YandexTranslate


class BotHandler:

    def __init__(self, token, translate_key):
        self.token = token
        self.api_url = 'https://api.telegram.org/bot{}/'.format(token)
        self.language = {"from": "ru", "to": "pl"}
        self.translate_key = translate_key
        self.offset = None
        self.response_types = ['text']
        self.commands = ['pshek']

    # API part
    def send_message(self, chat, message):
        """Send message to the chat."""""
        method = 'sendMessage'
        params = {"chat_id": chat, "text": message}
        response = requests.post(self.api_url + method, params)
        return response

    def get_updates(self, timeout=30):
        """Gets json of messages"""
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': self.offset}
        response = requests.get(self.api_url + method, params)
        result_json = response.json()['result']
        return result_json

    # /API part

    # setters
    def change_language(self):
        """Changes the language back and forth"""
        lng_to = self.language["to"]
        lng_from = self.language["from"]
        self.language["to"] = lng_from
        self.language["from"] = lng_to

    def set_offset(self, offset):
        """Setter for offset"""
        self.offset = offset

    #/ setters

    # getters
    def get_translation(self, text):
        """Translates text"""
        translate = YandexTranslate(self.translate_key)
        text = translate.translate(
            text, '{}-{}'.format(self.language["from"], self.language["to"]))
        return text["text"]

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
        """Gets response for text message"""
        response = self.get_translation(text)
        return response

    def get_command(self, text):
        """Checks if text contains commans
        If yes - returns first, if no - returns None"""
        for command in self.commands:
            if '/' + command == text:
                return command

    #/ getters

    def strip_update(self, update):
        """Retuns message part of update, 
        sets offset to the update_id of message"""
        self.set_offset(update['update_id'])
        if 'message' in update:
            return update['message']
        elif 'edited_message' in update:
            return update['edited_message']
        else:
            return []

    def execute_command(self, command, chat_id):
        """Executes appropriate action for a command"""
        if command == self.commands[0]:
            self.change_language()
            response = "Now translating from {} to {}".format(
                self.language["from"].upper(),
                self.language["to"].upper())
            self.send_message(chat_id, response)

#   main part

    def handle_updates(self, updates):
        """Hanles the update set and responses accordingly"""
        # print(updates)
        if not updates:
            pass
        for update in updates[-1:]:
            print(update)
            message = self.strip_update(update)
            typ = self.get_msg_type(message)
            if typ in self.response_types:
                meta = self.get_meta(message)
                text = self.get_text(message)
                command = self.get_command(text)
                if command:
                    self.execute_command(command, meta[0])
                else:
                    response = self.get_response(text)
                    self.send_message(meta[0], response)
            self.set_offset(self.offset + 1)
