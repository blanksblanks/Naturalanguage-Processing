from __future__  import division
from collections import defaultdict
from nltk.align  import AlignedSent
import nltk
import A

# (Optional) Improve the BerkeleyAligner.
class BetterBerkeleyAligner():

    def __init__(self, align_sents, num_iter):
        self.t, self.q = self.train(align_sents, num_iter)

    """def align(self, align_sent):
        '''
        Compute the alignments for align_sent, using this model's parameters. Return
        an AlignedSent object, with the sentence pair and the alignments computed.
        '''
        # print self.q
        alignment = []
        l = len(align_sent.words)
        m = len(align_sent.mots)
        for j, ger_word in enumerate(align_sent.words):
            max_align_prob = (self.t[(None, ger_word)]*self.q[(j+1,0,l,m)], None)
            for i, eng_word in enumerate(align_sent.mots):
                max_align_prob = max(max_align_prob, \
                        (self.t[(eng_word, ger_word)]*self.q[(j+1,i+1,l,m)], i),\
                        (self.t[(eng_word, ger_word)],i))
            if max_align_prob[1] is not None:
                alignment.append((j, max_align_prob[1]))
        return AlignedSent(align_sent.words, align_sent.mots, alignment)
    """

    def align(self, align_sent):
        """
        Use self.t which contains both t(f|e) and t(e|f) values to calculate the best
        alignments with p(f|e) and p(e|f), then calculate the intersection and union
        of these alignments, choosing the best
        """
        alignment = []
        e_sent = align_sent.words
        f_sent = align_sent.mots
        for i, f_word in enumerate(f_sent):
            p_fe = defaultdict(float)
            p_ef = defaultdict(float)
            for j, e_word in enumerate(e_sent):
                p_fe[(f_word, e_word)] = self.t[(f_word, e_word)]
                p_ef[(e_word, f_word)] = self.t[(e_word, f_word)]
            # Best alignments with p(f|e) and p(e|f)
            max_f_fe, max_e_fe = max(p_fe, key=p_fe.get)
            max_f_ef, max_e_ef = max(p_ef, key=p_ef.get)
            # Intersection
            if (max_f_fe == max_e_ef and max_e_fe == max_f_ef):
                alignment.append((e_sent.index(max_e_fe), f_sent.index(max_f_fe)))
            # Max of union
            else:
                max1 = p_fe[(max_f_fe,max_e_fe)]
                max2 = p_ef[(max_f_ef,max_e_ef)]
                if max1 >= max2:
                    alignment.append((e_sent.index(max_e_fe), f_sent.index(max_f_fe)))
                else:
                    alignment.append((e_sent.index(max_f_ef), f_sent.index(max_e_ef)))
        return AlignedSent(align_sent.words, align_sent.mots, alignment)
                
            

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
            
        # print t
        self.t = t
        self.t.update(t_flipped)
        self.q = q
        return (self.t, self.q) 
        '''
        final_t = {}
        final_q = {}
        for (f,e) in t.keys():
            try:
                final_t[(f,e)] = float(t[(f,e)] + t_flipped[(e,f)]) / 2
            except KeyError:
                final_t[(f,e)] = t[(f,e)]
                print 'Key Error for (f,e):', f, e, '->', e, f
        for (j,i,l,m) in q.keys():
            try:
                # Originally, j is eng, i is ger, l is len(ger), m is len(eng)
                # For flipped version, i+1 is ger (bc None), j-1 is eng (no None),
                # m-1 is len(eng - None), l+1 is len(ger + None)
                # NVM I don't consider None in the lengths l or m
                final_q[(j,i,l,m)] = float(q[(j,i,l,m)] + q_flipped[(i+1,j-1,m,l)]) / 2
            except KeyError:
                final_q[(j,i,l,m)] = q[(j,i,l,m)]
                print 'Key Error for (j,i,l,m):', j, i, l, m, '->', i+1, j-1, m, l
        self.t = final_t
        self.q = final_q
        
        return (final_t,final_q)
        '''

def main(aligned_sents):
    ba = BetterBerkeleyAligner(aligned_sents, 10)
    if ba.t is None:
        print "Better Berkeley Aligner Not Implemented"
    else:
        avg_aer = A.compute_avg_aer(aligned_sents, ba, 50)

        print ('Better Berkeley Aligner')
        print ('---------------------------')
        print('Average AER: {0:.3f}\n'.format(avg_aer))
