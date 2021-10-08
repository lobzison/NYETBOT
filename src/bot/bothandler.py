import requests
import message as msg

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

    def send_audio(self, chat, audio_id, reply_id=None):
        """Send audio to the chat."""""
        method = 'sendAudio'
        params = {"chat_id": chat, "audio": audio_id,
                  "reply_to_message_id": reply_id}
        response = requests.post(self.api_url + method, params)
        return response

    def send_document(self, chat, document_id, reply_id=None):
        """Send document to the chat."""""
        method = 'sendDocument'
        params = {"chat_id": chat, "document": document_id,
                  "reply_to_message_id": reply_id}
        response = requests.post(self.api_url + method, params)
        return response

    def send_video(self, chat, video_id, reply_id=None):
        """Send video to the chat."""""
        method = 'sendVideo'
        params = {"chat_id": chat, "video": video_id,
                  "reply_to_message_id": reply_id}
        response = requests.post(self.api_url + method, params)
        return response

    def send_voice(self, chat, voice_id, reply_id=None):
        """Send voice to the chat."""""
        method = 'sendVoice'
        params = {"chat_id": chat, "voice": voice_id,
                  "reply_to_message_id": reply_id}
        response = requests.post(self.api_url + method, params)
        return response

    def send_video_note(self, chat, video_note_id, reply_id=None):
        """Send vidoe note to the chat."""""
        method = 'sendVideoNote'
        params = {"chat_id": chat, "video_note": video_note_id,
                  "reply_to_message_id": reply_id}
        response = requests.post(self.api_url + method, params)
        return response

    def send_sticker(self, chat, sticker_id, reply_id=None):
        """Send sticker to the chat."""""
        method = 'sendSticker'
        params = {"chat_id": chat, "sticker": sticker_id,
                  "reply_to_message_id": reply_id}
        response = requests.post(self.api_url + method, params)
        return response

    def get_function_for_sending(self, msg_type):
        """Sends file based on type"""
        mapping = {'sticker': self.send_sticker,
                   'photo': self.send_photo,
                   'document': self.send_document,
                   'video': self.send_video,
                   'audio': self.send_audio,
                   'voice': self.send_voice,
                   'video_note': self.send_video_note}
        return mapping.get(msg_type)


    def get_updates(self, timeout=30):
        """Gets json of messages"""
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': self.offset}
        response = requests.get(self.api_url + method, params)
        print(response)
        result_json = response.json()['result']
        return result_json

    # setters
    def set_offset(self, offset):
        """Setter for offset"""
        self.offset = offset

    def get_response(self, message):
        """Responce for a text. Should be owerritter in child if you want to get any response"""
        return None

    def get_command(self, message):
        """Checks if text contains commans
        If yes - returns first, if no - returns None"""
        if message.get_type() == 'text':
            text = message.get_text()
            command = text.split('@', 1)[0]
            if command in self.commands.keys():
                return command

    def strip_update(self, update):
        """Retuns message part of update, 
        sets offset to the update_id of message + 1"""
        print(update)
        self.set_offset(update['update_id'] + 1)
        for message_type in self.message_types:
            if message_type in update:
                return update[message_type]
        return []

    def execute_command(self, command, message):
        """Executes appropriate action for a command"""
        self.commands[command](message)

#   main part

    def handle_updates(self, updates):
        """Hanles the update set and responses accordingly"""
        if not updates:
            pass
        for update in updates:
            message_body = self.strip_update(update)
            if not message_body:
                pass
            message = msg.Message(message_body)
            command = self.get_command(message)
            if command:
                self.execute_command(command, message)
            else:
                response = self.get_response(message)
                if response: self.send_message(message.get_chat_id(), response)
