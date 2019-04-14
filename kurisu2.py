#!/usr/bin/python3

import random
import time
import datetime

# cite note: (at) character is present for including special operators
# special operators are:
# @...@ - take variable from dictionary and print it out
#    (may also be some command)
# $...$ - remember word, located right in the position of ampersand to dict
#
# All the operators should only be used in learning mode!
mask = '@abcdefghijklmnopqrstuvwxyzабвгдежзийклмнопрстуфхцчшщыьъэюя1234567890 '

words = []  # words ,array[string]
vars = {}		# variables, dict[string]

phrases = []  # * phrases ,array[array[?]]
pairs = []  # * phrase - possible answers ,array[array[?]]
# * emotion table (. - neutral, ! - exclamaion, ? - question) ,array[string]
emotion = []

greetz = []		# greeting phrases list (only indexes)
learnt = []		# message after learning a new phrase

last_user_phrase = -1  # initialize last user phrase with -1

nickname = ''
user_nickname = ''


# prints out all the statistics
# i.e. count of words, phrases, all the total etc
def showStats():
    print(''.ljust(5)+'words: '+str(len(words))+', phrases: ' +
          str(len(phrases))+', ansbase: '+str(len(pairs)))
    print(''.ljust(5)+'greets: '+str(len(greetz)) +
          ', learning msgs: '+str(len(learnt)))

# takes two indexes of phrases
# returns some number - the more equal the phrases are, the
# greater the number; a->b


def comparePhrases(a, b):
    global phrases
    global emotion
    counter_RightFit = 0
    counter_WrongFit = 0
    counter_NonExist = 0

    if emotion[a] == emotion[b]:
        counter_RightFit += 1

    for i in range(len(phrases[a])):
        flag = False
        for j in range(len(phrases[b])):
            if i == j and phrases[a][i] == phrases[b][j]:
                flag = True
                counter_RightFit += 1
            elif i != j and phrases[a][i] == phrases[b][j]:
                flag = True
                counter_WrongFit += 1
        if not flag:
            counter_NonExist += 1

    for i in range(len(phrases[b])):
        flag = False
        for j in range(len(phrases[a])):
            if i == j and phrases[b][i] == phrases[a][j]:
                flag = True
                counter_RightFit += 1
            elif i != j and phrases[b][i] == phrases[a][j]:
                flag = True
                counter_WrongFit += 1
        if not flag:
            counter_NonExist += 1

    return (counter_RightFit*2 + counter_WrongFit - counter_NonExist)

# checks whether two arrays are equal


def arraysEqual(a, b):
    if len(a) == len(b):
        for i in range(len(a)):
            if a[i] != b[i]:
                return False
        return True
    else:
        return False

# takes phrase index as input
# prepares phrase for output
# returns print-ready phrase


def releasePhrase(i):
    global phrases
    global emotion
    global words
    s = ''
    for wi in phrases[i]:
        # check if word contains special operators
        if '@' in words[wi]:
            # if does, take away those operators
            k = words[wi][1:-1]

            try:
                # if variable exists, take it
                s += vars[k] + ' '

            except KeyError:
                # after exception came
                # user defined commands go right here
                if k == 'username':
                    s += user_nickname + ' '
                if k == 'time':
                    hour = '%02i' % (datetime.datetime.now().hour)
                    minute = '%02i' % (datetime.datetime.now().minute)
                    s += hour+':'+minute+' '
        else:
            # otherwise just add this word to sentence
            s += words[wi] + ' '

    return (s.rstrip() + emotion[i])

# takes phrase index
# prints it carefully


def printPhrase(i):
    global nickname
    print(' ' + nickname.ljust(10) + ' -> ' + releasePhrase(i))

# filters out chars by mask
# returns result string


def filterCharacters(s, m):
    r = ''
    for c in s:
        if c in m:
            r += c
    return r

# does linear search over the word list
# returns index if found, -1 if not found


def getWordIndex(s):
    global words
    for i in range(len(words)):
        if words[i] == s:
            return i
    return -1

# checks, whether word exists or not
# if not, appends it to list


def tossWord(s):
    global words
    if getWordIndex(s) == -1:
        words.append(s)

# takes an array of indexes
# chooses random one
# returns phrase with chosen index
# if the list is empty -> empty string


def returnRandomPhrase(a):
    if len(a) > 0:
        i = int(random.random()*len(a))
        return releasePhrase(a[i])
    return ''

# takes an array of indexes
# chooses random one
# prints out phrase with chosen index
# if the list is empty -> prints nothing


def showUpRandomPhrase(a):
    if len(a) > 0:
        i = int(random.random()*len(a))
        printPhrase(a[i])

# greets the user with random phrase


def ohayogozaimasu():
    global greetz
    showUpRandomPhrase(greetz)

# looks for the best answer to the chosen user phrase
# at index 'i'


def findBestFittingAnswer(i):
    global phrases
    global pairs
    result = -1
    if len(phrases) > 0:
        points = -1024
        for j in range(len(phrases)):
            if len(pairs[j]) > 0:
                cp = comparePhrases(i, j)
                if cp > points:
                    points = cp
                    result = j
    return result

# takes unformatted user-input phrase in string format
# does parse it, then discovers new words, indexes them
# finds best fit solution
# returns the answer


def analyzePhrase(s, no_output=False, return_as_text=False):
    global last_user_phrase
    global phrases
    global emotion
    global pairs
    global greetz
    global learnt
    global mask

    current_user_phrase = 0  # index of current phrase in phrases array

    # make it lowercase
    q = s.strip().lower()

    # check for tilda command
    teach = False
    if '~' in q:
        teach = True

    # check for emotion
    emo = ''
    if '!' in q:
        emo += '!'
    if '?' in q:
        emo += '?'
    if emo == '':
        emo = '.'

    # filter out all unnecessary characters
    a = filterCharacters(q, mask)

    # separate the words
    # and update word list
    a = a.split(' ')
    for i in range(len(a)):
        a[i] = a[i].strip()
        tossWord(a[i])

    # convert phrases' words to indexes
    for i in range(len(a)):
        a[i] = getWordIndex(a[i])

    # check if phrase already exists in list
    exist = False
    for i in range(len(phrases)):
        if arraysEqual(phrases[i], a):
            exist = True
            current_user_phrase = i
            break

    # if does not exist than add it to phrases list
    if not exist:
        phrases.append(a)
        emotion.append(emo)
        pairs.append([])
        current_user_phrase = len(phrases) - 1

    # do teaching related stuff
    if teach:
        if last_user_phrase == -1:
            greetz.append(current_user_phrase)
        elif last_user_phrase == -2:
            learnt.append(current_user_phrase)
        else:
            pairs[last_user_phrase].append(current_user_phrase)
        last_user_phrase = -2

        # if verbose mode (chatting)
        if not no_output:
            if return_as_text:
                return returnRandomPhrase(learnt)
            else:
                showUpRandomPhrase(learnt)  # show message

    # do answering stuff
    else:
        last_user_phrase = current_user_phrase
        i = findBestFittingAnswer(current_user_phrase)
        if i != -1:
            if not no_output:  # if verbose mode (i.e. chatting)
                if return_as_text:
                    return returnRandomPhrase(pairs[i])
                else:
                    showUpRandomPhrase(pairs[i])

# loads current state from a file
# file name should be: <nickname>.txt
# if no such file found, nothing is loaded
# i.e. new host initialized


def loadProgress():
    global nickname
    global words
    global phrases
    global pairs
    global emotion
    global greetz
    global learnt

    try:
        with open(nickname + '.txt', 'r') as f:
            s = [i.rstrip() for i in list(f)]
            phrases = []
            pairs = []
            words = []
            emotion = []
            greetz = []
            learnt = []
            if s[0] != '':
                words = s[0].split(' ')
            if s[3] != '':
                emotion = s[3].split(' ')
            if s[1] != '':
                lph = s[1].split(';')
                lpa = s[2].split(';')
                for i in range(len(lph)):
                    phrases.append([])
                    pairs.append([])
                    if lph[i] != '':
                        phrases[i] = lph[i].split(' ')
                        phrases[i] = list(map(int, phrases[i]))
                    if lpa[i] != '':
                        pairs[i] = lpa[i].split(' ')
                        pairs[i] = list(map(int, pairs[i]))
            if s[4] != '':
                greetz = s[4].split(' ')
                greetz = list(map(int, greetz))
            if s[5] != '':
                learnt = s[5].split(' ')
                learnt = list(map(int, learnt))
            print(' (Info) File loaded.')
    except IOError:
        print(' (Warning) No host data file found.')

# saves current state to a file
# file name should be: <nickname>.txt
# rewrites file if it exists


def saveProgress():
    global nickname
    global words
    global phrases
    global pairs
    global emotion
    global greetz
    global learnt

    try:
        s = ' '.join(words) + '\n'
        s += ';'.join([(' '.join(list(map(str, p)))) for p in phrases]) + '\n'
        s += ';'.join([(' '.join(list(map(str, p)))) for p in pairs]) + '\n'
        s += ' '.join(emotion) + '\n'
        s += ' '.join(list(map(str, greetz))) + '\n'
        s += ' '.join(list(map(str, learnt))) + '\n'
        with open(nickname + '.txt', 'w') as f:
            f.write(s)
            print(' (Info) File saved.')
    except IOError:
        print(' (Error) Cannot save file!')

# parses log file with some long
# conversation between somebody
# where there's a syntax: <user phrase> => <bot answer> \n <user phrase...


def loadDialogA(fn):
    try:
        with open(fn, 'r') as f:
            print(' (Info) Accepted '+fn+', loading...')
            s = f.read().split('\n')
            s = [i.split('=>') for i in s]

            # for each pair of phrases
            for pair in s:
                # do full analysis, but with hidden outputs
                deflen = len(pair[0].strip())
                # overwork the chain of sentences
                for i in range(1, len(pair)):
                    if deflen > 0:
                        analyzePhrase(pair[0].strip(), True)
                    analyzePhrase('~'+pair[i].strip(), True)
            print(' (Info) Done loading.')
            showStats()  # print out statistics
    except IOError:
        print(' (Error) File read error. Check if the name is correct.')

# parse user commands
# each command begins with asterisk sign
# if no one command passes, phrase parser is launched


def parseCommands(cmd):
    if cmd == '*ex':
        exit()
    elif cmd == '*sv':
        saveProgress()
    elif cmd == '*ld':
        loadProgress()
    elif cmd == '*safex':
        saveProgress()
        exit()
    elif cmd == '*ldlg':
        dlgfnm = input('\n Dialog file name: ')
        loadDialogA(dlgfnm)
        print()
    elif cmd == '*stats':
        showStats()
    else:
        time.sleep(0.5)
        analyzePhrase(cmd, False)

# main entry point


def main():
    global nickname
    global user_nickname

    print('Kurisu-san 0.1alpha')
    print('Written by Tyoma Bondarenko in January 2014')
    print()
    nickname = input('Host nickname: ')
    loadProgress()
    showStats()
    user_nickname = input('Log in as: ')
    print()

    ohayogozaimasu()
    while True:
        sentence = input(' ' + user_nickname.ljust(10) + ' -> ')
        parseCommands(sentence)


if __name__ == "__main__":
    main()
