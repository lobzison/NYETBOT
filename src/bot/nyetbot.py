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

    def set_memes(self, memes):
        """Setter for a meme object"""
        self.memes = memes

    def add_meme_to_file(self, meme_name, pic_addres):
        """Adds meme with picture addres to file"""
        self.memes[meme_name] = pic_addres
        redis_connection.set_value(meme_name, pic_addres)

    def del_meme_from_file(self, meme_name):
        """Delete meme from frile"""
        self.memes.pop(meme_name, None)
        redis_connection.delete(meme_name)

    def show_memes(self, meta):
        """Shows availbale commands"""
        chat_id = meta['chat_id']
        memes_list = 'Available memes:'
        for meme in self.memes.keys():
            memes_list += '\n' + meme
        self.send_message(chat_id, memes_list)

    def random_fuck_you(self, meta):
        """Randomly fuck-offs the user"""
        roll = random.randint(1, self.average_message_per_fuck)
        if roll == 1:
            fuck = random.choice(self.fucks)
            self.send_message(meta['chat_id'], fuck, meta['message_id'])

    def add_meme_init(self, meta):
        """Next text message from user will be name of the meme, and image is meme"""
        self.users_waiting_add.add(meta['user_id'])
        user_meme_struct = self.user_meme_struct.copy()
        self.user_memes[meta['user_id']]=  user_meme_struct
        self.send_message(meta['chat_id'], 'Send the name of the meme', meta['message_id'])

    def add_meme_name(self, meta, name):
        """Next text message from user will be name of the meme, and image is meme"""
        self.user_memes[meta['user_id']]['meme_name'] = name
        self.send_message(
            meta['chat_id'], 'Name set to '+ name+ '\nSend a photo', meta['message_id'])

    def add_meme_final(self, meta, pic_adress):
        """Next text message from user will be name of the meme, and image is meme"""
        # Check if picture
        self.user_memes[meta['user_id']]['meme_pic'] = pic_adress
        self.add_meme_to_file(self.user_memes[meta['user_id']]['meme_name'],
                              self.user_memes[meta['user_id']]['meme_pic'])
        self.user_memes.pop(meta['user_id'], None)
        self.users_waiting_add.remove(meta['user_id'])
        self.send_message(
                    meta['chat_id'], 'Succesfully set up new meme', meta['message_id'])

    def get_response(self, message, typ, meta):
        """Send accroding action"""
        self.random_fuck_you(meta)
        user_id = meta['user_id']
        if user_id in self.users_waiting_add:
            if not self.user_memes[user_id]['meme_name']:
                text = self.get_text(message)
                name = text.rstrip().lstrip()
                self.add_meme_name(meta, name)
            elif not self.user_memes[user_id]['meme_pic']:
                photo_id = self.get_photo_id(message)
                self.add_meme_final(meta, photo_id)
        if user_id in self.users_waiting_del:
            text = self.get_text(message)
            name = text.split(' ', 1)[0]
            self.del_meme_final(meta, name)

        self.parse_for_meme(message, typ, meta)
        
    def del_meme_final(self, meta, name):
        """Final operations for meme deletion"""
        if name in self.memes:
            self.del_meme_from_file(name)
        self.users_waiting_del.remove(meta['user_id'])
        self.send_message(
            meta['chat_id'], 'Meme deleted', meta['message_id'])

    def parse_for_meme(self, message, typ, meta):
        """Checks if text contains commans
        If yes - returns first, if no - returns None"""
        if typ == 'text':
            text = self.get_text(message)
            words = text.split()
            for word in words:
                if word in self.memes:
                    self.send_photo(meta['chat_id'],self.memes[word], meta['message_id'])

    def del_meme_init(self, meta):
        """Deletes the meme by name"""
        self.users_waiting_del.add(meta['user_id'])
        self.show_memes(meta)
        self.send_message(
            meta['chat_id'], 'Send the name of the meme to delete', meta['message_id'])
