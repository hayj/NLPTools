from nlptools.preprocessing import *

# Use doQuoteNormalization to normalize all quotation to ASCII ' and " chars:'
t = "« Hello World » I’m ``Mick´´"
print(preprocess(t, doQuoteNormalization=True))

# Remove the html and unescape the html:
t = "Hello <span>World</span>! &gt;&lt;"
print(preprocess(t, removeHtml=True, unescapeHtml=True))

# Reduce black spaces, remove accents and reduce long char sequences:
t = "  Hello Béà \t !!!!!!! \n\n \n Fine?"
print(preprocess(t, doReduceBlank=True, stripAccents=True, doReduceCharSequences=True, charSequencesMaxLength=3))

# Normalize emojis to the utf-8 char 
t = ":-) These are emojis ;) 😣 😀 :o)"
print(preprocess(t, doNormalizeEmojis=True))

# Normalize specific chars (for example ━, 一 and – are replaced by the normal form —, … is repaced by ...):
t = "Hello guy… I am━actually not━ok!"
print(preprocess(t, doSpecialMap=True))

# Remove unknown chars and badly encoded chars:
t = "Hello 10€ and 8$ ® 字 � are 20% µ ç"
print(preprocess(t, doBadlyEncoded=True, replaceUnknownChars=True, doReduceBlank=True, stripAccents=True))

# Remove urls:
t = "Pls visit http://test.com !!"
print(preprocess(t, doRemoveUrls=True))

