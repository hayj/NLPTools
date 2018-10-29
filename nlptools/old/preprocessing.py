
def magic1(text):

	# current = current.replace("…", '...')
	# current = current.replace("''", '"')
	# current = current.replace("``", '"')
	# current = current.replace("``", '"')
	# current = current.replace("`", "'")
	# current = current.replace("’", "'")
	# current = current.replace("’", "'")
	# current = current.replace("”", '"')
	# current = current.replace("“", '"')
	for form in ["NFC", "NFKC", "NFD", "NFKD"]:
		strToTmpFile(unicodedata.normalize(form, text).encode('ascii', 'ignore').decode('utf-8'), name="enc", ext="txt")
		input("form suivante")
def magic2(text):
	for form in ["NFC", "NFKC", "NFD", "NFKD"]:
		strToTmpFile(''.join(c for c in unicodedata.normalize('NFD', text)
				  if unicodedata.category(c) != 'Mn'), name="enc", ext="txt")
		input("form suivante")
def magic3(text):
		strToTmpFile(unidecode(text), name="enc", ext="txt")




def magicNormalizeText(text, chevronMaxCount=5):
	raise Exception("magicNormalizeText is deprecated")
	if text is None or len(text) == 0:
		return None
	if text.count('<') > chevronMaxCount and text.count('>') > chevronMaxCount:
		text = html2Text(text)
	text = normalizeQuote(text)
	text = reduceBlank(text, keepNewLines=True)
	return text


def stripAccent(s):
	print("stripAccent is DEPRECATED")
	if isinstance(s, str):
		return ''.join(c for c in unicodedata.normalize('NFD', s)
				  if unicodedata.category(c) != 'Mn')
	else:
		return s