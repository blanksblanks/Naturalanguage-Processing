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
    count = 0
    test = "I ate a slice of the  pizza and the pizza was tasty pizza. What?! It was good!"
    for sentence in brown: # each sentence in brown corpus is one line
        tokens = nltk.word_tokenize(sentence)
        tokens.append('STOP')
        count += 1
        for word in tokens:
            if word in unigram_c:
                unigram_c[word] += 1 # if seen, increment its count
            else:
                unigram_c[word] = 1 # init value at 0
    print unigram_c
    # tokens = [token.lower() for token in tokens if token not in string.punctuation]
    # print sentence
    # numTokens = len(tokens)
    # numTokens = float(numTokens)
    # print numTokens
   
    # counts for each n-gram
    # for item in set(unigram_c):
    #    unigram_count[item] = tokens.count(item)
    # unigram_c = [(item, tokens.count(item)) for item in set(tokens)]
    # print unigram_count

    # unigram: P(w) = c(w)/V = count of word / size of vocabulary
    # unigram_prob = [(item, (tokens.count(item)/numTokens)) for item in set(tokens)]
    # unigram_prob = {}
    # for item in set(unigram_c):
    #    unigram_prob[item] = math.log((unigram_c[item]/count),2)
    # printd(unigram_prob)

    # bigram_tuples = tuple(nltk.bigrams(tokens))
    # trigram_tuples = tuple(nltk.trigrams(tokens)

    # bigram: times appeared together / times word by itself
    # bigram_prob = {}
    # for item in set(bigram_tuples):
    #    fword = item[0]
    #    prob = bigram_tuples.count(item)/unigram_count[fword]
    #    bigram_prob[item] = prob
    # printd(bigram_prob)

    # count = {(item, (bigram_tuples.count(item)/unigram_c[(item[0])]) for item in set(bigram_tuples))}
    # print count

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
