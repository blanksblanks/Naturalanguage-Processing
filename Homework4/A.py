import nltk
from nltk.corpus import comtrans
from nltk.align.ibm1 import IBMModel1
from nltk.align.ibm2 import IBMModel2

# Initialize IBM Model 1 and return the model.
def create_ibm1(aligned_sents):
    # A1: Init using 10 iterations of EM for first 350 sentences in corpus
    ibm1 = IBMModel1(aligned_sents, 10)

    # A4: Init using 20 iterations of EM for first 10 sentences in corpus
    # ibm1 = IBMModel1(aligned_sents[:10], 20)

    return ibm1

# Initialize IBM Model 2 and return the model.
def create_ibm2(aligned_sents):
    # A2: Init using 10 iterations of EM for first 350 sentences in corpus
    ibm2 = IBMModel2(aligned_sents, 10)

    # A4: Init using 20 iterations of EM for first 10 sentences in corpus
    # ibm2 = IBMModel2(aligned_sents[:10],20)

    return ibm2

# Compute the average AER for the first n sentences
# in aligned_sents using model. Return the average AER.
def compute_avg_aer(aligned_sents, model, n):
    total = 0.0
    for i in xrange(n):
        aligned_sent = model.align(aligned_sents[i])
        aer = aligned_sent.alignment_error_rate(aligned_sents[i])
        total += aer
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
            print i, ': same aer (%f)' %(e1)
        elif (e2 > e1):
            print i, ': ibm2 (%f) outperformed ibm1 (%f)' %(e2,e1)
        else: # e1 > e2
            print i, ': ibm1 (%f) outperformed ibm2 (%f)' %(e1,e2)
        if (e1 != e2):
            print sentencify(ref.words)
            print sentencify(ref.mots)
            print '(refr)', ref.alignment
            print '(ibm1)', s1.alignment
            print '(ibm2)', s2.alignment
            print '\n'

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
        words = (u' '.join(aligned_sent.words).encode('utf8'))
        mots = (u' '.join(aligned_sent.mots).encode('utf8'))
        alignment = (u' '.join(u'%s-%s' %(tup[0], tup[1]) for tup in aligned_sent.alignment).encode('utf8'))
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

    compare_avg_aer(aligned_sents, ibm1, ibm2, 50)
