from typing import List
class Message(object):
    """Class for storting and retriving
       telegram message information"""

    def __init__(self, message):
        """Class initializator"""
        self.message_body = message
        self.message_types = ['text', 'sticker', 'photo', 'document','video', 'audio', 'voice',
                               'video_note', 'contact', 'location', 'venue', 'game', 'invoice' ]
        self.message_type = self.get_type()

    def _get_body(self):
        """Getter for message body"""
        return self.message_body

    def get_type(self):
        """Returns type of message."""
        for message_type in self.message_types:
            if message_type in self._get_body():
                return message_type

    def get_sender_id(self):
        """Returns id of message sender"""
        print(self._get_body())
        return self._get_body()['from']['id']

    def get_text(self) -> str:
        """Returns text of the message"""
        return self._get_body().get('text')

    def get_file_id(self):
        """Returns id of file"""
        typ = self.message_type
        body = self._get_body()
        if typ == 'photo':
            return body['photo'][0]['file_id']
        elif typ in ['sticker', 'photo', 'document','video', 'audio', 'voice',
                    'video_note']:
            return body[typ].get('file_id')

    def get_chat_id(self):
        """Return id of chat"""
        return self._get_body()['chat']['id']

    def get_message_id(self):
        return self._get_body()['message_id']
    
    def get_entities(self):
        return self._get_body().get('entities', [])

    def get_reply_user(self):
        reply = self._get_body().get('reply_to_message')
        if reply:
            return reply.get('from').get('id')

    def get_user_id(self):
        return self._get_body().get('from').get('id')

    def get_urls(self) -> List[str]:
        """ Returns list of urls from message"""
        text = self.get_text()
        entities = self.get_entities()
        res = []
        for entitiy in entities:
            if entitiy['type'] == 'url':
                begin = entitiy['offset']
                end = begin + entitiy['length']
                res.append(text[begin:end])
        return res
