
# pew in st-venv python /home/hayj/Workspace/Python/Utils/NLPTools/nlptools//overlap.py

from datastructuretools.processing import *
from systemtools.basics import *
from systemtools.logger import *
from systemtools.system import *
from nlptools.tokenizer import *
from nlptools.basics import *
from nlptools.preprocessing import *
import random



def countOverlaps(parsed1, parsed2, ngram):
    print("DEPRECATED")
    count = 0
    for _ in yieldOverlaps(parsed1, parsed2, ngram):
        count += 1
    return count

def hasOverlap(parsed1, parsed2, ngram):
    print("DEPRECATED")
    for _ in yieldOverlaps(parsed1, parsed2, ngram):
        return True
    return False

def yieldOverlaps(parsed1, parsed2, ngram):
    print("DEPRECATED")
    if len(parsed1) < ngram or len(parsed2) < ngram:
        return 0
    for i in range(len(parsed1) - (ngram - 1)):
        currentParsed1Ngram = parsed1[i:i + ngram]
        for i in range(len(parsed2) - (ngram - 1)):
            currentParsed2Ngram = parsed2[i:i + ngram]
            if currentParsed1Ngram == currentParsed2Ngram:
                yield currentParsed1Ngram


# TODO faire un TF.IDF des ngrams entre plusieurs overlaps

class Overlap():
	def __init__(self, documents, logger=None, verbose=True, preprocess=True,
		parallelCount=None, ngramsMin=3, removeEmbeddedNgrams=True, batchMaxSize=600):
		"""
			:params batchMaxSize: will split your documents in maximum size of `batchMaxSize`. You will generate approximation of overlaps because overlaps will be calculated on multiple sub-set of all documents and all ngrams will be merged. This parameter overcome the O(n2) complexity by approximating overlaps. In this setting, you will NOT have ngrams which are only one time in different batchs...
			if len(documents) > batchMaxSize the overlaps will also be reconstructed according to all batch, some ngrams will miss but some other will toke into account too much time in some docs even there are n+1 grams...
		"""
		self.removeEmbeddedNgrams = removeEmbeddedNgrams
		self.ngramsMin = ngramsMin
		self.parallelCount = parallelCount
		if self.parallelCount is None:
			self.parallelCount = cpuCount()
		self.documents = documents
		self.logger = logger
		self.overlaps = None
		self.overlapsScores = None
		self.overlapedDocs = None
		self.verbose = verbose
		self.batchMaxSize = batchMaxSize
		self.tt = TicToc(logger=self.logger, verbose=self.verbose)
		if isinstance(self.documents, set):
			self.documents = list(self.documents)
		if self.documents is None or len(self.documents) == 0:
			raise Exception("documents must be a list of documents.")
		self.poolParams = \
		{
			"parallelCount": self.parallelCount,
			"mapType": MAP_TYPE.multiprocessing,
			"logger": self.logger,
			"verbose": self.verbose,
		}
		# print(len(self.documents))
		# totalStringLen = 0
		# for doc in self.documents:
		# 	totalStringLen += len(doc)
		# print("totalStringLen " + str(totalStringLen))
		if not isinstance(self.documents[0], list) and preprocess:
			log("Preprocessing for Overlap...", self)
			self.tt.tic(display=False)
			self.normalize()
			self.lower()
			self.tokenize()
			self.removeNotWord()
			self.removeStopwords()
			self.tt.tic("Preprocessing done.")
		self.invertedIndex = None
		log("Generating the inverted index...", self)
		self.tt.tic(display=False)
		self.generateInvertedIndex()
		self.tt.tic("Inverted index generated.")


	def getInvertedIndex(self):
		return self.invertedIndex

	def getOverlapsScores(self):
		if self.overlapsScores is not None:
			return self.overlapsScores
		overlaps = self.getOverlaps()
		return self.invertedIndex

	def getDocuments(self):
		return self.documents

	def removeStopwords(self):
		initStopwordsList(stopwordsList=STOPWORDS_LIST.large)
		pool = Pool(**self.poolParams)
		self.documents = pool.map(removeStopwordsLarge, self.documents)

	def removeNotWord(self):
		pool = Pool(**self.poolParams)
		self.documents = pool.map(removeNotWord, self.documents)

	def lower(self):
		pool = Pool(**self.poolParams)
		self.documents = pool.map(lower, self.documents)

	def normalize(self):
		pool = Pool(**self.poolParams)
		self.documents = pool.map(softPreprocess, self.documents)

	def tokenize(self):
		pool = Pool(**self.poolParams)
		self.documents = pool.map(wordTokenize, self.documents)

	def generateInvertedIndex(self):
		"""
			The inverted index is structured like this:
			{
				vouchers: 
				{
					3: [70, 291, <wordIndex>, ...],
					10: [2, 4, <wordIndex>, ...],
					<documentIndex>: [21, 42, <wordIndex>, ...],
				},
				<word>: 
				{
					3: [70, 291, <wordIndex>, ...],
					10: [2, 4, <wordIndex>, ...],
					<documentIndex>: [21, 42, <wordIndex>, ...],
				},
				...
			}
		"""
		self.invertedIndex = dict()
		documentIndex = 0
		for document in self.documents:
			wordIndex = 0
			for word in document:
				if word not in self.invertedIndex:
					self.invertedIndex[word] = dict()
				theDict = self.invertedIndex[word]
				if documentIndex not in theDict:
					theDict[documentIndex] = []
				theDict[documentIndex].append(wordIndex)
				wordIndex += 1
			documentIndex += 1

	def getOverlaps(self):
		if self.overlaps is None:
			return self.generateOverlaps()
		else:
			return self.overlaps

	def generateOverlaps(self):
		"""
			An overlaps structure looks like:
			{
				('la', 'soupe', 'aux', 'choux', <a word>): {
					0: {0},
					<the document index>: {0}
				},
				('la', 'soupe', 'aux', 'choux'): {
					0: {90, 146},
					1: {<the first word index>, <the first word index for an other occurrence of the ngram in the same document>}
				},
				('rené', 'fallet', 'paru', 'en'): {
					0: {6},
					1: {23}
				},
				<the ngram tuple>: {
					0: {27},
					1: {51}
				}
			}

			O(n^2) but optimized with an inverted index:

			--> tic: 2.98s for 100 docs and a batchMaxSize of None.
			--> tic: 6.12s for 200 docs and a batchMaxSize of None.
			--> tic: 17.99s for 500 docs and a batchMaxSize of None.
			--> tic: 1m 22.209s for 1000 docs and a batchMaxSize of None.
			--> tic: 10m 35.409s for 3000 docs and a batchMaxSize of None.

			If you set a batchMaxSize of 200, yuo will approximate ngrams overlap but the complexity will be ~O(n):

			--> tic: 2.98s for 100 docs and a batchMaxSize of 200.
			--> tic: 6.12s for 200 docs and a batchMaxSize of 200.
			--> tic: 14.32s | message: for 500 docs and a batchMaxSize of 200.
			--> tic: 48.1s | message: for 1000 docs and a batchMaxSize of 200.
			--> tic: 2m 48.03s | message: for 3000 docs and a batchMaxSize of 200.
			
		"""
		# localTT = TicToc(logger=self.logger)
		# localTT.tic("generateOverlaps: start")
		batchCount = 1
		batchSize = len(self.documents)
		if self.batchMaxSize is not None and self.batchMaxSize > 1:
			batchCount = math.ceil(len(self.documents) / self.batchMaxSize)
			batchSize = math.ceil(len(self.documents) / batchCount)
		pairs = []
		# localTT.tic("generateOverlaps: step2")
		for batchIndex in range(batchCount):
		    currentStartIndex = batchIndex * batchSize
		    for a in range(currentStartIndex, currentStartIndex + batchSize):
		        for b in range(a, currentStartIndex + batchSize):
		            if a != b and a < len(self.documents) and b < len(self.documents):
		                pairs.append((a, b))
		log("Generating overlaps...", self)
		log("batchCount: " + str(batchCount), self)
		log("batchSize: " + str(batchSize), self)
		log("len(self.documents): " + str(len(self.documents)), self)
		self.tt.tic(display=False)
		pairs = split(pairs, self.parallelCount)
		pool = Pool(**self.poolParams)
		overlapss = pool.map(self.getOverlapsFromPairs, pairs)
		# localTT.tic("generateOverlaps: step3")
		overlaps = self.overlapsFusion(overlapss)
		# localTT.tic("generateOverlaps: step4")
		if batchCount > 1:
			# ttt = TicToc()
			# ttt.tic(display=False)
			# We reconstruct the overlaps structure because some ngram can be forgotten in some docs:
			ngrams = list(overlaps.keys())
			ngramss = split(ngrams, self.parallelCount)
			pool = Pool(**self.poolParams)
			overlapss = pool.map(self.reconstructOverlaps, ngramss)
			# localTT.tic("generateOverlaps: step5")
			overlaps = self.overlapsFusion(overlapss)
			# ttt.toc("the duration of the reconstruction")
			# A priori pas besoin de faire de removeEmbeddedNgrams, puisqu'on l'a deja fait entre pairs:
			# if self.removeEmbeddedNgrams:
			# 	overlaps = removeEmbeddedNgrams(overlaps, range(len(self.documents))
		self.tt.tic("Overlaps generated.")
		self.overlaps = overlaps
		# localTT.toc("generateOverlaps: end")
		return overlaps

	def reconstructOverlaps(self, ngrams):
		# tt = TicToc(logger=self.logger)
		# tt.tic("reconstructOverlaps: start")
		newOverlaps = dict()
		for ngram in ngrams:
			newOverlaps[ngram] = dict()
			for docIndex in range(len(self.documents)):
				doc = self.documents[docIndex]
				for wordIndex in range(len(doc)):
					word = doc[wordIndex]
					ngramFound = True
					if word == ngram[0]:
						for indexAdd in range(1, len(ngram)):
							newWordIndex = wordIndex + indexAdd
							if newWordIndex >= len(doc):
								ngramFound = False
								break
							if doc[newWordIndex] != ngram[indexAdd]:
								ngramFound = False
								break
					else:
						ngramFound = False
					if ngramFound:
						if docIndex not in newOverlaps[ngram]:
							newOverlaps[ngram][docIndex] = set()
						newOverlaps[ngram][docIndex].add(wordIndex)
		# tt.toc("reconstructOverlaps: end")
		return newOverlaps

	def overlapsFusion(self, overlapss):
		newOverlaps = dict()
		for overlaps in overlapss:
			for ngram, docs in overlaps.items():
				if ngram not in newOverlaps:
					newOverlaps[ngram] = dict()
				newOverlaps[ngram] = mergeDicts(newOverlaps[ngram], docs)
		return newOverlaps


	def getOverlapsFromPairs(self, pairs):
		overlaps = None
		try:
			# tt = TicToc(logger=self.logger)
			# tt.tic("getOverlapsFromPairs: start")
			overlapss = []
			for index1, index2 in pairs:
				pairOverlaps = self.getOverlapsFromPair(index1, index2)
				if len(pairOverlaps) > 0:
					overlapss.append(pairOverlaps)
			# tt.tic("getOverlapsFromPairs: step2")
			overlaps = self.overlapsFusion(overlapss)
		except Exception as e:
			# TODO DELETE
			logger = Logger(tmpDir(subDir="overlap-process-loggers") + "/" + getRandomStr() + ".log")
			logException(e, logger=logger, verbose=True)
		# tt.toc("getOverlapsFromPairs: end")
		return overlaps

	def getOverlapsFromPair(self, docIndex1, docIndex2):
		doc1 = self.documents[docIndex1]
		doc2 = self.documents[docIndex2]
		doc1Len = len(doc1)
		doc2Len = len(doc2)
		overlaps = dict()
		for wordIndex1 in range(len(doc1)):
			word = doc1[wordIndex1]
			inversedIndexEntry = self.invertedIndex[word]
			if docIndex2 in inversedIndexEntry:
				# Here we found indexes in doc2 for the word in doc1:
				for wordIndex2 in inversedIndexEntry[docIndex2]:
					i = 1
					while True:
						newIndex1 = wordIndex1 + i
						newIndex2 = wordIndex2 + i
						if newIndex1 >= doc1Len or newIndex2 >= doc2Len:
							break
						elif doc1[newIndex1] != doc2[newIndex2]:
							break
						else:
							i += 1
					ngramMaxIndex = i - 1
					ngramLength = ngramMaxIndex + 1
					if ngramLength >= self.ngramsMin:
						ngram = []
						for u in range(ngramLength):
							ngram.append(doc1[wordIndex1 + u])
						ngram = tuple(ngram)
						if ngram not in overlaps:
							overlaps[ngram] = dict()
						if docIndex1 not in overlaps[ngram]:
							overlaps[ngram][docIndex1] = set()
						if docIndex2 not in overlaps[ngram]:
							overlaps[ngram][docIndex2] = set()
						overlaps[ngram][docIndex1].add(wordIndex1)
						overlaps[ngram][docIndex2].add(wordIndex2)
		if self.removeEmbeddedNgrams:
			overlaps = removeEmbeddedNgrams(overlaps, [docIndex1, docIndex2])
		return overlaps

	def findDuplicates(self, threshold=0.93):
		"""
			Actually this algorithm is naive, if (1, 2) are similar according to the threshold and (2, 3) also, the algorithm will consider (1, 3) to be similar even it is not the case according to the threshold.

			The structure looks like this:
			[
				{6, 7},
				{1, 3}
			]
		"""
		# tt = TicToc(logger=self.logger)
		# tt.tic("findDuplicates: start")
		meanOverlapScores = self.getMeanOverlapScores(threshold=0.0)
		duplicatess = []
		for pair, similarity in meanOverlapScores.items():
			if similarity >= threshold:
				found = False
				for duplicates in duplicatess:
					if pair[0] in duplicates or pair[1] in duplicates:
						duplicates.add(pair[0])
						duplicates.add(pair[1])
						found = True
						break
				if not found:
					duplicatess.append({pair[0], pair[1]})
		# tt.toc("findDuplicates: end")
		return duplicatess


	def getMeanOverlapScores(self, threshold=0.6):
		"""
			A meanOverlapScores structure looks like this:
			{
				(1, 3): 0.58,
				(<doc id 1>, <doc id 2>): <ngram similarity score>,
			}
			You can not have a key (3, 1), there are no duplicates, all tuples values (which are key of the structure) are sorted.
		"""
		# tt = TicToc(logger=self.logger)
		# tt.tic("getMeanOverlapScores: start")
		overlapScores = self.getOverlapScores(threshold=0.0)
		meanOverlapScores = dict()
		for currentDocIndex, targets in overlapScores.items():
			for targetIndex, score in targets.items():
				if currentDocIndex < targetIndex:
					theKey = (currentDocIndex, targetIndex)
				else:
					theKey = (targetIndex, currentDocIndex)
				if theKey not in meanOverlapScores:
					theMean = (score + overlapScores[targetIndex][currentDocIndex]) / 2.0
					meanOverlapScores[theKey] = theMean
		# We filter:
		# tt.tic("getMeanOverlapScores: We filter")
		newMeanOverlapScores = dict()
		for theKey, score in meanOverlapScores.items():
			if score >= threshold:
				newMeanOverlapScores[theKey] = score
		meanOverlapScores = newMeanOverlapScores
		# tt.toc("getMeanOverlapScores: end")
		return meanOverlapScores


	def getOverlapScores(self, threshold=0.8):
		"""
			an overlapScores structure looks like this:
			{
				<doc index>: {
					1: 0.11049723756906077,
					3: 0.287292817679558
				},
				1: {
					0: 0.1702127659574468,
					3: 0.9042553191489362 # Here we have 90% of 0 in 3
				},
				3: {
					1: 0.25872093023255816, # Here we have 25% of 3 in 0
					<target doc>: <score>
				}
			}
		"""
		# if self.overlapedDocs is not None:
		# 	return self.overlapedDocs
		# else:
		# 	return self.generateOverlapedDocs(*args, **kwargs)
		# def generateOverlapedDocs(self, threshold=0.8):
		# tt = TicToc(logger=self.logger)
		# tt.tic("getOverlapScores: start")
		overlaps = self.getOverlaps()
		targetPairs = set()
		for ngram, docsIndexes in overlaps.items():
			for i in docsIndexes.keys():
				for u in docsIndexes.keys():
					if i != u:
						if i < u:
							targetPairs.add((i, u))
						else:
							targetPairs.add((u, i))
		overlapedDocs = dict()
		# tt.tic("getOverlapScores: step2")
		for docIndex1, docIndex2 in targetPairs:
			overlapVector1 = [False] * len(self.documents[docIndex1])
			overlapVector2 = [False] * len(self.documents[docIndex2])
			for ngram, docsIndexes in overlaps.items():
				ngramLen = len(ngram)
				if docIndex1 in docsIndexes and docIndex2 in docsIndexes:
					for wordIndex1 in docsIndexes[docIndex1]:
						for i in range(wordIndex1, wordIndex1 + ngramLen):
							overlapVector1[i] = True
					for wordIndex2 in docsIndexes[docIndex2]:
						for i in range(wordIndex2, wordIndex2 + ngramLen):
							overlapVector2[i] = True
			overlapAmount1 = overlapVector1.count(True)
			if docIndex1 not in overlapedDocs:
				overlapedDocs[docIndex1] = dict()
			overlapedDocs[docIndex1][docIndex2] = overlapAmount1 / len(self.documents[docIndex1])
			overlapAmount2 = overlapVector2.count(True)
			if docIndex2 not in overlapedDocs:
				overlapedDocs[docIndex2] = dict()
			overlapedDocs[docIndex2][docIndex1] = overlapAmount2 / len(self.documents[docIndex2])
		# tt.tic("getOverlapScores: step3")
		# We filter:
		newOverlapedDocs = dict()
		for target, currentOverlapedDocs in overlapedDocs.items():
			newCurrentOverlapedDocs = dict()
			for currentOverlapedDoc, score in currentOverlapedDocs.items():
				if score >= threshold:
					newCurrentOverlapedDocs[currentOverlapedDoc] = score
			if len(newCurrentOverlapedDocs) > 0:
				newOverlapedDocs[target] = newCurrentOverlapedDocs
		overlapedDocs = newOverlapedDocs
		# tt.toc("getOverlapScores: end")
		return overlapedDocs




def removeEmbeddedNgrams(overlaps, docIndexes):
	"""
		For now this function must be used only for 2 docs only
	"""
	# First we remove embedded ngrams:
	# print("aaaaaaaaaaaaaaaaaaaaaaaaaa")
	# printLTS(overlaps)
	# printLTS(docIndexes)
	# exit()
	# We get 2 docs:
	for currentDocIndex in docIndexes:
		# We get all ngrams with corresponding docs:
		for ngram1, currentDocs1 in overlaps.items():
			ngram1Len = len(ngram1)
			# We check if our current doc is in currentDocs1:
			if currentDocIndex in currentDocs1:
				wordIndexes1 = currentDocs1[currentDocIndex]
				# We find an other ngram in the same doc:
				for ngram2, currentDocs2 in overlaps.items():
					ngram2Len = len(ngram2)
					if currentDocIndex in currentDocs2:
						wordIndexes2 = currentDocs2[currentDocIndex]
						# We check if the ngram1 IS IN the ngram2:
						if ngram2Len > ngram1Len:
							toDelete = set()
							# For this purpose we calculate intervals:
							for wordIndex1 in wordIndexes1:
								for wordIndex2 in wordIndexes2:
									# Maybe we have to delete the ngram1 occurrence (checking intervals):
									ngram2Interval = (wordIndex2, wordIndex2 + ngram2Len)
									ngram1Interval = (wordIndex1, wordIndex1 + ngram1Len)
									# If ngram1 IS IN ngram2:, we retain the wordIndex1:
									if ngram1Interval[0] >= ngram2Interval[0] and ngram1Interval[1] <= ngram2Interval[1]:
										toDelete.add(wordIndex1)
										break
							# newWordIndexes1 = []
							# for current in wordIndexes1:
							# 	if current not in toDelete:
							# 		newWordIndexes1.append(current)
							# wordIndexes1 = newWordIndexes1
							# currentDocs1[currentDocIndex] = newWordIndexes1
							# # wordIndexes1.remove(current)
							for current in toDelete:
								wordIndexes1.remove(current)
	# Then we delete empty docIndex:
	for currentNgram, currentDocs in overlaps.items():
		docIndexesToDelete = []
		for currentDocIndex, wordIndexes in currentDocs.items():
			if len(wordIndexes) == 0:
				docIndexesToDelete.append(currentDocIndex)
		for current in docIndexesToDelete:
			del currentDocs[current]
	# Then we delete ngrams which appear only in one doc:
	ngramsToDelete = []
	for currentNgram, currentDocs in overlaps.items():
		if len(currentDocs) <= 1:
			ngramsToDelete.append(currentNgram)
	for current in ngramsToDelete:
		del overlaps[current]
	return overlaps



def test1():
	# from nlpstools.overlap import * # install our packae using https://github.com/hayj/Bash/blob/master/hjupdate.sh
	# Get your data:
    d0 = "Hello I am X and I did an Overlap librarie?"
    d1 = "Hello I am Y and I work on Overlap librarie tool."
    d2 = "You are working on this with my collegue, on the Overlap librarie tool!"
    # Init the Overlap object and set ngramsMin. If ngramsMin is 2, only 2grams will be taken into account:
    o = Overlap([d0, d1, d2], ngramsMin=2, verbose=False)
    # You can get overlaps:
    printLTS(o.getOverlaps())
    # You can get a pairwise scores between each document:
    printLTS(o.getMeanOverlapScores())
    # You can find similar document by searching for duplicates with a threshold:
    printLTS(o.findDuplicates(threshold=0.75))
    # You can get preprocessed document with this method, the preprocessing do char normalization, lower case chars, tokenize, remove tokens that are not wordw and finally remove stop words:
    printLTS(o.getDocuments())

def test2():
	for i in range(100):
		documents = []
		for u in range(100):
			doc = ""
			for w in range(100):
				doc += getRandomStr() + " "
			documents.append(doc)
		tt = TicToc()
		tt.tic(display=False)
		Overlap(documents)
		tt.tic()

if __name__ == '__main__':
	test1()










