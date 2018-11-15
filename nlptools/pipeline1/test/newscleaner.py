# coding: utf-8
# pew in st-venv python ~/Workspace/Python/Utils/NLPTools/nlptools/test/newscleaner.py


import os
import sys
sys.path.append('../')

import unittest
import doctest
from systemtools.location import *
from systemtools.duration import *
from nlptools.pipeline1 import newscleaner
from nlptools.pipeline1.newscleaner import *
from nlptools.test.utils import *
import re


# The level allow the unit test execution to choose only the top level test
mini = 0
maxi = 10
assert mini <= maxi

print("==============\nStarting unit tests...")



if mini <= 0 <= maxi:
    class DocTest(unittest.TestCase):
        def testDoctests(self):
            """Run doctests"""
            doctest.testmod(newscleaner)

if mini <= 1 <= maxi:
    class Test1(unittest.TestCase):
        def test1(self):
            for filename, text in newsCleanerDataTestGen():
                print(">>>>> " + filename)
                findMenuKwargs = \
                {
                    "meanTokenCount": 2.2,
                    "jumpMaxDiff": 0.8,
                    "lineMaxLength": 28,
                    "allowPunct": True,
                    "fistWordMustHaveAnUpperCase": True,
                    "blockSizeMin": 1,
                    "blockSizeMax": 500,
                }
                lines = text.split("\n")
                print(text)
                print()
                menuIntervals = findMenu(lines, **findMenuKwargs)
                lines = removeListIntervals(lines, menuIntervals)
                text = "\n".join(lines)
                print(text)
                if filename == "d1":
                    self.assertTrue(len(lines) == 7)
                elif filename == "d2":
                    self.assertTrue(len(lines) == 2)
                elif filename == "d4":
                    self.assertTrue(len(lines) == 10)
                print("\n" * 2 + "-" * 40 + "\n" * 2)


if mini <= 2 <= maxi:
    class Test2(unittest.TestCase):
        # def test0(self):
            # text = "aaa\nb\nccccc"
            # lines = text.split("\n")
            # print(lineIntervalsToStringIndexes(lines, [(0, 1), (0, 2), (1, 2)]))
            # printLTS(removeStringIntervals(text, lineIntervalsToStringIndexes(lines, [(1, 2)])))
            # printLTS(removeStringIntervals(text, lineIntervalsToStringIndexes(lines, [(0, 2)])))
            # printLTS(removeStringIntervals(text, lineIntervalsToStringIndexes(lines, [(0, 1)])))

        def test1(self):
            """
                This function will test removeStringIntervals and lineIntervalsToStringIndexes
            """
            text = "aa aaa aa\naaaa\naa\na\naaa - aa\na"
            lines = text.split("\n")
            print(lines)
            for expectedResult, intervals in \
            [
                ("", [(0, 3), (3, 6)]),
                ("aa\na", [(0, 2), (4, 6)]),
                ("", [(0, 5), (2, 6)]),
                ("a", [(0, 5)]),
                ("aaa - aa", [(0, 2), (2, 4), (5, 6)]),
                ("aaaa\naa\na\naaa - aa", [(0, 1), (5, 6)]),
                ("aa aaa aa\naa\naaa - aa\na", [(1, 2), (3, 4)]),
            ]:
                result = removeListIntervals(lines, intervals)
                result = "\n".join(result)
                print("Expected: " + expectedResult)
                print("Result: " + result)
                # printLTS(result)
                self.assertTrue(result == expectedResult)

if mini <= 3 <= maxi:
    class Test3(unittest.TestCase):
        def test1(self):
            l = ["a", "b", "c", "d", "e"]
            text = "".join(l)
            for expectedResult, intervals in \
            [
                ("ace", [(1, 2), (3, 4)]),
                ("abc", [(3, 5)]),
                ("acd", [(1, 2), (4, 5)]),
                ("bcde", [(0, 1)]),
                ("cde", [(0, 2)]),
            ]:
                print("Trying for text (expectation: " + expectedResult + "):")
                newText = removeStringIntervals(text, intervals)
                print(newText)
                self.assertTrue(newText == expectedResult)
                print("Trying for list (expectation: " + expectedResult + "):")
                newL = removeListIntervals(l, intervals)
                newL = "".join(newL)
                print(newL)
                self.assertTrue(newL == expectedResult)
                print()





if __name__ == '__main__':
    unittest.main() # Or execute as Python unit-test in eclipse


print("Unit tests done.\n==============")