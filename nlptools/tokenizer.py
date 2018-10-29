from systemtools.basics import *
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.tokenize import TweetTokenizer
from enum import Enum

WORD_TOKENIZER = Enum("WORD_TOKENIZER", "nltk nltktwitter")

twitterTokenizerSingleton = None
def wordTokenize(obj, wordTokenizer=WORD_TOKENIZER.nltk, logger=None, verbose=True):
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




if __name__ == "__main__":
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