
import re
from enum import Enum
from multiprocessing import Lock
from systemtools.location import *
from systemtools.file import *
from systemtools.basics import *
from datatools.htmltools import *
from unidecode import unidecode


# TODOOOOOOOOOOOOOO faire en sorte de faire une class topwords pour gérer l'init et le lock ? une seul  ouverture de fichier contrirement à la



def isNotWord(token):
    # and word not in ['-lrb-', '-rrb-', '-lsb-', '-rsb-', '-lcb-', '-rcb-']
    if re.search('([a-z]|[A-Z]|[0-9])', token) is not None:
        return False
    else:
        return True

def removeNotWords(*args, **kwargs):
    return removeNotWord(*args, **kwargs)
def removeNotWord(tokens):
    newTokens = []
    for token in tokens:
        if not isNotWord(token):
            newTokens.append(token)
    return newTokens


STOPWORDS_LIST = Enum("STOPWORDS_LIST", "large small")
stopwordsSingleton = None
# stopwordsLock = Lock()
def initStopwordsList(stopwordsList=STOPWORDS_LIST.small):
    global stopwordsLock
    global stopwordsSingleton
    # with stopwordsLock: 
    if stopwordsSingleton is None:
        stopwordsSingleton = dict()
    if stopwordsList.name not in stopwordsSingleton:
        path = execDir(__file__) + "/data/stopwords/stopwords-" + stopwordsList.name + ".txt"
        stopwordsSingleton[stopwordsList.name] = set(fileToStrList(path))
def removeStopWords(*args, **kwargs):
    return removeStopwords(*args, **kwargs)
def removeStopwords(tokens, stopwordsList=STOPWORDS_LIST.small):
    global stopwordsLock
    global stopwordsSingleton
    initStopwordsList(stopwordsList=stopwordsList)
    newTokens = []
    for token in tokens:
        if token not in stopwordsSingleton[stopwordsList.name]:
            newTokens.append(token)
    return newTokens
def removeStopwordsLarge(tokens):
    return removeStopwords(tokens, stopwordsList=STOPWORDS_LIST.large)

