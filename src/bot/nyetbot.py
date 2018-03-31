import json
import os
import random
import bothandler

class NyetBot(bothandler.BotHandler):
    """Parse all messages, posm memes, save memes, random fuck you"""

    def __init__(self, token):
        super(NyetBot, self).__init__(token)
        self.commands = {'/add_meme': self.add_meme_init,
                         '/del_meme': self.del_meme_init,
                         '/show_memes': self.show_memes}
        self.memes_file = r".\src\bot\resources\dicpics.json"
        self.average_message_per_fuck = 300
        self.fucks = ['pishov nahui', 'ssaniy loh', 'eto nepravda', 'dvachuiu', 'yr mom gay', 'nyet ty']
        with open(self.memes_file) as f:
            self.memes = json.load(f)
        self.users_waiting_add = set([])
        self.users_waiting_del = set([])
        self.user_memes = {}
        self.user_meme_struct = {'meme_name': "", "meme_pic": ""}
        self.response_types = set(['text', 'photo'])

    def set_memes(self, memes):
        """Setter for a meme object"""
        self.memes = memes

    # TODO multiple names for same meme without generating same line again
    def add_meme_to_file(self, meme_name, pic_addres):
        """Adds meme with picture addres to file"""
        with open(self.memes_file, "r+b") as f:
            data = json.load(f)
            data[meme_name] = pic_addres
            self.set_memes(data)
            f.seek(0)  # need to work on windows
            json.dump(data, f, indent=4, separators=(',', ': '))

    def del_meme_from_file(self, meme_name):
        """Delete meme from frile"""
        with open(self.memes_file, "r") as f:
            data = json.load(f)
            data.pop(meme_name, None)
            self.set_memes(data)
        with open(self.memes_file, "w") as f:
            #f.seek(0)  # need to work on windows
            json.dump(data, f, indent=4, separators=(',', ': '))

    def show_memes(self, meta):
        """Shows avalibale commands"""
        chat_id = meta['chat_id']
        memes_list = 'Avaliable memes:'
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
            meta['chat_id'], 'Name setted to '+ name+ '\n Send a photo', meta['message_id'])

    def add_meme_final(self, meta, pic_adress):
        """Next text message from user will be name of the meme, and image is meme"""
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
        print("add list" + str(self.users_waiting_add))
        print("del list" + str(self.users_waiting_del))
        print(self.user_memes)
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


    # TODO wrappers for add and delete funcs for user interactions
    # TODO recieve and send pictures
    # TODO add and delete in different thread
