import keys
import BotHandler


nyet_bot = BotHandler.BotHandler(keys.BOT_KEY, keys.TRANSLATE_KEY)


def main():
    while True:
        udates = nyet_bot.get_updates()
        nyet_bot.handle_updates(udates)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
