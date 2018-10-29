emojisAsciiToUtf8Strict = None
emojisAsciiToUtf8 = None
def normalizeEmojis(text, logger=None, verbose=True):
	global emojisAsciiToUtf8Strict
	global emojisAsciiToUtf8
	if text is None or len(text) <= 1:
		return text
	if emojisAsciiToUtf8Strict is None or emojisAsciiToUtf8 is None:
		emojisAsciiToUtf8Strict = dict()
		emojisAsciiToUtf8 = dict()
		lines = fileToStrList(getExecDir(__file__) + "/data/emojis/emojis-ascii-to-utf82.txt")
		for line in lines:
			line = line.split("\t")
			if len(line) == 3 and line[2] == "|":
				emojisAsciiToUtf8Strict[line[0]] = line[1]
			elif len(line) == 2:
				emojisAsciiToUtf8[line[0]] = line[1]
			else:
				logError("this line is not well formed:\n" + str(line), logger, verbose=verbose)
	text = " " + text + " "
	for asciiEmoji, utf8Emoji in emojisAsciiToUtf8Strict.items():
		# toEscape = "()|[]$^."
		# toEscape = list(toEscape)
		# for currentToEscape in toEscape:
		# 	asciiEmoji = asciiEmoji.replace(currentToEscape, "\\" + currentToEscape)
		asciiEmoji = re.escape(asciiEmoji)
		# if previousAsciiEmoji != asciiEmoji:
		# 	print(previousAsciiEmoji)
		# 	print(asciiEmoji)
		# 	print()
		# 	input()
		currentRegex = "(\s)(" + asciiEmoji + ")(\s)"
		currentRegex = re.compile(currentRegex)
		text = currentRegex.sub("\g<1>" + utf8Emoji + "\g<3>", text)
	for asciiEmoji, utf8Emoji in emojisAsciiToUtf8.items():
		text = text.replace(asciiEmoji, utf8Emoji)
	text = text[1:-1]
	return text
	# printLTS(emojisAsciiToUtf8Strict)
	# printLTS(emojisAsciiToUtf8)	