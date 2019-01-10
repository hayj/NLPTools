
## Dependances on Ubuntu

	sudo apt-get install libenchant1c2a

## Installation (Python 3)

	git clone https://github.com/hayj/NLPTools.git
	pip install ./NLPTools/wm-dist/*.tar.gz

Or use this script: <https://github.com/hayj/Bash/blob/master/hjupdate.sh>

## Import

See the code to have more information:

	>>> from nlptools.langrecognizer import *
	>>> from nlptools.basics import *
	>>> from nlptools.tokenizer import *

## Overlap

Get your data:

	>>> from nlpstools.overlap import *
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