import json
import redis_connection
import random
import bothandler

class NyetBot(bothandler.BotHandler):
    """Parse all messages, posm memes, save memes, random fuck you"""

    def __init__(self, token):
        super(NyetBot, self).__init__(token)
        self.commands = {'/add_meme': self.add_meme_init,
                         '/del_meme': self.del_meme_init,
                         '/show_memes': self.show_memes}
        self.average_message_per_fuck = 300
        self.fucks = ['pishov nahui', 'ssaniy loh', 'eto nepravda', 'dvachuiu', 'yr mom gay', 'nyet ty']
        self.memes = redis_connection.get_all_values()
        self.users_waiting_add = set([])
        self.users_waiting_del = set([])
        self.user_memes = {}
        self.user_meme_struct = {'meme_name': "", "meme_pic": ""}
        self.response_types = set(['text', 'photo'])

    def add_meme_to_file(self, meme_name, meme_info):
        """Adds meme with picture addres to file"""
        self.memes[meme_name] = meme_info
        redis_connection.set_value(meme_name, meme_info)

    def del_meme_from_file(self, meme_name):
        """Delete meme from frile"""
        self.memes.pop(meme_name, None)
        redis_connection.delete(meme_name)

    def show_memes(self, message):
        """Shows availbale commands"""
        chat_id = message.get_chat_id()
        memes_list = 'Available memes:'
        for meme in self.memes.keys():
            memes_list += '\n' + meme
        self.send_message(chat_id, memes_list)

    def random_fuck_you(self, message):
        """Randomly fuck-offs the user"""
        chat_id = message.get_chat_id()
        message_id = message.get_message_id()
        roll = random.randint(1, self.average_message_per_fuck)
        if roll == 1:
            fuck = random.choice(self.fucks)
            self.send_message(chat_id, fuck, message_id)

    def add_meme_init(self, message):
        """Next text message from user will be name of the meme, and image is meme"""
        user_id = message.get_sender_id()
        chat_id = message.get_chat_id()
        message_id = message.get_message_id()
        self.users_waiting_add.add(user_id)
        user_meme_struct = self.user_meme_struct.copy()
        self.user_memes[user_id]=  user_meme_struct
        self.send_message(chat_id, 'Send the name of the meme', message_id)

    def add_meme_name(self, message, name):
        user_id = message.get_sender_id()
        chat_id = message.get_chat_id()
        message_id = message.get_message_id()
        """Next text message from user will be name of the meme, and image is meme"""
        self.user_memes[user_id]['meme_name'] = name
        self.send_message(
            chat_id, 'Name set to '+ name+ '\nSend any media', message_id)

    def add_meme_final(self, message, pic_adress):
        """Next text message from user will be name of the meme, and image is meme"""
        # Check if picture
        user_id = message.get_sender_id()
        chat_id = message.get_chat_id()
        message_id = message.get_message_id()
        self.user_memes[user_id]['meme_pic'] = pic_adress
        typ = message.get_type()
        self.add_meme_to_file(self.user_memes[user_id]['meme_name'],
                              [self.user_memes[user_id]['meme_pic'], typ])
        self.user_memes.pop(user_id, None)
        self.users_waiting_add.remove(user_id)
        self.send_message(
                    chat_id, 'Succesfully set up new meme', message_id)

    def get_response(self, message):
        """Send accroding action"""
        self.random_fuck_you(message)
        user_id = message.get_sender_id()
        text = message.get_text()
        if user_id in self.users_waiting_add:
            if not self.user_memes[user_id]['meme_name']:
                name = text.rstrip().lstrip().lower()
                self.add_meme_name(message, name)
            elif not self.user_memes[user_id]['meme_pic']:
                photo_id = message.get_file_id()
                if photo_id:
                    self.add_meme_final(message, photo_id)
        if user_id in self.users_waiting_del:
            name = text.split(' ', 1)[0]
            self.del_meme_final(message, name)

        self.parse_for_meme(message)
        
    def del_meme_final(self, message, name):
        """Final operations for meme deletion"""
        user_id = message.get_sender_id()
        chat_id = message.get_chat_id()
        message_id = message.get_message_id()
        if name in self.memes:
            self.del_meme_from_file(name)
        self.users_waiting_del.remove(user_id)
        self.send_message(
            chat_id, 'Meme deleted', message_id)

    def parse_for_meme(self, message):
        """Checks if text contains commans
        If yes - returns first, if no - returns None"""
        if message.get_type() == 'text':
            chat_id = message.get_chat_id()
            message_id = message.get_message_id()
            text = message.get_text()
            words = text.split()

            for word in words:
                if word.lower() in self.memes:
                    meme = self.memes[word]
                    func = self.get_function_for_sending(meme[1])
                    if func is not None:
                        func(chat_id, meme[0], message_id)

    def del_meme_init(self, message):
        """Deletes the meme by name"""
        user_id = message.get_sender_id()
        chat_id = message.get_chat_id()
        message_id = message.get_message_id()
        self.users_waiting_del.add(user_id)
        self.show_memes(message)
        self.send_message(
            chat_id, 'Send the name of the meme to delete', message_id)
