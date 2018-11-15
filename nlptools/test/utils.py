from systemtools.basics import *
from systemtools.file import *
from systemtools.location import *
from datatools.jsonutils import NDJson
import random
from datastructuretools.processing import *
import copy

def threadedTextGenerator(*args, **kwargs):
	def __gen():
		for current in textGenerator(*args, **kwargs):
			yield current
	for current in threadGen(__gen()):
		yield current

def textGenerator(seed=0, whiteList=[], blackList=[], logger=None, verbose=True, maxFiles=4, maxSamplesPerFile=10, maxTweets=3, limit=None):
	if whiteList is None or len(whiteList) == 0:
		whiteList = None
	if blackList is None or len(blackList) == 0:
		blackList = None
	rowCount = 0
	random.seed(seed)
	dataDirs = [x for x in sortedGlob(dataDir() + "/News/*") if isDir(x)]
	dataDirs.append(dataDir() + "/TwitterNewsrec/twitternewsrec3/users")
	random.shuffle(dataDirs)
	for current in dataDirs:
		(_, dirName, _, _) = decomposePath(current)
		if (whiteList is None or dirName in whiteList) and (blackList is None or dirName not in blackList):
			filesPath = random.sample(sortedGlob(current + "/*.bz2"), maxFiles)
			if dirName == "users":
				for path in filesPath:
					for user in random.sample(list(NDJson(path)), maxSamplesPerFile):
						for tweet in random.sample(user["tweets"], maxTweets):
							yield (dirName, tweet["text"])
							rowCount += 1
							if limit is not None and rowCount > limit:
								return
			else:
				for path in filesPath:
					for news in random.sample(list(NDJson(path)), maxSamplesPerFile):
						yield (dirName, news["text"])
						rowCount += 1
						if limit is not None and rowCount > limit:
							return

def getTestTexts(oneLineFilter=None):
	path = getExecDir(__file__) + "/testdata/pipeline/texts.txt"
	texts = fileToStr(path)
	texts = re.compile("\n+-+\n+").split(texts)
	oneLineTexts = texts[0].split("\n")
	multiLinesTexts = texts[1:]
	newOneLineTexts = []
	currentComment = None
	for current in oneLineTexts:
		if current.startswith("###"):
			currentComment = current
		elif not (current is None or len(current) == 0):
			if oneLineFilter is None or oneLineFilter in currentComment:
				newOneLineTexts.append(current)
	oneLineTexts = newOneLineTexts
	return (oneLineTexts, multiLinesTexts)

def sentencesToParagraph(sentences, sentencesSeparator="\n"):
	if sentences is None or len(sentences) == 0:
		return None
	sentences = copy.deepcopy(sentences)
	for i in range(len(sentences)):
		sentence = sentences[i]
		if len(sentence) > 0:
			if isinstance(sentence[0], tuple):
				newSentence = []
				for word, tag in sentences[i]:
					newSentence.append(word)
				sentences[i] = newSentence
			sentences[i] = " ".join(sentences[i])
	return sentencesSeparator.join(sentences)