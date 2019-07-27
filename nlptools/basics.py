
import re
from enum import Enum
from multiprocessing import Lock
from systemtools.duration import *
from systemtools.location import *
from systemtools.logger import *
from systemtools.file import *
from systemtools.basics import * # stripAccents, reduceBlank
from datatools.htmltools import *
from unidecode import unidecode
from nlptools.preprocessing import *
from nlptools.stopword import *
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np




def generateTFIDF(docs, logger=None, verbose=True, returnVoc=False, mode="vocabulary"):
    """
        If mode is vocabulary the function will return a scipy.sparse.csr.csr_matrix
        of shape (docs count, vocabulary size)
        Else if mode is tokens, the function will return a list of tfidf values (np.array)
        for each word in all docs (vectors will have the same length)
    """
    # We check inputs:
    assert docs is not None
    assert len(docs) > 1
    docs = copy.deepcopy(docs)
    if isinstance(docs[0][0], list):
        logWarning("You provided a list of sentences, we will flatten all docs.", logger, verbose=verbose)
        docs = flattenLists(docs)
    assert isinstance(docs[0][0], str)
    for doc in docs:
        assert len(doc) > 0
    # We init tools:
    def dummy_fun(doc):
        return doc
    tfidf = TfidfVectorizer(
        analyzer='word',
        tokenizer=dummy_fun,
        preprocessor=dummy_fun,
        token_pattern=None)
    # We generate tfidf vectors:
    tfidf.fit(docs)
    tfidfData = tfidf.transform(docs)
    # We log informations:
    log("tfidf data shape: " + str(tfidfData.shape), logger, verbose=verbose)
    log("tfidf voc len: " + str(len(tfidf.vocabulary_)), logger, verbose=verbose)
    # And finally we return all:
    if mode == "vocabulary":
        if returnVoc:
            return (tfidfData, tfidf.vocabulary_)
        else:
            return tfidfData
    else:
        tfidfScores = []
        pbar = ProgressBar(len(docs), verbose=verbose and (len(docs) > 1000), logger=logger, message="Building TFIDF tokens")
        for docId in range(len(docs)):
            # https://stackoverflow.com/questions/34449127/sklearn-tfidf-transformer-how-to-get-tf-idf-values-of-given-words-in-documen
            feature_index = tfidfData[docId,:].nonzero()[1]
            currentScores = np.array([tfidfData[docId, x] for x in feature_index])
            aaa = dict()
            for i in range(len(feature_index)):
                aaa[feature_index[i]] = currentScores[i]
            tokensTFIDF = []
            for word in docs[docId]:
                tokensTFIDF.append(aaa[tfidf.vocabulary_[word]])
            tfidfScores.append(tokensTFIDF)
            pbar.tic()
        if returnVoc:
            return (tfidfScores, tfidf.vocabulary_)
        else:
            return tfidfScores