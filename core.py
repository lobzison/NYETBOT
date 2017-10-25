import requests
from yandex_translate import YandexTranslate


class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = 'https://api.telegram.org/bot{}/'.format(token)
        self.language = {"from": "ru", "to": "pl"}

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


nyet_bot = BotHandler("421347401:AAEZMIsjJT3yOh-68r_TJ0FjdTQo8O177BM")


def main():
    new_offset = None
    translate = YandexTranslate('trnsl.1.1.20170919T102055Z.7f2a9a244baf350b.f0f9abb8803ad4a6301be24d6ad71ba11b310840')
    while True:

        nyet_bot.get_updates(new_offset)
        last_update = nyet_bot.get_last_update()

        if last_update != []:
            last_update_id = last_update['update_id']
            last_chat_id = last_update['message']['chat']['id']

            if 'message' not in last_update or 'text' not in last_update['message']:
                nyet_bot.send_message(last_chat_id, 'PSHEK PSHEK PSHEK NE PONIMAY PISHI TEKST')
            else:
                last_chat_text = last_update['message']['text']
                if last_chat_text.lower() == "/pshek":
                    nyet_bot.change_language()
                    l_message = nyet_bot.language
                    nyet_bot.send_message(last_chat_id, 'NOW TRANSLATING %s' % l_message)
                else:
                    l_message = translate.translate(last_chat_text, '%s-%s' % (nyet_bot.language["from"], nyet_bot.language["to"] ))
                    if l_message["code"] != 200 or l_message["text"] == []:
                        l_answer = 'YA OBOSRALSA, SORYAN'

                    else:
                        l_answer = l_message["text"]
                    nyet_bot.send_message(last_chat_id, l_answer)

            new_offset = last_update_id + 1


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
