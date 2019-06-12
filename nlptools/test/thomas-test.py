from nlptools.embedding import *
from systemtools.system import *
import random

for aaa in [True, False]:
	loader = Embeddings("glove-6B", None, doMultiprocessing=aaa)
	wordVectors = loader.getVectors()
	print(wordVectors["the"])
	print(loader.isLower())

d = []
for i in range(100000000):
	d.append(i * " text")
	if freeRAM() < 10:
		break
print(len(d))