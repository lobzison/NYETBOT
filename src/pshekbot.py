from yandex_translate import YandexTranslate
import bothandler

class PshekBot(bothandler.BotHandler):
    """ Simple translation """

    def __init__(self, token, translate_key):
        super(PshekBot, self).__init__(token)
        self.translate_key = translate_key
        self.language = {"from": "ru", "to": "pl"}
        self.commands = {'/pshek': self.change_language}

    def change_language(self, chat_id):
        """Changes the language back and forth"""
        lng_to = self.language["to"]
        lng_from = self.language["from"]
        self.language["to"] = lng_from
        self.language["from"] = lng_to
        response = "Now translating from {} to {}".format(
            self.language["from"].upper(),
            self.language["to"].upper())
        self.send_message(chat_id, response)

    def get_translation(self, text):
        """Translates text"""
        translate = YandexTranslate(self.translate_key)
        text = translate.translate(
            text, '{}-{}'.format(self.language["from"], self.language["to"]))
        return text["text"]

    def get_response(self, text):
        """Response for a text. Should be owerritter in child if you want to get any response"""
        return self.get_translation(text)
