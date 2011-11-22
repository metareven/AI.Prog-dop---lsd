#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Lars
#
# Created:     21.11.2011
# Copyright:   (c) Lars 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
#The shit you need to get this to work can be found at http://osteele.com/projects/pywordnet/installation.html
from wordnet import *
from wntools import *

def main():
    print FindSynonyms("heater","Noun")

def FindSynonyms(word,wordType):
    if wordType == "Noun" and (N.has_key(word)):
        search = N[word]
    elif wordType == "Adjective" and (ADJ.has_key(word)):
        search = ADJ[word]
    elif wordType == "Verb" and (V.has_key(word)):
        search = V[word]
    elif wordType == "Adverb" and (ADV.has_key(word)):
        search = ADV[word]
    else:
        return [word]
    res = []
    for w in search:
        temp = str(w)
        temp = temp.split(":")
        temp = temp[1]
        temp = temp[0:len(temp)-1]
        temp = temp.split(", ")
        for t in temp:
            temp2 = t.strip()
            res.append(temp2)
    return res

main()