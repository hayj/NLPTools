# pew in st-venv python ~/Workspace/Python/Utils/NLPTools/nlptools/pipeline.py


from emojinormalizer import *
from nlptools.preprocessing import *
from nlptools.tokenizer import *
from systemtools.basics import *


def pipelineV1(text, logger=None, verbose=True):
	# We first preprocess the text:
	preprocessedText = preprocess\
	(
		text, logger=logger, verbose=verbose,

		removeHtml=True,

		doQuoteNormalization=True,

		doReduceBlank=True,
		keepNewLines=True,

		stripAccents=True,
		doUnidecode=False,

		noneNonStrings=True,
		noneEmptyStrings=True,

		doRemoveUrls=True,

		doLower=False,

		unescapeHtml=True,

		doBadlyEncoded=True,

		doReduceCharSequences=True,
		charSequencesMaxLength=3,

		replaceUnknownChars=False,
		unknownReplacer=" ",

		replacePunctLevel=None,
		punctReplacer=" ",
		
		replaceQuoteLevel=None,
		quoteReplacer=" ",
		
		replaceCurrencyLevel=None,
		currencyReplacer=" ",
		
		replaceSocialLevel=None,
		socialReplacer=" ",

		replaceFunctionLevel=None,
		functionReplacer=" ",

		doSpecialMap=True,

    	doNormalizeEmojis=True,
	)
	# Then we tokenize all sentences and words:
	

	print(text)
	print(preprocessedText)

	# for wordTokenizer in WORD_TOKENIZER:
	# 	tokenizedText = sentenceTokenize\
	# 	(
	# 		preprocessedText,
	# 		wordTokenizer=wordTokenizer,
	# 		logger=logger,
	# 		verbose=verbose,
	# 	)
	# 	# Here just for debugging:
	# 	if weAreBefore("30/10/2018"):
	# 		if tokenizedText is not None:
	# 			for sentence in tokenizedText:
	# 				for word in sentence:
	# 					if " " in word:
	# 						logError("We found a space in a word!!!", logger)
	# 	else:
	# 		logError("Please delete this debug bloc....")


		
	# 	if tokenizedText is None:
	# 		print(tokenizedText)
	# 	else:
	# 		reconstructedText = ""
	# 		for sentence in tokenizedText:
	# 			for word in sentence:
	# 				reconstructedText += word + " "
	# 			reconstructedText += "\n"
	# 		reconstructedText = reconstructedText[:-1]
	# 		print("#" * 10 + wordTokenizer.name + "#" * 10)
	# 		print(reconstructedText)
	print()

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

def getTestTexts():
	path = getExecDir(__file__) + "/test/testdata/pipeline/texts.txt"
	texts = fileToStr(path)
	texts = re.compile("\n+-+\n+").split(texts)
	oneLineTexts = texts[0].split("\n")
	multiLinesTexts = texts[1:]
	newOneLineTexts = []
	for current in oneLineTexts:
		if not (current is None or len(current) == 0 or current.startswith("###")):
			newOneLineTexts.append(current)
	oneLineTexts = newOneLineTexts
	return (oneLineTexts, multiLinesTexts)

def test():
	(oneLineTexts, multiLinesTexts) = getTestTexts()
	for text in oneLineTexts + multiLinesTexts:
		pipelineV1(text)

if __name__ == '__main__':
	# test()
	# all = []
	# for current in fileToStrList(sortedGlob(getExecDir(__file__) + "/data/*")[0]):
	# 	all.append(current[1:])
	# for current in all:
	# 	print(current)
	test()