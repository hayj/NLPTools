from nlptools.test.utils import *
from nlptools.tokenizer import *
from systemtools.basics import *
from nlptools.pipeline1 import pipeline as pipelinev1


def normalTest():
	(oneLineTexts, multiLinesTexts) = getTestTexts(oneLineFilter="Tokenization and unknown tokens")
	for text in oneLineTexts:
		print(text)
		print("### preprocessed text ###")
		text = pipelinev1.preprocess(text)
		print(text)
		for wordTokenizer in WORD_TOKENIZER:
			print("###" + wordTokenizer.name + "###")
			sentences = sentenceTokenize(text, wordTokenizer=wordTokenizer)
			for i in range(len(sentences)):
				sentences[i] = " ".join(sentences[i])
			tokens = " | ".join(sentences)
			print(tokens)
		print("\n" * 2)

def testDataset():
	allUnknown = set()
	for dirname, text in textGenerator(limit=20):
		preprocessedText = pipelinev1.preprocess(text)
		tokenizedText = pipelinev1.tokenize(preprocessedText)
		taggedTokens = pipelinev1.tagTokensByType(tokenizedText)
		for sentences in taggedTokens:
			for token, theType in sentences:
				if theType == pipelinev1.TOKEN_TYPE.unknown:
					if token not in allUnknown:
						allUnknown.add(token)
						print(token)
		# printLTS(taggedTokens)
		print("\n" * 2)



def regexTest():
	a = 'unjust",wee and, ry,R,0,., .'
	a = re.sub(',([a-z"])', ", \g<1>", a)
	print(a)

if __name__ == '__main__':
	testA()