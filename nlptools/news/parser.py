# pew in st-venv python ~/Workspace/Python/Utils/NLPTools/nlptools/pipeline.py


from nlptools.emojinormalizer import *
from nlptools import preprocessing
from nlptools.news import cleaner
from nlptools.tokenizer import *
from systemtools.basics import *
from systemtools.printer import *
from systemtools.logger import *
from nlptools.news.utils import *
from newstools.goodarticle.utils import *

__swSingleton = None
def swRatio(tokens):
    global __swSingleton
    if __swSingleton is None:
        __swSingleton = {'the', 'to', 'and', 'of', 'a', 'in', 'that', 'is', 'for', 'i', 'it', 'on', 'with', 'was', 'as', 'he', 'be', 'are', 'this', 'at', 'you', 'have', 'not', 'from', 'by', 'but', 'they', 'we', 'an', 'has', 'said', 'his', 'or', 'who', 'will', 'about', 'one', 'do', 'more', 'had', 'their', 'all', 'so', 'she', 'can', 'new', 'when', 'there', 'my', 'her', 'up', 'which', 'what', 'would', 'were', 'if', 'out', 'like', 'people', 'been', 'its', 'than', 'just', 'no', 'also', 'some', 'me', 'other', 'time', 'them', 'into', 'your', 'how', 'year', 'our', 'after', 'because', 'even', 'could', 'over', 'now', 'first', 'two', 'him', 'did', 'only', 'then', 'most', 'get', 'many', 'years', 'see', 'us', 'any', 'where', 'does'}
    if tokens is None or len(tokens) == 0:
        return 0.0
    else:
        if isinstance(tokens[0], list):
            tokens = flattenLists(tokens)
        if tokens is None or len(tokens) == 0:
            return 0.0
        else:
            c = 0
            for token in tokens:
                if token.lower() in __swSingleton:
                    c += 1
            return c / len(tokens)

def isNewsValid(sentences, minTokens=25, minSentences=3, minSentencesLengthMean=4, maxSentencesLengthMean=40, minSWRatio=0.29):
	if sentences is None or len(sentences) == 0:
		return False
	else:
		if len(sentences) < minSentences:
			return False
		if len(flattenLists(sentences)) < minTokens:
			return False
		sentencesLengthMean = [len(sentence) for sentence in sentences]
		sentencesLengthMean = sum(sentencesLengthMean) / len(sentencesLengthMean)
		if sentencesLengthMean < minSentencesLengthMean or sentencesLengthMean > maxSentencesLengthMean:
			return False
		if swRatio(sentences) < minSWRatio:
			return False
		return True

def parseNews(text, logger=None, verbose=True):
	text = newsPreclean(text)
	if not isGoodArticle(text):
		return (None, None)
	text = preprocess(text, logger=logger, verbose=verbose)
	text = cleaner.precleanv1(text, logger=logger, verbose=verbose)
	tokens = tokenize(text, logger=logger, verbose=verbose)
	tokens = tagTokens(tokens, logger=logger, verbose=verbose)
	tokens = cleanTokens(tokens, logger=logger, verbose=verbose)
	tokens = cleaner.postcleanv1(tokens, logger=logger, verbose=verbose)
	tokens = removeTokenType(tokens)
	if isNewsValid(tokens):
		return (text, tokens)
	else:
		return (None, None)

# def parseTitle(text, logger=None, verbose=True):
# 	if text is None:
# 		return None
# 	text = preprocess(text, logger=logger, verbose=verbose)
# 	text = tokenize(text, logger=logger, verbose=verbose)
# 	text = tagTokensByType(text, logger=logger, verbose=verbose)
# 	text = cleanTokens(text, logger=logger, verbose=verbose)
# 	text = removeTokenType(text)
# 	return text


def removeTokenType(l):
	if isinstance(l, list):
		newL = []
		for current in l:
			newL.append(removeTokenType(current))
		return newL
	elif isinstance(l, tuple):
		return l[0]
	else:
		raise Exception("Unexpected arg type")

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


def tagTokens(tokens, logger=None, verbose=True, **kwargs):
	if tokens is None:
		return None
	elif len(tokens) == 0:
		return []
	elif isinstance(tokens, list):
		newTokens = []
		for current in tokens:
			newTokens.append(tagTokens(current, logger=logger, verbose=verbose))
		return newTokens
	elif isinstance(tokens, str):
		return (tokens, tokenType(tokens, logger=logger, verbose=verbose, **kwargs))


allowedTokenTypes = \
{
	TOKEN_TYPE.alpha_strict: None,
	TOKEN_TYPE.alpha_num: None,
	TOKEN_TYPE.mixed_strict: None,
	TOKEN_TYPE.punct1: None,
	TOKEN_TYPE.atreply: None,
	TOKEN_TYPE.hashtag: None,
	TOKEN_TYPE.known_emoji: None,
	TOKEN_TYPE.quote: None,
	TOKEN_TYPE.alpha_accent: lambda token: stripAccents(token),
	TOKEN_TYPE.price: lambda token: "__price_" + str(len(str(abs(int(getFirstNumber(token)))))) + "__",
	TOKEN_TYPE.int: lambda token: "__int_" + str(len(str(abs(int(token))))) + "__",
	TOKEN_TYPE.float: lambda token: "__float_" + str(len(str(abs(int(float(token)))))) + "__",
	TOKEN_TYPE.url: "__url__",
	TOKEN_TYPE.email: "__email__",
	TOKEN_TYPE.netloc: "__netloc__",
}

def replaceToken(token, tokenType, logger=None, verbose=True):
	# We do not allow this token type:
	if tokenType not in allowedTokenTypes:
		return None
	# We allow it:
	elif allowedTokenTypes[tokenType] is None:
		return token
	# We replace it:
	else:
		if callable(allowedTokenTypes[tokenType]):
			try:
				return allowedTokenTypes[tokenType](token)
			except Exception as e:
				logException(e, logger, verbose=verbose)
				return None
		else:
			return allowedTokenTypes[tokenType]

def cleanTokens\
(
	l,
	allowedSequenceType={TOKEN_TYPE.alpha_strict, TOKEN_TYPE.mixed_strict},
	logger=None, verbose=True,
):
	if isinstance(l, list):
		if len(l) == 0:
			return None
		elif isinstance(l[0], tuple):
			newL = []
			notAllowedCount = 0
			for current in l:
				(token, tokenType) = current
				token = replaceToken(token, tokenType, logger=logger, verbose=verbose)
				if token is not None:
					if tokenType in allowedSequenceType:
						newL.append((token, tokenType))
						notAllowedCount = 0
					elif notAllowedCount == 0:
						newL.append((token, tokenType))
						notAllowedCount += 1
					else:
						notAllowedCount += 1
			if len(newL) == 0:
				return None
			else:
				return newL
		else:
			newL = []
			for current in l:
				current = cleanTokens(current, allowedSequenceType=allowedSequenceType,
					logger=logger, verbose=verbose)
				if current is not None:
					newL.append(current)
			return newL			
	else:
		raise Exception("Please give a list of words or a list of sentences")



# def cleanTokens(taggedTokens, maxTokenLength=200, logger=None, verbose=True):
# 	"""
# 		Here the only allowed type to appear more than 1 time consecutivly is alpha.
		
# 		You can pass sentences (list) of words (list), so a list of lists, or just words (list).
# 		It can be already tagged or not
# 	"""
# 	if taggedTokens is None or len(taggedTokens) == 0:
# 		# logError("taggedTokens is None or empty", logger, verbose=verbose)
# 		return taggedTokens
# 	if not isinstance(taggedTokens, list):
# 		logError("taggedTokens is not a list", logger, verbose=verbose)
# 		return None
# 	try:
# 		if isinstance(taggedTokens[0], list):
# 			# Here we have sentences so we call recursively:
# 			sentences = taggedTokens
# 			newSentences = []
# 			for sentence in sentences:
# 				currentNewSentence = cleanTokens(sentence, logger=logger, verbose=verbose)
# 				if currentNewSentence is not None and len(currentNewSentence) > 0:
# 					newSentences.append(currentNewSentence)
# 			return newSentences
# 		else:
# 			def initCount():
# 				counts = {}
# 				for current in TOKEN_TYPE:
# 					counts[current] = 0
# 				return counts
# 			if not isinstance(taggedTokens[0], tuple):
# 				raise Exception("taggedTokens must be tagged by tagTokensByType")
# 			newTaggedTokens = []
# 			counts = initCount()
# 			for (token, theType) in taggedTokens:
# 				token = replaceToken(token, theType)
# 				if token is not None:
# 					if len(token) <= maxTokenLength:
# 						if theType == TOKEN_TYPE.alpha:
# 							counts = initCount()
# 							newTaggedTokens.append((token, theType))
# 						else:
# 							counts[theType] += 1
# 							if counts[theType] <= 1:
# 								newTaggedTokens.append((token, theType))
# 			return newTaggedTokens
# 	except Exception as e:
# 		logException(e, logger, verbose=verbose)
# 		return None



def tokenType(token, logger=None, verbose=True):
	if token is None or len(token) == 0:
		return TOKEN_TYPE.none
	else:
		if token in {',', ')', '...', ';', '-', '!', ':', '?', '.', '('}:
			return TOKEN_TYPE.punct1
		if len(token) > 60:
			return TOKEN_TYPE.unknown
		elif len(token) == 1:
			if token in set("<>[]|{}~^_/*—"):
				return TOKEN_TYPE.punct2
			elif token in set("'\""):
				return TOKEN_TYPE.quote
			elif token in set("$€£¥"):
				return TOKEN_TYPE.currency
			elif token in set("@#"):
				return TOKEN_TYPE.social
			elif token in set("&%+="):
				return TOKEN_TYPE.function
			elif re.match("^[a-zA-Z]$", token):
				return TOKEN_TYPE.alpha_strict
			elif re.match("^[a-zA-Z]$", stripAccents(token)):
				return TOKEN_TYPE.alpha_accent
			elif representsInt(token):
				return TOKEN_TYPE.int
			elif isKnownEmoji(token):
				return TOKEN_TYPE.known_emoji
			elif isEmoji(token):
				return TOKEN_TYPE.emoji
		else:
			if re.search("[a-zA-Z]", token) is not None:
				if re.match("^[a-zA-Z]*$", token):
					return TOKEN_TYPE.alpha_strict
				elif re.match("^[a-zA-Z]*$", stripAccents(token)):
					return TOKEN_TYPE.alpha_accent
				elif re.match("^[a-zA-Z0-9]*$", token):
					return TOKEN_TYPE.alpha_num
				elif re.match("^[a-zA-Z][a-zA-Z-.]*[a-zA-Z]\.?$", token):
					if (len(token) > 4 and token[-4:] in netLocEnd3) or (len(token) > 3 and token[-3:] in netLocEnd2):
						return TOKEN_TYPE.netloc
					else:
						return TOKEN_TYPE.mixed_strict
				elif re.match("^[a-zA-Z-.0-9_]*$", stripAccents(token)):
					return TOKEN_TYPE.mixed
				elif re.match("^@[a-zA-Z-.0-9_]+$", token):
					return TOKEN_TYPE.atreply
				elif re.match("^#[a-zA-Z-.0-9_]+$", token):
					return TOKEN_TYPE.hashtag
				elif re.match("^(?:http|ftp)s?://\S+$", token):
					return TOKEN_TYPE.url
				elif re.match("^[a-zA-Z0-9-._]+@[a-zA-Z0-9-._]+\.[a-z]{2,5}$", token):
					return TOKEN_TYPE.email
			elif representsInt(token):
				return TOKEN_TYPE.int
			elif representsFloat(token):
				return TOKEN_TYPE.float
			elif re.match("^[$€£¥][0-9]+(\.[0-9]+)?$", token) or re.match("^[0-9]+(\.[0-9]+)?[$€£¥]$", token):
				return TOKEN_TYPE.price
		return TOKEN_TYPE.unknown


if __name__ == '__main__':
	tokens = \
	[
		[
			"a", "1", "1", "@ooo", "iuhd", "!", ".", "rààà", "ytt"
		],
		[
			"a", "1", "@ooo",
		],
	]

	tokens = tagTokens(tokens)

	bp(tokens, 5)

	tokens = cleanTokens(tokens)

	bp(tokens, 5)