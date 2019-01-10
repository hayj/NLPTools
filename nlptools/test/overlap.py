# coding: utf-8
# pew in st-venv python ./test/overlap.py


import os
import sys
sys.path.append('../')

import unittest
import doctest
from systemtools.duration import *
from nlptools import overlap
from nlptools.overlap import *
from twitternewsrec.newscrawler.utils import *
import threading


# The level allow the unit test execution to choose only the top level test
mini = 5
maxi = 10
assert mini <= maxi

print("==============\nStarting unit tests...")

if mini <= 0 <= maxi:
    class DocTest(unittest.TestCase):
        def testDoctests(self):
            """Run doctests"""
            doctest.testmod(overlap)

if mini <= 1 <= maxi:
    class Test1(unittest.TestCase):
        def test1(self):
            newsCrawl = getNewsCrawlSingleton()
            tt = TicToc()
            tt.tic()
            domains = \
            [
                "washingtonpost.com",
                # "nytimes.com",
                # "forbes.com",
                # "cnn.com",
                # "theguardian.com",
            ]
            for config in \
            [
                # (600, 200),
                # (600, 600),

                # (100, 200),
                # (200, 200),
                # (500, 200),
                (1000, 200),
                # (3000, 200),

                # (100, 10000),
                # (200, 10000),
                # (500, 10000),
                # (1000, None),
                # (3000, 10000),
            ]:
                news = dict()
                limit = config[0]
                batchMaxSize = config[1]
                for domain in domains:
                    for newsData in newsCrawl.find({"lastUrlDomain": domain}):
                        if domain not in news:
                            news[domain] = list()
                        if len(news[domain]) == limit:
                            break
                        try:
                            assert len(newsData["scrap"]["text"]) > 100
                            news[domain].append(newsData["scrap"]["text"])
                        except:
                            pass
                            # print("fail")

                # 880 et 898 il est censé y avoir 58% --> ok
                # 78, 598 92% --> ok
                # for i in [78, 598]: 
                #     strToFile(news[domains[0]][i], tmpDir() + "/news" + str(i) + ".txt")
                # exit()


                o = Overlap(news[domains[0]], ngramsMin=5, parallelCount=4, removeEmbeddedNgrams=True, batchMaxSize=batchMaxSize, verbose=False)
                # strToFile(lts(o.getInvertedIndex()), tmpDir() + "/test.txt")
                # strToFile(lts(o.getDocuments()), tmpDir() + "/test.txt")
                overlaps = o.getOverlaps()
                tt.tic("for " + str(limit) + " docs and a batchMaxSize of " + str(batchMaxSize) + ".")
                meanOverlapScores = o.getMeanOverlapScores(threshold=0.2)
                strToFile(lts(meanOverlapScores), tmpDir() + "/meanOverlapScores" + str(batchMaxSize) + ".txt")
                tt.tic("meanOverlapScores DONE.")

if mini <= 2 <= maxi:
    class Test2(unittest.TestCase):
        def test1(self):
            d1 = fileToStr(execDir(__file__) + "/testdata/overlapdata/doc0.txt")
            d2 = fileToStr(execDir(__file__) + "/testdata/overlapdata/doc1.txt")
            # print(d1)
            # print(d2)
            o = Overlap([d1, d2], ngramsMin=2, parallelCount=1,
                removeEmbeddedNgrams=True)
            printLTS(o.getOverlaps())
            strToFile(lts(o.getDocuments()), tmpDir() + "/test.txt")

if mini <= 3 <= maxi:
    class Test3(unittest.TestCase):
        def test1(self):
            docs = []
            for i in range(3):
                d = fileToStr(execDir(__file__) + "/testdata/overlapdata/doc" + str(i) + ".txt")
                docs.append(d)
            o = Overlap(docs, ngramsMin=2, parallelCount=1,
                removeEmbeddedNgrams=True)
            # overlaps = o.getOverlaps()

            # Normalement 1 > 3 = 0.8
            # 3 > 1 = 0.6 (un peu moins)
            # 4 > * et * > 4 = 0.001
            overlaps = o.generateOverlaps()
            printLTS(overlaps)
            # overlapedDocs = o.getOverlapScores(threshold=0.1)
            # printLTS(overlapedDocs)
            # meanOverlapedDocs = o.getMeanOverlapScores(threshold=0.5)
            # printLTS(meanOverlapedDocs)

            # strToFile(lts(overlaps) + "\n" * 10 + lts(o.getDocuments()), tmpDir() + "/test-nonreconstruit.txt")

if mini <= 4 <= maxi:
    class Test4(unittest.TestCase):
        def test1(self):
            newsCrawl = getNewsCrawlSingleton()
            tt = TicToc()
            tt.tic()
            news = dict()
            limit = 50
            batchMaxSize = 10000
            domain = "washingtonpost.com"
            for newsData in newsCrawl.find({"lastUrlDomain": domain}):
                if domain not in news:
                    news[domain] = list()
                if len(news[domain]) == limit:
                    break
                try:
                    assert len(newsData["scrap"]["text"]) > 100
                    news[domain].append(newsData["scrap"]["text"])
                except:
                    pass
                    # print("fail")
            o = Overlap(news[domain], ngramsMin=5, parallelCount=8, removeEmbeddedNgrams=True, batchMaxSize=batchMaxSize, verbose=True)
            # strToFile(lts(o.getInvertedIndex()), tmpDir() + "/test.txt")
            # strToFile(lts(o.getDocuments()), tmpDir() + "/test.txt")
            overlaps = o.getOverlapedDocs()
            # strToFile(lts(overlaps), tmpDir() + "/test-batch" + str(batchMaxSize) + ".txt")
            tt.tic("for " + str(limit) + " docs and a batchMaxSize of " + str(batchMaxSize) + ".")

if mini <= 5 <= maxi:
    class Test5(unittest.TestCase):
        def test1(self):
            docs = []
            for i in range(8):
                filePath = execDir(__file__) + "/testdata/overlapdata/doc" + str(i) + ".txt"
                if isFile(filePath):
                    d = fileToStr(filePath)
                    docs.append(d)
            o = Overlap(docs, ngramsMin=2, parallelCount=2,
                removeEmbeddedNgrams=True)
            meanOverlapScores = o.getMeanOverlapScores(threshold=0.001)
            printLTS(meanOverlapScores)
            duplicates = o.findDuplicates(threshold=0.3)
            printLTS(duplicates)



if __name__ == '__main__':
    unittest.main() # Or execute as Python unit-test in eclipse


print("Unit tests done.\n==============")