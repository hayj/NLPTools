
from systemtools.basics import *
import re
from nlptools.pipeline1.utils import *
import copy

def precleanv1(text, logger=None, verbose=True):
	lines = text.split("\n")
	text = None
	for findMenuKwargs in \
	[
		# Remove any sized blocks:
		{
			"meanTokenCount": 2.2,
			"jumpMaxDiff": 0.8,
			"lineMaxLength": 28,
			"allowPunct": True,
			"fistWordMustHaveAnUpperCase": True,
			"blockSizeMin": 1,
			"blockSizeMax": 500,
			"punctAsWord": False,
		},
		# Remove all blocks which have line with no punct but 3 words like "Get Started Now":
		# {
		# 	"meanTokenCount": 3,
		# 	"jumpMaxDiff": 1,
		# 	"lineMaxLength": 30,
		# 	"allowPunct": False,
		# 	"fistWordMustHaveAnUpperCase": True,
		# 	"blockSizeMin": 1,
		# 	"blockSizeMax": 500,
		# 	"punctAsWord": True,
		# },
	]:
		menuIntervals = findMenu(lines, **findMenuKwargs)
		# menuIntervals = lineIntervalsToStringIndexes(lines, menuIntervals)
		if len(menuIntervals) > 0:
			lines = removeListIntervals(lines, menuIntervals)
		#text = reduceBlank(text, keepNewLines=True)

	nonWordLinesIntervals = findLinesWithoutLowerCase(lines)
	if len(nonWordLinesIntervals) > 0:
		lines = removeListIntervals(lines, nonWordLinesIntervals)

	text = "\n".join(lines)
	return text

def postcleanv1(taggedSentences, minAlphasPerSentence=1, minAlphaForBoundaries=5, logger=None, verbose=True):
	# We first eliminate all too short sentences:
	newTaggedSentences = []
	for sentence in taggedSentences:
		alphaCount = 0
		for word, tag in sentence:
			if tag == TOKEN_TYPE.alpha:
				alphaCount += 1
		if alphaCount >= minAlphasPerSentence:
			newTaggedSentences.append(sentence)
	taggedSentences = newTaggedSentences
	# Then we delete first sentences which has less than minAlphaForBoundaries alhas:
	indexesToDelete = set()
	forwardIndexes = list(range(len(taggedSentences)))
	reverseIndexes = list(range(len(taggedSentences) - 1, -1, -1))
	for indexes in [forwardIndexes, reverseIndexes]:
		for index in indexes:
			currentSentence = taggedSentences[index]
			alphaCount = 0
			for word, tag in currentSentence:
				if tag == TOKEN_TYPE.alpha:
					alphaCount += 1
			if alphaCount < minAlphaForBoundaries:
				indexesToDelete.add(index)
			else:
				break
	newTaggedSentences = []
	for currentIndex in range(len(taggedSentences)):
		sentence = taggedSentences[currentIndex]
		if currentIndex not in indexesToDelete:
			newTaggedSentences.append(sentence)
	taggedSentences = newTaggedSentences
	# And finally we return taggedSentences:
	return taggedSentences

def isNewsValid(sentences, minTokens=15):
	if sentences is None or len(sentences) == 0:
		return False
	else:
		tokenCount = 0
		for sentence in sentences:
			tokenCount += len(sentence)
		if tokenCount >= minTokens:
			return True
		else:
			return False

def findLinesWithoutLowerCase(lines):
	intervals = []
	count = 0
	for line in lines:
		if not re.match(".*[a-z].*", line):
			intervals.append((count, count + 1))
		count += 1
	return intervals

# def lineIntervalsToStringIndexes(lines, intervals):
# 	"""
# 		This function convert line indexes in a intervals struct to string indexes
# 	"""
# 	newIntervals = []
# 	for a, b in intervals:
# 		lineIndex = 0
# 		charCount = 0
# 		lineCount = 0
# 		for lineIndex in range(lineIndex, a):
# 			charCount += len(lines[lineIndex]) + 1
# 			lineCount += 1
# 		newA = charCount
# 		lineIndex = lineCount
# 		for lineIndex in range(lineIndex, b + 1):
# 			charCount += len(lines[lineIndex]) + 1
# 		newB = charCount - 1
# 		newIntervals.append((newA, newB))
# 	return newIntervals

def removeStringIntervals(text, intervals):
	"""
		This function will remove portions of text according to string intervals.
		You have to apply `text = reduceBlank(text, keepNewLines=True)` just after.
	"""
	newText = ""
	currentIndex = 0
	for a, b in intervals:
		newText += text[currentIndex:a]
		currentIndex = b
	newText += text[currentIndex:]
	return newText

def removeListIntervals(l, intervals):
	"""
		This function will remove portions of text according to string intervals.
		You have to apply `text = reduceBlank(text, keepNewLines=True)` just after.

		:example:
		>>> removeListIntervals(['a', 'b', 'c', 'd', 'e'], [(1, 2), (3, 4)])
		['a', 'c', 'e']
	"""
	newL = []
	currentIndex = 0
	for a, b in intervals:
		newL += l[currentIndex:a]
		currentIndex = b
	newL += l[currentIndex:]
	return newL

def getListIntervals(l, intervals):
	newL = []
	for a, b in intervals:
		newL += l[a:b]
	return newL

def findMenu\
(
	lines,
	meanTokenCount=2.2,
	jumpMaxDiff=0.8,
	lineMaxLength=28,
	allowPunct=True,
	fistWordMustHaveAnUpperCase=False,
	blockSizeMin=1,
	blockSizeMax=300,
	punctAsWord=True,
):
	intervals = []
	a = None
	b = None
	currentMeanTokenCount = None
	for lineIndex in range(len(lines)):
		line = lines[lineIndex]
		weTakeThisLine = True
		if len(line) >= lineMaxLength:
			weTakeThisLine = False
		else:
				# not allowNonStartWithUppercase and (not re.match("[A-Z]", line[0])):
			punctMarker = "__:__"
			if not punctAsWord:
				punctMarker = " "
			line = re.sub("[^a-zA-Z ]", " " + punctMarker + " ", line)
			if not allowPunct and punctMarker in line:
				weTakeThisLine = False
			else:
				line = reduceBlank(line)
				tokens = line.split(" ")
				if fistWordMustHaveAnUpperCase:
					for token in tokens:
						if re.match(".*[a-zA-Z].*", token):
							if not re.match("[A-Z]", token[0]):
								weTakeThisLine = False
							break
				if weTakeThisLine:
					if a is not None and len(tokens) > meanTokenCount + jumpMaxDiff:
						weTakeThisLine = False
					else:
						if currentMeanTokenCount is None:
							currentMeanTokenCount = len(tokens)
						else:
							nbLines = lineIndex - a
							currentMeanTokenCount = (currentMeanTokenCount * nbLines + len(tokens)) / (nbLines + 1)
						if currentMeanTokenCount > meanTokenCount:
							weTakeThisLine = False
		if weTakeThisLine and (a is None or (lineIndex - a) <= blockSizeMax):
			if a is None:
				a = lineIndex
			else:
				b = lineIndex
		else:
			if a is not None and b is None:
				b = a
			if a is not None and b is not None:
				intervals.append((a, b + 1))
			a = None
			b = None
			currentMeanTokenCount = None
	# In case we reach the end:
	if a is not None and b is None:
		b = a
	if a is not None and b is not None:
		intervals.append((a, b + 1))
	# We remove all too big or too small intrevals:
	newIntervals = []
	for a, b in intervals:
		diff = b - a
		if diff >= blockSizeMin and diff <= blockSizeMax:
			newIntervals.append((a, b))
	intervals = newIntervals
	return intervals