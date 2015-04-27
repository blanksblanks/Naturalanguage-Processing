import nltk
from nltk.corpus import comtrans
from nltk.align.ibm1 import IBMModel1
from nltk.align.ibm2 import IBMModel2

"""
    # A1: Init IBMModel1 using 10 iterations of EM for first 350 sentences in corpus
    # A2: Init IBMModel2 using 10 iterations of EM for first 350 sentences in corpus
    # A3: For each of the first 50 sentence pairs in the corpus, compute the AER
    # A4: Experiment with num_iter for EM algorithm
"""

# Initialize IBM Model 1 and return the model.
def create_ibm1(aligned_sents):
    ibm1 = IBMModel1(aligned_sents, 10)
    # convergence point: 25 iterations
    return ibm1

# Initialize IBM Model 2 and return the model.
def create_ibm2(aligned_sents):
    ibm2 = IBMModel2(aligned_sents, 10)
    # convergence point: 25 iterations
    return ibm2

# Compute the average AER for the first n sentences
# in aligned_sents using model. Return the average AER.
def compute_avg_aer(aligned_sents, model, n):
    total = 0.0
    for i in xrange(n):
        aligned_sent = model.align(aligned_sents[i])
        aer = aligned_sent.alignment_error_rate(aligned_sents[i])
        total += aer
        """ Comment out to print info
        print sentencify(aligned_sent.words)
        print sentencify(aligned_sent.mots)
        print 'Alignment:',  aligned_sent.alignment
        print 'Should be:', aligned_sents[i].alignment
        print 'AER:', aer, '\n'
        """
    avg = total / n
    return avg

# Helper method to compare the AER results between the two models
# and find a sentence pair where one model outperforms the other
def compare_avg_aer(aligned_sents, ibm1, ibm2, n):
    for i in xrange(n):
        ref = aligned_sents[i]
        s1 = ibm1.align(ref)
        s2 = ibm2.align(ref)
        e1 = s1.alignment_error_rate(ref)
        e2 = s2.alignment_error_rate(ref)
        if (e1 == e2):
            print '\n', i+1, ': same aer (%f)' %(e1)
        elif (e2 < e1):
            print '\n', i+1, ': ibm2 (%f) outperformed ibm1 (%f)' %(e2,e1)
        else: # e1 < e2
            print '\n', i+1, ': ibm1 (%f) outperformed ibm2 (%f)' %(e1,e2)
        if (e1 != e2):
            print sentencify(ref.words)
            print sentencify(ref.mots)
            print '(refr)', ref.alignment
            print '(ibm1)', s1.alignment
            print '(ibm2)', s2.alignment

# Helper method to convert list of words or list of tuples to Unicode string
def sentencify(lst, mode=1):
    if (mode == 1):
        return u' '.join(lst).encode('utf8')
    elif (mod == 2):
        return u' '.join(u'%s-%s' %(tup[0], tup[1]) for tup in lst).encode('utf8')

# Computes the alignments for the first 20 sentences in
# aligned_sents and saves the sentences and their alignments
# to file_name. Use the format specified in the assignment.
def save_model_output(aligned_sents, model, file_name):
    target = open(file_name,'w')
    for i in xrange(20):
        aligned_sent = model.align(aligned_sents[i])
        words = str(aligned_sent.words).encode('utf8') # (u' '.join(aligned_sent.words).encode('utf8'))
        mots = str(aligned_sent.mots).encode('utf8') # (u' '.join(aligned_sent.mots).encode('utf8'))
        alignment = str(aligned_sent.alignment).encode('utf8') # (u' '.join(u'%s-%s' %(tup[0], tup[1]) for tup in aligned_sent.alignment).encode('utf8'))
        target.write(words + '\n' +  mots + '\n' + alignment + '\n\n')
        # print(words + '\n' +  mots + '\n' + alignment + '\n')
    target.close()

# Where aligned_sents = comtrans.aligned_sents()[:350]
def main(aligned_sents):
    ibm1 = create_ibm1(aligned_sents)
    save_model_output(aligned_sents, ibm1, "ibm1.txt")
    avg_aer = compute_avg_aer(aligned_sents, ibm1, 50)

    print ('IBM Model 1')
    print ('---------------------------')
    print('Average AER: {0:.3f}\n'.format(avg_aer))

    ibm2 = create_ibm2(aligned_sents)
    save_model_output(aligned_sents, ibm2, "ibm2.txt")
    avg_aer = compute_avg_aer(aligned_sents, ibm2, 50)
    
    print ('IBM Model 2')
    print ('---------------------------')
    print('Average AER: {0:.3f}\n'.format(avg_aer))

    # compare_avg_aer(aligned_sents, ibm1, ibm2, 50)
