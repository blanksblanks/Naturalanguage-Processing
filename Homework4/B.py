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
        ge_vocab = set() # e_set: source in unidirectional model
        en_vocab = set() # f_set: target in unidirectional model
        for align_sent in aligned_sents:
            en_vocab.update(align_sent.mots)
            ge_vocab.update(align_sent.words) 
        ge_vocab.add(None) # add NULL values to e_set
        # print "Eng", en_vocab
        # print "Ger", ge_vocab
        return (t,q)

def main(aligned_sents):
    ba = BerkeleyAligner(aligned_sents, 20)
    # A.save_model_output(aligned_sents, ba, "ba.txt")
    # avg_aer = A.compute_avg_aer(aligned_sents, ba, 50)

    print ('Berkeley Aligner')
    print ('---------------------------')
    # print('Average AER: {0:.3f}\n'.format(avg_aer))
