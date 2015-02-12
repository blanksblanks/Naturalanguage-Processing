from __future__ import division
import nltk
import string
import math

#a function that calculates unigram, bigram, and trigram probabilities
#brown is a python list of the sentences
#this function outputs three python dictionaries, where the key is a tuple expressing the ngram and the value is the log probability of that ngram
#make sure to return three separate lists: one for each ngram
def calc_probabilities(brown):
    unigram_c = {}
    bigram_c = {}
    trigram_c = {}
    unigram_p = {}
    bigram_p = {}
    trigram_p = {}
    totalCount = 0
    test = "I ate a slice of the  pizza and the pizza was tasty pizza. What?! It was good!"
    
    # counts for each n-gram
    for sentence in brown: # each sentence in brown corpus is one line
        tokens = nltk.word_tokenize(sentence)
        tokens.append('STOP')
        for word in tokens:
            totalCount += 1
            if (word,) in unigram_c:
                unigram_c[word,] += 1 # if seen, increment its count
            else:
                unigram_c[word,] = 1 # init value at 0
        tokens.insert(0, '*')
        bigram_tuples = tuple(nltk.bigrams(tokens))
        for bigram in set(bigram_tuples):
            if bigram in bigram_c:
                bigram_c[bigram] += 1
            else:
                bigram_c[bigram] = 1
        tokens.insert(0, '*')
        trigram_tuples = tuple(nltk.trigrams(tokens))
        for trigram in set(trigram_tuples):
            if trigram in trigram_c:
                trigram_c[trigram] += 1
            else:
                trigram_c[trigram] = 1

    # unigram: P(w) = c(w)/V = count of word / size of vocabulary
    for item in unigram_c:
        unigram_p[item] = math.log((unigram_c[item]/totalCount),2)

    # bigram: times appeared together / times word by itself
    for item in bigram_c:
        word = item[0]
        if word is '*':
            word = 'STOP'
        prob = bigram_c[item]/unigram_c[word,]
        bigram_p[item] = math.log(prob,2)
    
    # trigram:  
    for item in trigram_c:
        bigram = item[:-1]
        if bigram[1] is '*':
            prob = trigram_c[item]/unigram_c['STOP',]
        #  print item, trigram_c[item], unigram_c['STOP',], prob, math.log(prob,2)
        else:
            prob = trigram_c[item]/bigram_c[bigram]
            # print item, trigram_c[item], bigram_c[bigram], prob, math.log(prob,2)
        trigram_p[item] = math.log(prob,2)

#    print bigram_p, trigram_p
    return unigram_p, bigram_p, trigram_p

# helper method to print dictionary lineb y line
def printd(dictionary):
    for item in dictionary:
        print item, ':', dictionary[item]

#each ngram is a python dictionary where keys are a tuple expressing the ngram, and the value is the log probability of that ngram
def q1_output(unigrams, bigrams, trigrams):
    #output probabilities
    outfile = open('A1.txt', 'w')
    for unigram in unigrams:
        outfile.write('UNIGRAM ' + unigram[0] + ' ' + str(unigrams[unigram]) + '\n')
    for bigram in bigrams:
        outfile.write('BIGRAM ' + bigram[0] + ' ' + bigram[1]  + ' ' + str(bigrams[bigram]) + '\n')
    for trigram in trigrams:
        outfile.write('TRIGRAM ' + trigram[0] + ' ' + trigram[1] + ' ' + trigram[2] + ' ' + str(trigrams[trigram]) + '\n')
    outfile.close()
    
#a function that calculates scores for every sentence
#ngram_p is the python dictionary of probabilities
#n is the size of the ngram
#data is the set of sentences to score
#this function must return a python list of scores, where the first element is the score of the first sentence, etc. 
def score(ngram_p, n, data):
    scores = []
    for sentence in data:
        tokens = nltk.word_tokenize(sentence)
        tokens.append('STOP')
        prob = 0
        if n == 1:
            for unigram in tokens:
                if (unigram,) in ngram_p:
                    prob += ngram_p[unigram,] # sum all log probabilities
                else:
                    prob = -1000.0
                    break
        elif n == 2:
            tokens.insert(0, '*')
            bigram_tuples = tuple(nltk.bigrams(tokens))
            for bigram in bigram_tuples:
                if bigram in ngram_p:
                    prob += ngram_p[bigram]
                else:
                    prob = -1000.0
                    break
        elif n == 3:
            tokens.insert(0, '*')
            tokens.insert(0, '*')
            trigram_tuples = tuple(nltk.trigrams(tokens))
            for trigram in trigram_tuples:
                if trigram in ngram_p:
                    prob += ngram_p[trigram]
                else:
                    prob = -1000.0
                    break
        scores.append(prob) 
    # print scores
    return scores


#this function outputs the score output of score()
#scores is a python list of scores, and filename is the output file name
def score_output(scores, filename):
    outfile = open(filename, 'w')
    for score in scores:
        outfile.write(str(score) + '\n')
    outfile.close()


#this function scores brown data with a linearly interpolated model
#each ngram argument is a python dictionary where the keys are tuples that express an ngram and the value is the log probability of that ngram
#like score(), this function returns a python list of scores
def linearscore(unigrams, bigrams, trigrams, brown):
    scores = []
    return scores

def main():
    #open data
    infile = open('Brown_train.txt', 'r')
    brown = infile.readlines()
    infile.close()

    #calculate ngram probabilities (question 1)
    unigrams, bigrams, trigrams = calc_probabilities(brown)

    #question 1 output
    q1_output(unigrams, bigrams, trigrams)

    #score sentences (question 2)
    uniscores = score(unigrams, 1, brown)
    biscores = score(bigrams, 2, brown)
    triscores = score(trigrams, 3, brown)

    #question 2 output
    score_output(uniscores, 'A2.uni.txt')
    score_output(biscores, 'A2.bi.txt')
    score_output(triscores, 'A2.tri.txt')

    #linear interpolation (question 3)
    linearscores = linearscore(unigrams, bigrams, trigrams, brown)

    #question 3 output
    score_output(linearscores, 'A3.txt')

    #open Sample1 and Sample2 (question 5)
    infile = open('Sample1.txt', 'r')
    sample1 = infile.readlines()
    infile.close()
    infile = open('Sample2.txt', 'r')
    sample2 = infile.readlines()
    infile.close() 

    #score the samples
    sample1scores = linearscore(unigrams, bigrams, trigrams, sample1)
    sample2scores = linearscore(unigrams, bigrams, trigrams, sample2)

    #question 5 output
    score_output(sample1scores, 'Sample1_scored.txt')
    score_output(sample2scores, 'Sample2_scored.txt')

if __name__ == "__main__": main()
