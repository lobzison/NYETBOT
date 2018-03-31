import keys
import pshekbot


nyet_bot = pshekbot.PshekBot(keys.PSHEKBOT_KEY, keys.TRANSLATE_KEY)


def main():
    while True:
        updates = nyet_bot.get_updates()
        nyet_bot.handle_updates(updates)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
