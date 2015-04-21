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
        init_prob = 1/len(ger_vocab)
        count_ef = {e:{} for e in ger_vocab}
        # print count_ef
        # total_f = {}
        for aligned_sent in aligned_sents:
            ger_sent = aligned_sent.words
            eng_sent = [None] + aligned_sent.mots # this works, tested in IDLE
            for e in ger_sent:
                for f in eng_sent:
                    if (f,e) in count_ef[e]: # where f given e
                        count_ef[e][(f,e)] += 1
                    else:
                        count_ef[e][(f,e)] = 1 # initialize count
        # print count_ef
        for e in count_ef:
            dic =  count_ef[e]
            for pair in dic:
                t[pair] = float(dic[pair]) / len(dic)
            #for key, value in count_ef[e].items:
            #    t[key] = value / len(count_ef[e])
        print t




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
