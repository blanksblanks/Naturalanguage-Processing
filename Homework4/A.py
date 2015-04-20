import nltk
from nltk.corpus import comtrans
from nltk.align.ibm1 import IBMModel1
from nltk.align.ibm2 import IBMModel2

# Initialize IBM Model 1 and return the model.
def create_ibm1(aligned_sents):
    ibm1 = IBMModel1(aligned_sents[:10], 20)
    return ibm1

# Initialize IBM Model 2 and return the model.
def create_ibm2(aligned_sents):
    ibm2 = IBMModel2(aligned_sents[:10],20)
    return ibm2

# Compute the average AER for the first n sentences
# in aligned_sents using model. Return the average AER.
def compute_avg_aer(aligned_sents, model, n):
    # for i in xrange(n):
    return 0

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
    # avg_aer = compute_avg_aer(aligned_sents, ibm1, 50)

    print ('IBM Model 1')
    print ('---------------------------')
    # print('Average AER: {0:.3f}\n'.format(avg_aer))

    ibm2 = create_ibm2(aligned_sents)
    save_model_output(aligned_sents, ibm2, "ibm2.txt")
    # avg_aer = compute_avg_aer(aligned_sents, ibm2, 50)
    
    print ('IBM Model 2')
    print ('---------------------------')
    # print('Average AER: {0:.3f}\n'.format(avg_aer))

