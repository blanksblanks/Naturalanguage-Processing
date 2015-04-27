from __future__  import division

import nltk
import A
from collections import defaultdict
from nltk.align  import AlignedSent


class BerkeleyAligner():

    def __init__(self, align_sents, num_iter):
        self.t, self.q = self.train(align_sents, num_iter)

    def align(self, align_sent):
        """
        Compute the alignments for align_sent, using this model's parameters. Return
        an AlignedSent object, with the sentence pair and the alignments computed.
        """
        # print self.q
        alignment = []
        l = len(align_sent.words)
        m = len(align_sent.mots)
        for j, ger_word in enumerate(align_sent.words):
            max_align_prob = (self.t[(None, ger_word)]*self.q[(j+1,0,l,m)], None)
            for i, eng_word in enumerate(align_sent.mots):
                max_align_prob = max(max_align_prob, \
                        (self.t[(eng_word, ger_word)]*self.q[(j+1,i,l,m)], i),\
                        (self.t[(eng_word, ger_word)],i))
            if max_align_prob[1] is not None:
                alignment.append((j, max_align_prob[1]))
        return AlignedSent(align_sent.words, align_sent.mots, alignment)


    def train(self, aligned_sents, num_iters):
        """
        Implement the EM algorithm. num_iters is the number of iterations. Returns the 
        translation and distortion parameters as a tuple. Invoked upon initialization.
        """
        # ger -> eng
        t = {}
        q = {}
        # eng -> ger
        t_flipped = {}
        q_flipped = {}
        # for averaging
        final_t = {}
        final_q = {}

        ger_vocab, eng_vocab = self.init_vocab(aligned_sents, False)
        t = self.init_t(aligned_sents, False)
        t_flipped = self.init_t(aligned_sents, True)
       

        for i in xrange(num_iters):
            print 'Iteration', i+1, '...'
            
            c_fe = {tup:0 for tup in t.keys()}
            c_e = {e:0 for e in ger_vocab}
            c_ilm = defaultdict(int)
            c_jilm = defaultdict(int)


            for aligned_sent in aligned_sents:
                ger_sent = aligned_sent.words
                eng_sent = [None] + aligned_sent.mots
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
                       delta = (q[(j,i,l,m)] * t[(f,e)])/float(delta_d)
                       c_fe[(f,e)] += delta
                       c_e[e] += delta
                       c_ilm[(i,l,m)] += delta
                       c_jilm[(j,i,l,m)] += delta
            
            # Update t and q
            for (f,e) in c_fe.keys():
                t[(f,e)] = float(c_fe[(f,e)] / float(c_e[e]))
            for (j,i,l,m) in c_jilm.keys():
                q[(j,i,l,m)] = float(c_jilm[(j,i,l,m)]) / float(c_ilm[(i,l,m)]) 
            
            # DRY: Don't repeat yourself... yet here I am again
            c_fe_flipped = {tup:0 for tup in t_flipped.keys()}
            c_e_flipped = {e:0 for e in eng_vocab if e != None}
            c_ilm_flipped = defaultdict(int)
            c_jilm_flipped = defaultdict(int)

            for aligned_sent in aligned_sents:
                e_sent = aligned_sent.mots
                f_sent = [None] + aligned_sent.words
                l = len(e_sent)
                m = len(f_sent) - 1
                for i in xrange(m+1):
                   # Calculate delta denominator for q(j|i,l,m)
                   f = f_sent[i]
                   delta_d = 0
                   for j in xrange(1, l+1):
                       e = e_sent[j-1]
                       # We can just take care of initialization of q here!
                       if (j,i,l,m) not in q_flipped:
                           q_flipped[(j,i,l,m)] = 1/float(l+1)
                       delta_d += q_flipped[(j,i,l,m)] * t_flipped[(f,e)]
                   for j in xrange(1, l+1):
                       e = e_sent[j-1]
                       delta = (q_flipped[(j,i,l,m)] * t_flipped[(f,e)])/float(delta_d)
                       c_fe_flipped[(f,e)] += delta
                       c_e_flipped[e] += delta
                       c_ilm_flipped[(i,l,m)] += delta
                       c_jilm_flipped[(j,i,l,m)] += delta

            # Update t and q for flipped model
            for (f,e) in c_fe_flipped.keys():
                t_flipped[(f,e)] = float(c_fe_flipped[(f,e)] / float(c_e_flipped[e]))
            for (j,i,l,m) in c_jilm_flipped.keys():
                q_flipped[(j,i,l,m)] = float(c_jilm_flipped[(j,i,l,m)]) / float(c_ilm_flipped[(i,l,m)]) 
            

            """# NVM, this results in high AER in the 0.588 range (0.600 for the second implementation)
            # Average the counts
            for (f,e) in c_fe.keys():
                try:
                    # t[(f,e)] = ( (float(c_fe[(f,e)]) / c_e[e]) + \
                    #               (c_fe_flipped[(e,f)] / c_e_flipped[f]) )  / 2
                    t[(f,e)] = ( (float(c_fe[(f,e)])) + c_fe_flipped[(e,f)] / \
                                 (c_e[e] + c_e_flipped[f]) )
                    t_flipped[(e,f)] = t[(f,e)]
                except KeyError:
                    t[(f,e)] = (float(c_fe[(f,e)]) / c_e[e])
            for (j,i,l,m) in c_jilm.keys():
                try:
                    # q[(j,i,l,m)] = ( (float(c_jilm[(j,i,l,m)]) / c_ilm[(i,l,m)]) + \
                    #                  (c_jilm_flipped[(i+1,j-1,m,l)] / c_ilm_flipped[(j-1,m,l)]) )  / 2
                    q[(j,i,l,m)] = ( ((float(c_jilm[(j,i,l,m)])) + (c_jilm_flipped[(i+1,j-1,m,l)])) / \
                                       (c_ilm[(i,l,m)] + c_ilm_flipped[(j-1,m,l)]))
                    q_flipped[(i+1,j-1,m,l)] = q[(j,i,l,m)]
                except KeyError:
                    q[(j,i,l,m)] = q[(j,i,l,m)]
        self.t = t
        self.q = q
        return (t,q)
        """

        # Average the q and t parameters here after iterations for 0.561 AER
        for (f,e) in t.keys():
            try:
                final_t[(f,e)] = float(t[(f,e)] + t_flipped[(e,f)]) / 2
                # t[(f,e)] = final_t[(f,e)]
                # t_flipped[(e,f)] = final_t[(f,e)]
            except KeyError:
                final_t[(f,e)] = t[(f,e)]
                # print 'Key Error for (f,e):', f, e, '->', e, f
        for (j,i,l,m) in q.keys():
            try:
                # Originally, j is eng, i is ger, l is len(ger), m is len(eng)
                # For flipped version, i+1 is ger (bc None), j-1 is eng (no None),
                # m is len(end), l is len(ger)
                final_q[(j,i,l,m)] = float(q[(j,i,l,m)] + q_flipped[(i+1,j-1,m,l)]) / 2
                # q[(j,i,l,m)] = final_q[(j,i,l,m)] 
                # q_flipped[(i+1,j-1,m,l)] = final_q[(j,i,l,m)]
            except KeyError:
                final_q[(j,i,l,m)] = q[(j,i,l,m)]
                # print 'Key Error for (j,i,l,m):', j, i, l, m, '->', i+1, j-1, m, l
                # Don't average the distortion values
                # final_q = q
        self.t = final_t
        self.q = final_q
        print '\n'
        return (final_t,final_q)

    def init_vocab(self, aligned_sents, flipped):
        """
        Return vocabulary set for source language e and target language f.
        Helper function.
        """
        e_vocab = set() # source language in unidirectional model
        f_vocab = set() # taget language in unidirectional model
        for aligned_sent in aligned_sents:
            if (flipped):
                e_vocab.update(aligned_sent.mots)
                f_vocab.update(aligned_sent.words)
            else:
                e_vocab.update(aligned_sent.words) 
                f_vocab.update(aligned_sent.mots)
        # Add None to vocabulary set of target language
        f_vocab.add(None)
        return e_vocab, f_vocab
        
    def init_t(self, aligned_sents, flipped):
        """
        Initialize the translation parameters to be the uniform distribution over
        all possible words thats appear in a target sentence of a sentence
        containing the source word. Helper function.
        """
        t = {}
        e_vocab, f_vocab = self.init_vocab(aligned_sents, flipped)
        count_fe = {e:{} for e in e_vocab} # count of f and e co-appearing
        # print c_fe
        for aligned_sent in aligned_sents:
            if (flipped):
                e_sent = aligned_sent.mots
                f_sent = [None] + aligned_sent.words
            else:
                e_sent = aligned_sent.words
                f_sent = [None] + aligned_sent.mots # this works, tested in IDLE
            for e in e_sent:
                for f in f_sent:
                    if (f,e) in count_fe[e]: # where f given e
                        count_fe[e][(f,e)] += 1
                    else:
                        count_fe[e][(f,e)] = 1 # initialize count
        # print c_fe
        for e in count_fe:
            dic =  count_fe[e]
            for pair in dic: # where pair = (f,e)
                t[pair] = float(dic[pair]) / len(dic)
        return t
        # print t
        """
            # c_fe = t <- doing that makes AER go up > 0.05

            # Update t
            # count = {tup:0 for tup in t.keys()}
            # count_e = {e:0 for e in ger_vocab}
            # Update q

            # t, q, c_fe, c_e, c_ilm, c_jilm == self.iter_step(aligned_sents, t, q, False)
            # t2_flipped, q_flipped, c_e, c_fe, c_ilm, c_jilm == self.iter_step(aligned_sents, t, q, True)
            # t2, q2, c_fe2, c_e2, c_ilm2, c_jilm2 == self.iter_step(aligned_sents, t2, q2, False)


                # Update t
                # for f in eng_sent:
                #    sum_e = 0
                #    for e in ger_sent:
                #        sum_e += t[(f,e)]
                #    for e in ger_sent:
                #        count[(f,e)] += (t[(f,e)] / float(sum_e))
                #        count_e[e] += (t[(f,e)] / float(sum_e))
                # Update q


            '''# Check new method
            # t2, q2, c_fe2, c_e2, c_ilm2, c_jilm2 == self.iter_step(aligned_sents, t2, q2, False)
            retval = self.iter_step(aligned_sents, t2, q2, False)
            t2 = retval[0]
            q2 = retval[1]
            c_e2 = retval[2]
            c_fe2 = retval[3]
            c_ilm2 = retval[4]
            c_jilm2 = retval[5]
            print 'Are they equal? t, q, c_fe, c_e, c_ilm, c_jilm'
            print (t2 == t), (q2 == q), (c_fe2 == c_e), (c_e2 == c_fe), (c_ilm2 == c_jilm), (c_jilm2 == c_ilm)
            print c_fe2[u'Respekt'], c_e[u'Respekt']
            print c_e2[(u'dimension', u'vorhanden')], c_fe[(u'dimension', u'vorhanden')]
            print c_ilm2[(12,23,38)], c_ilm[(12,23,38)]
            print c_jilm2[(9,4,40,37)], c_jilm[(9,4,40,37)]
            '''
            '''print '\n\n\n\n\n\n', c_fe2
            print '\n\n\n\n\n\n', c_e2
            print '\n\n\n\n\n\n', c_ilm2
            print '\n\n\n\n\n\n', c_jilm2
            
            if (t2 == t):
                print 'True'
            else:
                print 't2', t2, '\n\n\n\n\n\n\n\n\n', 't', t
            if (q2 == q):
                print 'True'
            else:
                print 'q2', q2, '\n\n\n\n\n\n\n\n\n', 'q', q
            if (c_fe2 == c_fe):
                print 'True'
            else:
                print 'c_fe2', c_fe2, '\n\n\n\n\n\n\n\n\n', 'c_fe', c_fe
            if (c_e2 == c_e):
                print 'True'
            else:
                print 'c_e2', c_e2, '\n\n\n\n\n\n\n\n\n', 'c_e', c_e
            if (c_ilm2 == c_ilm):
                print 'True'
            else:
                print 'c_ilm2', c_ilm2, '\n\n\n\n\n\n\n\n\n', 'c_ilm', c_ilm
            if (c_jilm2 == c_jilm):
                print 'True'
            else:
                print 'c_jilm2', c_jilm2, '\n\n\n\n\n\n\n\n\n', 't', c_jilm
            # print 'Are they equal?', (c_fe, c_e, c_ilm, c_jilm) == self.iter_step(aligned_sents, t, q, False)
            # print t2 == t, q2 == q, c_fe2 == c_fe, c_e == c
            '''
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

        # t2 = t
        # q2 = q
       """

def main(aligned_sents):
    ba = BerkeleyAligner(aligned_sents, 10)
    A.save_model_output(aligned_sents, ba, "ba.txt")
    avg_aer = A.compute_avg_aer(aligned_sents, ba, 50)

    print ('Berkeley Aligner')
    print ('---------------------------')
    print('Average AER: {0:.3f}\n'.format(avg_aer))
