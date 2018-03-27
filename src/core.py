import keys
import BotHandler


nyet_bot = BotHandler.BotHandler(keys.BOT_KEY, keys.TRANSLATE_KEY)


def main():
    new_offset = None
    while True:

        nyet_bot.get_updates(new_offset)
        last_update = nyet_bot.get_last_update()

        nyet_bot.handle_update(last_update)

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
