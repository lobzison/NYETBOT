import requests

class BotHandler(object):
    """Generic class for any bot using long pooling"""

    def __init__(self, token):
        self.token = token
        self.offset = None
        self.commands = {}
        self.response_types = set(['text'])
        self.message_types = set(['message', 'edited_message'])
        self.api_url = 'https://api.telegram.org/bot{}/'.format(token)

    # API part
    def send_message(self, chat, message, reply_id = None):
        """Send message to the chat."""""
        method = 'sendMessage'
        params = {"chat_id": chat, "text": message, "reply_to_message_id": reply_id}
        response = requests.post(self.api_url + method, params)
        return response

    def send_photo(self, chat, photo_id, reply_id=None):
        """Send photo to the chat."""""
        method = 'sendPhoto'
        params = {"chat_id": chat, "photo": photo_id,
                  "reply_to_message_id": reply_id}
        response = requests.post(self.api_url + method, params)
        return response

    def get_updates(self, timeout=30):
        """Gets json of messages"""
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': self.offset}
        response = requests.get(self.api_url + method, params)
        result_json = response.json()['result']
        return result_json

    # setters
    def set_offset(self, offset):
        """Setter for offset"""
        self.offset = offset

    # getters
    def get_text(self, message):
        """Gets text part of message"""
        if 'text' in message:
            return message['text']

    def get_photo_id(self, message):
        """Gets text part of message"""
        if 'photo' in message:
            return message['photo'][0]["file_id"]

    def get_msg_type(self, message):
        """Returns type of message"""
        for typ in self.response_types:
            if typ in message:
                return typ

    def get_meta(self, message):
        """Returns metadata of message"""
        meta = {}
        meta['chat_id'] = message['chat']['id']
        meta['message_id'] = message['message_id']
        meta['user_id'] = message['from']['id']
        return meta

    def get_response(self, message, typ, meta):
        """Responce for a text. Should be owerritter in child if you want to get any response"""
        return None

    def get_command(self, message, typ, meta):
        """Checks if text contains commans
        If yes - returns first, if no - returns None"""
        if typ == 'text':
            text = self.get_text(message)
            command = text.split('@', 1)[0]
            if command in self.commands.keys():
                return command

    def strip_update(self, update):
        """Retuns message part of update, 
        sets offset to the update_id of message + 1"""
        self.set_offset(update['update_id'] + 1)
        for message_type in self.message_types:
            if message_type in update:
                return update[message_type]
        return []

    def execute_command(self, command, meta):
        """Executes appropriate action for a command"""
        self.commands[command](meta)

#   main part

    def handle_updates(self, updates):
        """Hanles the update set and responses accordingly"""
        if not updates:
            pass
        for update in updates[:]:
            message = self.strip_update(update)
            typ = self.get_msg_type(message)
            if not typ:
                pass
            meta = self.get_meta(message)
            command = self.get_command(message, typ, meta)
            if command:
                self.execute_command(command, meta)
            else:
                response = self.get_response(message, typ, meta)
                if response: self.send_message(meta['chat_id'], response)
