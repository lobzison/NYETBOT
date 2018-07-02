# NYETBOT

## Generic telegram bot handler
BotHandler class in src/bot/bothandler module provides generic fuctionality of bot using long pool requests. Webhooks are planned. To use this class derive your bot from this class, and override the reply() method.

## Nyetbot
Bot for chat groups. Have a random phrase function, adding and deleteing of memes. Memes are basicly some string associated with media. If the message containing the string is posted, the associated media is posted by bot.

## Pshekbot
Really simple bot. Just a wrapper for yandex.translate API.
