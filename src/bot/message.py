
class Message(object):
    """Class for storting and retriving
       telegram message information"""

    def __init__(self, message):
        """Class initializator"""
        self.message_body = message
        self.message_types = set(['message', 'edited_message'])
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
        pass

    def 

    



    
