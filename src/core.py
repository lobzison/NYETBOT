import keys
import BotHandler


nyet_bot = BotHandler.BotHandler(keys.BOT_KEY, keys.TRANSLATE_KEY)


def main():
    while True:
        updates = nyet_bot.get_updates()
        nyet_bot.handle_updates(upates)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
