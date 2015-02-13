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
    for word in set(wbrown):
        if wbrown.count(word) > 5:
            print word, wbrown.count(word)
            knownwords.append(word)
    # print knownwords
    # print wbrown
    return knownwords

#this function takes a set of sentences and a set of words that should not be marked '_RARE_'
#brown is a python list where every element is a python list of the words of a particular sentence
#and outputs a version of the set of sentences with rare words marked '_RARE_'
def replace_rare(brown, knownwords):
    rare = []
    sentence = []
    print brown
    for word in brown:
        if word in knownwords:
            # rare.append(word)
            sentence.append(word)
            # if word is 'STOP' - DIDN'T WORK, WHY?
            if word == 'STOP': # detect sentence
                sentence.append(word)
                rare.append(sentence) # add sentence to rare
                sentence = [] # create empty list for next sentence
            else:
                print 'False', word
                print sentence
        else:
            # rare.append('_RARE_')
            sentence.append('_RARE_')
    print rare
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
    taglist = []
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

    #do viterbi on brown_dev (question 5)
    viterbi_tagged = viterbi(brown_dev, taglist, knownwords, qvalues, evalues)

    #question 5 output
    q5_output(viterbi_tagged)

    #do nltk tagging here
    nltk_tagged = nltk_tagger(brown_dev)

    #question 6 output
    q6_output(nltk_tagged)
if __name__ == "__main__": main()
