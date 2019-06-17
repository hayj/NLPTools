# pew in st-venv python ~/Workspace/Python/Utils/NLPTools/nlptools/embedding.py

from systemtools.file import *
from systemtools.location import *
from systemtools.basics import *
from systemtools.logger import *
from datastructuretools.processing import *
from datastructuretools.hashmap import *
import bz2
import re
import numpy as np
import bz2

def bin2txtFile(path):
	(dir, filename, _, _) = decomposePath(path)
	from gensim.models.keyedvectors import KeyedVectors
	model = KeyedVectors.load_word2vec_format(path, binary=True)
	outputPath = dir + "/" + filename + ".txt"
	model.save_word2vec_format(outputPath, binary=False)
	return outputPath

def d2vTokenssToEmbeddings(tokenss, model, doLower=False, logger=None, verbose=True):
    if isinstance(tokenss[0], str):
        tokenss = [tokenss]
    mtx = None
    for tokens in pb(tokenss, logger=logger, message="Infering vectors"):
        if doLower:
            for i in range(len(tokens)):
                tokens[i] = tokens[i].lower()
        vector = model.infer_vector(tokens)
        if mtx is None:
            mtx = vector
        else:
            mtx = np.vstack((mtx, vector))
    return mtx

def tokensToEmbedding(tokens, wordVectors=None, operation='sum', removeDuplicates=True, doLower=False):
    """
        This function take tokens (or a list of tokens)
        And a map word->vector
        It return a sentence embedding according to the operation given (sum, mean).
    """
    if wordVectors is None:
        wordVectors = getWordVectorsSingleton().load()
    if isinstance(tokens[0], list):
        nbDocs = len(tokens)
        mtx = None
        tokens = copy.deepcopy(tokens)
        for i in range(len(tokens)):
            currentArray = tokensToEmbedding(tokens[i], wordVectors=wordVectors, operation=operation,
                                          removeDuplicates=removeDuplicates, doLower=doLower)
            if mtx is None:
                mtx = currentArray
            else:
                mtx = np.vstack((mtx, currentArray))
        return mtx
    else:
        if removeDuplicates:
            tokens = set(tokens)
        vectors = []
        for current in tokens:
            if doLower:
                current = current.lower()
            if current in wordVectors:
                vectors.append(wordVectors["current"])
        if operation == 'sum':
            return np.sum(np.array(vectors), axis=0)
        elif operation == 'mean':
            return np.mean(np.array(vectors), axis=0)
        print(vectors.shape)
        return vectors


WORD_EMBEDDINGS_RESSOURCES = \
{
	"fasttext-wiki-news-1M": ("https://dl.fbaipublicfiles.com/fasttext/vectors-english/wiki-news-300d-1M.vec.zip", [300]),
	"fasttext-wiki-news-1M-subword": ("https://dl.fbaipublicfiles.com/fasttext/vectors-english/wiki-news-300d-1M-subword.vec.zip", [300]),
	"fasttext-crawl-2M": ("https://dl.fbaipublicfiles.com/fasttext/vectors-english/crawl-300d-2M.vec.zip", [300]),
	"fasttext-crawl-2M-subword": ("https://dl.fbaipublicfiles.com/fasttext/vectors-english/crawl-300d-2M-subword.zip", [300]),
	"glove-6B": ("http://nlp.stanford.edu/data/glove.6B.zip", [50, 100, 200, 300]),
	"glove-42B": ("http://nlp.stanford.edu/data/glove.42B.300d.zip", [300]),
	"glove-840B": ("http://nlp.stanford.edu/data/glove.840B.300d.zip", [300]),
	"glove-twitter-27B": ("http://nlp.stanford.edu/data/glove.twitter.27B.zip", [25, 50, 100, 200]),
	"word2vec-googlenews": ("https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz", [300]),
}
class Embeddings():
	def __init__\
	(
		self,
		key="glove-6B",
		dimension=None,
		dataDir=None,
		logger=None,
		verbose=True,
		doMultiprocessing=True,
	):
		self.logger = logger
		self.verbose = verbose
		self.dataDir = dataDir
		if self.dataDir is None:
			self.dataDir = tmpDir(self.__class__.__name__)
		self.key = self.__keyPatternToKey(key)
		self.location, availableDimensions = WORD_EMBEDDINGS_RESSOURCES[self.key]
		self.dimension = dimension
		if self.dimension is None:
			self.dimension = 100 if 100 in availableDimensions else availableDimensions[0]
		else:
			if self.dimension not in availableDimensions:
				raise Exception("Please choose a dimension in " + str(availableDimensions) + " for " + self.key)
		self.multipartsDir = self.dataDir + "/" + self.key
		self.multipartsDir += "-dim" + str(self.dimension)
		self.multipartsDir += "-multiparts"
		self.vectors = None
		self.doMultiprocessing = doMultiprocessing
	
	def __keyPatternToKey(self, keyPattern):
		key = None
		for current in WORD_EMBEDDINGS_RESSOURCES.keys():
			if re.search(keyPattern, current):
				key = current
				break
		if key is None:
			raise Exception("We didn't found the pattern " + key + " in " + str(self.locations.keys()))
		return key

	def isLower(self):
		for word in self.vectors.keys():
			if word.lower() != word:
				return False
		return True

	def hasPunct(self):
		if "." in self.vectors:
			return True
		else:
			return False

	def checkDimension(self):
		assert len(self.vectors["the"] == self.dimension)

	def __download(self):
		if not isDir(self.multipartsDir) or len(sortedGlob(self.multipartsDir + "/*")) == 0:
			if self.location.startswith("http"):
				log("Downloading " + self.key + " from " + str(self.location))
				downloadedFile = download(self.location, skipIfExists=True)
				if decomposePath(downloadedFile)[2] in  ["zip", "bz", "gz"]:
					log("Extracting " + downloadedFile, self)
					extractedThing = extract(downloadedFile, destinationDir=tmpDir("downloads"))
					if decomposePath(extractedThing)[2] == "bin":
						log("Converting the bin file to a txt file format...", self)
						newExtractedThing = bin2txtFile(extractedThing)
						if ".bin" in extractedThing: rm(extractedThing, secure=False)
						extractedThing = newExtractedThing
					if isFile(extractedThing):
						extractedFile = extractedThing
					elif isDir(extractedThing):
						try:
							extractedFile = sortedGlob(extractedThing + "/*" + str(self.dimension) + "*")[0]
						except:
							extractedFile = sortedGlob(extractedThing + "/*")[0]
					else:
						raise Exception("Cannot extract " + downloadedFile)
					log("Generating multi-parts of " + extractedFile + "...", self)
					fileToMultiParts(extractedFile, outputDir=self.multipartsDir)
					log(self.key + " done.", self)
					rm(extractedThing, minSlashCount=4)
				else:
					raise Exception("Not yet implemented")
				remove(downloadedFile, minSlashCount=4)
			else:
				raise Exception("Not yet implemented")
		else:
			log("We already generated multiparts dir of " + self.key + ".", self)

	def getVectors(self, maxWords=None):
		"""
			This function return a dict mapping words and vectors
		"""
		if self.vectors is None:
			self.__download()
			filesPath = sortedGlob(self.multipartsDir + "/*")
			if len(filesPath) == 0:
				raise Exception("Multiparts files not found.")
			def itemGenerator(filePath, logger=None, verbose=True):
				opener = open
				if filesPath[0][-4:] == ".bz2":
					opener = bz2.open
				with opener(filePath, 'r') as f:
					vectors = {}
					for line in f:
						try:
							tokens = line.split()
							word = tokens[0]
							values = tokens[1:]
							assert len(word) > 0
							assert len(values) > 3
							vector = np.asarray(values, dtype='float32')
							yield (word, vector)
						except:
							logError("Cannot parse " + str(line), logger, verbose=verbose)
			if self.doMultiprocessing:
				mg = MultiprocessingGenerator(filesPath, itemGenerator, logger=self.logger, queueMaxSize=20, verbose=self.verbose)
			else:
				def itGenWrapper(filesPath, itemGenerator, logger=None, verbose=True):
					for filePath in pb(filesPath, logger=logger, verbose=verbose):
						for current in itemGenerator(filePath, logger=logger, verbose=verbose):
							yield current
				mg = itGenWrapper(filesPath, itemGenerator, logger=self.logger, verbose=self.verbose)
			self.vectors = dict()
			count = 0
			for word, vector in mg:
				word = byteToStr(word)
				self.vectors[word] = vector
				if maxWords is not None and count > maxWords:
					logWarning("Please kill the python script because zombies process remains...", self)
					break
				count += 1
			self.checkDimension()
		return self.vectors


def test1():
	loader = Embeddings("glove-6B", None, doMultiprocessing=False)
	wordVectors = loader.getVectors()
	print(wordVectors["the"])
	wordVectors = loader.getVectors()
	wordVectors = loader.getVectors()
	print(wordVectors["the"])
	print(loader.isLower())


if __name__ == '__main__':
	test1()












############################ OLD ############################




def example_old():
	wordVectors = getWordVectorsSingleton().load("glove-6B" if hjlat() else "glove-840B")

def test2_old():
	wv = WordVectors()
	data = wv.load()
	print(reducedLTS(list(data.items())))

def test1_old():
	vectors = getWordVectorsSingleton().load("twitterglove-27B.300d" if hjlat() else "glove-840B")
	print(vectors["the"])



wordVectorsSingleton = None
def getWordVectorsSingleton(*args, **kwargs):
	global wordVectorsSingleton
	print("DEPRECATED getWordVectorsSingleton")
	if wordVectorsSingleton is None:
		wordVectorsSingleton = WordVectors(*args, **kwargs)
	return wordVectorsSingleton

class WordVectors():
	def __init__\
	(
		self,
		dataDir=None,
		# defaultKeyPattern="fasttext.*300d.*2M",
		# defaultKeyPattern="glove-6B",
		defaultKeyPattern="glove-840B",
		# defaultKeyPattern="840B.300d",
		logger=None,
		verbose=True
	):
		print("DEPRECATED getWordVectorsSingleton")
		self.logger = logger
		self.verbose = verbose
		self.dataDir = dataDir
		if self.dataDir is None:
			self.dataDir = tmpDir(self.__class__.__name__)
		self.defaultKeyPattern = defaultKeyPattern
		self.locations = \
		{
			"fasttext-crawl-300d-2M": "https://dl.fbaipublicfiles.com/fasttext/vectors-english/crawl-300d-2M.vec.zip",
			"glove-6B": "http://nlp.stanford.edu/data/glove.6B.zip",
			"glove-42B.300d": "http://nlp.stanford.edu/data/glove.42B.300d.zip",
			"glove-840B.300d": "http://nlp.stanford.edu/data/glove.840B.300d.zip",
			"twitterglove-27B": "http://nlp.stanford.edu/data/glove.twitter.27B.zip",
			"word2vec": homeDir() + "/Downloads/word2vec.zip",
		}
		self.cache = SerializableDict\
		(
	        logger=self.logger,
	        limit=3,
	        cleanEachNAction=1,
	        doSerialize=False,
	        useMongodb=False,
		)

	def keyToMultiPartsDir(self, key):
		return self.dataDir + "/" + key + "-multiparts"
	
	def keyPatternToKey(self, keyPattern):
		key = None
		for current in self.locations.keys():
			if re.search(keyPattern, current):
				key = current
				break
		return key

	def download(self, keyPattern=None):
		if keyPattern is None:
			keyPattern = self.defaultKeyPattern
		key = self.keyPatternToKey(keyPattern)
		if key is None:
			logError(keyPattern + " not found in " + str(self.locations.keys()))
		outputDir = self.keyToMultiPartsDir(key)
		if not isDir(outputDir) or len(sortedGlob(outputDir + "/*")) == 0:
			location = self.locations[key]
			if location.startswith("http"):
				log("Downloading " + location)
				downloadedFile = download(location, skipIfExists=True)
				if downloadedFile[-4:] == ".zip":
					log("Extracting " + downloadedFile)
					extractedThing = extract(downloadedFile, destinationDir=tmpDir("downloads"))
					extractedFile = extractedThing
					if isDir(extractedFile):
						extractedFile = sortedGlob(extractedFile + "/*")[0]
					log("Generating multi-parts of " + extractedFile)
					fileToMultiParts(extractedFile, outputDir=outputDir)
					log("Getting " + key + " done.")
					rm(extractedThing)
				else:
					raise Exception("Not yet implemented")
				rm(downloadedFile)
			else:
				raise Exception("Not yet implemented")
		else:
			log(key + " already downloaded.")

	def load(self, keyPattern=None, maxWords=None):
		"""
			This function return a dict mapping words and vectors
		"""
		if keyPattern is None:
			keyPattern = self.defaultKeyPattern
		if keyPattern in self.cache:
			return self.cache[keyPattern]
		else:
			self.download(keyPattern=keyPattern)
			key = self.keyPatternToKey(keyPattern)
			outputDir = self.keyToMultiPartsDir(key)
			filesPath = sortedGlob(outputDir + "/*")
			if len(filesPath) == 0:
				raise Exception("Files not found.")
			def itemGenerator(filePath, logger=None, verbose=True):
				opener = open
				if filesPath[0][-4:] == ".bz2":
					opener = bz2.open
				with opener(filePath, 'r') as f:
					vectors = {}
					for line in f:
						try:
							tokens = line.split()
							word = tokens[0]
							values = tokens[1:]
							assert len(word) > 0
							assert len(values) > 3
							vector = np.asarray(values, dtype='float32')
							yield (word, vector)
						except:
							logError("Cannot parse " + str(line), logger, verbose=verbose)
			mg = MultiprocessingGenerator(filesPath, itemGenerator, logger=self.logger, queueMaxSize=20)
			data = dict()
			count = 0
			for word, vector in mg:
				word = byteToStr(word)
				data[word] = vector
				if maxWords is not None and count > maxWords:
					logWarning("Please kill the python script because zombies process remains...")
					break
				count += 1
			self.cache[keyPattern] = data
			return data