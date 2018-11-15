# coding: utf-8
# pew in st-venv python /home/hayj/Workspace/Python/Utils/NLPTools/nlptools/test/preprocessing.py

import os
import sys
sys.path.append('../')

import unittest
import doctest
from nlptools import preprocessing
from nlptools.preprocessing import *
from systemtools.location import *
from datatools.htmltools import *

# The level allow the unit test execution to choose only the top level test
mini = 1
maxi = 12
assert mini <= maxi

print("==============\nStarting unit tests...")

dataDir = getExecDir(__file__) + "/testdata/preprocessing"

if mini <= 0 <= maxi:
	class DocTest(unittest.TestCase):
		def testDoctests(self):
			"""Run doctests"""
			doctest.testmod(preprocessing)

if mini <= 1 <= maxi:
	class QuoteTest(unittest.TestCase):
		def test1(self):
			t = fileToStr(dataDir + "/strange-quote.txt")
			strangeQuotes = ["‘‘", "’’", "``", "''", "”", "“", "`", "’", "‘", "´´", "´"]
			for current in strangeQuotes:
				self.assertTrue(current in t)
			t = normalizeQuote(t)
			for current in strangeQuotes:
				self.assertTrue(current not in t)

if mini <= 2 <= maxi:
	class HtmlTest(unittest.TestCase):
		def test1(self):
			hasNotHtml = []
			for current in sortedGlob(dataDir + "/*hasn*html*"):
				hasNotHtml.append(fileToStr(current))
			for current in hasNotHtml:
				self.assertTrue(not containsHtml(current))
			hasHtml = []
			for current in sortedGlob(dataDir + "/*has-html*"):
				hasHtml.append(fileToStr(current))
			for current in hasHtml:
				# print(current)
				self.assertTrue(containsHtml(current))
		def test2(self):
			return
			hasHtml = []
			for current in sortedGlob(dataDir + "/*has-html*"):
				hasHtml.append(fileToStr(current))
			for current in hasHtml:
				print("\n" * 3 + "-" * 30)
				print(current)
				print()
				print("--")
				print()
				current = html2Text(current)
				print(current)

if mini <= 3 <= maxi:
	class HtmlTest(unittest.TestCase):
		def test1(self):
			hasNotHtml = []
			for current in sortedGlob(dataDir + "/*hasn*html*"):
				hasNotHtml.append(fileToStr(current))
			for current in hasNotHtml:
				self.assertTrue(not containsHtml(current))
			hasHtml = []
			for current in sortedGlob(dataDir + "/*has-html*"):
				hasHtml.append(fileToStr(current))
			for current in hasHtml:
				# print(current)
				self.assertTrue(containsHtml(current))
			self.assertTrue(containsHtml("""Good variety of great items.
<br>
Girls & boys clothes. Womens clothes. Dresser and recliner. Electronics. Some fish tank stuff. Rubbermaid type totes. Just too much to list.
<br>"""))
			self.assertTrue(not containsHtml(""" items. to list<brdsgd"""))
			self.assertTrue(containsHtml(""" items. to list<  br  /  >dsgd"""))
			content = softPreprocess(""" items. to list<br  >dsgd""")
			self.assertTrue("br" not in content)
			self.assertTrue("list" in content)
			self.assertTrue(len(content) > 10)

if mini <= 4 <= maxi:
	class CharSequenceTest(unittest.TestCase):
		def test1(self):
			print("CharSequenceTest")
			for current in \
			[
				("aaaa", "aaa"),
				("^sdsf$ù*ù('_è-t'ééééyhgfse", "^sdsf$ù*ù('_è-t'éééyhgfse"),
				("----fg", "---fg"),
				("--- -fg", "--- -fg"),
				("^^\"\"\"\"^^", "^^\"\"\"^^"),
				("aaaa", "aaa"),
			]:
				print(reduceCharSequences(current[0]))
				self.assertTrue(reduceCharSequences(current[0]) == current[1])

if mini <= 5 <= maxi:
	class Test5(unittest.TestCase):
		def test1(self):
			text = "œ°~$µ£[]().aé!#@<^^+&¤"
			result = preprocess\
			(
				text,
			)
			self.assertTrue(result == text)

			result = preprocess\
			(
				text + "aaaaaa",
				doReduceCharSequences=True,
			)
			self.assertTrue(result == "œ°~$µ£[]().aé!#@<^^+&¤aaa")

			result = preprocess\
			(
				text,
				stripAccents=True,
				replaceUnknownChars=True,
			)
			self.assertTrue(result.replace(" ", "") == "~$£[]().ae!#@<^^+&")

			result = preprocess\
			(
				text,
				stripAccents=False,
				replaceUnknownChars=False,
				replacePunctLevel=2,
			)
			self.assertTrue(result.replace(" ", "") == "œ°$µ£[]().aé!#@<+&¤")

			result = preprocess\
			(
				"aaa\\aaa\\a\errd~",
				stripAccents=True,
				replaceUnknownChars=True,
				unknownReplacer="",
				replacePunctLevel=1,
				punctReplacer="",
			)
			self.assertTrue(result == "aaaaaaaerrd")

			result = preprocess\
			(
				text,
				stripAccents=True,
				replaceUnknownChars=False,
				replacePunctLevel=1,
			)
			self.assertTrue(result == "œ° $µ£  ().ae!#@   +&¤")

			result = preprocess\
			(
				text,
				stripAccents=True,
				replaceUnknownChars=False,
				replacePunctLevel=2,
			)
			self.assertTrue(result == "œ° $µ£[]().ae!#@<  +&¤")

			result = preprocess\
			(
				text,
				stripAccents=True,
				replaceUnknownChars=True,
				replacePunctLevel=1,
				punctReplacer="¤",
			)
			self.assertTrue(result == "  ¤$ £¤¤().ae!#@¤¤¤+& ")

			result = preprocess\
			(
				text,
				stripAccents=True,
				replaceUnknownChars=True,
				replacePunctLevel=0,
				punctReplacer="¤",
			)
			self.assertTrue(result == "  ¤$ £¤¤¤¤¤ae¤#@¤¤¤+& ")

			result = preprocess\
			(
				text,
				stripAccents=False,
				replaceUnknownChars=False,
				replacePunctLevel=0,
				punctReplacer="¤",
			)
			self.assertTrue(result == "œ°¤$µ£¤¤¤¤¤aé¤#@¤¤¤+&¤")

			result = preprocess\
			(
				text,
				stripAccents=False,
				replaceUnknownChars=False,
				replacePunctLevel=10,
				punctReplacer="¤",
			)
			self.assertTrue(result == "œ°~$µ£[]().aé!#@<^^+&¤")

			result = preprocess\
			(
				text,
				stripAccents=False,
				replaceUnknownChars=False,
				replacePunctLevel=3,
				punctReplacer="¤",
			)
			self.assertTrue(result == "œ°~$µ£[]().aé!#@<^^+&¤")

			result = preprocess\
			(
				text,
				stripAccents=False,
				replaceUnknownChars=False,
				replacePunctLevel=2,
				punctReplacer="¤",
			)
			self.assertTrue(result != "œ°~$µ£[]().aé!#@<^^+&¤")

			result = preprocess\
			(
				text,
				stripAccents=False,
				replaceUnknownChars=False,
				replacePunctLevel=0,
				punctReplacer="¤",
				replaceCurrencyLevel=0,
				currencyReplacer="¤¤",
			)
			self.assertTrue(result == "œ°¤¤¤µ¤¤¤¤¤¤¤aé¤#@¤¤¤+&¤")

			result = preprocess\
			(
				text + ' "blaaaah........." !',
				stripAccents=True,
				replaceUnknownChars=True,
				replacePunctLevel=1,
				punctReplacer=" \t ",
				doReduceCharSequences=True,
				replaceQuoteLevel=1,
				quoteReplacer="  ",
				doReduceBlank=True,
			)
			self.assertTrue(result == '$ £ ().ae!#@ +& "blaaah..." !')

			result = preprocess\
			(
				text + ' "blaaaah........." !',
				stripAccents=True,
				replaceUnknownChars=True,
				replacePunctLevel=1,
				punctReplacer=" \t ",
				doReduceCharSequences=True,
				replaceQuoteLevel=0,
				quoteReplacer="  ",
				doReduceBlank=True,
			)
			self.assertTrue(result == '$ £ ().ae!#@ +& blaaah... !')

			result = preprocess\
			(
				text,
				stripAccents=True,
				replaceUnknownChars=False,
				doReduceCharSequences=True,
				replaceSocialLevel=0,
				socialReplacer="  ",
				doReduceBlank=True,
			)
			self.assertTrue(result == "œ°~$µ£[]().ae! <^^+&¤")

			result = preprocess\
			(
				text,
				stripAccents=True,
				replaceUnknownChars=False,
				doReduceCharSequences=True,
				replaceSocialLevel=0,
				socialReplacer="  ",
				doReduceBlank=True,
			    replaceFunctionLevel=1,
			    functionReplacer=" ",
			)
			self.assertTrue(result == "œ°~$µ£[]().ae! <^^ &¤")

			result = preprocess\
			(
				text,
				stripAccents=True,
				replaceUnknownChars=False,
				doReduceCharSequences=True,
				replaceSocialLevel=0,
				socialReplacer="  ",
				doReduceBlank=True,
			    replaceFunctionLevel=0,
			    functionReplacer=" ",
			)
			self.assertTrue(result == "œ°~$µ£[]().ae! <^^ ¤")

			result = preprocess\
			(
				text,
				stripAccents=True,
				replaceUnknownChars=False,
				doReduceCharSequences=True,
				replaceSocialLevel=0,
				doReduceBlank=False,
			    replaceFunctionLevel=0,
			)
			self.assertTrue(result == "œ°~$µ£[]().ae!  <^^  ¤")

			result = preprocess\
			(
				text + "AAAAAA",
				stripAccents=True,
				replaceUnknownChars=False,
				doReduceCharSequences=True,
				replaceSocialLevel=0,
				doReduceBlank=False,
			    replaceFunctionLevel=0,
			)
			self.assertTrue(result == "œ°~$µ£[]().ae!  <^^  ¤AAA")

			result = preprocess\
			(
				text + "AAAAAA`'\"",
				doQuoteNormalization=True,
				stripAccents=True,
				replaceUnknownChars=False,
				doReduceCharSequences=True,
				replaceSocialLevel=0,
				doReduceBlank=False,
			    replaceFunctionLevel=0,
			)
			self.assertTrue(result == "œ°~$µ£[]().ae!  <^^  ¤AAA\"\"")

			result = preprocess\
			(
				text + "AAAAAA`'\"",
				doQuoteNormalization=True,
				stripAccents=True,
				replaceUnknownChars=False,
				doReduceCharSequences=True,
				replaceSocialLevel=0,
				doReduceBlank=True,
			    replaceFunctionLevel=0,
			    replaceQuoteLevel=0,
			)
			self.assertTrue(result == "œ°~$µ£[]().ae! <^^ ¤AAA")



def datasetTest():

	def p1(text):
		return preprocess\
		(
			text,

			removeHtml=True,

			doQuoteNormalization=False, # TODO vary this

			doReduceBlank=False,
			keepNewLines=True, # TODO vary this

			stripAccents=False,
			doUnidecode=True,

			noneNonStrings=True,
			noneEmptyStrings=True,

			doRemoveUrls=False,

			doLower=False,

			unescapeHtml=False,

			doBadlyEncoded=False,

			doReduceCharSequences=False,
			charSequencesMaxLength=3,

		    replaceUnknownChars=False, # TODO vary this
		    unknownReplacer=" ",

		    replacePunctLevel=1, # TODO vary this
		    punctReplacer=" ",
		    
		    replaceQuoteLevel=None, # TODO vary this
		    quoteReplacer=" ",
		    
		    replaceCurrencyLevel=None, # TODO vary this
		    currencyReplacer=" ",
		    
		    replaceSocialLevel=None, # TODO vary this
		    socialReplacer=" ",

		    replaceFunctionLevel=1, # TODO vary this
		    functionReplacer=" ",
		)

	from datastructuretools.processing import threadGen
	from nltk.tokenize import sent_tokenize, word_tokenize
	TOKENIZATION = Enum("TOKENIZATION", "no sentence word")
	tokenization = TOKENIZATION.word
	logger = None
	onlyStopWhenNotEquals = True
	deleteQuotes = True
	allDirNames = set()
	for dirName, text in threadGen(textGenerator(seed=8, whiteList=["users"]), maxsize=10):
		if dirName not in allDirNames:
			allDirNames.add(dirName)
			log("#" * 28, logger)
			log("#" * 10 + dirName + "#" * 10, logger)
			log("#" * 28, logger)
		if tokenization == TOKENIZATION.sentence:
			tokens = sent_tokenize(text)
		elif tokenization == TOKENIZATION.word:
			tokens = word_tokenize(text)
		elif tokenization == TOKENIZATION.no:
			tokens = [text]
		for token in tokens:
			if deleteQuotes:
				token = preprocess(token, doQuoteNormalization=True, replaceQuoteLevel=0)
			preprocessedToken = p1(token)
			print(token)
			if tokenization == TOKENIZATION.no:
				print()
			print(preprocessedToken)
			if onlyStopWhenNotEquals and preprocessedToken != token:
				print(">>> different <<<")
				input()
			print()
			if tokenization == TOKENIZATION.no:
				print()
				print()

	# Prob % et — 




if __name__ == '__main__':
	unittest.main() # Or execute as Python unit-test in eclipse
	# urlParser = URLParser()
	# url = "https://mobile.nytimes.com/aponline/2018/01/30/us/ap-us-airbnb.html?partner=IFTTT&referer=https://www.google.com/url?q=https://www.nytimes.com/aponline/2018/01/30/us/ap-us-airbnb.html?partner%3DIFTTT&source=gmail&ust=1517439940393000&usg=AFQjCNFb8LNTMw9dVTx40GU_hNCMg_PsEw&sa=D"
	# print(url)
	# print(urlParser.normalize(url))
	# datasetTest()


print("Unit tests done.\n==============")




