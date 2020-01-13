# coding: utf-8
# pew in systemtools-venv python ./test/basics.py

import os
import sys
sys.path.append('../')

import unittest
import doctest
from nlptools import basics
from nlptools.basics import *
from systemtools.printer import *

# The level allow the unit test execution to choose only the top level test
mini = 0
maxi = 15
assert mini <= maxi

print("==============\nStarting unit tests...")

if mini <= 0 <= maxi:
    class DocTest(unittest.TestCase):
        def testDoctests(self):
            """Run doctests"""
            doctest.testmod(basics)

if mini <= 1 <= maxi:
    class Test1(unittest.TestCase):
        def test1(self):
            docs = [['aa', 'bb', 'cc'], ['uu'], ['pp', 'tt'], ['ii'], ['..'], ['zz', 'ee', 'rr', 'rr', 'rr', 'oo', 'pp'], ['ii'], ['..'], ['ii'], [';;'], ['??']]
            ngrams = extractNgrams\
            (
                docs,
                ngrams=1,
                minDF=1,
                doLower=False,
                returnDF=False,
                useTuple=False,
                flattenSentences=False,
                verbose=False,
            )
            self.assertTrue(ngrams == set(flattenLists(docs)))

        def test2(self):
            docs = [['aa', 'bb', 'cc'], ['uu'], ['pp', 'tt'], ['ii'], ['..'], ['zz', 'ee', 'rr', 'rr', 'rr', 'OO', 'pp'], ['ii'], ['..'], ['ii'], [';;'], ['??']]
            ngrams = extractNgrams\
            (
                docs,
                ngrams=1,
                minDF=1,
                doLower=True,
                returnDF=False,
                useTuple=False,
                flattenSentences=False,
                verbose=False,
            )
            self.assertTrue(ngrams == set([e.lower() for e in flattenLists(docs)]))

        def test3(self):
            docs = [['aa', 'bb', 'cc'], ['uu'], ['pp', 'tt'], ['ii'], ['..'], ['zz', 'ee', 'rr', 'rr', 'rr', 'OO', 'pp'], ['ii'], ['..'], ['ii'], [';;'], ['??']]
            ngrams = extractNgrams\
            (
                docs,
                ngrams=1,
                minDF=1,
                doLower=False,
                returnDF=False,
                useTuple=False,
                flattenSentences=False,
                verbose=False,
            )
            self.assertTrue(ngrams != set([e.lower() for e in flattenLists(docs)]))

        def test4(self):
            docs = [['aa'], ['uu'], ['pp', 'tt'], ['ii'], ['..'], ['zz', 'ee', 'rr', 'rr', 'rr', 'OO', 'pp'], ['ii']]
            ngrams = extractNgrams\
            (
                [docs, docs],
                ngrams=2,
                minDF=1,
                doLower=False,
                returnDF=False,
                useTuple=False,
                flattenSentences=True,
                verbose=False,
            )
            result = {'aa uu', 'uu pp', 'pp tt', 'tt ii', 'ii ..', '.. zz', 'zz ee', 'ee rr', 'rr rr', 'rr OO', 'OO pp', 'pp ii'}
            self.assertTrue(ngrams == result)

        def test5(self):
            docs = [['aa'], ['uu'], ['pp', 'tt'], ['ii'], ['..'], ['zz', 'ee', 'rr', 'rr', 'rr', 'OO', 'pp'], ['ii']]
            gotException = False
            try:
                ngrams = extractNgrams\
                (
                    docs,
                    ngrams=2,
                    minDF=1,
                    doLower=False,
                    returnDF=False,
                    useTuple=False,
                    flattenSentences=True,
                    verbose=False,
                )
            except: gotException = True
            self.assertTrue(gotException)

        def test6(self):
            docs = [['aa'], ['uu'], ['pp', 'tt'], ['ii'], ['..'], ['zz', 'ee', 'rr', 'rr', 'rr', 'OO', 'pp'], ['ii']]
            ngrams = extractNgrams\
            (
                [docs],
                ngrams=2,
                minDF=1,
                doLower=False,
                returnDF=False,
                useTuple=False,
                flattenSentences=False,
                verbose=False,
            )
            result = {'pp tt', 'zz ee', 'ee rr', 'rr rr', 'rr OO', 'OO pp'}
            self.assertTrue(ngrams == result)

        def test7(self):
            docs = [['aa'], ['uu'], ['pp', 'tt'], ['ii'], ['..'], ['zz', 'ee', 'rr', 'rr', 'rr', 'OO', 'pp'], ['ii']]
            gotException = False
            try:
                ngrams = extractNgrams\
                (
                    [[docs, docs]],
                    ngrams=2,
                    minDF=1,
                    doLower=False,
                    returnDF=False,
                    useTuple=False,
                    flattenSentences=False,
                    verbose=False,
                )
            except: gotException = True
            self.assertTrue(gotException)

        def test8(self):
            docs = [['aa'], ['uu'], ['pp', 'tt'], ['ii'], ['..'], ['zz', 'ee', 'rr', 'rr', 'rr', 'OO', 'pp'], ['ii']]
            ngrams = extractNgrams\
            (
                docs,
                ngrams=3,
                minDF=1,
                doLower=False,
                returnDF=False,
                useTuple=False,
                flattenSentences=False,
                verbose=False,
            )
            result = {'zz ee rr', 'ee rr rr', 'rr rr rr', 'rr rr OO', 'rr OO pp'}
            self.assertTrue(ngrams == result)

        def test9(self):
            docs = [['aa'], ['uu'], ['pp', 'tt'], ['ii'], ['..'], ['zz', 'ee', 'rr', 'rr', 'rr', 'OO', 'pp'], ['ii']]
            gotException = False
            try:
                ngrams = extractNgrams\
                (
                    docs,
                    ngrams=3,
                    minDF=1,
                    doLower=False,
                    returnDF=False,
                    useTuple=False,
                    flattenSentences=True,
                verbose=False,
                )
            except: gotException = True
            self.assertTrue(gotException)

        def test10(self):
            docs = [['aa'], ['uu'], ['pp', 'tt'], ['ii'], ['..'], ['zz', 'ee', 'rr', 'rr', 'rr', 'OO', 'pp'], ['ii']]
            ngrams = extractNgrams\
            (
                [docs, docs],
                ngrams=3,
                minDF=1,
                doLower=False,
                returnDF=False,
                useTuple=False,
                flattenSentences=False,
                verbose=False,
            )
            result = {'zz ee rr', 'ee rr rr', 'rr rr rr', 'rr rr OO', 'rr OO pp'}
            self.assertTrue(ngrams == result)

        def test11(self):
            docs = [['aa'], ['uu'], ['pp', 'tt'], ['ii'], ['..'], ['zz', 'ee', 'rr', 'rr', 'rr', 'OO', 'pp'], ['ii']]
            ngrams = extractNgrams\
            (
                [docs, docs],
                ngrams=3,
                minDF=1,
                doLower=False,
                returnDF=False,
                useTuple=False,
                flattenSentences=True,
                verbose=False,
            )
            self.assertTrue(len(ngrams) == len(flattenLists(docs)) - 2)

        def test12(self):
            docs = [['aa'], ['uu'], ['pp', 'tt'], ['ii'], ['..'], ['zz', 'ee', 'rr', 'rr', 'rr', 'OO', 'pp', 'tt'], ['ii']]
            ngrams = extractNgrams\
            (
                docs,
                ngrams=2,
                minDF=2,
                doLower=False,
                returnDF=False,
                useTuple=False,
                flattenSentences=False,
                verbose=False,
            )
            self.assertTrue(ngrams == {"pp tt"})


if mini <= 2 <= maxi:
    class Test2(unittest.TestCase):
        def test1(self):
            docs = [['aa', 'bb', 'cc'], ['uu'], ['pp', 'tt'], ['ii'], ['..'], ['zz', 'ee', 'rr', 'rr', 'rr', 'oo', 'pp'], ['ii'], ['..'], ['ii'], [';;'], ['??']]
            ngrams = toNgrams\
            (
                docs,
                ngrams=1,
                doLower=False,
                flattenSentences=False,
                verbose=False,
            )
            self.assertTrue(ngrams == docs)

        def test2(self):
            docs = [['aa', 'bb', 'cc'], ['uu'], ['pp', 'tt'], ['ii'], ['..'], ['zz', 'ee', 'rr', 'rr', 'rr', 'OO', 'pp'], ['ii'], ['..'], ['ii'], [';;'], ['??']]
            ngrams = toNgrams\
            (
                docs,
                ngrams=1,
                doLower=True,
                flattenSentences=False,
                verbose=False,
            )
            self.assertTrue(ngrams == [['aa', 'bb', 'cc'], ['uu'], ['pp', 'tt'], ['ii'], ['..'], ['zz', 'ee', 'rr', 'rr', 'rr', 'oo', 'pp'], ['ii'], ['..'], ['ii'], [';;'], ['??']])

        def test3(self):
            docs = [['aa', 'bb', 'cc'], ['uu'], ['pp', 'tt'], ['ii'], ['..'], ['zz', 'ee', 'rr', 'rr', 'rr', 'OO', 'pp'], ['ii'], ['..'], ['ii'], [';;'], ['??']]
            ngrams = toNgrams\
            (
                docs,
                ngrams=1,
                doLower=False,
                flattenSentences=False,
                verbose=False,
            )
            self.assertTrue(ngrams == [['aa', 'bb', 'cc'], ['uu'], ['pp', 'tt'], ['ii'], ['..'], ['zz', 'ee', 'rr', 'rr', 'rr', 'OO', 'pp'], ['ii'], ['..'], ['ii'], [';;'], ['??']])

        def test4(self):
            docs = [['aa'], ['uu'], ['pp', 'tt'], ['ii'], ['..'], ['zz', 'ee', 'rr', 'rr', 'rr', 'OO', 'pp'], ['ii']]
            ngrams = toNgrams\
            (
                [docs, docs],
                ngrams=2,
                doLower=False,
                flattenSentences=False,
                verbose=False,
            )
            result = [[[], [], ['pp tt'], [], [], ['zz ee', 'ee rr', 'rr rr', 'rr rr', 'rr OO', 'OO pp'], []]] * 2
            # bp(ngrams, 5)
            # bp(result, 5)
            self.assertTrue(ngrams == result)

        def test4_2(self):
            docs = [['aa'], ['uu'], ['pp', 'tt'], ['ii'], ['..'], ['zz', 'ee', 'rr', 'rr', 'rr', 'OO', 'pp'], ['ii']]
            docs = [docs, docs]
            ngrams = toNgrams\
            (
                docs,
                ngrams=2,
                doLower=False,
                flattenSentences=True,
                verbose=False,
            )
            result = [['aa uu', 'uu pp', 'pp tt', 'tt ii', 'ii ..', '.. zz', 'zz ee', 'ee rr', 'rr rr', 'rr rr', 'rr OO', 'OO pp', 'pp ii'], ['aa uu', 'uu pp', 'pp tt', 'tt ii', 'ii ..', '.. zz', 'zz ee', 'ee rr', 'rr rr', 'rr rr', 'rr OO', 'OO pp', 'pp ii']]
            self.assertTrue(ngrams == result)

        def test5(self):
            docs = [['aa'], ['uu'], ['pp', 'tt'], ['ii'], ['..'], ['zz', 'ee', 'rr', 'rr', 'rr', 'OO', 'pp'], ['ii']]
            gotException = False
            try:
                ngrams = toNgrams\
                (
                    docs,
                    ngrams=2,
                    doLower=False,
                    flattenSentences=True,
                    verbose=False,
                )
            except: gotException = True
            self.assertTrue(gotException)

        def test6(self):
            docs = [['aa'], ['uu'], ['pp', 'tt'], ['ii'], ['..'], ['zz', 'ee', 'rr', 'rr', 'rr', 'OO', 'pp'], ['ii']]
            ngrams = toNgrams\
            (
                [docs],
                ngrams=2,
                doLower=False,
                flattenSentences=False,
                verbose=False,
            )
            result = [[[], [], ['pp tt'], [], [], ['zz ee', 'ee rr', 'rr rr', 'rr rr', 'rr OO', 'OO pp'], []]]
            self.assertTrue(ngrams == result)

        def test6_2(self):
            docs = [['aa'], ['uu'], ['pp', 'tt'], ['ii'], ['..'], ['zz', 'ee', 'rr', 'rr', 'rr', 'OO', 'pp'], ['ii']]
            ngrams = toNgrams\
            (
                [docs],
                ngrams=2,
                doLower=True,
                flattenSentences=False,
                verbose=False,
            )
            result = [[[], [], ['pp tt'], [], [], ['zz ee', 'ee rr', 'rr rr', 'rr rr', 'rr oo', 'oo pp'], []]]
            self.assertTrue(ngrams == result)

        def test7(self):
            docs = [['aa'], ['uu'], ['pp', 'tt'], ['ii'], ['..'], ['zz', 'ee', 'rr', 'rr', 'rr', 'OO', 'pp'], ['ii']]
            gotException = False
            try:
                ngrams = toNgrams\
                (
                    [[docs, docs]],
                    ngrams=2,
                    doLower=False,
                    flattenSentences=False,
                    verbose=False,
                )
            except: gotException = True
            self.assertTrue(gotException)

        def test8(self):
            docs = [['aa'], ['uu'], ['pp', 'tt'], ['ii'], ['..'], ['zz', 'ee', 'rr', 'rr', 'rr', 'OO', 'pp'], ['ii']]
            ngrams = toNgrams\
            (
                [docs],
                ngrams=3,
                doLower=False,
                flattenSentences=False,
            )
            result = [[[], [], [], [], [], ['zz ee rr', 'ee rr rr', 'rr rr rr', 'rr rr OO', 'rr OO pp'], []]]
            self.assertTrue(ngrams == result)

        def test8_2(self):
            docs = [['aa'], ['uu'], ['pp', 'tt'], ['ii'], ['..'], ['zz', 'ee', 'rr', 'rr', 'rr', 'OO', 'pp'], ['ii']]
            ngrams = toNgrams\
            (
                docs,
                ngrams=3,
                doLower=False,
                flattenSentences=False,
            )
            result = [[], [], [], [], [], ['zz ee rr', 'ee rr rr', 'rr rr rr', 'rr rr OO', 'rr OO pp'], []]
            self.assertTrue(ngrams == result)

        def test8_3(self):
            docs = [[['aa'], ['uu'], ['pp', 'tt'], ['ii'], ['..'], ['zz', 'ee', 'rr', 'rr', 'rr', 'OO', 'pp'], ['ii']], [['ii'], ['pp']]]
            ngrams = toNgrams\
            (
                docs,
                ngrams=3,
                doLower=False,
                flattenSentences=True,
            )
            result = [['aa uu pp', 'uu pp tt', 'pp tt ii', 'tt ii ..', 'ii .. zz', '.. zz ee', 'zz ee rr', 'ee rr rr', 'rr rr rr', 'rr rr OO', 'rr OO pp', 'OO pp ii'], []]
            self.assertTrue(ngrams == result)

        def test8_4(self):
            docs = [[['aa'], ['uu'], ['pp', 'tt'], ['ii'], ['..'], ['zz', 'ee', 'rr', 'rr', 'rr', 'OO', 'pp'], ['ii']], [['ii'], ['pp']]]
            ngrams = toNgrams\
            (
                docs,
                ngrams=3,
                doLower=False,
                flattenSentences=False,
            )
            result = [[[], [], [], [], [], ['zz ee rr', 'ee rr rr', 'rr rr rr', 'rr rr OO', 'rr OO pp'], []], [[], []]]
            # bp(ngrams, 5)
            self.assertTrue(ngrams == result)

        def test9(self):
            docs = [['aa'], ['uu'], ['pp', 'tt'], ['ii'], ['..'], ['zz', 'ee', 'rr', 'rr', 'rr', 'OO', 'pp'], ['ii']]
            gotException = False
            try:
                ngrams = toNgrams\
                (
                    docs,
                    ngrams=3,
                    doLower=False,
                    flattenSentences=True,
                )
            except: gotException = True
            self.assertTrue(gotException)

        def test10(self):
            docs = [['aa'], ['uu'], ['pp', 'tt'], ['ii'], ['..'], ['zz', 'ee', 'rr', 'rr', 'rr', 'OO', 'pp'], ['ii']]
            ngrams = toNgrams\
            (
                [docs, docs],
                ngrams=3,
                doLower=False,
                flattenSentences=False,
            )
            result = [[[], [], [], [], [], ['zz ee rr', 'ee rr rr', 'rr rr rr', 'rr rr OO', 'rr OO pp'], []], [[], [], [], [], [], ['zz ee rr', 'ee rr rr', 'rr rr rr', 'rr rr OO', 'rr OO pp'], []]]
            self.assertTrue(ngrams == result)

        def test11(self):
            docs = [['aa'], ['uu'], ['pp', 'tt'], ['ii'], ['..'], ['zz', 'ee', 'rr', 'rr', 'rr', 'OO', 'pp'], ['ii']]
            ngrams = toNgrams\
            (
                [docs, docs],
                ngrams=3,
                doLower=False,
                flattenSentences=True,
            )
            result = [['aa uu pp', 'uu pp tt', 'pp tt ii', 'tt ii ..', 'ii .. zz', '.. zz ee', 'zz ee rr', 'ee rr rr', 'rr rr rr', 'rr rr OO', 'rr OO pp', 'OO pp ii'], ['aa uu pp', 'uu pp tt', 'pp tt ii', 'tt ii ..', 'ii .. zz', '.. zz ee', 'zz ee rr', 'ee rr rr', 'rr rr rr', 'rr rr OO', 'rr OO pp', 'OO pp ii']]
            self.assertTrue(ngrams == result)

        def test12(self):
            docs = [['aa'], ['uu'], ['pp', 'tt'], ['ii'], ['..'], ['zz', 'ee', 'rr', 'rr', 'rr', 'OO', 'pp', 'tt'], ['ii']]
            ngrams = toNgrams\
            (
                docs,
                ngrams=2,
                doLower=False,
                flattenSentences=False,
            )
            result = [[], [], ['pp tt'], [], [], ['zz ee', 'ee rr', 'rr rr', 'rr rr', 'rr OO', 'OO pp', 'pp tt'], []]
            self.assertTrue(ngrams == result)

        def test13(self):
            docs = [['aa'], ['uu'], ['pp', 'tt'], ['ii'], ['..'], ['zz', 'ee', 'rr', 'rr', 'rr', 'OO', 'pp', 'tt'], ['ii']]
            ngrams = toNgrams\
            (
                [docs],
                ngrams=20,
                doLower=False,
                flattenSentences=True,
            )
            result = [[]]
            self.assertTrue(ngrams == result)

        def test14(self):
            docs = [['aa'], ['uu'], ['pp', 'tt'], ['ii'], ['..'], ['zz', 'ee', 'rr', 'rr', 'rr', 'OO', 'pp', 'tt'], ['ii']]
            ngrams = toNgrams\
            (
                [docs],
                ngrams=1,
                doLower=False,
                flattenSentences=False,
            )
            self.assertTrue(ngrams == [docs])

        def test15(self):
            docs = [['aa'], ['uu'], ['pp', 'tt'], ['ii'], ['..'], ['zz', 'ee', 'rr', 'rr', 'rr', 'OO', 'pp', 'tt'], ['ii']]
            ngrams = toNgrams\
            (
                [docs],
                ngrams=2,
                doLower=False,
                flattenSentences=True,
            )
            result = [['aa uu', 'uu pp', 'pp tt', 'tt ii', 'ii ..', '.. zz', 'zz ee', 'ee rr', 'rr rr', 'rr rr', 'rr OO', 'OO pp', 'pp tt', 'tt ii']]
            self.assertTrue(ngrams == result)


if __name__ == '__main__':
    unittest.main() # Orb execute as Python unit-test in eclipse


print("Unit tests done.\n==============")