# AI

import random


class AIBotPhrase(list):
    PunctChars = '!?.,-'

    def __init__(self, text="", words=[]):
        if text:
            self.populate(text, words)

    def populate(self, text, words):
        text = text.lower()
        # punctuation characters are considered as separate words
        for c in AIBotPhrase.PunctChars:
            text = text.replace(c, ' ' + c + ' ')
        text_words = text.split()
        for w in text_words:
            if not w in words:
                words.append(w)
                self.append(len(words) - 1)
            else:
                self.append(words.index(w))

    def to_string(self, words):
        s = ' '.join(list(map(lambda x: words[x], self)))
        for c in AIBotPhrase.PunctChars:
            s = s.replace(' ' + c, c)
        return s.capitalize()

    def diff(self, other, i=-1, j=-1):
        # levenstein distance
        if i == -1:
            i = len(self)
        if j == -1:
            j = len(other)
        if i == 0:
            return j
        elif j == 0:
            return i
        elif self[i-1] == other[j-1]:
            cost = 0
        else:
            cost = 1
        return min(diff(other, i-1, j)+1, diff(other, i, j-1)+1, diff(other, i-1, j-1)+cost)


class AIBotAnswer:
    def __init__(self, phrase=AIBotPhrase(), phrase_list=[]):
        self.phrase = phrase
        self.options = phrase_list

    def get_key_phrase(self):
        return self.phrase

    def get_random(self):
        return random.choice(self.options)


class AIBot:
    def __init__(self, nick="Bot"):
        self.nick = nick
        self.words = []
        self.phrases = []
        self.answers = []

    def learn(self, nick, query, response):
        pass

    def answer(self, nick, text):
        user_phrase = AIBotPhrase(text, self.words)
        if not user_phrase in self.phrases:
            self.phrases.append(user_phrase)
            user_phrase_index = len(self.phrases)-1
        else:
            user_phrase_index = self.phrases.index(user_phrase)
        if not self.answers:
            return None
        fit_ans = self.answers[0]
        min_diff = self.answers[0].diff(user_phrase)
        for ans in self.answers:
            cur_diff = ans.get_key_phrase().diff(user_phrase)
            if cur_diff < min_diff:
                fit_ans = ans
                min_diff = cur_diff
        return fit_ans
