import requests
from yandex_translate import YandexTranslate


class BotHandler:

    def __init__(self, token, translate_key):
        self.token = token
        self.api_url = 'https://api.telegram.org/bot{}/'.format(token)
        self.language = {"from": "ru", "to": "pl"}
        self.translate_key = translate_key

    def send_message(self, chat, message):
        """Send message to the chat."""""
        method = 'sendMessage'
        params = {"chat_id": chat, "text": message}
        response = requests.post(self.api_url + method, params)
        return response

    def get_updates(self, offset=None, timeout=30):
        """Gets json of messages"""
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        response = requests.get(self.api_url + method, params)
        result_json = response.json()['result']
        return result_json

    def get_last_update(self):
        """Gets last update"""
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = []

        return last_update

    def change_language(self):
        """Changes the language back and forth"""
        lng_to = self.language["to"]
        lng_from = self.language["from"]
        self.language["to"] = lng_from
        self.language["from"] = lng_to

    def get_translation_obj(self):
        """Creates translate object from key"""
        translate = YandexTranslate(self.translate_key)
        return translate

    def handle_update(self, update):
        """Handles incoming updates"""
        if update != []:
            update_id = update['update_id']
            last_chat_id = update['message']['chat']['id']

            if 'message' not in update or 'text' not in update['message']:
                self.send_message(
                    last_chat_id, 'PSHEK PSHEK PSHEK NE PONIMAY PISHI TEKST')
            else:
                last_chat_text = update['message']['text']
                if last_chat_text.lower() == "/pshek":
                    self.change_language()
                    l_message = self.language
                    self.send_message(
                        last_chat_id, 'NOW TRANSLATING %s' % l_message)
                else:
                    translate = self.get_translation_obj()
                    l_message = translate.translate(
                        last_chat_text, '%s-%s' % (self.language["from"], self.language["to"]))
                    if l_message["code"] != 200 or l_message["text"] == []:
                        l_answer = 'YA OBOSRALSA, SORYAN'

                    else:
                        l_answer = l_message["text"]
                    self.send_message(last_chat_id, l_answer)
