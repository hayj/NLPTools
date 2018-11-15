
import re

class MultiReplacer():
	"""
		https://gist.github.com/bgusach/a967e0587d6e01e889fd1d776c5f3729
    	https://stackoverflow.com/questions/6116978/how-to-replace-multiple-substrings-of-a-string

    	If wrapWhiteSpaces, all replacements must be wrapped by white spaces (or beginning/end of the text) to be taken into account
	"""
	def __init__(self, replacements, wrapWhiteSpaces=False, logger=None, verbose=True):
		self.replacements = replacements
		self.wrapWhiteSpaces = wrapWhiteSpaces
		self.logger = logger
		self.verbose = verbose
		if self.wrapWhiteSpaces:
			self.substrs = sorted(replacements, key=len, reverse=True)
			for i in range(len(self.substrs)):
				self.substrs[i] = "(\s)(" + re.escape(self.substrs[i]) + ")(\s)"
			self.regexp = re.compile('|'.join(self.substrs))
		else:
			self.substrs = sorted(replacements, key=len, reverse=True)
			self.regexp = re.compile('|'.join(map(re.escape, self.substrs)))

	def __matchToReplacement(self, match):
		element = match.group(0)
		return element[0] + self.replacements[match.group(0)[1:-1]] + element[-1]

	def replace(self, text):
		if isinstance(text, list):
			newText = []
			for t in text:
				newText.append(self.__replace(t))
			return newText
		else:
			return self.__replace(text)

	def __replace(self, text):
		if text is None or len(text) == 0:
			return text
		if self.wrapWhiteSpaces:
			text = " " + text + " "
		if self.wrapWhiteSpaces:
			# We do it twice because of emojis which are one after the other
			text = self.regexp.sub(self.__matchToReplacement, text)
			text = self.regexp.sub(self.__matchToReplacement, text)
		else:
			text = self.regexp.sub(lambda match: self.replacements[match.group(0)], text)
		if self.wrapWhiteSpaces:
			text = text[1:-1]
		return text
