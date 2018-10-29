# coding: utf-8

from nltk.corpus import stopwords
import re
from nltk.stem import WordNetLemmatizer
from collections import OrderedDict
from nltk.stem.porter import PorterStemmer
import random

import unicodedata

dls2015SwPunctList1 = None

def initDls2015SwPunctList1():
    global dls2015SwPunctList1
    if dls2015SwPunctList1 is None:
        dls2015SwPunctList1 = list(set(['(','-lrb-','.',',','-','?','!',';','_',':','{','}','[','/',']','...','"','\'',')', '-rrb-'] + \
        stopwords.words('english') + \
#         StopWord.swDict["nltkextrasw1"] + \
#         StopWord.swDict["nltkextrasw2"] + \
        ['\'s', '\'d', '\'ll']))
    return dls2015SwPunctList1

def isDLS2015SwOrPunct1(word):
    initDls2015SwPunctList1()
    return word.lower() in dls2015SwPunctList1

dls2015SwPunctList2 = None

def initDls2015SwPunctList2():
    global dls2015SwPunctList2
    if dls2015SwPunctList2 is None:
        dls2015SwPunctList2 = list(set(['(','-lrb-','.',',','-','?','!',';','_',':','{','}','[','/',']','...','"','\'',')', '-rrb-'] + \
        stopwords.words('english') + \
        StopWord.swDict["nltkextrasw1"] + \
        StopWord.swDict["nltkextrasw2"] + \
        ['-lrb-', '-rrb-', '-lsb-', '-rsb-', '-lcb-', '-rcb-'] + \
        ['\'s', '\'d', '\'ll']))
    return dls2015SwPunctList2

def isDLS2015SwOrPunct2(word):
    initDls2015SwPunctList2()
    return word.lower() in dls2015SwPunctList2

def stripAccents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

lemmatizer = None
def lemmatize(words):
    global lemmatizer
    if lemmatizer is None:
        lemmatizer = WordNetLemmatizer()
    if isinstance(words, list):
        newWords = []
        for word in words:
            newWords.append(lemmatizer.lemmatize(word))
        return newWords
    else:
        return lemmatizer.lemmatize(words.decode("utf-8"))

porter_stemmer = None
def stem(words):
    global porter_stemmer
    if porter_stemmer is None:
        porter_stemmer = PorterStemmer()
    if isinstance(words, list):
        newWords = []
        for word in words:
            newWords.append(porter_stemmer.stem(word))
        return newWords
    else:
        return porter_stemmer.stem(words.decode("utf-8"))


def isStopWordOrPunct(word):
    if isPunct(word) or isStopWord(word):
        return True
    else:
        return False

def isStopWordOrPunctList(word, swList):
    if isPunct(word):
        return True
    return isStopWordList(word, swList)

def isStopWordList(word, swList):
    return word in swList

englishNLTKStopWords = None
def initNLTKStopWords():
    global englishNLTKStopWords
    if englishNLTKStopWords is None:
        englishNLTKStopWords = stopwords.words('english') + \
        [str(word) for word in StopWord.swDict["nltkextrasw1"]] + \
        [str(word) for word in StopWord.swDict["nltkextrasw2"]]

        
def isStopWord(word):
    initNLTKStopWords()
    if (word.lower() not in englishNLTKStopWords):
        return False
    else:
        return True
    

def isWord(word):
    return not isPunct(word);
    


def removeStopWordsAndPunct(tokens, lower=False):
    newTokens = [];
    for word in tokens:
        if not isStopWordOrPunct(word):
            newTokens.append(word.lower() if lower else word);
    return newTokens;


def removeStopWords2(tokens):
    newTokens = [];
    for word in tokens:
        if not isStopWord(word):
            newTokens.append(word);
    return newTokens;

def removeStopWords(tokens):
    initNLTKStopWords()
    return [word for word in tokens if word.lower() not in englishNLTKStopWords]

def removeStopWordsSwList(tokens, swList):
    return [word for word in tokens if word.lower() not in swList]

def removeStopWordsAlreadyLowered(tokens):
    initNLTKStopWords()
    return [word for word in tokens if word not in englishNLTKStopWords]



def toLower(tokens):
    for i in range(len(tokens)):
        tokens[i] = tokens[i].lower();
    return tokens;





class StopWord(object):
    version = 1
    swDict = OrderedDict()
    # WARNING yo instead of you for the enwiki maltconverter...
    swDict["nltksw1"] = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves']
    swDict["nltksw2"] = ['what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those']
    swDict["nltksw3"] = ['am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing']
    swDict["nltksw4"] = ['a', 'an', 'the']
    swDict["nltksw5"] = ['and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very']
    swDict["nltksw6"] = ['s', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn', 'hasn', 'haven', 'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren', 'won', 'wouldn']
    swDict["nltkextrasw1"] = ["'d", "'ve", "'ll", "'s", "'m", "'t", "'re"]
    swDict["nltkextrasw2"] = ["n't"]
    swDict["smallsw1"] = ['a', 'an', 'and', 'are', 'as', 'at', 'be',
                           'by', 'for', 'from', 'has', 'he', 'in', 
                           'is', 'it', 'its', 'of', 'on', 'that',
                           'the', 'to', 'was', 'were', 'will', 'with',
                           'this', "'d", "'ll", "'s", "'m", "'t",
                           "'re", "d", "ve", "ll", "s", "m", "t", "re"]
    
    swDict["smallsw2"] = ['a', 'an', 'and', 'are', 'as', 'at', 'be',
                           'by', 'in', 'is', 'it', 'of', 'on',
                           'that', 'the', 'to', 'was', 'were', 'will',
                           'this', "'d", "'ll", "'s", "'m", "'t",
                           "'re", "d", "ve", "ll", "s", "m", "t", "re"]
    
    swDict["smallsw3"] = ['a', 'an', 'and', 'are', 'as', 'at', 'be',
                       'by', 'in', 'is', 'it', 'of', 'on',
                       'that', 'the', 'to', 'was', 'were', 'will',
                       'this', "'d", "'ll", "'s", "'m", "'t",
                       "'re", "d", "ve", "ll", "s", "m", "t", "re",
                       'don', 'do', 'does', 'not', 'won', "n't"]
    
    swDict["smallsw4"] = ['a', 'an', 'and', 'are', 'as', 'at', 'be',
                           'by', 'for', 'from', 'has', 'he', 'in', 
                           'is', 'it', 'its', 'of', 'on', 'that',
                           'the', 'to', 'was', 'were', 'will', 'with',
                           'this', "'d", "'ll", "'s", "'m",
                           "'re", "d", "ve", "ll", "s", "m", "re"]
    
    # WARNING : "n't" added after converting enwiki with matltconverter modeule
    swDict["bigsw1"] = ["a", "able", "about", "above", "abst", "accordance", "according", "accordingly", "across", "act", "actually", "added", "adj", "affected", "affecting", "affects", "after", "afterwards", "again", "against", "ah", "all", "almost", "alone", "along", "already", "also", "although", "always", "am", "among", "amongst", "an", "and", "announce", "another", "any", "anybody", "anyhow", "anymore", "anyone", "anything", "anyway", "anyways", "anywhere", "apparently", "approximately", "are", "aren", "arent", "arise", "around", "as", "aside", "ask", "asking", "at", "auth", "available", "away", "awfully", "b", "back", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "begin", "beginning", "beginnings", "begins", "behind", "being", "believe", "below", "beside", "besides", "between", "beyond", "biol", "both", "brief", "briefly", "but", "by", "c", "ca", "came", "can", "cannot", "can't", "cause", "causes", "certain", "certainly", "co", "com", "come", "comes", "contain", "containing", "contains", "could", "couldnt", "d", "date", "did", "didn't", "different", "do", "does", "doesn't", "doing", "done", "don't", "down", "downwards", "due", "during", "e", "each", "ed", "edu", "effect", "eg", "eight", "eighty", "either", "else", "elsewhere", "end", "ending", "enough", "especially", "et", "et-al", "etc", "even", "ever", "every", "everybody", "everyone", "everything", "everywhere", "ex", "except", "f", "far", "few", "ff", "fifth", "first", "five", "fix", "followed", "following", "follows", "for", "former", "formerly", "forth", "found", "four", "from", "further", "furthermore", "g", "gave", "get", "gets", "getting", "give", "given", "gives", "giving", "go", "goes", "gone", "got", "gotten", "h", "had", "happens", "hardly", "has", "hasn't", "have", "haven't", "having", "he", "hed", "hence", "her", "here", "hereafter", "hereby", "herein", "heres", "hereupon", "hers", "herself", "hes", "hi", "hid", "him", "himself", "his", "hither", "home", "how", "howbeit", "however", "hundred", "i", "id", "ie", "if", "i'll", "im", "immediate", "immediately", "importance", "important", "in", "inc", "indeed", "index", "information", "instead", "into", "invention", "inward", "is", "isn't", "it", "itd", "it'll", "its", "itself", "i've", "j", "just", "k", "keep     keeps", "kept", "kg", "km", "know", "known", "knows", "l", "largely", "last", "lately", "later", "latter", "latterly", "least", "less", "lest", "let", "lets", "like", "liked", "likely", "line", "little", "'ll", "look", "looking", "looks", "ltd", "m", "made", "mainly", "make", "makes", "many", "may", "maybe", "me", "mean", "means", "meantime", "meanwhile", "merely", "mg", "might", "million", "miss", "ml", "more", "moreover", "most", "mostly", "mr", "mrs", "much", "mug", "must", "my", "myself", "n", "na", "name", "namely", "nay", "nd", "near", "nearly", "necessarily", "necessary", "need", "needs", "neither", "never", "nevertheless", "new", "next", "nine", "ninety", "no", "nobody", "non", "none", "nonetheless", "noone", "nor", "normally", "nos", "not", "noted", "nothing", "now", "nowhere", "o", "obtain", "obtained", "obviously", "of", "off", "often", "oh", "ok", "okay", "old", "omitted", "on", "once", "one", "ones", "only", "onto", "or", "ord", "other", "others", "otherwise", "ought", "our", "ours", "ourselves", "out", "outside", "over", "overall", "owing", "own", "p", "page", "pages", "part", "particular", "particularly", "past", "per", "perhaps", "placed", "please", "plus", "poorly", "possible", "possibly", "potentially", "pp", "predominantly", "present", "previously", "primarily", "probably", "promptly", "proud", "provides", "put", "q", "que", "quickly", "quite", "qv", "r", "ran", "rather", "rd", "re", "readily", "really", "recent", "recently", "ref", "refs", "regarding", "regardless", "regards", "related", "relatively", "research", "respectively", "resulted", "resulting", "results", "right", "run", "s", "said", "same", "saw", "say", "saying", "says", "sec", "section", "see", "seeing", "seem", "seemed", "seeming", "seems", "seen", "self", "selves", "sent", "seven", "several", "shall", "she", "shed", "she'll", "shes", "should", "shouldn't", "show", "showed", "shown", "showns", "shows", "significant", "significantly", "similar", "similarly", "since", "six", "slightly", "so", "some", "somebody", "somehow", "someone", "somethan", "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "specifically", "specified", "specify", "specifying", "still", "stop", "strongly", "sub", "substantially", "successfully", "such", "sufficiently", "suggest", "sup", "sure     t", "take", "taken", "taking", "tell", "tends", "th", "than", "thank", "thanks", "thanx", "that", "that'll", "thats", "that've", "the", "their", "theirs", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "thered", "therefore", "therein", "there'll", "thereof", "therere", "theres", "thereto", "thereupon", "there've", "these", "they", "theyd", "they'll", "theyre", "they've", "think", "this", "those", "thou", "though", "thoughh", "thousand", "throug", "through", "throughout", "thru", "thus", "til", "tip", "to", "together", "too", "took", "toward", "towards", "tried", "tries", "truly", "try", "trying", "ts", "twice", "two", "u", "un", "under", "unfortunately", "unless", "unlike", "unlikely", "until", "unto", "up", "upon", "ups", "us", "use", "used", "useful", "usefully", "usefulness", "uses", "using", "usually", "v", "value", "various", "'ve", "very", "via", "viz", "vol", "vols", "vs", "w", "want", "wants", "was", "wasnt", "way", "we", "wed", "welcome", "we'll", "went", "were", "werent", "we've", "what", "whatever", "what'll", "whats", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "wheres", "whereupon", "wherever", "whether", "which", "while", "whim", "whither", "who", "whod", "whoever", "whole", "who'll", "whom", "whomever", "whos", "whose", "why", "widely", "willing", "wish", "with", "within", "without", "wont", "words", "world", "would", "wouldnt", "www", "x", "y", "yes", "yet", "you", "youd", "you'll", "your", "youre", "yours", "yourself", "yourselves", "you've", "z", "zero", "'d", "'ll", "'s", "'m", "'t", "'re", "d", "ve", "ll", "s", "m", "t", "re", "n't"]
    swDict["sentsw1"] = ['no', 'not', 't', "'t", 'don', 'ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn', 'hasn', 'haven', 'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren', 'won', 'wouldn', "n't"]
    swDict["sentsw2"] = ['good', 'nice', 'well']
    swDict["sentsw3"] = ['bad', 'worst', 'worse', 'badly']
    swDict["sentsw4"] = ['very', 'strong', 'too', 'quiet', 'many', 'lot', 'much', 'big', 'strongest', 'best', 'better', 'bigger', 'bigest', 'stronger', 'pretty']
    
    # Agrregation :
    swDict["nltksw"] = swDict["nltksw1"] + swDict["nltksw2"] +  swDict["nltksw3"] \
                        + swDict["nltksw4"] + swDict["nltksw5"] + swDict["nltksw6"] \
                        + swDict["nltkextrasw1"] + swDict["nltkextrasw2"]
                        
    swDict["sentsw"] = swDict["sentsw1"] + swDict["sentsw2"] +  swDict["sentsw3"] \
                        + swDict["sentsw4"]
    
    
    
