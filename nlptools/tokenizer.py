from systemtools.basics import *
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.tokenize import TweetTokenizer
from enum import Enum
import spacy
from mosestokenizer import MosesDetokenizer
from nlptools.utils import *
import copy

"""
    Spacy is the best tokenizer
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
    print("DEPRECATED tokenize(obj)")
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
        # pew in st-venv python -m spacy download en
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



multiReplacerSingleton = None
# detokenizeSingleton = None
def detokenize(wordsOrSentences, joinSentences=True, logger=None, verbose=True):
    global multiReplacerSingleton
    wordsOrSentences = copy.deepcopy(wordsOrSentences)
    words = wordsOrSentences
    if multiReplacerSingleton is None:
        repls = \
        {
            # " ,": ",",
            # " .": ".",
            # " ?": "?",
            # " !": "!",
            # " )": ")",
            # "( ": "(",
            # " :": ":",
            # " '": "'",
            " n't": "n't",
        }
        multiReplacerSingleton = MultiReplacer(repls)
    with MosesDetokenizer('en') as detokenizeSingleton:
        def __detokenizeWords(words):
            text = detokenizeSingleton(words)
            text = multiReplacerSingleton.replace(text)
            return text
        if words is None or len(words) == 0:
            return ""
        if isinstance(words[0], list):
            sentences = words
            for i in range(len(sentences)):
                words = sentences[i]
                text = __detokenizeWords(words)
                sentences[i] = text
            if joinSentences:
                return "\n".join(sentences)
            else:
                return sentences
        elif isinstance(words[0], str):
            return __detokenizeWords(words)
        else:
            logError("words[0] must be either a list (so words are sentences)", logger, verbose=verbose)
            return None



# multiReplacerSingleton = None
# detokenizeSingleton = None
# def detokenize(wordsOrSentences, joinSentences=True, logger=None, verbose=True):
#     global detokenizeSingleton
#     wordsOrSentences = copy.deepcopy(wordsOrSentences)
#     words = wordsOrSentences
#     detokenizeSingleton = MosesDetokenizer('en')
#     if words is None or len(words) == 0:
#         return ""
#     if isinstance(words[0], list):
#         sentences = words
#         for i in range(len(sentences)):
#             words = sentences[i]
#             text = detokenizeSingleton(words)
#             sentences[i] = text
#         if joinSentences:
#             detokenizeSingleton.close()
#             return "\n".join(sentences)
#         else:
#             detokenizeSingleton.close()
#             return sentences
#     elif isinstance(words[0], str):
#         detokenizeSingleton.close()
#         return detokenizeSingleton(words)
#     else:
#         logError("words[0] must be either a list (so words are sentences)", logger, verbose=verbose)
#         detokenizeSingleton.close()
#         return None



def detokenizerTest():
    s1 = ["I", "am", "the", "thing", ",", "you", "did", "n't", "do", ".", "Yeah", "!"]
    s2 = ["I", "'m", "the", "(", "thing", ")", "you", ":", "did", "?"]
    sentences = [s1, s2]

    print(detokenize(s1))
    print("\n" * 2)
    print(detokenize(s2))
    print("\n" * 2)
    print(detokenize(sentences))
    


def test2():
    print(wordTokenize("Hello 'things' and ''tool'' my name is \"Abi\". I like this!"))



if __name__ == "__main__":
    detokenizerTest()