from nlptools.pipeline1.utils import *
from nlptools.pipeline1.pipeline import *




if __name__ == '__main__':
	for currentTokenType, examples in TOKEN_TYPE_EXAMPLES.items():
		for example in examples:
			pred = tokenType(example)
			true = currentTokenType
			try:
				assert pred == true
			except:
				print(example)
				print("pred: " + str(pred))
				print("true: " + str(true))
				print()
				print()
				print()
