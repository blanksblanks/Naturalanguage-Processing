from __future__ import division
import sys
import nltk
import math

#this function takes the words from the training data and returns a python list of all of the words that occur more than 5 times
#wbrown is a python list where every element is a python list of the words of a particular sentence
def calc_known(wbrown):
    knownwords = []
    # copy word to list if its count is greater than 5
    # knownwords = [word for word in set(wbrown) if wbrown.count(word) > 5] # TOO SLOW
    # for word in set(wbrown):
    #    if wbrown.count(word) > 5: # these counts make things too slow
    #        print word, wbrown.count(word) # log to convince self smth is happening
    #        knownwords.append(word)
    word_c = {}
    for word in wbrown:
        if word in word_c:
            word_c[word] += 1
        else:
            word_c[word] = 1
    for word in word_c:
        if word_c[word] > 5:
            knownwords.append(word) 
    return knownwords

#this function takes a set of sentences and a set of words that should not be marked '_RARE_'
#brown is a python list where every element is a python list of the words of a particular sentence
#and outputs a version of the set of sentences with rare words marked '_RARE_'
def replace_rare(brown, knownwords):
    rare = []
    sentence = []
    # print brown
    for word in brown:
        if word in knownwords:
            sentence.append(word)
            if word == 'STOP': # detect sentence - why doesn't this work? if word is 'STOP'
                rare.append(sentence) # add sentence to rare
                sentence = [] # create empty list for next sentence
        else:
            sentence.append('_RARE_')
    # print rare
    return rare

#this function takes the ouput from replace_rare and outputs it
def q3_output(rare):
    outfile = open("B3.txt", 'w')

    for sentence in rare:
        outfile.write(' '.join(sentence[2:-1]) + '\n')
    outfile.close()

#this function takes tags from the training data and calculates trigram probabilities
#tbrown (the list of tags) should be a python list where every element is a python list of the tags of a particular sentence
#it returns a python dictionary where the keys are tuples that represent the trigram, and the values are the log probability of that trigram
def calc_trigrams(tbrown):
    qvalues = {}
    unigram_c = {}
    bigram_c = {}
    trigram_c = {}
    bigram_tuples = tuple(nltk.bigrams(tbrown))   
    for bigram in bigram_tuples:
        if bigram in bigram_c:
            bigram_c[bigram] += 1
        else:
            bigram_c[bigram] = 1
    trigram_tuples = tuple(nltk.trigrams(tbrown))
    for trigram in trigram_tuples:
        if trigram in trigram_c:
            trigram_c[trigram] += 1
        else:
            trigram_c[trigram] = 1
    for trigram in trigram_c:
        bigram = trigram[:-1]
        prob = trigram_c[trigram]/bigram_c[bigram]
        qvalues[trigram] = math.log(prob,2)
    return qvalues

#this function takes output from calc_trigrams() and outputs it in the proper format
def q2_output(qvalues):
    #output
    outfile = open("B2.txt", "w")
    for trigram in qvalues:
        output = " ".join(['TRIGRAM', trigram[0], trigram[1], trigram[2], str(qvalues[trigram])])
        outfile.write(output + '\n')
    outfile.close()

#this function calculates emission probabilities and creates a list of possible tags
#the first return value is a python dictionary where each key is a tuple in which the first element is a word
#and the second is a tag and the value is the log probability of that word/tag pair
#and the second return value is a list of possible tags for this data set
#wbrown is a python list where each element is a python list of the words of a particular sentence
#tbrown is a python list where each element is a python list of the tags of a particular sentence
def calc_emission(wbrown, tbrown):
    evalues = {}
    taglist = [tag for tag in set(tbrown)]
    pair_c = {}
    tag_c = {}
    # note: wbrown is wbrown_rare version
    i = 0
    for sentence in wbrown:
        # print sentence
        for word in sentence: # could skip first *,* and last STOP
            tag = tbrown[i]
            # print i, tag
            i += 1 # now that tag is assigned, incr tag index for next iter
            pair = (word, tag)
            # print pair
            if pair in pair_c:
                pair_c[pair] += 1
            else:
                pair_c[pair] = 1
            # note: we could replace with list comp but this is cheaper in current loop
            # tag_c = { tag : tbrown.count(tag) for tag in set(tbrown) }
            if tag in tag_c:
                tag_c[tag] += 1
            else:
                tag_c[tag] = 1
    for pair in pair_c:
        tag = pair[1]
        prob = pair_c[pair]/tag_c[tag] # emission is count('word/tag') / count('tag')
        evalues[pair] = math.log(prob, 2)

    return evalues, taglist

#this function takes the output from calc_emissions() and outputs it
def q4_output(evalues):
    #output
    outfile = open("B4.txt", "w")
    for item in evalues:
        output = " ".join([item[0], item[1], str(evalues[item])])
        outfile.write(output + '\n')
    outfile.close()


#this function takes data to tag (brown), possible tags (taglist), a list of known words (knownwords),
#trigram probabilities (qvalues) and emission probabilities (evalues) and outputs a list where every element is a string of a
#sentence tagged in the WORD/TAG format
#brown is a list where every element is a list of words
#taglist is from the return of calc_emissions()
#knownwords is from the the return of calc_knownwords()
#qvalues is from the return of calc_trigrams
#evalues is from the return of calc_emissions()
#tagged is a list of tagged sentences in the format "WORD/TAG". Each sentence is a string with a terminal newline, not a list of tokens.
def viterbi(brown, taglist, knownwords, qvalues, evalues):
    tagged = []
    # our four look up tables: qvalues, evalues, pi and bp
    pi = {} # key: (k, v, w)
    bp = {}
    pi[0,'*','*'] = 0.0 # base case: 1, math.log(1,2) = 0
    print taglist, knownwords, qvalues, evalues
    test = [['*','*','We','saw','her','duck','.','STOP'],['*','*','I','gave','her','cat','food','.','STOP']]
    for sentence in test:
        n = len(sentence) - 3
        y = []
        for k in range(1, n+1): # u @ k - 2, v @ k - 1, w @ k
            if sentence[k+1] not in knownwords: # replace with rare
                word = '_RARE_'
                print 'found RAREWORD'
            else:
                word = sentence[k+1]
            
            if k == 1: # u = s_-1 = s_0 = '*'
                u = v = '*'
                for wtag in taglist:
                    w = wtag
                    print k, u, v, w
                    if (u,v,w) in qvalues and (word,w) in evalues:
                        print 'NEW PI VALUE?!'
                        prob = pi[k-1,u,v] + qvalues[u,v,w] + evalues[word,w]
                        if (k,v,w) not in pi or prob > pi[k,v,w]:
                            pi[k,v,w] = prob
                            bp[k,v,w] = u
                            print 'NEW PI ALERT!'
                            print k, pi, bp
            
            elif k == 2:
                print 'k = 2'
                u = '*'
                for vtag in taglist:
                    v = vtag
                    for wtag in taglist:
                        w = wtag
                        print k, v, w, u
                        if (u,v,w) in qvalues and (word,w) in evalues and (k-1,u,v) in pi:
                            print 'NEW PI VALUE?'
                            prob = pi[k-1,u,v] + qvalues[u,v,w] + evalues[word,w]
                            if (k,v,w) not in pi or prob > pi[k,v,w]:
                                pi[k,v,w] = prob
                                bp[k,v,w] = u
                                print 'NEW PI ALERT!'
                                print k, pi, bp
            else:
                for utag in taglist:
                    u = utag
                    for vtag in taglist:
                        v = vtag
                        for wtag in taglist:
                            w = wtag
                            print k,v,w,u
                            if (u,v,w) in qvalues and (word,w) in evalues and (k-1,u,v) in pi:
                                print 'NEW PI VALUE?!'
                                prob = pi[k-1,u,v] + qvalues[u,v,w] + evalues[word,w]
                                if (k,v,w) not in pi or prob > pi[k,v,w]:
                                    pi[k,v,w] = prob
                                    bp[k,v,w] = u
                                    print 'NEW PI ALERT!'
                                    print k, pi, bp
        
        prev = -1000.0
        endtags = []
        print pi
        print bp
        w = 'STOP'
        for utag in taglist:
            u = utag
            for vtag in taglist:
                v = vtag
                print u,v,w
                print n,u,v
                if (u,v,w) in qvalues and (n,u,v) in pi:
                    print qvalues[u,v,w], pi[n,u,v]
                    print 'STOP - reached end?'
                    prob = pi[n,u,v] + qvalues[u,v,w]
                    if prob > prev:
                        print prob, prev
                        prev = prob
                        print 'ENDTAGS!'
                        print u, v
                        endtags.append(u)
                        endtags.append(v)
                        print endtags
        # [*,*,N,V,N,V,STOP] equivalent to y0, y1, y2...y
        # [0,1,2,3,4,5,6]
        print endtags
        y.extend(endtags)
        y.append('STOP')
        print 'Y!!!!!!!!!!!!'
        print y

        for k in range(n-1, 0, -1):
            backpointer = bp(k+2,y[k+1],y[k+2])
            y.insert(0, backpointer)
       
        print y
        tagged.append(y)

    print tagged
    return tagged

#this function takes the output of viterbi() and outputs it
def q5_output(tagged):
    outfile = open('B5.txt', 'w')
    for sentence in tagged:
        outfile.write(sentence)
    outfile.close()

#this function uses nltk to create the taggers described in question 6
#brown is the data to be tagged
#tagged is a list of tagged sentences the WORD/TAG format. Each sentence is a string with a terminal newline rather than a list of tokens.
def nltk_tagger(brown):
    tagged = []
    return tagged

def q6_output(tagged):
    outfile = open('B6.txt', 'w')
    for sentence in tagged:
        outfile.write(output)
    outfile.close()

#a function that returns two lists, one of the brown data (words only) and another of the brown data (tags only)
def split_wordtags(brown_train):
    wbrown = []
    tbrown = []
    for sentence in brown_train:
        tokens = sentence.split()
        tokens.append('STOP/STOP')
        tokens.insert(0, '*/*')
        tokens.insert(0, '*/*')
        for token in tokens:
            wordtags = token.split('/')
            if len(wordtags) > 2:
                wbrown.append('/'.join(wordtags[:-1]))
            else:
                wbrown.append(wordtags[0])
            tbrown.append(wordtags[-1])
    # print wbrown, tbrown
    return wbrown, tbrown

def main():
    #open Brown training data
    infile = open("Brown_tagged_train.txt", "r")
    brown_train = infile.readlines()
    infile.close()

    #split words and tags, and add start and stop symbols (question 1)
    wbrown, tbrown = split_wordtags(brown_train)

    #calculate trigram probabilities (question 2)
    qvalues = calc_trigrams(tbrown)

    #question 2 output
    q2_output(qvalues)

    #calculate list of words with count > 5 (question 3)
    knownwords = calc_known(wbrown)

    #get a version of wbrown with rare words replace with '_RARE_' (question 3)
    wbrown_rare = replace_rare(wbrown, knownwords)

    #question 3 output
    q3_output(wbrown_rare)

    #calculate emission probabilities (question 4)
    evalues, taglist = calc_emission(wbrown_rare, tbrown)

    #question 4 output
    q4_output(evalues)

    #delete unneceessary data
    del brown_train
    del wbrown
    del tbrown
    del wbrown_rare

    #open Brown development data (question 5)
    infile = open("Brown_dev.txt", "r")
    brown_dev = infile.readlines()
    infile.close()

    #format Brown development data here
    brown_copy = []
    for sentence in brown_dev:
        tokens = nltk.word_tokenize(sentence)
        tokens.insert(0, '*')
        tokens.insert(0, '*')
        tokens.append('STOP')
        brown_copy.append(tokens)
    brown_dev = brown_copy
    del brown_copy
    # print brown_dev

    #do viterbi on brown_dev (question 5)
    viterbi_tagged = viterbi(brown_dev, taglist, knownwords, qvalues, evalues)

    #question 5 output
    q5_output(viterbi_tagged)

    #do nltk tagging here
    nltk_tagged = nltk_tagger(brown_dev)
    
    #question 6 output
    q6_output(nltk_tagged)
if __name__ == "__main__": main()
