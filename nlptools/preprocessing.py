
# pew in st-venv python ~/Workspace/Python/Utils/NLPTools/nlptools/preprocessing.py

import re
from enum import Enum
from multiprocessing import Lock
from systemtools.location import *
from systemtools.file import *
from systemtools.basics import * # stripAccents, reduceBlank
from datatools.htmltools import *
from datatools.url import *
from unidecode import unidecode
import html
from nlptools.utils import *
from nlptools.emojinormalizer import *

def softPreprocessV1(text, **kwargs):
	"""
		Used for News dataset
	"""
	return preprocess\
	(
		text,
		removeHtml=True,
		doReduceBlank=True,
		keepNewLines=True,
		**kwargs
	)

def softPreprocess(text, **kwargs):
	return preprocess\
	(
		text,
		removeHtml=True,
		doReduceBlank=True,
		keepNewLines=True,
		**kwargs
	)

def hardPreprocess(text, doRemoveUrls=False, doLower=False, **kwargs):
	"""
		You can use extractUrls before calling this function
	"""
	pass # TODO
	# return preprocess\
	# (
	# 	text,
	# 	removeHtml=True,
	# 	doQuoteNormalization=True,
	# 	doReduceBlank=True,
	# 	keepNewLines=True,
	# 	doUnidecode=True,
	# 	doRemoveUrls=doRemoveUrls,
	# 	doLower=doLower,
	# 	unescapeHtml=True,
	# 	doBadlyEncoded=True,
	# 	**kwargs
	# )



def tweetSoftPreprocess(*args, **kwargs):
	return softPreprocessing(*args, **kwargs)

def tweetHardPreprocess(*args, **kwargs):
	return hardPreprocessing(*args, **kwargs)

def lower(theString):
	return theString.lower()

def normalizeQuote(texts):
	"""
		Tested
	"""
	if not isinstance(texts, list):
		texts = [texts]
	newTexts = []
	for current in texts:
		current = re.sub("[‘’`']{2,}", '"', current)
		current = current.replace("”", '"')
		current = current.replace("“", '"')
		current = current.replace("`", "'")
		current = current.replace("’", "'")
		current = current.replace("‘", "'")
		newTexts.append(current)
	texts = newTexts
	if len(texts) == 1:
		return texts[0]
	else:
		return texts

def containsHtml(text):
	if text is None:
		return False
	else:
		openingMarkupPattern = r"<[^<]+>"
		closingMarkupPattern = r"</[^<]+>"
		if re.search(openingMarkupPattern, text) and re.search(closingMarkupPattern, text):
			return True
		brPattern = r"< *br */? *>"
		if re.search(brPattern, text):
		 	return True
		return False

def reduceCharSequences(text, maxLength=3):
	if text is None:
		return None
	else:
		search = r"(.)\1{" + str(maxLength) + ",}"
		replace = r''
		for current in range(maxLength):
			replace += r'\1'
		return re.sub(search, replace, text)     

def badlyEncodedPreprocess(text, logger=None, verbose=True):
	if text is None:
		return None
	if len(text) == 0:
		return text
	text = text.replace("<U+0091>", "'")
	text = text.replace("", "'")
	text = text.replace("<U+0092>", "'")
	text = text.replace("", '"')
	text = text.replace("<U+0093>", '"')
	text = text.replace("", '"')
	text = text.replace("<U+0094>", '"')
	text = re.sub("<U\+\d+>", " ", text)
	text = re.sub("�", " ", text)
	text = re.sub("ïṡẄ", " ", text)
	return text

specialMapMRSingleton = None
def specialMap(text, logger=None, verbose=True):
	global specialMapMRSingleton
	if specialMapMRSingleton is None:
		repl = {"…": "...", " ": " "}
		specialMapMRSingleton = MultiReplacer(repl, logger=logger, verbose=verbose)
	return specialMapMRSingleton.replace(text)

compiledNotAllowedRegex = None
def preprocess\
(
	text, logger=None, verbose=True,

	removeHtml=False,

	doQuoteNormalization=False,

	doReduceBlank=False,
	keepNewLines=True,

	stripAccents=False, # Replace all accent
	doUnidecode=False, # Replace all non-ascii char to its equivalent, warning: "¤" will be replaced by "?", so it's better to use stripAccents and replaceUnknownChars together instead of doUnidecode.

	noneNonStrings=False,
	noneEmptyStrings=True,

	doRemoveUrls=False,

	doLower=False,

	unescapeHtml=False,

	doBadlyEncoded=False,

	doReduceCharSequences=False,
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

    doSpecialMap= False,

    doNormalizeEmojis= False,
):
	"""
		This function will convert all special chars (accents...) to ascii equivalent using unidecode. It will replace special usage of `` ´´ by it's equivalent, will replace '' by a doublequote etc. This function will also reduce blanks to unique space but will keep new lines. It will strip the string, remove the html.
		You can path a list of string or 

		WARNING: a backslash is considered an unknown char and will be deleted replaceUnknownChars=True, pls do a unit test to handle it properly.

		Ordering notes:
		 * We do insert urls at the very end
		 * We do reduce blank at the very and because other preprocessing can introduce spaces
		 * We do 
	"""
	global compiledNotAllowedRegex
	if text is None:
		return None
	elif isinstance(text, str):
		try:
			if doBadlyEncoded:
				text = badlyEncodedPreprocess(text)
			if removeHtml and containsHtml(text):
				text = html2Text(text)
			urls = None
			if doRemoveUrls:
				text = removeUrls(text)
			else:
				(text, urls) = extractUrls(text)
			if unescapeHtml:
				text = html.unescape(text)
			if doNormalizeEmojis:
				text = normalizeEmojis(text, logger=logger, verbose=verbose)
			if doQuoteNormalization:
				text = normalizeQuote(text)
			if doUnidecode:
				text = unidecode(text)
			elif stripAccents:
				text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
			if doSpecialMap:
				text = specialMap(text)

			# We remove special chars (not in punct etc):
			allowedChars = "a-zA-Z0-9-_ \n"
			punctChars = ["./:!?;,()", "<>[\]*—", "|{}~^"]
			quoteChars = ["'\""]
			currencyChars = ["$€£"]
			socialChars = ["@#"]
			functionChars = ["&%", "+="]
			# smileyChars = ["()='<>-:|^;_,/", "*{}[]", "\\"] # TODO ?
			if replaceUnknownChars:
				if compiledNotAllowedRegex is None:
					allowedChars = allowedChars \
					+ "".join(punctChars) \
					+ "".join(quoteChars) \
					+ "".join(currencyChars) \
					+ "".join(socialChars) \
					+ "".join(functionChars)
					allowedRegex = "[" + allowedChars + "]"
					notAllowedRegex = "[^" + allowedChars + "]"
					# print(notAllowedRegex)
					compiledNotAllowedRegex = re.compile(notAllowedRegex)
				text = compiledNotAllowedRegex.sub(unknownReplacer, text)

			# We handle punct and others known chars:
			for level, charsList, replacer in \
			[
				(replacePunctLevel, punctChars, punctReplacer),
				(replaceQuoteLevel, quoteChars, quoteReplacer),
				(replaceCurrencyLevel, currencyChars, currencyReplacer),
				(replaceSocialLevel, socialChars, socialReplacer),
				(replaceFunctionLevel, functionChars, functionReplacer),
			]:
				if level is not None:
					# print("aaaaaaaaaaaa")
					if level > len(charsList):
						level = len(charsList)
					elif level < 0:
						level = 0
					removeRegex = ""
					for i in range(level, len(charsList)):
						removeRegex += charsList[i]
					if len(removeRegex) > 0:
						# print(text)
						text = re.sub("[" + removeRegex + "]", replacer, text)
						# print(text)

			if doReduceCharSequences:
				text = reduceCharSequences(text, maxLength=charSequencesMaxLength)
			if doLower:
				text = text.lower()
			if doReduceBlank:
				text = reduceBlank(text, keepNewLines=keepNewLines)
			if not doRemoveUrls:
				text = insertUrls(text, urls)
		except Exception as e:
			if text is None:
				message = None
			else:
				message = str(text)[:100]
			logException(e, logger=logger, message=message, verbose=verbose)
		if noneEmptyStrings and len(text) == 0:
			text = None
		return text
	else:
		logError("text must be a list or a str.",
			logger=logger, verbose=verbose)
		if noneNonStrings:
			return None
		else:
			return text

def preprocessTest():
	filesPath = sortedGlob(execDir(__file__) + "/test/testdata/preprocessing/*")
	for path in filesPath:
		text = fileToStr(path)
		print("-" * 50)
		print("--- ORIGINAL TEXT OF " + decomposePath(path)[3] + " ---")
		printLTS(text)
		print("\n" * 2) ; input()
		print("--- soft ---")
		printLTS(softPreprocess(text))
		print("\n" * 2) ; input()
		print("--- hard ---")
		printLTS(hardPreprocess(text))
		print("\n" * 2) ; input()
		print("\n" * 2)

if __name__ == '__main__':
	preprocessTest()
