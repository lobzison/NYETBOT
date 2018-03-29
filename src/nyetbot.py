import json
import os
import random
import bothandler


class NyetBot(bothandler.BotHandler):
    """Parse all messages, posm memes, save memes, random fuck you"""

    def __init__(self, token):
        super(NyetBot, self).__init__(token)
        self.commands = {'/add_meme': self.add_meme,
                         '/del_meme': self.del_meme,
                         '/show_memes': self.show_memes}
        self.memes_file = "dicpics.json"
        self.average_message_per_fuck = 300
        self.fucks = ['pishov nahui']
        with open(self.memes_file) as f:
            self.memes = json.load(f)

    def get_response(self, text):
        """Responce for a text. Should be owerritter in child if you want to get any response"""
        return None

    def set_memes(self, memes):
        """Setter for a meme object"""
        self.memes = memes

    # TODO multiple names for same meme without generating same line again
    def add_meme(self, meme_name, pic_addres):
        """Adds meme with picture addres to file"""
        with open(self.memes_file, "r+b") as f:
            data = json.load(f)
            data[meme_name] = pic_addres
            self.set_memes(data)
            f.seek(0)  # need to work on windows
            json.dump(data, f, indent=4, separators=(',', ': '))

    def del_meme(self, meme_name):
        """Delete meme from frile"""
        with open(self.memes_file, "r+b") as f:
            data = json.load(f)
            data.pop(meme_name, None)
            self.set_memes(data)
            f.seek(0)  # need to work on windows
            json.dump(data, f, indent=4, separators=(',', ': '))

    def show_memes(self, chat_id):
        """Shows avalibale commands"""
        memes_list = 'Avaliable memes:'
        for meme in self.memes.keys():
            memes_list += '\n' + meme
        self.send_message(chat_id, memes_list)

    def random_fuck_you(self, chat_id, user_id, message_id):
        """Randomly fuck-offs the user"""
        roll = random.randint(1, self.average_message_per_fuck)
        if roll == 1:
            fuck = random.choice(self.fucks)
            # TODO not just message but a reply
            self.send_message(chat_id, fuck)
    # TODO wrappers for add and delete funcs for user interactions
    # TODO recieve and send pictures
    # TODO add and delete in different thread
