# nn -o nohup-downloader.out pew in st-venv python ~/Workspace/Python/Utils/NLPTools/nlptools/test/downloader.py

wvPatterns = \
[
	"fasttext-wiki-news-1M",
	"fasttext-crawl-2M",
	"glove-840B",
	"glove-6B",
	"word2vec-googlenews",
]
from nlptools.embedding import *                                                                              
for p in wvPatterns:
	try:
		Embeddings(p).getVectors()
	except Exception as e:
		print(e)


