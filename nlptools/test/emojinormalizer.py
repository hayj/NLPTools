# coding: utf-8
# pew in st-venv python ~/Workspace/Python/Utils/NLPTools/nlptools/test/emojinormalizer.py


import os
import sys
sys.path.append('../')

import unittest
import doctest
from systemtools.duration import *
from nlptools import emojinormalizer
from nlptools.emojinormalizer import *
import re


# The level allow the unit test execution to choose only the top level test
mini = 0
maxi = 3
assert mini <= maxi

print("==============\nStarting unit tests...")

if mini <= 0 <= maxi:
    class DocTest(unittest.TestCase):
        def testDoctests(self):
            """Run doctests"""
            doctest.testmod(emojinormalizer)

if mini <= 1 <= maxi:
    class Test1(unittest.TestCase):
        def test1(self):
            for emoji in \
            [
                "😖", "😣", "😀", "😅", "👨", "😇", "😄", "😴", 
                "👋", "🌹", "🎅", "🚚", "🌍", "🚬", "🎧", "🐍", "🙆", 
                "🙅", "😶", "🙆", "♥", "🌈", "😀", "♯",
            ]:
                print(emoji)
                self.assertTrue(isEmoji(emoji))

            for nonEmoji in \
            [
                "�", "€", "a", ":-)", "'", "=", "&", "%",
                "", "\xa0", "<U+0093>", "¶", "漢", "", None, "€",
                "\xF0", "\xF0\x9F\x98\x8C", ":man:", "\xE2\x9C\x82",
                # "\U+1F60C",
            ]:
                print(nonEmoji)
                self.assertTrue(not isEmoji(nonEmoji))

if __name__ == '__main__':
    unittest.main() # Or execute as Python unit-test in eclipse


print("Unit tests done.\n==============")