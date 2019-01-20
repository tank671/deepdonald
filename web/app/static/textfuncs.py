## assumes learn already being set up and trained/loaded with weights
import time

def rawPredict(starter='xxbos', length=100):
    res = learn.predict(starter, length, temperature=1.1, min_p=0.0001)
    time.sleep(2)
    return "".join(res)

def cleanText(text, for_twitter=False):
    words = text.split()
    n = len(words)-1
    for i, word in enumerate(words):
        if word == 'xxbos':
            words[i] = ''
        elif word == 'xxmaj':
            if i < n:
                words[i+1] = words[i+1][0].upper() + words[i+1][1:]
            words[i] = ''
        elif word == 'xxup':
            if i < n:
                words[i+1] = words[i+1].upper()
            words[i] = ''
        elif word == 'xxunk' or word == '(' or word == ')' or word == '"':
            words[i] = ''
        elif word == 'xxrep':
            if i < n-1:
                if i == 0:
                    words[i] = words[i+2]*int(words[i+1])
                else:
                    words[i-1] += words[i+2]*int(words[i+1])
                    words[i] = ''
                words[i+1] = ''
                words[i+2] = ''               
            else:
                words[i] = ''
                if i < n:
                    words[i+1] = ''
        elif word == '.' or word == '!' or word == '?' or word == ';' or word == ',' or word == ':' or word == '%':
            if i > 0:
                j = i - 1
                while (j >= 0) & (words[j] == ''):
                    j -= 1
                words[j] += words[i]
                words[i] = ''
        elif word == '#':
            if i < n-1:
                if words[i+1] == 'xxup':
                    words[i] = '#' + words[i+2].upper()
                    words[i+1] = ''
                    words[i+2] = ''
                elif words[i+1] == 'xxmaj':
                    words[i] = '#' + words[i+2][0].upper() + words[i+2][1:]
                    words[i+1] = ''
                    words[i+2] = ''
            if i < n:
                words[i] += words[i+1]
                words[i+1] = ''
        elif word == "n't":
            if i > 1:
                words[i-1] += words[i]
                words[i] = ''
        elif len(word) > 1:
            if word[0] == "'" or word[0] == "’":
                if i > 0:
                    words[i-1] += words[i]
                    words[i] = ''
        if len(word) > 1:
             if (word[0] == '@') & (for_twitter==True):
                words[i] = '(@)' + word[1:]
    res = ' '.join(words).strip()
    res = re.sub(r"\s+", " ", res)
    return res

def trimText(text, n=0, for_twitter=False):
    if len(text) == 0:
        res = False
    else:
        pieces = re.split(r"[\.\!\?]", text)
        punc = re.findall(r"[\.\!\?]", text)
        weave = [pieces[i]+punc[i] for i in range(len(pieces)-(n+1))]
        res = "".join(weave)
        last = res.split()[-1].lower()
        if last == 'mr.' or last == 'mrs.':
            res = trimText(text, n+1)
        if (for_twitter==True) & (len(res)>250):
            res = trimText(text, n+1, for_twitter=True)
    return res

def generateText(starter='xxbos', length=100):
    mytext = rawPredict(starter=starter, length=length)
    mytext = cleanText(mytext, for_twitter=False)
    mytext = trimText(mytext)
    return mytext
