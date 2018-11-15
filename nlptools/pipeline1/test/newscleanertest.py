from nlptools.test.utils import *
from nlptools.pipeline1.test.utils import *
from nlptools.pipeline1.newscleaner import *
from nlptools.pipeline1 import pipeline as pipelinev1

def test1():
    for filename, text in newsCleanerDataTestGen():
        # if "d7" in filename:
            print(">>>>> " + filename)
            print(text)
            print()
            print(precleanv1(text))
            print("\n" * 2 + "-" * 40 + "\n" * 2)

def test3():
    for dirname, text in threadedTextGenerator(seed=1, limit=200):
        # if "d7" in filename:
            print(">>>>> " + dirname)
            print(text)
            print()
            print(precleanv1(text))
            print("\n" * 2 + "-" * 40 + "\n" * 2)


def test2():
    findMenuKwargs = \
    {
        "meanTokenCount": 2.2,
        "jumpMaxDiff": 0.8,
        "lineMaxLength": 28,
        "allowPunct": True,
        "fistWordMustHaveAnUpperCase": True,
        "blockSizeMin": 1,
        "blockSizeMax": 500,
        "punctAsWord": False,
    }
    for finder, kwargs in [(findLinesWithoutLowerCase, {}), (findMenu, findMenuKwargs), ]:
        print(">>>>>>>> " + str(finder))
        for dirname, text in threadedTextGenerator(seed=1, limit=200):
            print(">>>>>>>>>>>>>>>>>>>>> " + str(dirname))
            lines = text.split("\n")
            menuIntervals = finder(lines, **kwargs)
            # print(text)
            if len(menuIntervals) > 0:
                lines = getListIntervals(lines, menuIntervals)
                eliminatedText = "\n".join(lines)
                # print("-" * 40)
                print(eliminatedText)
                # print("-" * 40)
                print("\n" * 1)
        

def test3():
    for filename, text in newsCleanerDataTestGen():
        # if "postclean" in filename:
            originalText = copy.deepcopy(text)
            firstSep = "\n" * 2
            secondSep = firstSep + "-" * 40 + firstSep
            print("### ORIGINAL ###")
            print(text + firstSep)
            text = pipelinev1.preprocess(text)
            print("### preprocess ###")
            print(text + firstSep)
            text = precleanv1(text)
            print("### precleanv1 ###")
            print(text + firstSep)
            text = pipelinev1.tokenize(text)
            text = pipelinev1.tagTokensByType(text)
            text = pipelinev1.cleanTokens(text)
            print("### tokenized and cleaned ###")
            print(sentencesToParagraph(text) + firstSep)
            text = postcleanv1(text)
            text = pipelinev1.removeTokenType(text)
            print("### postprocessed ###")
            print(sentencesToParagraph(text) + firstSep)
            print("### is news valid? ###")
            print(str(isNewsValid(text)) + firstSep)
            if isNewsValid(text):
                assert sentencesToParagraph(pipelinev1.pipelinev1(originalText)) == sentencesToParagraph(text)
                print("ok")
            else:
                print("Non valide")
            print(secondSep)

def test4():
    firstSep = "\n" * 2
    secondSep = firstSep + "-" * 40 + firstSep
    for dirname, text in threadedTextGenerator(seed=58, limit=None):
        tokens = pipelinev1.pipelinev1(text)
        textFromTokens = sentencesToParagraph(tokens)
        print(text)
        print(secondSep)
        # if textFromTokens is None:
        #     print("############ NOOOOOOOOOOOOOONE ################")
        #     print(text)
        #     print(secondSep)
        # else:
        #     diff = len(text) - len(textFromTokens)
        #     print("ok")
        #     if diff > 2:
        #         print("diff = " + str(diff))
        #     if diff > 50:
        #         print("############ HUGE DIFF ################")
        #         print(text)
        #         print(firstSep)
        #         print(textFromTokens)
        #         print(secondSep)

if __name__ == '__main__':
    test4()
