# pew in st-venv python ~/Workspace/Python/Utils/NLPTools/nlptools/pipeline1/test/pipelinetest.py



from nlptools.emojinormalizer import *
from nlptools.preprocessing import *
from nlptools.tokenizer import *
from systemtools.basics import *
from nlptools.pipeline1 import pipeline as pipelinev1
from nlptools.test.utils import *

def getEmojiString():
	path = getExecDir(__file__) + "/test/testdata/pipeline/texts.txt"
	texts = fileToStr(path)
	texts = texts.split("\n")
	emojiString = [x for x in texts if "emoji" in x]
	return emojiString

def emojisTest():
	texts = getEmojiString()
	for text in texts:
		print(text)
		text = normalizeEmojis(text)
		print(text)
		print()
		print()



def testTagging():
	import itertools
	(oneLineTexts, multiLinesTexts) = getTestTexts()
	for text in oneLineTexts + multiLinesTexts:
		tokens = pipelineV1(text)
		tokens = tagTokensByType(tokens)
		print(text)
		printLTS(tokens)
		# if tokens is None:
		# 	logError("tokens is None")
		# else:
		# 	for current in tokens:
		# 		print(current)
		print("\n" * 5)

def testTagCleaning():
	(oneLineTexts, multiLinesTexts) = getTestTexts()
	for text in oneLineTexts + multiLinesTexts:
		tokens = pipelineV1(text)
		taggedTokens = tagTokensByType(tokens)
		cleanedTaggedTokens = cleanTokens(taggedTokens)
		print(text)
		cleanedText = ""
		for sentence in cleanedTaggedTokens:
			for token, theType in sentence:
				cleanedText += token + " "
			cleanedText += "| "
		print(cleanedText)
		# printLTS(taggedTokens)
		# printLTS(cleanedTaggedTokens)
		# print("\n" * 3)
		print("\n" * 2)

def test():
	(oneLineTexts, multiLinesTexts) = getTestTexts()
	for text in oneLineTexts + multiLinesTexts:
		pipelineV1(text)

def seeAllTypes():
	allUnknown = set()
	for dirname, text in textGenerator(seed=15, limit=200):
		print(">>>>>>>>>>>>" + dirname)
		# print(text)
		# continue
		preprocessedText = pipelinev1.preprocess(text)
		tokenizedText = pipelinev1.tokenize(preprocessedText)
		taggedTokens = pipelinev1.tagTokensByType(tokenizedText)
		for sentences in taggedTokens:
			for token, theType in sentences:
				if theType == pipelinev1.TOKEN_TYPE.unknown:
					if token not in allUnknown:
						allUnknown.add(token)
						print(token)
						# if 'Trump' in text and 'they' in text:
						# 	print(text)
		# printLTS(taggedTokens)
		# print("\n" * 2)




def seePipelinev1():
	for dirname, text in threadedTextGenerator(seed=22, limit=200):
		print(">>>>>>>>>>>> " + dirname)
		text = text[:30] + " " + "abc" * 100 + " " + text[30:]
		tokens = pipelinev1.pipelinev1(text)
		paragraph = sentencesToParagraph(tokens)
		print(text)
		print()
		print(paragraph)
		print()
		print()
		print()
		input()



if __name__ == '__main__':
	# test()
	# all = []
	# for current in fileToStrList(sortedGlob(getExecDir(__file__) + "/data/*")[0]):
	# 	all.append(current[1:])
	# for current in all:
	# 	print(current)
	seePipelinev1()