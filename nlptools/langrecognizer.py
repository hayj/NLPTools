
from langdetect import DetectorFactory
DetectorFactory.seed = 0
from langdetect import detect as detectLanguage, detect_langs as langProbs
from langdetect.lang_detect_exception import LangDetectException
from systemtools.logger import *
from datastructuretools.hashmap import *
from systemtools.basics import *
from systemtools.file import *
from systemtools.location import *
from datatools.url import *
from guess_language import guess_language


# TODO use cache singleton instead of class

# def langProbs(*args, **kwargs):
#     return detect_langs(*args, **kwargs)

def isEn(text, hard=True, **kwargs):
    if hard:
        langs = []
        for current in RECOGNIZER:
            langs.append(recognize(text, recognizer=current, **kwargs))
        for current in langs:
            if current != "en":
                return False
        return True
    else:
        return recognize(text, **kwargs) == "en"

RECOGNIZER = Enum("RECOGNIZER", "langdetect guess_language")
def recognize(text, logger=None, verbose=True, recognizer=RECOGNIZER.langdetect):
    if text is None or text == "":
        return None
    # And we detect the language:
    lang = None
    try:
        text = text.lower()
        text = removeUrls(text)
        if recognizer == RECOGNIZER.langdetect:
            lang = detectLanguage(text)
        elif recognizer == RECOGNIZER.guess_language:
            lang = guess_language(text)
        else:
            lang = detectLanguage(text)
    except Exception as e:
        if not isinstance(e, LangDetectException):
            logException(e, logger, verbose=verbose, location="getTweetTextLanguage")
    return lang

class LangRecognizer:
    """
        This class introduce a cache mecanism to the function recognize
        Because sometimes langdetect doesn't return the same lang for
        the same text, so we don't check the coherence (cacheCheckRatio=0.0)
        And you can use langdetect (through this class) safely with a upper cache.
        See TwitterScraper for example.
    """
    def __init__(self, logger=None, verbose=True):
        self.logger = logger
        self.verbose = verbose
        self.data = SerializableDict \
        (
#             "LangRecognizerCache",
#              dirPath=tmpDir(),
             funct=recognize,
             limit=1000000,
             cacheCheckRatio=0.0,
             raiseBadDesignException=False
        )
    def recognize(self, text):
        return self.data.get(text, logger=self.logger, verbose=self.verbose)

    def isEn(self, *args, **kwargs):
        return self.data.get(*args, **kwargs) == "en"



def guessLanguageTest():
    print(guess_language("Hello my"))
    print(guess_language("what is a dump?"))
    print(guess_language("Uncomfortable"))
    print(guess_language("been repulsed"))
    print(guess_language("Operation Ke was the largely successful withdrawal of Japanese forces from Guadalcanal in the Solomon Islands during World War II. All attempts by the Japanese army to recapture Henderson Field, the only airfield on the island being used by Allied aircraft, had"))
    print(guess_language("Allied forces"))
    print(guess_language("heavy loss"))
    print(guess_language("who won"))
    print(guess_language("municipalities"))

if __name__ == '__main__':
    guessLanguageTest()