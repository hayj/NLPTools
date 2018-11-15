# pew in st-venv python ~/Workspace/Python/Utils/NLPTools/nlptools/pipeline.py


from nlptools.emojinormalizer import *
from nlptools import preprocessing
from nlptools.pipeline1 import newscleaner
from nlptools.tokenizer import *
from systemtools.basics import *
from systemtools.logger import *
from nlptools.pipeline1.utils import *


def pipelinev1(text, logger=None, verbose=True):
	text = preprocess(text, logger=logger, verbose=verbose)
	text = newscleaner.precleanv1(text, logger=logger, verbose=verbose)
	text = tokenize(text, logger=logger, verbose=verbose)
	text = tagTokensByType(text, logger=logger, verbose=verbose)
	text = cleanTokens(text, logger=logger, verbose=verbose)
	text = newscleaner.postcleanv1(text, logger=logger, verbose=verbose)
	text = removeTokenType(text)
	if newscleaner.isNewsValid(text):
		return text
	else:
		return None


def preprocess(text, logger=None, verbose=True):
	# We first preprocess the text:
	preprocessedText = preprocessing.preprocess\
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

    	doTokenizingHelp=True,
	)
	return preprocessedText

def tokenize(preprocessedText, logger=None, verbose=True):
	# Then we tokenize all sentences and words:
	tokenizedText = sentenceTokenize\
	(
		preprocessedText,
		wordTokenizer=WORD_TOKENIZER.spacy,
		logger=logger,
		verbose=verbose,
	)

	return tokenizedText


# def test():
# 	for wordTokenizer in WORD_TOKENIZER:
# 		tokenizedText = sentenceTokenize\
# 		(
# 			preprocessedText,
# 			wordTokenizer=wordTokenizer,
# 			logger=logger,
# 			verbose=verbose,
# 		)
# 		# Here just for debugging:
# 		if weAreBefore("31/10/2018"):
# 			if tokenizedText is not None:
# 				for sentence in tokenizedText:
# 					for word in sentence:
# 						if " " in word:
# 							logError("We found a space in a word!!!", logger)
# 		else:
# 			logError("Please delete this debug bloc....")


		
# 		if tokenizedText is None:
# 			print(tokenizedText)
# 		else:
# 			reconstructedText = ""
# 			for sentence in tokenizedText:
# 				for word in sentence:
# 					reconstructedText += word + " "
# 				reconstructedText += "\n"
# 			reconstructedText = reconstructedText[:-1]
# 			print("#" * 10 + wordTokenizer.name + "#" * 10)
# 			print(reconstructedText)
# 	print()



def tagTokensByType(tokens, logger=None, verbose=True):
	if tokens is None:
		return None
	if len(tokens) == 0:
		return []
	if isinstance(tokens[0], list):
		sentences = tokens
		newSentences = []
		for sentence in sentences:
			newSentences.append(tagTokensByType(sentence))
		return newSentences
	newTokens = []
	for current in tokens:
		newTokens.append((current, tokenType(current)))
	return newTokens

def sentenceToWordTokenization(tokens):
	return list(itertools.chain(*tokens))

def tokenTypeReplace(token, theType):
	if theType == TOKEN_TYPE.price:
		return "__P_R_I_C_E__"
	elif theType == TOKEN_TYPE.num:
		return "__N_U_M_" + str(len(token)) + "__"
	elif theType == TOKEN_TYPE.unknown:
		return None
	elif theType == TOKEN_TYPE.url:
		return DEFAULT_URL_MARKER
	elif theType == TOKEN_TYPE.email:
		return "__E_M_A_I_L__"
	elif theType == TOKEN_TYPE.punct2:
		return None
	elif theType == TOKEN_TYPE.none:
		return None
	elif theType == TOKEN_TYPE.currency:
		return None
	elif theType == TOKEN_TYPE.social:
		return None
	elif theType == TOKEN_TYPE.function:
		return None
	else:
		return token

def regexSquareBracketedEscape(text):
	text = text.replace("]", "\\]")
	text = text.replace("^", "\\^")
	text = text.replace("-", "\\-")
	return text

def cleanTokens(taggedTokens, logger=None, verbose=True):
	"""
		Here the only allowed type to appear more than 1 time consecutivly is alpha.
		
		You can pass sentences (list) of words (list), so a list of lists, or just words (list).
		It can be already tagged or not
	"""
	if taggedTokens is None or len(taggedTokens) == 0:
		logError("taggedTokens is None or empty", logger, verbose=verbose)
		return taggedTokens
	if not isinstance(taggedTokens, list):
		logError("taggedTokens is not a list", logger, verbose=verbose)
		return None
	try:
		if isinstance(taggedTokens[0], list):
			# Here we have sentences so we call recursively:
			sentences = taggedTokens
			newSentences = []
			for sentence in sentences:
				currentNewSentence = cleanTokens(sentence, logger=logger, verbose=verbose)
				if currentNewSentence is not None and len(currentNewSentence) > 0:
					newSentences.append(currentNewSentence)
			return newSentences
		else:
			def initCount():
				counts = {}
				for current in TOKEN_TYPE:
					counts[current] = 0
				return counts
			if not isinstance(taggedTokens[0], tuple):
				raise Exception("taggedTokens must be tagged by tagTokensByType")
			newTaggedTokens = []
			counts = initCount()
			for (token, theType) in taggedTokens:
				token = tokenTypeReplace(token, theType)
				if token is not None:
					if theType == TOKEN_TYPE.alpha:
						counts = initCount()
						newTaggedTokens.append((token, theType))
					else:
						counts[theType] += 1
						if counts[theType] <= 1:
							newTaggedTokens.append((token, theType))
			return newTaggedTokens
	except Exception as e:
		logException(e, logger, verbose=verbose)
		return None


def removeTokenType(typedSentences):
	sentences = []
	for typedTokens in typedSentences:
		currentTokens = []
		for token, _ in typedTokens:
			currentTokens.append(token)
		sentences.append(currentTokens)
	return sentences


def tokenType(token):
	if token is None or len(token) == 0:
		return TOKEN_TYPE.none
	else:
		punctChars1 = "-_./:!?;,()*—"
		punctChars2 = "<>[]|{}~^"
		quoteChars = "'\""
		currencyChars = "$€£¥"
		socialChars = "@#"
		functionChars = "&%+="
		if len(token) == 1:
			if re.match("[a-zA-Z]", token):
				return TOKEN_TYPE.alpha
			elif re.match("[" + regexSquareBracketedEscape(punctChars1) + "]", token):
				return TOKEN_TYPE.punct1
			elif re.match("[" + regexSquareBracketedEscape(punctChars2) + "]", token):
				return TOKEN_TYPE.punct2
			elif re.match("[0-9]", token):
				return TOKEN_TYPE.num
			elif re.match("[" + socialChars + "]", token):
				return TOKEN_TYPE.social
			elif re.match("[" + functionChars + "]", token):
				return TOKEN_TYPE.function
			elif re.match("[" + quoteChars + "]", token):
				return TOKEN_TYPE.quote
			elif re.match("[" + currencyChars + "]", token):
				return TOKEN_TYPE.currency
			elif isEmoji(token):
				return TOKEN_TYPE.emoji
		else:
			if re.match(".*[a-zA-Z].*", token):
				if token.startswith("@"):
					return TOKEN_TYPE.atreply
				elif token.startswith("#"):
					return TOKEN_TYPE.hashtag
				else:
					if re.match(".*[^a-zA-Z0-9-'_.&/ ].*", token):
						return TOKEN_TYPE.unknown
					elif re.match(".*[0-9].*", token):
						return TOKEN_TYPE.alphanum
					else:
						return TOKEN_TYPE.alpha
			elif re.match("^[0-9]+(([., ][0-9]+)+)?$", token):
				return TOKEN_TYPE.num
			# Here the regex of a price, a currency is optional at the beggining and the end but you will have one of two because TOKEN_TYPE.num was not returned:
			elif re.match("^[" + currencyChars + "]?" + "[0-9]+(([., ][0-9]+)+)?" + "[" + currencyChars + "]?$", token): 
				return TOKEN_TYPE.price
			elif token == '...':
				return TOKEN_TYPE.punct1
			elif token == "``" or token == "''":
				return TOKEN_TYPE.quote
		return TOKEN_TYPE.unknown


