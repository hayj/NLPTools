
import re
from enum import Enum
from multiprocessing import Lock
from systemtools.duration import *
from systemtools.location import *
from systemtools.printer import *
from systemtools.logger import * 
from systemtools.file import *
from systemtools.basics import * # stripAccents, reduceBlank
from datatools.htmltools import *
from unidecode import unidecode
from nlptools.preprocessing import *
from nlptools.stopword import *
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import scipy
import numpy as np
import textstat

# textstatInstalledSingleton = None
def stylo\
(
    document,
    asNpArray=False,
    allowedFunctions=\
    [
        'automated_readability_index',
        'avg_character_per_word',
        'avg_letter_per_word',
        'avg_sentence_length',
        'avg_sentence_per_word',
        'char_count',
        'coleman_liau_index',
        'letter_count',
        'lexicon_count',
        'lix',
        'reading_time',
        'rix',
        'sentence_count',
        'smog_index',
        'spache_readability',
        'dale_chall_readability_score',
        'dale_chall_readability_score_v2',
        'difficult_words',
        'gunning_fog',
    ],
    logger=None, verbose=True,
):
    # global textstatInstalledSingleton
    # if textstatInstalledSingleton:
    #     import textstat
    # else:
    #     try:
    #         import textstat
    #     except:
    #         path = strToTmpFile("-e git://github.com/shivam5992/textstat.git#egg=textstat")
    #         bash("pip install -r " + path)
    #         import textstat
    #     textstatInstalledSingleton = True
    features = []
    for name in allowedFunctions:
        try:
            funct = textstat.__dict__[name]
            feature = funct(document)
            assert isinstance(feature, int) or isinstance(feature, float)
            feature = float(feature)
            features.append(feature)
        except Exception as e:
            features.append(0.0)
    if asNpArray:
        return np.array(features)
    else:
        return features


def toNgrams\
(
    docs,
    mode="document",
    ngrams=1,
    doLower=False,
    flattenSentences=False,
    logger=None,
    verbose=True,
):
    """
        This function convert a list of docs (a document can be composed of sentences (list) or words (str))
        The returned object has the same shape of the input docs object, but if you set flattenSentences as True, all sentences will be flattened. 
    """
    assert docs is not None and len(docs) > 0 and len(docs[0]) > 0
    if isinstance(docs[0][0], list):
        sentencesCorpus = True
    else:
        sentencesCorpus = False
    if not sentencesCorpus and flattenSentences:
        raise Exception("You give documents that are not composed of sentences but you set flattenSentences as True")
    if sentencesCorpus:
        if ngrams > 1 and not flattenSentences:
            logWarning("You gave a corpus of sentences but you set ngrams > 1 and flattenSentences as False, you won't get ngrams riding on 2 sentences...", logger, verbose=verbose)
        if flattenSentences:
            docs = [flattenLists(doc) for doc in docs]
    if not doLower:
        logWarning("You set doLower as False", logger=logger, verbose=verbose)
    ngramss = []
    # bp(docs, 5)
    for sentences in pb(docs, logger=logger, verbose=verbose and len(docs) > 20, message="Extracting " + str(ngrams) + "-grams"):
        if not sentencesCorpus or flattenSentences:
            sentences = [sentences]
        sentencesNgrams = []
        # bp(sentences, 5)
        for sentence in sentences:
            # bp(sentence, 5)
            if sentence is None:
                raise Exception("Found None in docs")
            elif len(sentence) == 0:
                logWarning("Found an empty doc", logger, verbose=verbose)
            elif not isinstance(sentence[0], str):
                raise Exception("Found a word that is not a str")
            else:
                if len(sentence) >= ngrams:
                    grams = []
                    for i in range(len(sentence) - ngrams + 1):
                        ngram = " ".join(sentence[i:i + ngrams])
                        if doLower:
                            ngram = ngram.lower()
                        grams.append(ngram)
                    sentencesNgrams.append(grams)
                else:
                    sentencesNgrams.append([])
        # if len(sentencesNgrams) > 0:
        if not sentencesCorpus or flattenSentences:
            ngramss.append(sentencesNgrams[0])
        else:
            ngramss.append(sentencesNgrams)
    return ngramss


def extractNgrams\
(
    docs,
    ngrams=1,
    minDF=1,
    doLower=False,
    returnDF=False,
    useTuple=False,
    flattenSentences=False,
    logger=None,
    verbose=True
):
    """
        You must give a list of documents. A document is either a list of words (str) or a liste of sentences (list).
        This function extract the vocab of a corpus (i.e. set of ngrams).
    """
    assert docs is not None and len(docs) > 0 and len(docs[0]) > 0
    if isinstance(docs[0][0], list):
        sentencesCorpus = True
    else:
        sentencesCorpus = False
    if not sentencesCorpus and flattenSentences:
        raise Exception("You give documents that are not composed of sentences but you set flattenSentences as True")
    if sentencesCorpus:
        if ngrams > 1 and not flattenSentences:
            logWarning("You gave a corpus of sentences but you set ngrams > 1 and flattenSentences as False, you won't get ngrams riding on 2 sentences...", logger, verbose=verbose)
        if flattenSentences:
            docs = [flattenLists(doc) for doc in docs]
        else:
            docs = flattenLists(docs)
    if not doLower:
        logWarning("You set doLower as False", logger=logger, verbose=verbose)
    vocDF = dict()
    for doc in pb(docs, logger=logger, verbose=verbose and len(docs) > 20, message="Extracting " + str(ngrams) + "-grams"):
        if doc is None:
            logWarning("Found None in docs", logger, verbose=verbose)
        elif len(doc) == 0:
            logWarning("Found an empty doc", logger, verbose=verbose)
        elif not isinstance(doc[0], str):
            raise Exception("Found a word that is not a str")
        else:
            if len(doc) >= ngrams:
                alreadySeenInThisDoc = set()
                for i in range(len(doc) - ngrams + 1):
                    if useTuple:
                        ngram = tuple(doc[i:i + ngrams])
                    else:
                        ngram = " ".join(doc[i:i + ngrams])
                    if doLower:
                        if useTuple:
                            ngram = tuple([e.lower() for e in ngram])
                        else:
                            ngram = ngram.lower()
                    if ngram not in vocDF:
                        vocDF[ngram] = 1
                    elif ngram not in alreadySeenInThisDoc:
                        vocDF[ngram] += 1
                    alreadySeenInThisDoc.add(ngram)
    ngramsToDelete = set()
    for ngram, count in vocDF.items():
        if count < minDF:
            ngramsToDelete.add(ngram)
    for ngram in ngramsToDelete:
        del vocDF[ngram]
    if returnDF:
        return vocDF
    else:
        return set(vocDF.keys())

def generateTFIDF(docs, minDF=1, sublinearTF=True, ngramRange=(1, 1), doLower=False, logger=None, verbose=True):
    tt = TicToc(logger=logger, verbose=verbose)
    tt.tic()
    if doLower:
        docs = copy.deepcopy(docs)
        tt.tic("Docs copied")
        warnFreeRAM(logger=logger, verbose=verbose)
        for doc in docs:
            for i in range(len(doc)):
                doc[i] = doc[i].lower()
        tt.tic("Words lowered")
    tfidf = TfidfVectorizer\
    (
        analyzer='word',
        tokenizer=lambda x: x,
        preprocessor=lambda x: x,
        token_pattern=None,
        # lowercase=True, # Doesn't work because we erased preprocessor
        ngram_range=ngramRange,
        sublinear_tf=sublinearTF,
        min_df=minDF,
    )
    # We generate tfidf vectors:
    log("Computing TFIDF...", logger, verbose=verbose)
    tfidf.fit(docs)
    tt.tic("TFIDF computed")
    warnFreeRAM(logger=logger, verbose=verbose)
    tfidfMatrix = tfidf.transform(docs)
    tt.tic("TFIDF matrix generated")
    warnFreeRAM(logger=logger, verbose=verbose)
    # We log informations:
    log("TFIDF data shape: " + str(tfidfMatrix.shape), logger, verbose=verbose)
    log("TFIDF voc len: " + str(len(tfidf.vocabulary_)), logger, verbose=verbose)
    tt.toc("TFIDF computation done")
    return (tfidf, tfidfMatrix)

def flattenedIndexes(sentences, ngrams=1, doLower=False, returnFlattenedDoc=False, logger=None, verbose=True):
    """
        This function convert a document composed of sentences in a list of indexes.

        For example:

        >>> (ngramIndexes, grams) = flattenedIndexes([['a', 'b'], ['c'], ['d']], ngrams=2, returnFlattenedDoc=True)
        >>> ngramIndexes
        [{0}, {0, 1}, {1, 2}]
        >>> grams
        ['a b', 'b c', 'c d']

        The 2-grams 'a b' is only in the first sentence but the 2-grams 'b c' is in the first sentence and the second sentence.
    """
    if not doLower:
        logWarning("You set doLower as False", logger=logger, verbose=verbose)
    if sentences is None or len(sentences) == 0:
        if returnFlattenedDoc:
            return ([], [])
        else:
            return []
    assert isinstance(sentences[0], list) and isinstance(sentences[0][0], str)
    # First we get sentence indexes of each word:
    indexes = []
    currentIndex = 0
    for sentence in sentences:
        for word in sentence:
            indexes.append(currentIndex)
        currentIndex += 1
    # Then we get ngrams:
    grams = toNgrams\
    (
        [sentences],
        ngrams=ngrams,
        flattenSentences=True,
        doLower=doLower,
        logger=logger,
        verbose=verbose,
    )[0]
    # And we calculate indexes:
    ngramIndexes = []
    gramIndex = 0
    for gram in grams:
        ngramIndexes.append(set())
        for i in range(ngrams):
            try:
                ngramIndexes[gramIndex].add(indexes[gramIndex + i])
            except Exception as e:
                logException(e, logger=logger, verbose=verbose)
        gramIndex += 1
    if returnFlattenedDoc:
        return (ngramIndexes, grams)
    else:
        return ngramIndexes

class TFIDF:
    def __init__\
    (
        self,
        docs,
        doLower=True,
        sublinearTF=True,
        ngramRange=(1, 1),
        minDF=1,
        cumhistoIntervalsSize=1000,
        logger=None,
        verbose=True,
    ):
    """
        This class is a wrapper of `sklearn.feature_extraction.text.TfidfVectorizer`. It takes documents and generates TFIDF vectors of a given ngrams range. It handle either already tokenized docs for words or already tokenized docs for sentences and words. You can automatically access useful data such as specific TFIDF values using `TFIDFValue(docId, ngram)`, filter sentences that have a high max TFIDF value given a deletion ratio using `removeSentences(deletionRatio)` and so on. 
    """
        # All vars:
        self.logger = logger
        self.verbose = verbose
        self.minDF = minDF
        self.ngramRange = ngramRange
        self.sublinearTF = sublinearTF
        self.doLower = doLower
        self.cumhistoIntervalsSize = cumhistoIntervalsSize

        # Computed vars:
        self.tops = None
        self.voc = None
        self.vocIndexes = None
        self.tfidf = None
        self.tfidfMatrix = None
        self.tfidfVectors = None
        self.tfidfMap = None
        self.maxTFIDFs = None
        self.cumhisto = None
        self.cumhistoIntervals = None

        # We keep sentences in memory:
        if isinstance(docs[0][0], list):
            self.sentencesCorpus = True
        else:
            self.sentencesCorpus = False
        if self.sentencesCorpus:
            self.docsSentences = docs
        else:
            self.docsSentences = None

        # We handle docs:
        assert docs is not None
        assert len(docs) > 1
        if isinstance(docs[0][0], list):
            logWarning("You provided a list of sentences, we flatten all docs.", self)
            # docs = flattenLists(docs)
            docs = [flattenLists(doc) for doc in docs]
        assert isinstance(docs[0][0], str)
        for doc in docs:
            assert len(doc) > 0
            assert isinstance(doc[0], str)
        self.docs = docs

        # We generate TFIDF:
        self.__generate()

    def __generate(self):
        # We get tfidf:
        (self.tfidf, self.tfidfMatrix) = generateTFIDF\
        (
            self.docs,
            minDF=self.minDF,
            sublinearTF=self.sublinearTF,
            ngramRange=self.ngramRange,
            doLower=self.doLower,
            logger=self.logger,
            verbose=self.verbose
        )
        self.vocIndexes = self.tfidf.vocabulary_
        self.getVoc()

    def getTFIDFMatrix(self):
        """
            Return the matrix docs vocabulary with all TFIDF values, a scipy.sparse.csr.csr_matrix of shape (docs count, vocabulary size)
        """
        return self.tfidfMatrix


    def getTFIDFVectors(self, ngrams=1):
        """
            Return docs with TFIDF values instead of tokens
        """
        if ngrams != 1:
            raise Exception("ngrams > 1 not yet implemented")
        if self.tfidfVectors is None:
            tfidfScores = []
            pbar = ProgressBar(len(self.docs), verbose=self.verbose and (len(self.docs) > 1000), logger=self.logger, message="Building TFIDF tokens")
            for docId in range(len(self.docs)):
                # https://stackoverflow.com/questions/34449127/sklearn-tfidf-transformer-how-to-get-tf-idf-values-of-given-words-in-documen
                feature_index = self.tfidfMatrix[docId,:].nonzero()[1]
                currentScores = np.array([self.tfidfMatrix[docId, x] for x in feature_index])
                aaa = dict()
                for i in range(len(feature_index)):
                    aaa[feature_index[i]] = currentScores[i]
                tokensTFIDF = []
                for word in self.docs[docId]:
                    if self.doLower:
                        word = word.lower()
                    tokensTFIDF.append(aaa[self.vocIndexes[word]])
                tfidfScores.append(tokensTFIDF)
                pbar.tic()
            self.tfidfVectors = tfidfScores
        return self.tfidfVectors

    def getVoc(self):
        """
            Return the list of ngrams
        """
        if self.voc is None:
            self.voc = [None] * len(self.vocIndexes)
            for word, index in self.vocIndexes.items():
                self.voc[index] = word
        return self.voc

    def getVocIndexes(self):
        """
            Return a mapping voc -> index
        """
        return self.vocIndexes

    def getTFIDFMap(self):
        """
            Return a list docId -> (dict of ngram -> tfidf value)
        """
        if self.tfidfMap is None:
            self.tfidfMap = []
            for i in range(self.tfidfMatrix.shape[0]):
                self.tfidfMap.append(dict())
            cx = scipy.sparse.coo_matrix(self.tfidfMatrix)
            pbar = ProgressBar(self.tfidfMatrix.shape[0], logger=self.logger, verbose=self.verbose, message="Collecting TFIDF values")
            alreadySeenDocs = set()
            for docId, vocId, tfidfValue in zip(cx.row, cx.col, cx.data):
                ngram = self.voc[vocId]
                ngrams = ngram.count(" ") + 1
                self.tfidfMap[docId][ngram] = tfidfValue
                if docId not in alreadySeenDocs:
                    pbar.tic()
                    alreadySeenDocs.add(docId)
        return self.tfidfMap

    def getTFIDFValue(self, docId, ngram):
        """
            Return the TFIDF value of a ngram in a specific doc
        """
        valuesDict = self.getTFIDFMap()[docId]
        if ngram not in valuesDict:
            logError('"' + ngram + '"' + " not in doc " + str(docId), self)
            return 0.0
        else:
            return valuesDict[ngram]
            
    def getTops(self):
        """
            This method takes tfidfMatrix a sparse matric (from `generateTFIDF`).
            It takes voc a list of ngrams corresponding to tfidfMatrix columns.
            It return top ngrams (according to there tfidf values) for each doc looking:
            [
              {
                1: [ sunye, bosu, ..., jan., ryan ],
                2: [ sarah bean, master jay, ..., and former, added . ],
                <ngrams>: [ <word>, <word>, ..., <word>, <word> ]
              },
              <doc>,
              ...,
              {
                1: [ hu, candid, ..., of, is ],
                2: [ private talks, with hu, ..., to a, in a ],
                3: [ worshipped at a, with some olympic, ..., , he said, as well as ]
              }
            ]
        """
        if self.tops is None:
            self.getVoc()
            self.tops = []
            for i in range(self.tfidfMatrix.shape[0]):
                grams = {1: [], 2: [], 3: []}
                self.tops.append(grams)
            cx = scipy.sparse.coo_matrix(self.tfidfMatrix)
            pbar = ProgressBar(self.tfidfMatrix.shape[0], logger=self.logger, verbose=self.verbose, message="Collecting TFIDF values")
            alreadySeenDocs = set()
            for docId, vocId, tfidfValue in zip(cx.row, cx.col, cx.data):
                ngram = self.voc[vocId]
                ngrams = ngram.count(" ") + 1
                self.tops[docId][ngrams].append((ngram, tfidfValue))
                if docId not in alreadySeenDocs:
                    pbar.tic()
                    alreadySeenDocs.add(docId)
            for i in pb(list(range(len(self.tops))), logger=self.logger, verbose=self.verbose, message="Sorting ngrams by TFIDF values"):
                for u in self.tops[i].keys():
                    self.tops[i][u] = [e[0] for e in sorted(self.tops[i][u], key=lambda x: x[1], reverse=True)]
        return self.tops

    def getMaxTFIDFsPerSentence(self):
        """
            To use this function, you must give a corpus of docs composed of sentences at the init step.
            This function return a structure looking:
            [
                <doc 0>,
                {
                    <ngrams>: [<max tfidf value of sentence 0>, <max tfidf value of sentence 1>, <...>],
                    2: [0.2, 0.1],
                    <...>,
                },
                <...>,
            ]
        """
        assert self.sentencesCorpus
        if self.maxTFIDFs is None:
            self.getTFIDFMap()
            self.maxTFIDFs = []
            maxNgrams = self.ngramRange[1]
            docId = 0
            for doc in pb(self.docsSentences, logger=self.logger, verbose=self.verbose, message="Collecting max TFIDF value per sentence"):
                perNgrams = dict()
                for ngrams in range(1, maxNgrams + 1):
                    (sentenceIndexes, flattenedSentences) = flattenedIndexes(doc, doLower=self.doLower, ngrams=ngrams, returnFlattenedDoc=True)
                    allMax = [-1] * len(doc)
                    for i in range(len(flattenedSentences)):
                        sentenceHit = sentenceIndexes[i]
                        ngram = flattenedSentences[i]
                        for hit in sentenceHit:
                            value = self.getTFIDFValue(docId, ngram)
                            if value > allMax[hit]:
                                allMax[hit] = value
                    perNgrams[ngrams] = allMax
                self.maxTFIDFs.append(perNgrams)
                docId += 1
        return self.maxTFIDFs

    def getCumhistoIntervals(self):
        if self.cumhistoIntervals is None:
            self.getCumhisto()
        return self.cumhistoIntervals

    def getCumhisto(self):
        """
            This method return the cumulative histogram of tfidf values.
            Example of structure:
            {
              <ngrams>: [<count of sentences so that the max TFIDF is higher than this value in self.cumhistoIntervals>, <...>]
              '2': [ 39600, 39600, 35000, ..., 84, 2, 2, 0, 0, 0, 0, 0, 0, 0 ],
            }
        """
        if self.cumhisto is None:
            tt = TicToc(logger=self.logger, verbose=self.verbose)
            tt.tic()
            maxTFIDFs = self.getMaxTFIDFsPerSentence()
            maxNgrams = len(maxTFIDFs[0])
            intervalsSize = self.cumhistoIntervalsSize
            # We calculate intervals:
            minis, maxis = dict(), dict()
            for ngrams in range(1, maxNgrams + 1):
                if ngrams not in minis:
                    minis[ngrams] = None
                if ngrams not in maxis:
                    maxis[ngrams] = None
                for doc in maxTFIDFs:
                    currentMin = min(doc[ngrams])
                    if minis[ngrams] is None or currentMin < minis[ngrams]:
                        minis[ngrams] = currentMin
                    currentMax = max(doc[ngrams])
                    if maxis[ngrams] is None or currentMax > maxis[ngrams]:
                        maxis[ngrams] = currentMax
            tt.tic("We got min and max TFIDF values")
            intervals = dict()
            for ngrams in range(1, maxNgrams + 1):
                mini = minis[ngrams]
                maxi = maxis[ngrams]
                epsilon = 0.01 * (maxi - mini)
                mini = mini - epsilon
                maxi = maxi + epsilon
                jump = (maxi - mini) / intervalsSize
                intervals[ngrams] = list(np.arange(mini, maxi, jump))
            # We make cumulative histograms:
            cumhisto = dict()
            for ngrams in range(1, maxNgrams + 1):
                currentIntervals = intervals[ngrams]
                if ngrams not in cumhisto:
                    cumhisto[ngrams] = [0] * len(currentIntervals)
                for currentMaxTFIDFs in maxTFIDFs:
                    currentMaxTFIDFs = currentMaxTFIDFs[ngrams]
                    for value in currentMaxTFIDFs:
                        for i in range(len(currentIntervals)):
                            if value > currentIntervals[i]:
                                cumhisto[ngrams][i] += 1
            tt.tic("We calculated the cumulative histogram of tfidf values")
            self.cumhisto = cumhisto
            self.cumhistoIntervals = intervals
        return self.cumhisto

    def getBlackNgrams(self, deletionRatio, *args, **kwargs):
        """
            Return a black list of ngrams for each document
            The black list  is calculate according a ratio of deletion of all sentences in the cirpus 
            Each ngram in the black list is an indicator when chossing to delete or not a sentence in the corpus
            The structure looks like:
            [
                <list of ngrams for doc 1>,
                [<ngram 1>, <ngram 2>, ...],
                ...
            ]
        """
        maxTFIDFs = self.getMaxTFIDFsPerSentence()
        cumhisto = self.getCumhisto()
        tfidfThresholds = getOptimalTFIDFThresholds\
        (
            maxTFIDFs, cumhisto, deletionRatio, self.getCumhistoIntervals(),
            *args, logger=self.logger, verbose=self.verbose, **kwargs
        )
        blackNgrams = []
        maxNgrams = len(maxTFIDFs[0])
        for docId in pb(list(range(len(maxTFIDFs))),
                        logger=self.logger, verbose=self.verbose,
                        message="Collecting ngrams TFIDF black list for threshold " + str(tfidfThresholds)):
            blackNgrams.append(set())
            voc = self.getTFIDFMap()[docId]
            for ngram in voc:
                ngrams = ngram.count(" ") + 1
                theshold = tfidfThresholds[ngrams]
                currentTFIDF = self.getTFIDFValue(docId, ngram)
                if currentTFIDF >= theshold:
                    blackNgrams[docId].add(ngram)
        return blackNgrams

    def removeSentences(self, deletionRatio, *args, **kwargs):
        assert self.sentencesCorpus
        maxTFIDFs = self.getMaxTFIDFsPerSentence()
        cumhisto = self.getCumhisto()
        intervals = self.getCumhistoIntervals()
        tfidfThresholds = getOptimalTFIDFThresholds(maxTFIDFs, cumhisto, deletionRatio, intervals,
                *args, logger=self.logger, verbose=self.verbose, **kwargs)
        newDocs = []
        maxNgrams = len(maxTFIDFs[0])
        for docId in range(len(maxTFIDFs)):
            newsSentences = []
            for sentenceId in range(len(maxTFIDFs[docId][list(maxTFIDFs[docId].keys())[0]])):
                foundHigher = False
                for ngrams in range(1, maxNgrams + 1):
                    if maxTFIDFs[docId][ngrams][sentenceId] > tfidfThresholds[ngrams]:
                        foundHigher = True
                        break
                if not foundHigher:
                    newsSentences.append(self.docsSentences[docId][sentenceId])
            newDocs.append(newsSentences)
        return newDocs


def estimateDeletion(maxTFIDFs, cumhisto, deletionRatio, intervals, logger=None, verbose=True):
    """
        This function calculate how final deletion ratio which will be higher in case we handle multiple ngrams...
    """
    tfidfThresholds = dict()
    maxNgrams = len(maxTFIDFs[0])
    for ngrams in range(1, maxNgrams + 1):
        countThreshold = deletionRatio * cumhisto[ngrams][0]
        for i in range(len(cumhisto[ngrams])):
            if cumhisto[ngrams][i] < countThreshold:
                break
        tfidfThresholds[ngrams] = intervals[ngrams][i]
    sentencesToRemove = []
    for docId in range(len(maxTFIDFs)):
        currentSentencesToRemove = set()
        currentMaxTFIDFs = maxTFIDFs[docId]
        for ngrams in range(1, maxNgrams + 1):
            for sentenceId in range(len(currentMaxTFIDFs[ngrams])):
                if currentMaxTFIDFs[ngrams][sentenceId] >= tfidfThresholds[ngrams]:
                    currentSentencesToRemove.add(sentenceId)
        sentencesToRemove.append(currentSentencesToRemove)
    deletedCount = 0
    totalCount = 0
    for docId in range(len(maxTFIDFs)):
        currentSentencesToRemove = sentencesToRemove[docId]
        newDoc = []
        for sentenceId in range(len(maxTFIDFs[docId][list(maxTFIDFs[docId].keys())[0]])):
            if sentenceId in currentSentencesToRemove:
                deletedCount += 1
            totalCount += 1
    # log("We delete " + str(int(deletedCount / totalCount * 100)) + "% of sentences", logger=logger, verbose=verbose)
    # print(tfidfThresholds)
    return deletedCount / totalCount


def estimateOptimalDeletionRatio(maxTFIDFs, cumhisto, targetDeletionRatio, intervals, *args,
                                 minimumDichotomicMove=0.000001,
                                 logger=None, verbose=True, **kwargs):
    deletionRatio = targetDeletionRatio
    move = targetDeletionRatio / 2
    while move > minimumDichotomicMove:
        computedDeletionRatio = estimateDeletion(maxTFIDFs, cumhisto, deletionRatio, intervals,
                                    *args, logger=logger, verbose=verbose, **kwargs)
        if computedDeletionRatio < targetDeletionRatio:
            deletionRatio = deletionRatio + move
        else:
            deletionRatio = deletionRatio - move
        move = move / 2
    return deletionRatio

def getOptimalTFIDFThresholds(maxTFIDFs, cumhisto, targetDeletionRatio, intervals,
                              *args, logger=None, verbose=True, **kwargs):
    optimalDeletionRatio = estimateOptimalDeletionRatio(maxTFIDFs, cumhisto, targetDeletionRatio, intervals, *args, logger=logger, verbose=verbose, **kwargs)
    tfidfThresholds = dict()
    maxNgrams = len(maxTFIDFs[0])
    for ngrams in range(1, maxNgrams + 1):
        countThreshold = optimalDeletionRatio * cumhisto[ngrams][0]
        for i in range(len(cumhisto[ngrams])):
            if cumhisto[ngrams][i] < countThreshold:
                break
        tfidfThresholds[ngrams] = intervals[ngrams][i]
    return tfidfThresholds

