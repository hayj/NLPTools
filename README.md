
# NLPTools

## Dependency on Ubuntu

	sudo apt-get install libenchant1c2a

## Installation (Python 3)

	git clone https://github.com/hayj/NLPTools.git
	pip install ./NLPTools/wm-dist/*.tar.gz

Or use this script: <https://github.com/hayj/Bash/blob/master/hjupdate.sh>

## Preprocessing of text

This module provide a complete preprocessing function, see the usage:

	>>> from nlptools.preprocessing import *

Use doQuoteNormalization to normalize all quotation to ASCII ' and " chars:

	>>> t = "« Hello World » I’m ``Mick´´"
	>>> preprocess(t, doQuoteNormalization=True)
	" Hello World " I'm "Mick"

Remove the html and unescape the html:

	>>> t = "Hello <span>World</span>! &gt;&lt;"
	>>> preprocess(t, removeHtml=True, unescapeHtml=True)
	Hello World! ><

Reduce black spaces, remove accents and reduce long char sequences:

	>>> t = "  Hello Béà \t !!!!!!! \n\n \n Fine?"
	>>> preprocess(t, doReduceBlank=True, stripAccents=True, doReduceCharSequences=True, charSequencesMaxLength=3)
	Hello Bea !!!
	Fine?

Normalize emojis to the utf-8 char:

	>>> t = ":-) These are emojis ;) 😣 😀 :o)"
	>>> preprocess(t, doNormalizeEmojis=True)
	😄 These are emojis 😉 😣 😀 😄

Normalize specific chars (for example ━, 一 and – are replaced by the normal form —, … is repaced by ...):

	>>> t = "Hello guy… I am━actually not━ok!"
	>>> preprocess(t, doSpecialMap=True)
	Hello guy... I am—actually not—ok!

Remove unknown chars and badly encoded chars:

	>>> t = "Hello 10€ and 8$ ® 字 � are 20% µ ç"
	>>> preprocess(t, doBadlyEncoded=True, replaceUnknownChars=True, doReduceBlank=True, stripAccents=True)
	Hello 10€ and 8$ are 20% c

Remove urls:

	>>> t = "Pls visit http://test.com !!"
	>>> preprocess(t, doRemoveUrls=True))
	Pls visit  !!

And other parameters like `replaceCurrencyLevel`, `replaceSocialLevel`, `replaceFunctionLevel`... You will also find others functions for post-tokenization processing etc.

## Embeddings

This tool provide usefull functin to load and handle word embeddings.

Load GloVe vectors:

	emb = Embeddings("glove")
	wordVectors = emb.getVectors()

**How it works :** all vectors will be downloaded and stored in a tmp directory (in case of googlenews vector, it will convert the bin format to a compressed txt format). So the next time you wil load vectors, it will automatically load vectors from disk if it was already downloaded.

Print informations about loaded vectors:

	print(emb.isLower())
	print(emb.getVectors()["the"])

You can also choose a specific dimension for a given vector key:

	emb = Embeddings("glove-twitter", 200)

You can choose these keys (please pm me to suggest other embeddings) :

	"fasttext-wiki-news-1M": [300]
	"fasttext-wiki-news-1M-subword": [300]
	"fasttext-crawl-2M": [300]
	"fasttext-crawl-2M-subword": [300]
	"glove-6B": [50, 100, 200, 300]
	"glove-42B": [300]
	"glove-840B": [300]
	"glove-twitter-27B": [25, 50, 100, 200]
	"googlenews": [300]

## Overlap

Get your data:

	>>> from nlptools.overlap import *
    >>> d0 = "Hello I am X and I did an Overlap librarie?"
    >>> d1 = "Hello I am Y and I work on Overlap librarie tool."
    >>> d2 = "You are working on this with my collegue, on the Overlap librarie tool!"

Init the Overlap object and set ngramsMin. If ngramsMin is 2, only 2grams will be taken into account:

    >>> o = Overlap([d0, d1, d2], ngramsMin=2, verbose=False)

You can get overlaps:

    >>> print(o.getOverlaps())
    {
		('overlap', 'librarie'): {
			0: {0},
			1: {1},
			2: {2}
		},
		('overlap', 'librarie', 'tool'): {
			1: {1},
			2: {2}
		}
	}

You can get a pairwise scores between each document:

    >>> print(o.getMeanOverlapScores())
    {
		(0, 1): 0.75,
		(0, 2): 0.7,
		(1, 2): 0.675
	}

You can find similar document by searching for duplicates with a threshold:

    >>> print(o.findDuplicates(threshold=0.75))
    [
		{0, 1}
	]

You can get preprocessed document with this method, the preprocessing do char normalization, lower case chars, tokenize, remove tokens that are not wordw and finally remove stop words:

    >>> print(o.getDocuments())
    [
		[
			"overlap",
			"librarie"
		],
		[
			"work",
			"overlap",
			"librarie",
			"tool"
		],
		[
			"working",
			"collegue",
			"overlap",
			"librarie",
			"tool"
		]
	]


## Others

See the code to have more information for:

	>>> from nlptools.langrecognizer import *
	>>> from nlptools.basics import *
	>>> from nlptools.tokenizer import *