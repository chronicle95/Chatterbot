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
        return min(self.diff(other, i-1, j)+1, self.diff(other, i, j-1)+1, self.diff(other, i-1, j-1)+cost)


class AIBotAnswer:
    def __init__(self, phrase_index, phrase_index_list):
        self.phrase = phrase_index
        if type(phrase_index_list) == int:
            self.options = [phrase_index_list]
        else:
            self.options = phrase_index_list

    def add_option(self, phrase_index):
        # allow for same index to be reapplied many times
        self.options.append(phrase_index)

    def get_key_index(self):
        return self.phrase

    def get_answer_index(self):
        return random.choice(self.options)


class AIBot:
    def __init__(self, nick="Bot"):
        self.nick = nick
        self.words = []
        self.phrases = []
        self.answers = []

    def _assign_phrase_index(self, phrase):
        if not phrase in self.phrases:
            self.phrases.append(phrase)
            return len(self.phrases) - 1
        else:
            return self.phrases.index(phrase)

    def learn(self, nick, query_text, response_text):
        user_phrase = AIBotPhrase(query_text, self.words)
        bot_answer = AIBotPhrase(response_text, self.words)
        user_phrase_index = self._assign_phrase_index(user_phrase)
        bot_answer_index = self._assign_phrase_index(bot_answer)
        for ans in self.answers:
            if ans.get_key_index() == user_phrase_index:
                ans.add_option(bot_answer_index)
                return
        self.answers.append(AIBotAnswer(user_phrase_index, bot_answer_index))

    def answer(self, nick, query_text):
        user_phrase = AIBotPhrase(query_text, self.words)
        user_phrase_index = self._assign_phrase_index(user_phrase)
        if not self.answers:
            return None
        fit_ans = self.answers[0]
        min_diff = self.phrases[self.answers[0].get_answer_index()].diff(
            user_phrase)
        for ans in self.answers:
            cur_diff = self.phrases[ans.get_key_index()].diff(user_phrase)
            if cur_diff < min_diff:
                fit_ans = ans
                min_diff = cur_diff
        return self.phrases[fit_ans.get_answer_index()].to_string(self.words)


class AIBotKeeper:
    def __init__(self, bot):
        self.bot = bot

    def write(self, file_name):
        with open(file_name, 'w') as f:
            for ans in self.answers:
                b = self.bot
                key_str = b.phrases[ans.get_key_index()].to_string(b.words)
                for opt in ans.options:
                    s = key_str + ' => ' + b.phrases[opt].to_string(b.words)
                    f.write(s + '\n')

    def read(self, nick, file_name):
        with open(file_name, 'r') as f:
            for line in f:
                pair = line.split('=>')
                self.bot.learn(nick, pair[0], pair[1])
