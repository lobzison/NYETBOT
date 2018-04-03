import keys
import os
import nyetbot

# uncomment for local run
# bot_key = keys.NYETBOT_KEY
bot_key = os.environ['NYETBOT_KEY']
nyet_bot = nyetbot.NyetBot(bot_key)


def main():
    while True:
        updates = nyet_bot.get_updates()
        nyet_bot.handle_updates(updates)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
