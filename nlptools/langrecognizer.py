
from langdetect import detect as detectLanguage
from langdetect.lang_detect_exception import LangDetectException
from systemtools.logger import *
from datastructuretools.hashmap import *
from systemtools.basics import *
from systemtools.file import *
from systemtools.location import *


def recognize(text, logger=None, verbose=True):
    if text is None or text == "":
        return None
    # And we detect the language:
    lang = None
    try:
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
