from systemtools.basics import *
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.tokenize import TweetTokenizer
from enum import Enum
import spacy

"""
    Spay is the best tokenizer
"""
WORD_TOKENIZER = Enum("WORD_TOKENIZER", "nltk nltktwitter spacy")

twitterTokenizerSingleton = None
def wordTokenize(obj, wordTokenizer=WORD_TOKENIZER.spacy, logger=None, verbose=True):
    global twitterTokenizerSingleton
    if obj is None:
        return None
    elif isinstance(obj, str):
        if wordTokenizer == WORD_TOKENIZER.nltk:
            return word_tokenize(obj)
        elif wordTokenizer == WORD_TOKENIZER.nltktwitter:
            if twitterTokenizerSingleton is None:
                twitterTokenizerSingleton = TweetTokenizer()
            return twitterTokenizerSingleton.tokenize(obj)
        elif wordTokenizer == WORD_TOKENIZER.spacy:
            return spaCyTokenize(obj)
        else:
            logError("No tokenizer provided.", logger, verbose=verbose)
    elif isinstance(obj, list):
        return [wordTokenize(i) for i in obj]
    else:
        return obj # Or throw an exception, or parse a dict, a set...

def sentenceTokenize(obj, *args, logger=None, verbose=True, **kwargs):
    if obj is None:
        return None
    elif isinstance(obj, str):
        sentences = sent_tokenize(obj)
        for i in range(len(sentences)):
            sentences[i] = wordTokenize(sentences[i], *args, logger=logger, verbose=verbose, **kwargs)
        return sentences
    elif isinstance(obj, list):
        return [sentenceTokenize(i) for i in obj]
    else:
        return obj # Or throw an exception, or parse a dict, a set...


def tokenize(obj):
    print("DEPRECATED")
    if obj is None:
        return None
    elif isinstance(obj, str):
        return word_tokenize(obj)
    elif isinstance(obj, list):
        return [tokenize(i) for i in obj]
    else:
        return obj # Or throw an exception, or parse a dict, a set...


def spaCyTokenize(*args, **kwargs):
    return list(spaCyTokenizeYielder(*args, **kwargs))
spacyNlpForTokenizer = None
def spaCyTokenizeYielder(text):
    global spacyNlpForTokenizer
    if spacyNlpForTokenizer is None:
        spacyNlpForTokenizer = spacy.load('en_core_web_sm')
    doc = spacyNlpForTokenizer(text, disable=['parser', 'tagger', 'ner'])
    for token in doc:
        yield token.text


def test2():
    data = \
    [
        "jhg bfdguyjgfd fd gjd",
        [
            [
                ["ugtuyf", "vuhgvds"],
                None
            ],
            [
                [None],
                ["a", "b bdsf! id"]
            ],
        ],
        [
            [
                "jhsdg fjhdsg fgvsdk fksd ", None
            ],
            [
                "jhgsv defhgv sdufg uksdf jsd"
            ],
            "hjubvkujhv refgh. bvuljg ug udsfg li d. isdgf v . usdgf? sdvf ?"
        ],
    ]

    data = [["Lorem ipsum dolor. Sit amet?", "Hello World!", None], ["a"], "Hi!", None, ""]
    print(tokenize(data))


def test2():
    print(wordTokenize("Hello 'things' and ''tool'' my name is \"Abi\". I like this!"))


if __name__ == "__main__":
    test2()