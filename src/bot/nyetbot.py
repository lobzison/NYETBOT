from redis_connection import RedisConnection
from bothandler import BotHandler
import random
import os

connection_string = os.environ.get("REDIS_URL")

class NyetBot(BotHandler):
    """Parse all messages, posm memes, save memes, random fuck you"""

    def __init__(self, token):
        super(NyetBot, self).__init__(token)
        self.commands = {'/add_meme': self.add_meme_init,
                         '/del_meme': self.del_meme_init,
                         '/show_memes': self.show_memes,
                         '/discard': self.discard}
        self.average_message_per_fuck = 300
        self.fucks = ['pishov nahui', 'ssaniy loh', 'eto nepravda', 'dvachuiu', 'yr mom gay', 'nyet ty']
        self.redis_connection = RedisConnection(connection_string)
        self.memes = self.redis_connection.get_all_memes()
        self.users_waiting_del = set([])
        self.user_memes = {}
        self.user_meme_struct = {'meme_name': None, "meme_pic": None}
        self.meme_meta_struct = {'type': None, "adress": None}
        self.response_types = set(['text', 'photo'])

    def add_meme(self, meme_name, meme_info):
        """Adds meme with picture addres to file"""
        self.memes[meme_name] = meme_info
        self.redis_connection.set_all_memes(self.memes)

    def del_meme(self, meme_name):
        """Delete meme from frile"""
        self.memes.pop(meme_name, None)
        self.redis_connection.set_all_memes(self.memes)

    def show_memes(self, message):
        """Shows availbale commands"""
        chat_id = message.get_chat_id()
        memes_list = 'Available memes:'
        for meme in self.memes.keys():
            memes_list += '\n' + meme
        self.send_message(chat_id, memes_list)

    def random_fuck_you(self, chat_id, message_id):
        """Randomly fuck-offs the user"""
        roll = random.randint(1, self.average_message_per_fuck)
        if roll == 1:
            fuck = random.choice(self.fucks)
            self.send_message(chat_id, fuck, message_id)

    def add_meme_init(self, message):
        """Next text message from user will be name of the meme, and image is meme"""
        user_id = message.get_sender_id()
        chat_id = message.get_chat_id()
        message_id = message.get_message_id()
        user_meme_struct = self.user_meme_struct.copy()
        self.user_memes[user_id]=  user_meme_struct
        self.send_message(chat_id, 'Send the name of the meme', message_id)

    def add_meme_name(self, user_id, chat_id, message_id, name):
        """Next text message from user will be name of the meme, and image is meme"""
        self.user_memes[user_id]['meme_name'] = name
        self.send_message(
            chat_id, 'Name set to '+ name+ '\nSend any media', message_id)

    def add_meme_pic(self, msg_type, user_id, chat_id, message_id, pic_adress):
        """Next text message from user will be name of the meme, and image is meme"""
        self.user_memes[user_id]['meme_pic'] = pic_adress
        meme_meta = self.meme_meta_struct.copy()
        meme_meta['type'] = msg_type
        meme_meta['adress'] = pic_adress
        self.add_meme(self.user_memes[user_id]['meme_name'], meme_meta)
        self.user_memes.pop(user_id, None)
        self.send_message(
                    chat_id, 'Succesfully set up new meme', message_id)

    def get_response(self, message):
        """Send accroding action"""
        # get all meta information about message
        user_id = message.get_sender_id()
        chat_id = message.get_chat_id()
        message_id = message.get_message_id()
        text = message.get_text()
        msg_type = message.get_type()
        #process itself
        self.random_fuck_you(chat_id, message_id)
        if user_id in self.user_memes:
            if not self.user_memes[user_id]['meme_name'] and msg_type == 'text':
                name = text.rstrip().lstrip().lower()
                self.add_meme_name(user_id, chat_id, message_id, name)
            elif not self.user_memes[user_id]['meme_pic']:
                photo_id = message.get_file_id()
                if photo_id:
                    self.add_meme_pic(
                        msg_type, user_id, chat_id, message_id, photo_id)
        elif user_id in self.users_waiting_del:
            self.del_meme_final(user_id, chat_id, message_id, name)
        elif msg_type == 'text':
            self.parse_for_meme(chat_id, message_id, text)
        
    def del_meme_final(self, user_id, chat_id, message_id, name):
        """Final operations for meme deletion"""
        l_name = name.rstrip().lstrip().lower()
        if l_name in self.memes:
            self.del_meme(l_name)
        self.users_waiting_del.remove(user_id)
        self.send_message(
            chat_id, 'Meme deleted', message_id)

    def parse_for_meme(self, chat_id, message_id, text):
        """Checks if text contains commans
        If yes - returns first, if no - returns None"""
        lower_text = text.lower()
        for meme in self.memes:
            if meme in lower_text:
                meme_meta = self.memes[meme]
                func = self.get_function_for_sending(meme_meta['type'])
                if func is not None:
                    func(chat_id, meme_meta['adress'], message_id)

    def del_meme_init(self, message):
        """Deletes the meme by name"""
        user_id = message.get_sender_id()
        chat_id = message.get_chat_id()
        message_id = message.get_message_id()
        self.users_waiting_del.add(user_id)
        self.show_memes(message)
        self.send_message(
            chat_id, 'Send the name of the meme to delete', message_id)
            
    def discard(self, message):
        user_id = message.get_sender_id()
        chat_id = message.get_chat_id()
        flag = False
        if user_id in self.users_waiting_del:
            self.users_waiting_del.discard(user_id)
            flag = True
        if user_id in self.user_memes:
            self.user_memes.pop(user_id, False)
            flag = True
        if flag:
            self.send_message(
            chat_id, 'Command discarded')

        
