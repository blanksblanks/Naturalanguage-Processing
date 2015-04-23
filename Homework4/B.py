from __future__  import division

import nltk
import A
from collections import defaultdict
from nltk.align  import AlignedSent


class BerkeleyAligner():

    def __init__(self, align_sents, num_iter):
        self.t, self.q = self.train(align_sents, num_iter)

    # Computes the alignments for align_sent, using this model's parameters. Return
    # an AlignedSent object, with the sentence pair and the alignments computed.
    def align(self, align_sent):
        # print self.q
        alignment = []
        l = len(align_sent.words)
        m = len(align_sent.mots)
        for j, ger_word in enumerate(align_sent.words):
            max_align_prob = (self.t[(None, ger_word)]*self.q[(j+1,0,l,m)], None)
            for i, eng_word in enumerate(align_sent.mots):
                max_align_prob = max(max_align_prob, (self.t[(eng_word, ger_word)]*self.q[(j+1,i+1,l,m)], i), (self.t[(eng_word, ger_word)],i))
            if max_align_prob[1] is not None:
                alignment.append((j, max_align_prob[1]))
        return AlignedSent(align_sent.words, align_sent.mots, alignment)

    # Invoked upon initialization
    # Implement the EM algorithm. num_iters is the number of iterations. Returns the 
    # translation and distortion parameters as a tuple.
    def train(self, aligned_sents, num_iters):
        t = {}
        q = {}

        ger_vocab = set() # e_set: source in unidirectional model
        eng_vocab = set() # f_set: target in unidirectional model
        for aligned_sent in aligned_sents:
            ger_vocab.update(aligned_sent.words) 
            eng_vocab.update(aligned_sent.mots)
        eng_vocab.add(None) # add NULL values to e_set
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
        
        # print t

        # Initialize the alignment parameters to be the uniform distribution over the
        # length of the source sentence
        # Can just take care of it in the loop below
        '''for aligned_sent in aligned_sents:
            ger_sent = aligned_sent.words
            eng_sent = [None] + aligned_sent.mots
            l = len(ger_sent)
            m = len(eng_sent)
            for i in xrange(l):
                # delta_d = 0
                for j in xrange(m): # right?
                    if (j,i,l,m) not in q:
                        q[(j,i,l,m)] = 1/float(l+1)
        # print q
        '''

        # total_e = defaultdict(lambda: 0.0)
        # t_ef = t

        for i in xrange(num_iters):
            print '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nIteration', i+1, '...'

            # Update t
            # count = {tup:0 for tup in t.keys()}
            # count_e = {e:0 for e in ger_vocab}
            # Update q
            c_fe = {tup:0 for tup in t.keys()}
            # c_fe = t <- doing that makes AER go up > 0.05
            c_e = {e:0 for e in ger_vocab}
            c_ilm = defaultdict(int)
            c_jilm = defaultdict(int)

            for aligned_sent in aligned_sents:
                ger_sent = aligned_sent.words
                eng_sent = [None] + aligned_sent.mots
                # Update t
                # for f in eng_sent:
                #    sum_e = 0
                #    for e in ger_sent:
                #        sum_e += t[(f,e)]
                #    for e in ger_sent:
                #        count[(f,e)] += (t[(f,e)] / float(sum_e))
                #        count_e[e] += (t[(f,e)] / float(sum_e))
                # Update q
                l = len(ger_sent)
                m = len(eng_sent) - 1
                for i in xrange(m+1):
                   # Calculate delta denominator for q(j|i,l,m)
                   f = eng_sent[i]
                   delta_d = 0
                   for j in xrange(1, l+1):
                       e = ger_sent[j-1]
                       # We can just take care of initialization of q here!
                       if (j,i,l,m) not in q:
                           q[(j,i,l,m)] = 1/float(l+1)
                       delta_d += q[(j,i,l,m)] * t[(f,e)]
                   for j in xrange(1, l+1):
                       e = ger_sent[j-1]
                       # Update q rule
                       delta = (q[(j,i,l,m)] * t[(f,e)])/float(delta_d)
                       c_fe[(f,e)] += delta
                       c_e[e] += delta
                       c_ilm[(i,l,m)] += delta
                       c_jilm[(j,i,l,m)] += delta
            # Update t
            for (f,e) in c_fe.keys():
                t[(f,e)] = float(c_fe[(f,e)] / float(c_e[e]))
            for (j,i,l,m) in c_jilm.keys():
                q[(j,i,l,m)] = float(c_jilm[(j,i,l,m)]) / float(c_ilm[(i,l,m)]) 

            

        # print t
        self.t = t
        self.q = q
        return (t,q)
       

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
    ba = BerkeleyAligner(aligned_sents, 10)
    A.save_model_output(aligned_sents, ba, "ba.txt")
    avg_aer = A.compute_avg_aer(aligned_sents, ba, 50)

    print ('Berkeley Aligner')
    print ('---------------------------')
    print('Average AER: {0:.3f}\n'.format(avg_aer))
