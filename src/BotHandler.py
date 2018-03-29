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
        print(text)
        words = text.split()
        for command in words:
            print(command)
            if command in self.commands.keys():
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
