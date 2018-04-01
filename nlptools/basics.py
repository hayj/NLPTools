
def countOverlaps(parsed1, parsed2, ngram):
    count = 0
    for _ in yieldOverlaps(parsed1, parsed2, ngram):
        count += 1
    return count

def hasOverlap(parsed1, parsed2, ngram):
    for _ in yieldOverlaps(parsed1, parsed2, ngram):
        return True
    return False

def yieldOverlaps(parsed1, parsed2, ngram):
    if len(parsed1) < ngram or len(parsed2) < ngram:
        return 0
    for i in range(len(parsed1) - (ngram - 1)):
        currentParsed1Ngram = parsed1[i:i + ngram]
        for i in range(len(parsed2) - (ngram - 1)):
            currentParsed2Ngram = parsed2[i:i + ngram]
            if currentParsed1Ngram == currentParsed2Ngram:
                yield currentParsed1Ngram

