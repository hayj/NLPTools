
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

And other parameters like `replaceCurrencyLevel`, `replaceSocialLevel`, `replaceFunctionLevel`... You will also find others function for post-tokenization processing etc.

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