import networkx as nx
import random
import sys
import time

def progress(D, letter, seq):
    if letter not in D:
        return
    next = D[letter]
    flatlist = dict()
    for endletter in D[letter]:
        for order in D[letter][endletter]:
            flatlist[D[letter][endletter][order]["word"]] = endletter, order
    wordcol = [word for word in flatlist]
    if len(wordcol) == 0:
        yield seq
    random.shuffle(wordcol)
    for word in wordcol:
        next, order = flatlist[word]
        D.remove_edge(letter, next, order)
        yield from progress(D, next, seq+[word])
        D.add_edge(letter, next, key=order, word=word)


with open(sys.argv[1]) as f:
    words = [word.strip() for word in f.readlines() if word[0] != "#"]

# remove simgle letter word and make a list of the first letter
words = [word for word in words if len(word)>1]
letters = list(set([word[0] for word in words]))
random.shuffle(letters)
print(f"Number of words in the dictionary: {len(words)}")
time.sleep(2)

D = nx.MultiDiGraph()
for word in words:
    if len(word) <= 1:
        continue
    if "." in word:
        continue
    head = word[0]
    tail = word[-1]
    D.add_edge(head,tail, word=word)

maxseq = []
for letter in letters:
    print(letter)
    for seq in progress(D, letter, []):
        if len(seq) > len(maxseq):
            maxseq = seq
            print(len(maxseq), maxseq)
