from __future__  import division

import nltk
import A
from collections import defaultdict


class BerkeleyAligner():

    def __init__(self, align_sents, num_iter):
        self.t, self.q = self.train(align_sents, num_iter)

    # Computes the alignments for align_sent, using this model's parameters. Return
    # an AlignedSent object, with the sentence pair and the alignments computed.
    # def align(self, align_sent):

    # Invoked upon initialization
    # Implement the EM algorithm. num_iters is the number of iterations. Returns the 
    # translation and distortion parameters as a tuple.
    def train(self, aligned_sents, num_iters):
        t = {}
        q = {}

        ger_vocab = set() # e_set: source in unidirectional model
        eng_vocab = set() # f_set: target in unidirectional model
        for aligned_sent in aligned_sents:
            eng_vocab.update(aligned_sent.mots)
            ger_vocab.update(aligned_sent.words) 
        ger_vocab.add(None) # add NULL values to e_set
        # print "Eng", en_vocab
        # print "Ger", ge_vocab
        
        # Usually t(f|e) is given by 1 over set of foreign words
        # init_prob = 1/len(ger_vocab)
        
        # Initialize the translation parameters to be the uniform distribution over
        # all possible words thats appear in a target sentence of a sentence
        # containing the source word
        c_fe = {e:{} for e in ger_vocab}
        # print c_fe
        for aligned_sent in aligned_sents:
            ger_sent = aligned_sent.words
            eng_sent = [None] + aligned_sent.mots # this works, tested in IDLE
            for e in ger_sent:
                for f in eng_sent:
                    if (f,e) in c_fe[e]: # where f given e
                        c_fe[e][(f,e)] += 1
                    else:
                        c_fe[e][(f,e)] = 1 # initialize count
        # print c_fe
        for e in c_fe:
            dic =  c_fe[e]
            for pair in dic: # where pair = (f,e)
                t[pair] = float(dic[pair]) / len(dic)
        
        print t

        # Initialize the alignment parameters to be the uniform distribution over the
        # length of the source sentence
        for aligned_sent in aligned_sents:
            ger_sent = aligned_sent.words
            eng_sent = [None] + aligned_sent.mots
            l = len(ger_sent)
            m = len(eng_sent)
            for i in xrange(l):
                delta_d = 0
                for j in xrange(m): # right?
                    if (j,i,l,m) not in q:
                        q[(j,i,l,m)] = 1/float(l+1)
        # print q

        # total_e = defaultdict(lambda: 0.0)
        # t_ef = t

        for i in xrange(num_iters):
            print '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nIteration', i+1, '...'
            count = {}
            count_e = {}
            for aligned_sent in aligned_sents:
                ger_sent = aligned_sent.words
                eng_sent = [None] + aligned_sent.mots
                sum_e = 0
                for e in ger_sent:
                    sum_e += t[(f,e)]
                for e in ger_sent:
                    count[(f,e)] += (t[(f,e)] / float(sum_e))
                    count_e[e] += (t[(f,e)] / float(sum_e))
            for (f,e) in count.keys():
                t[(f,e)] = float(count[(f,e)] / float(count_e[e]))

        return (t,q)
       
        # print t

    '''
    count_ef = defaultdict(lambda: defaultdict(lambda: 0.0))
    total_f = defaultdict(lambda: 0.0)

    for alignSent in aligned_sents:
        en_set = alignSent.words
        fr_set = [None] + alignSent.mots  

        # Compute normalization
        for e in en_set:
            total_e[e] = 0.0
            for f in fr_set:
                total_e[e] += t_ef[(f,e)]

        # Collect counts
        for e in en_set:
            for f in fr_set:
                c = t_ef[(f,e)] / total_e[e]
                count_ef[e][f] += c
                total_f[f] += c

    # Compute the estimate probabilities
    for f in eng_vocab:
        for e in ger_vocab:
            t_ef[(f,e)] = count_ef[e][f] / total_f[f]

    print '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', t_ef
    '''

    def counting_dict(dictionary, key):
        if key in dictionary:
            dictionary[key] += 1
        else:
            dictionary[key] = 1
        return dictionary

def main(aligned_sents):
    ba = BerkeleyAligner(aligned_sents, 1)
    print ba[0]
    # A.save_model_output(aligned_sents, ba, "ba.txt")
    # avg_aer = A.compute_avg_aer(aligned_sents, ba, 50)

    print ('Berkeley Aligner')
    print ('---------------------------')
    # print('Average AER: {0:.3f}\n'.format(avg_aer))
