# coding: utf-8
# pew in st-venv python /home/hayj/Workspace/Python/Utils/NLPTools/nlptools/test/pipeline.py

import os
import sys
sys.path.append('../')

import unittest
import doctest
from nlptools import pipeline
from nlptools.pipeline1.pipeline import *
from nlptools.pipeline1.test.pipelinetest import *

# The level allow the unit test execution to choose only the top level test
mini = 1
maxi = 12
assert mini <= maxi

print("==============\nStarting unit tests...")

if mini <= 0 <= maxi:
	class DocTest(unittest.TestCase):
		def testDoctests(self):
			"""Run doctests"""
			doctest.testmod(pipeline)

if mini <= 1 <= maxi:
	class QuoteTest(unittest.TestCase):
		def testCheckTagging(self):
			for current in \
			[
				("%kjh$$", TOKEN_TYPE.unknown),
				("-", TOKEN_TYPE.punct1),
				(".", TOKEN_TYPE.punct1),
				("'", TOKEN_TYPE.quote),
				("a", TOKEN_TYPE.alpha),
				("'m", TOKEN_TYPE.alpha),
				("9.9M", TOKEN_TYPE.alphanum),
				("5,5€", TOKEN_TYPE.price),
				("300 000,00", TOKEN_TYPE.num),
				('...',  TOKEN_TYPE.punct1),
				('x=\\frac', TOKEN_TYPE.unknown),
				('{', TOKEN_TYPE.punct2),
				('}', TOKEN_TYPE.punct2),
				('^', TOKEN_TYPE.punct2),
				('~this~', TOKEN_TYPE.unknown),
				('thingsœ', TOKEN_TYPE.unknown),
				('一so', TOKEN_TYPE.unknown),
				(']', TOKEN_TYPE.punct2),
				('[', TOKEN_TYPE.punct2),
				('Jean-Yves', TOKEN_TYPE.alpha),
				("mister_yo", TOKEN_TYPE.alpha),
				("@toto", TOKEN_TYPE.atreply),
				("#t111", TOKEN_TYPE.hashtag),
				("@1000", TOKEN_TYPE.unknown),
				("#1000", TOKEN_TYPE.unknown),
				("$6.6", TOKEN_TYPE.price),
				('-', TOKEN_TYPE.punct1),
				(None, TOKEN_TYPE.none),
				(" ", TOKEN_TYPE.unknown),
				("", TOKEN_TYPE.none),
				("``", TOKEN_TYPE.quote),
				("''", TOKEN_TYPE.quote),
				("H&M", TOKEN_TYPE.alpha),
				("John/Mary", TOKEN_TYPE.alpha),
				("///", TOKEN_TYPE.unknown),
			]:
				theType = tagTokensByType([current[0]])[0][1]
				print(str(current[0]) + ", expected " + current[1].name + ", found " + theType.name)
				self.assertTrue(current[1] == theType)


if __name__ == '__main__':
	unittest.main() # Or execute as Python unit-test in eclipse


print("Unit tests done.\n==============")







