from pdb import set_trace
from random import choice
from string import ascii_lowercase
from collections import defaultdict
import requests
import json

with open('words') as f:
    words = f.read().split('\n')[:-1]

def wordle():
    sol = choice(words)
    #sol = 'locie'

    def fn(guess):
        if sol == guess:
            return True

        out = ''
        for c1, c2 in zip(sol, guess):
            if c1 == c2:
                out += 'g'
            elif c2 in sol:
                out += 'y'
            else:
                out += '.'

        return out

    for i in range(6):
        yield fn, sol

uniq = [a for a in words if len(set(a)) == 5]

set_trace()

#['cimex', 'grypt', 'waqfs', 'blunk', 'vozhd']
guesses = ['gymps', 'chunk', 'waltz', 'vibex', 'fjord']
guesses = ['mould', 'night', 'spear']

def get_words(words, word):
    return [a for a in words if all([c not in a for c in word])]

ss = requests.Session()

set_trace()

res = ss.get('https://wordle.ctf.bsidestlv.com/')

for _ in range(100):
    print(f'Trial: {_}')
    gg = {}
    yy = defaultdict(lambda: [])
    used = set([])
    solved = False

    for i in range(6):
        if i < 3:
            #fn, sol = next(game)

            guess = guesses[i]

            for ch in guess: used.add(ch)

            #res = fn(guess)

            #set_trace()
            res = ss.post('https://wordle.ctf.bsidestlv.com/step', headers={"Content-Type": "application/json"}, json={'guess': guess.upper()})

            print(res.text)

            res = json.loads(res.text)['result'] 

            if res == True:
                print(f'Success in {i} tries')
            else:
                for j, ch in enumerate(res):
                    if ch == 'g': gg[j] = guess[j]
                    elif ch == 'y': yy[guess[j]].append(j)

            continue

        cands = [(a, len(set(a) & used)) for a in words if all([a[i] == gg[i] for i in gg]) and all([x in a for x in yy])]

        cands2 = []

        for cand, cc in cands:
            for ch in yy:
                if any([cand[idx] == ch for idx in yy[ch]]): break 
            else: 
                cands2.append((cand, cc))


        guess = sorted(cands2, key=lambda a: a[1])[0][0]

        for ch in guess: used.add(ch)

        #fn, sol = next(game)

        #set_trace()
        #res = fn(guess)

        res = ss.post('https://wordle.ctf.bsidestlv.com/step', headers={"Content-Type": "application/json"}, json={'guess': guess.upper()})

        print(res.text)

        res = json.loads(res.text)
        
        if res['status'] == 'win':
            #exit()
            solved = True
            break
        else:
            res = res['result']
            for j, ch in enumerate(res):
                if ch == 'g': gg[j] = guess[j]
                elif ch == 'y': yy[guess[j]].append(j)


    if not solved:
        print('Fail')
        #print(f'Fail {sol}')
    else:
        print('Sucess')
        #print(f'Success in {i} tries: {sol}')

exit()

def rec(words, word, sol=[], level=0):
    if level == 3:
        pass
        #print(sol + [word])
        #set_trace()


    if level == 4:
        set_trace()
        unused = set(ascii_lowercase) - set(''.join(sol + [word]))
    
    next_words = get_words(words, word)

    for next_word in next_words:
        rec(next_words, next_word, sol=sol + [word], level=level + 1)

ln = len(uniq)

uniq = uniq[uniq.index('gymps') + 1:]

for word in uniq:
    print(ln)
    ln -= 1
    sol = []
    rec(uniq, word, sol)
