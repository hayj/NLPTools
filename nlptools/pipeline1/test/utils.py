from systemtools.basics import *
from systemtools.file import *
from systemtools.location import *
from datatools.jsonutils import NDJson
import random
from datastructuretools.processing import *
import copy

def newsCleanerDataTestGen():
    for filePath in sortedGlob(execDir(__file__) + "/testdata/newscleaner/*.txt"):
        (dir, filename, ext, filenameExt) = decomposePath(filePath)
        text = fileToStr(filePath)
        text = text.strip()
        if len(text) > 2:
            yield (filename, text)