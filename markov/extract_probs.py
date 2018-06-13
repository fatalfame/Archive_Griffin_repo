import pickle
import numpy as np
import re

#text files to extract probabilities from
#filepath = "data/kjv_bible.txt"
filepath = '..//markov/depechedad.txt'

f = open(filepath,"r")
lines = f.readlines()
f.close()

print("Read in "+str(filepath))
print("Lines = "+str(len(lines)))

#destroy leading spaces
def destroyLeadingSpaces(s):
    i = 0
    while s[i] == " ":
        i += 1
    return s[i:]

#destroy final \n
def destroyNewLine(s):
    if s[-1] == "\n":
        return s[:-1]+" "
    else:
        return s

def destroyCharacters(s,toExclude): return [c for c in s if c not in toExclude]

def destroyCharactersApartFrom(s,toKeep): return [c for c in s if c in toKeep]

def removeMultipleSpaces(line):
    new_line = []
    space = False
    for x in list(line):
        if ((x == " ") and (space == False)):
            new_line.append(x)
            space = True
        elif (x != " "):
            new_line.append(x)
            space = False
    return new_line

maxorder = 10 #maximal order of Markov chain counts to extract (order == 1 => looks at 1 previous character)
orders = range(1,maxorder+1) #orders to generate files for
for order in orders:
    print("Markov order = "+str(order))

    #count dictionary
    counts = {} #dictionary of dictionaries of counts

    for j,line in enumerate(lines):

        if (j+1) % 10000 == 0: #progress
            print(j+1,"/",len(lines))

        #cleaing the line
        line = line.lower() #lower case
        line = destroyLeadingSpaces(line) #destroys leading spaces
        line = destroyNewLine(line) #destroys \n at the end

        toKeep_english = " abcdefghijklmnopqrstuvwxyz"
        #toKeep_czech = " aábcčdďeéěfghiíjklmnoópqrřsštťuůúvwxyýzž"

        line = destroyCharactersApartFrom(line,toKeep_english)
        line = removeMultipleSpaces(line) #removing duplicite spaces

        chars = list(line)

        for i in range(len(chars)-order):

            key_history = tuple(chars[i:i+order])
            key_current = chars[i+order]
            if key_history in counts:
                if key_current in counts[key_history]:
                    (counts[key_history])[key_current] += 1
                else:
                    (counts[key_history])[key_current] = 1
            else:
                counts[key_history] = {}
                (counts[key_history])[key_current] = 1

    print("Done loading order "+str(order)+".")

    #storing results for generation
    with open(filepath+"_order_"+str(order)+".pickle", 'wb') as fp:  # Python 3: open(..., 'wb')
        pickle.dump(counts, fp)
        fp.close()
