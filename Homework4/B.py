import nltk
import A

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
        print q






        return (t,q)

    def counting_dict(dictionary, key):
        if key in dictionary:
            dictionary[key] += 1
        else:
            dictionary[key] = 1
        return dictionary

def main(aligned_sents):
    ba = BerkeleyAligner(aligned_sents, 20)
    # A.save_model_output(aligned_sents, ba, "ba.txt")
    # avg_aer = A.compute_avg_aer(aligned_sents, ba, 50)

    print ('Berkeley Aligner')
    print ('---------------------------')
    # print('Average AER: {0:.3f}\n'.format(avg_aer))
