

from nlptools.preprocessing import *
from nlptools.tokenizer import *
from systemtools.basics import *
from nlptools.utils import *
import emoji
import re


class EmojiNormalizer():
	def __init__(self, logger=None, verbose=True, useEmojiLib=True):
		self.useEmojiLib = useEmojiLib			
		self.logger = logger
		self.verbose = verbose
		emojisAsciiToUtf8Strict = dict()
		emojisAsciiToUtf8 = dict()
		lines = fileToStrList(getExecDir(__file__) + "/data/emojis/emojis-ascii-to-utf8.txt")
		for originalLine in lines:
			line = originalLine.split("\t")
			if len(line) == 3 and line[2] == "|":
				emojisAsciiToUtf8Strict[line[0]] = line[1]
			elif len(line) == 2:
				emojisAsciiToUtf8[line[0]] = line[1]
			else:
				logError("this line is not well formed:\n" + str(line), logger, verbose=verbose)
		self.emojisMRStrict = MultiReplacer(emojisAsciiToUtf8Strict, logger=logger, verbose=verbose, wrapWhiteSpaces=True)
		self.emojisMR = MultiReplacer(emojisAsciiToUtf8, logger=logger, verbose=verbose)

	def replace(self, text):
		if text is None or len(text) <= 1:
			return text
		else:
			text = self.emojisMR.replace(text)
			text = self.emojisMRStrict.replace(text)
			if self.useEmojiLib:
				try:
					text = emoji.emojize(text, use_aliases=True)
				except Exception as e:
					logException(e, self)
			return text





emojiNormalizerSingleton = None
def normalizeEmojis(text, logger=None, verbose=True):
	global emojiNormalizerSingleton
	if emojiNormalizerSingleton is None:
		emojiNormalizerSingleton = EmojiNormalizer(logger=logger, verbose=verbose)
	return emojiNormalizerSingleton.replace(text)