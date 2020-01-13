

from systemtools.basics import *
from systemtools.file import *
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

def isEmoji2(token):
	emoji_pattern = re.compile(
    u"(\ud83d[\ude00-\ude4f])|"  # emoticons
    u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
    u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
    u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
    u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
	"+", flags=re.UNICODE)
	return emoji_pattern.match(token)

def isEmoji(token):
	if token is None or len(token) == 0:
		return False
	RE_EMOJI = re.compile('^([\U00010000-\U0010ffff]|[\U00002600-\U000026FF])$', flags=re.UNICODE)
	return RE_EMOJI.match(token)

def isKnownEmoji(token):
	return token in getEmojisSet()


emojiNormalizerSingleton = None
def normalizeEmojis(text, logger=None, verbose=True):
	global emojiNormalizerSingleton
	if emojiNormalizerSingleton is None:
		emojiNormalizerSingleton = EmojiNormalizer(logger=logger, verbose=verbose)
	return emojiNormalizerSingleton.replace(text)


emojisSet = None
def getEmojisSet():
	global emojisSet
	if emojisSet is None:
		emojisSet = set()
		for line in fileToStrList(getExecDir(__file__) + "/data/emojis/emojis-ascii-to-utf8.txt"):
			try:
				emoji = line.split("\t")[1]
				if isEmoji(emoji):
					emojisSet.add(emoji)
			except: pass
	return emojisSet


emojisASCIISet = None
def getASCIIEmojisSet():
	global emojisASCIISet
	if emojisASCIISet is None:
		text = " ".join(fileToStrList(getExecDir(__file__) + "/data/emojis/emojis-ascii-to-utf8.txt"))
		emojisASCIISet = text.split()
		sub = {"|", " ", "\t", "\n"}.union(getEmojisSet())
		emojisASCIISet = substract(emojisASCIISet, sub)
	return emojisASCIISet


if __name__ == '__main__':
	printLTS(getEmojisSet())