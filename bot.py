#!/usr/bin/env python3

from kurisu3 import AIBot

UserName = 'user'
BotName = 'bot'
DontKnowMessage = 'no data'

def check_answer(text):
    if text:
        return text
    return DontKnowMessage

def main():
    bot = AIBot()

    last_phrase = None
    while True:
        phrase = input(UserName + ': ')
        if phrase == 'exit':
            break
        if phrase.startswith('~') and last_phrase:
            bot.learn(UserName, last_phrase, phrase[1:])
        else:
            print(BotName + ': ' + check_answer(bot.answer(UserName, phrase)))
        last_phrase = phrase

if __name__=="__main__":
    main()
