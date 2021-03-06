



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