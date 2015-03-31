from __future__ import division
from xml.dom import minidom
import json
import codecs
import sys
import unicodedata
import string
import math
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import *
from nltk.corpus import wordnet as wn
from sklearn import datasets
from sklearn import svm
from sklearn import neighbors

# ============================================================
# Constants
# ============================================================

k = 20 # set context window to 10 words preceding and following the head
top = 100 # number of 'top' words for each sense by relevance score

stemmer = PorterStemmer()

# ============================================================
# Main Functions
# ============================================================

# 2
def parse_data(input_file):
    '''
    Parse the .xml dev data file

    param str input_file: The input data file path
    return dict: A dictionary with the following structure
            {
                    lexelt: [(instance_id, context), ...],
                    ...
            }
    '''
    xmldoc = minidom.parse(input_file)
    data = {}
    lex_list = xmldoc.getElementsByTagName('lexelt')
    for node in lex_list:
        lexelt = node.getAttribute('item')
        data[lexelt] = []
        inst_list = node.getElementsByTagName('instance')
        for inst in inst_list:
            instance_id = inst.getAttribute('id')
            if language == 'English':
                l = inst.getElementsByTagName('context')[0]
            else:
                l = inst.getElementsByTagName('target')[0]
            context = (l.childNodes[0].nodeValue + l.childNodes[1].firstChild.nodeValue + l.childNodes[2].nodeValue).replace('\n', '')
            # print 'context', context
            data[lexelt].append((instance_id, context))
    print 'data', data
    return data

# 1
def build_dict(language):
    '''
    Count the frequency of each sense
    '''
    data = {}
    xmldoc = minidom.parse('data/' + language + '-train.xml')
    data = {}
    '''head_list = xmldoc.getElementsByTagName('head')
    # print 'head_list', head_list
    for head in head_list:
        hd = head.childNodes[0].nodeValue
            print 'head', hd
    '''
    lex_list = xmldoc.getElementsByTagName('lexelt')
    for node in lex_list:
        lexelt = node.getAttribute('item')
        # print 'lexelt', lexelt
        data[lexelt] = {}
        inst_list = node.getElementsByTagName('instance')
        for inst in inst_list:
            sense_id = inst.getElementsByTagName('answer')[0].getAttribute('senseid')
            # print 'sense_id',  sense_id
            try:
                cnt = data[lexelt][sense_id]
            except KeyError:
                data[lexelt][sense_id] = 0
            data[lexelt][sense_id] += 1
    
    record = {}
    for key, cntDict in data.iteritems():
        sense = max(cntDict, key = lambda s: cntDict[s])
        print 'key, cntDict, sense', key, cntDict, sense
        record[key] = sense
    print 'record', record
    return record

# 5
def getFrequentSense(lexelt, sense_dict):
    '''
        Return the most frequent sense of a word (lexelt) in the training set
        '''
    sense = ''
    try:
        sense = sense_dict[lexelt]
    except KeyError:
        pass
    return sense


def most_frequent_sense(language, sense_dict):
    data = parse_data('data/' + language + '-dev.xml')
    outfile = codecs.open(language + '.baseline', encoding = 'utf-8', mode = 'w')
    for lexelt, instances in sorted(data.iteritems(), key = lambda d: replace_accented(d[0].split('.')[0])):
        for instance_id, context in sorted(instances, key = lambda d: int(d[0].split('.')[-1])):
            sid = getFrequentSense(lexelt, sense_dict)
            outfile.write(replace_accented(lexelt + ' ' + instance_id + ' ' + sid + '\n'))
    outfile.close()



# ============================================================
# Preprocessing Functions
# ============================================================

''' Replace accents so unicode text can be cast to string '''
def replace_accented(input_str):
    nkfd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

''' Remove punctuation and make all words lowercase'''
def remove_punc(tokens):
    unpunctuated = [token.lower() for token in tokens if token not in string.punctuation]
    return unpunctuated

''' Remove stop words '''
def remove_stops(tokens, lang):
    lang = lang.lower()
    try:
        filtered = [w for w in tokens if not w in stopwords.words(lang)]
    except IOError:
        print "NLTK stopwords does not support this language (" + lang + ")"
        sys.exit(1)
    return filtered

''' Stem tokens using the Porter Stemmer '''
def stem(tokens):
    stemmed = []
    for token in tokens:
        stemmed.append(stemmer.stem(token))
    return stemmed

''' Return list of synonyms for list of tokens '''
def find_synonyms(tokens):
    synonyms = []
    sss = []
    for token in tokens:
        # [ss.name() for ss in wn.synsets(token)]
        # syn_list = ['.'.join(ss.name().split('.')[:-1]) for ss in wn.synsets(token)]
        # if (language == 'English'):
        syn_list = [ss.name().split('.')[0] for ss in wn.synsets(token) if '_' not in ss.name()]
        ss_list = [ss.name() for ss in wn.synsets(token) if '_' not in ss.name()]
        # if (language == 'Spanish'):
        #    syn_list = [ss.name().split('.')[0] for ss in wn.synsets(token,lang='spa') if '_' not in ss.name()]
        #    ss_list = [ss.name() for ss in wn.synsets(token) if '_' not in ss.name()]
        # if (language == 'Catalan'):
        #    syn_list = [ss.name().split('.')[0] for ss in wn.synsets(token,lang='cat') if '_' not in ss.name()]
        #    ss_list = [ss.name() for ss in wn.synsets(token) if '_' not in ss.name()]
        # synonyms.append(set(syn_list))
        synonyms.extend(set(syn_list))
        sss.extend(set(ss_list))
    # print 'synonyms', synonyms
    return synonyms, sss

''' Find hyponyms and hypernyms of tokens ''' 
def find_hnyms(tokens):
    hnyms = []
    for token in tokens:
        # for idx in xrange(len(wn.synsets(token))):
        # ss = wn.synsets(token)[idx]
        # ss = wn.synsets(token)[0] # take only the first meaning instead of all
        ss = wn.synset(token)
        # print 'ss', ss
        # sys.exit(1)
        # hypo = set([i.name().split('.')[0] for i in ss.closure(lambda s:s.hyponyms()) if '_' not in i.name()])
        # hyper = set([i.name().split('.')[0] for i in ss.closure(lambda s:s.hypernyms()) if '_' not in i.name()])
        # both = hypo.union(hyper)
        # hnyms.append(both)
        hypo = [h.name().split('.')[0] for h in ss.hyponyms() if '_' not in h.name()]
        hyper = [h.name().split('.')[0] for h in ss.hypernyms() if '_' not in h.name()] 
        hnyms.extend(hypo)
        hnyms.extend(hyper)
    # print 'hyponyms and hypernyms', hnyms
    return hnyms
 
def compute_relevance(s_i_data, lexelt, features):
    senses = {}
    word_c = {}
    sense_c = {}
    coappear_c = {}
    relevance = {}
    pmi = {}
    most_rel = set([])
    most_pmi = set([])

    t = len(s_i_data)

    for inst in s_i_data[lexelt]:
        sense = inst[1]
        s_i = inst[2]
        
        # count number of instances sense appears for lexelt 
        if sense not in senses:
            senses[sense] = 0
        if sense not in sense_c:
            sense_c[sense] = 1
        else:
            sense_c[sense] += 1

        for word in s_i: # word, count in s_i.items():
            # count number of instances a context word appears
            if word not in word_c:
                word_c[word] = 1
            else:
                word_c[word] += 1
            # count number of instances word and sense appear together
            if (sense,word) not in coappear_c:
                coappear_c[(sense,word)] = 1
            else:
                coappear_c[(sense,word)] += 1
    
    for pair in coappear_c:
        sense = pair[0]
        word = pair[1]
        
        psc = coappear_c[pair] / word_c[word]
        
        # calculate relevance score
        if (5 in features):
            pnotsc = (word_c[word] - coappear_c[pair]) / word_c[word]
            if (pnotsc == 0):
                p = 100 # Assign arbitrarily high score
            else:
                p = psc / pnotsc
            relevance[pair] = math.log(p,2)
        
        # calculate pmi: log p(s,w) / p(s)p(w) = log p(s|w) / p(s)
        if (6 in features):
            ps = sense_c[sense] / t
            pmi[pair] = math.log(psc/ps, 2)
            # pw = word_c[word] / t
        
    if (7 in features):
        chi = {}
        sorted_chi = []
        most_chi = set([])
        for pair in coappear_c:
            s = sense_c[sense]
            w = word_c[word]
            exp = s/t * w/t * t
            obs = coappear_c[pair]
            chi[pair] = ((obs - exp) * (obs - exp)) / exp
        sorted_chi = sorted(chi, key=lambda k:chi[k])
        for pair in sorted_chi:
            print chi[pair], pair
            sense = pair[0]
            word = pair[1]
            if senses[sense] < top:
                print 'added', word
                most_chi.add(word)
        print "vector length:", len(most_rel)
        return most_chi
    
    if (5 in features):
        sorted_rel = sorted(relevance, key=lambda k:-relevance[k])
        
        # select top words for each sense for final set of features
        for pair in sorted_rel:
            print relevance[pair], pair
            sense = pair[0]
            word = pair[1]
            '''if senses[sense] < top:
                print 'ADDED', word
                most_rel.add(word)
                senses[sense] += 1
            '''
            if (relevance[pair] > -2.0):
                most_rel.add(word)
    
        print "vector length:", len(most_rel)
        return most_rel
    
    if (6 in features):
        sorted_pmi = sorted(pmi, key=lambda k:pmi[k])
        for pair in sorted_pmi:
            print pmi[pair], pair
            sense = pair[0]
            word = pair[1]
            if senses[sense] < top:
                print 'ADDED', word
                most_pmi.add(word)
                senses[sense] += 1
        return most_pmi
    

    # print 'relevance', relevance
    # print 'sorted', sorted_rel
    # print 'most relev ant', most_rel
    # return most_rel, most_pmi


# ============================================================
# Parsing and Computing Context Vectors
# ============================================================

'''
If features include 0, use default tokens for context vectors
If features include 1, remove stop words
If features include 2, do stemming
If features include 3, remove punctuation and make words lowercase
If features include 4, obtain synonyms, hyponyms and hypernyms
If features include  5, compute relevance scores
'''

def compute_context_vectors(language, features):
    # define our training data and parse with minidom
    input_file = 'data/' + language + '-train.xml'
    xmldoc = minidom.parse(input_file)

    # s_i_data is a dictionary; key=lexelt, value=ordered list of tuples
    # tuple for each test instance t_i where [0] = instanceid, [1] = senseid,
    # [2] = list of words that appear in the context window
    s_i_data = {} 

    # s_data is a dictionary; key=lexelt, value=set(context windows for each t_i)
    s_data = {}

    # these are our return values: ordered lists of context vectors, instanceids, senseid's
    # for each lexelt in their respective data dictionaries
    context_data = {}
    instance_data = {}
    target_data = {}

    # for each lexelt in the xml file
    lex_list = xmldoc.getElementsByTagName('lexelt') 
    for node in lex_list:

        # identify the lexelt to use as key for data dictionaries
            lexelt = node.getAttribute('item')
            print 'lexelt', lexelt

            # initialize the following:
            #  - ordered list of tuples (instance, sense, s_i)
            #  - unique list (set) of all s_i (union)
            #  - ordered list of context vectors
            #  - ordered list of instance id's
            #  - ordered list of sense id's
            s_i_data[lexelt] = []
            s = set([])
            context_data[lexelt] = []
            instance_data[lexelt] = []
            target_data[lexelt] = []

            # for each test instances t_i of the lexelt
            inst_list = node.getElementsByTagName('instance')
            for inst in inst_list:

                # identify the instance_id
                    instance_id = inst.getAttribute('id')
                    # print 'instance_id', instance_id
                    sense_id = inst.getElementsByTagName('answer')[0].getAttribute('senseid')
                    # print 'sense_id', sense_id

                    # parse context to find words within k distance of head
                    # note that 'is' is identity testing, '==' is equality testing
                    if language == 'English':
                        l = inst.getElementsByTagName('context')[0]
                    else:
                        l = inst.getElementsByTagName('target')[0]
                    pretokens = nltk.word_tokenize(l.childNodes[0].nodeValue)
                    head = l.childNodes[1].firstChild.nodeValue
                    posttokens = nltk.word_tokenize(l.childNodes[2].nodeValue)
                    tokens = pretokens[-k:]
                    tokens.extend(posttokens[:k])
                 
                    if (1 in features):
                        tokens = remove_stops(tokens, language)
                    if (2 in features):
                        tokens = stem(tokens)
                    if (3 in features):
                        tokens = remove_punc(tokens)
                    if (4 in features):
                        tokens, sss = find_synonyms(tokens)
                        hnyms = find_hnyms(sss)
                        tokens.extend(hnyms)
                    # print 'tokens', tokens

                    # s.extend(tokens)

                    # create s_i as a dictionary to keep track of words within k distance of
                    # current head and counts for the number of time it appears in the window
                    s_i = {}
                    for token in tokens:
                        if token not in s:
                            s.add(token)
                        if token in s_i:
                            s_i[token] += 1
                        else:
                            s_i[token] = 1

                    # s_i = {item : index for index, item in enumerate(s_i)}
                    # print 's_i', s_i
                    # print '0', l.childNodes[0].nodeValue
                    # print '1', l.childNodes[1].firstChild.nodeValue
                    # print '2', l.childNodes[2].nodeValue
                    # print 'instance_id', instance_id, 'context', context
                    # data[lexelt].append((instance_id, context))
                    # print 'data[lexelt]',  data[lexelt]

                    # append tuple to s_i_data[lexelt]
                    s_i_data[lexelt].append((instance_id, sense_id, s_i))
            
            print "vector length", len(s)

            # print 's_data for', lexelt, s_data[lexelt]
            # print 's_i_data for', lexelt, s_i_data[lexelt]
            if (5 in features or 6 in features or 7 in features):
                s = compute_relevance(s_i_data, lexelt, features)

            # transform feature set to list and  append to s_data[lexelt]
            s = list(s)
            s_data[lexelt] = s
            
            # calculate context vectors for each instance in ordered s_i_data[lexelt] list
            for inst in s_i_data[lexelt]:
                # print 's_i_data', s_i_data[lexelt]
                    instance = inst[0]
                    try:
                        sense = str(inst[1]) # cast to string to avoid unicode error for NumPY<1.7.0
                    except UnicodeEncodeError:
                        sense = str(replace_accented(inst[1]))
                        print 'replaced accented', inst[1], sense
                    s_i = inst[2]
                    vector = []
                    for idx in xrange(len(s)):
                        word = s[idx]
                        if word in s_i:
                            vector.append(s_i[word]) # append the count from s_i dict
                        else:
                            vector.append(0)
                    context_data[lexelt].append(vector)
                    instance_data[lexelt].append(instance)
                    target_data[lexelt].append(sense)
                    # print 'instance', instance
                    # print 'sense', sense
                    # print 'vector', vector
    # print 'target_data', target_data
    return context_data, target_data, s_data

    # reminder: context_vex[lexelt] = [] -> [(id, vector), (id, vector)]


def parse_dev_data(language, features, s_data):
    input_file = 'data/' + language + '-dev.xml'
    xmldoc = minidom.parse(input_file)
    context_data = {}
    instance_data = {}
    s_i_data = {}
    
    lex_list = xmldoc.getElementsByTagName('lexelt') 
    for node in lex_list:
        lexelt = node.getAttribute('item')
        print 'lexelt', lexelt
        s_i_data[lexelt] = []
        context_data[lexelt] = []
        instance_data[lexelt] = []

        # for each test instances t_i of the lexelt
        inst_list = node.getElementsByTagName('instance')
        for inst in inst_list:

            # identify the instance_id
            instance_id = inst.getAttribute('id')
            # print 'instance_id', instance_id

            # parse context to find words within k distance of head
            if language == 'English':
                l = inst.getElementsByTagName('context')[0]
            else:
                l = inst.getElementsByTagName('target')[0]
            pretokens = nltk.word_tokenize(l.childNodes[0].nodeValue)
            head = l.childNodes[1].firstChild.nodeValue
            posttokens = nltk.word_tokenize(l.childNodes[2].nodeValue)
            tokens = pretokens[-k:]
            tokens.extend(posttokens[:k])
            # print 'tokens', tokens
            if (2 in features):
                tokens = stem(tokens)
            if (3 in features):
                tokens = remove_punc(tokens)

            # create s_i as a dictionary to keep track of words within k distance of
            # current head and counts for the number of time it appears in the window
            s_i = {}
            for token in tokens:
                if token in s_i:
                    s_i[token] += 1
                else:
                    s_i[token] = 1

            s_i_data[lexelt].append((instance_id, s_i))

        # calculate context vectors for each instance in ordered s_i_data[lexelt] list
        for inst in s_i_data[lexelt]:
            instance = inst[0]
            s_i = inst[1]
            s = s_data[lexelt]
            vector = []
            for idx in xrange(len(s)):
                word = s[idx]
                if word in s_i:
                    vector.append(s_i[word]) # append the count from s_i dict
                else:
                    vector.append(0)
            context_data[lexelt].append(vector)
            instance_data[lexelt].append(instance)
    return context_data, instance_data

def train_classifiers(context_data, target_data):
    # initialize K-Nearest Neighbors and Linear SVM classifiers
    knn_data = {}
    svc_data = {}

    for lexelt in context_data:
        context_list = context_data[lexelt]
        target_list = target_data[lexelt]

        # KNN: given a new observation, take the label of training samples closests to its
        # n-dimensional space, where nis the number of features in each sample
        knn = neighbors.KNeighborsClassifier()
        knn.fit(context_list, target_list)
        knn_data[lexelt] = knn
        # SVM: learn from existing data by creating an estimator and calling its fit(X, Y) method 
        # SVMs try to construct a hyperplane maximizing the margin between two classes
        svc = svm.LinearSVC()
        svc.fit(context_list, target_list)
        svc_data[lexelt] = svc

    return knn_data, svc_data


def test_classifier(language, feats, classifier, clf_data, context_dev, instance_dev):
    # data = parse_data('data/' + language + '-dev.xml')
    filename = (language + '_' + ''.join(feats) + '.' + classifier)
    print 'writing to', filename + '...'
    outfile = codecs.open(filename, encoding = 'utf-8', mode = 'w')
    for lexelt in context_dev:
        context_list = context_dev[lexelt]
        instance_list = instance_dev[lexelt]
        clf = clf_data[lexelt]
        for idx in xrange(len(context_list)):
            instance_id = instance_list[idx]
            vector = context_list[idx]
            sid = clf.predict(vector)
            outfile.write(replace_accented(lexelt + ' ' + instance_id + ' ' + sid + '\n'))
    outfile.close()

if __name__ == '__main__':
    
    if len(sys.argv) < 2:
        print 'Usage: python baseline.py [language] [feature ids]'
        sys.exit(0)

    # sense_dict = build_dict(sys.argv[1])
    # most_frequent_sense(sys.argv[1], sense_dict)
    # find_synonyms(['cat','dog'])
    # find_hnyms(['cat','dog'])
    
    lang = sys.argv[1]
    ft = set([int(i) for i in (sys.argv[2:])])
    print ft

    if 0 in ft:
        print 'default: no processing...'
    if 1 in ft:
        print 'removing stops...'
    if 2 in ft:
        print 'stemming words...'
    if 3 in ft: 
        print 'removing punctuation...'

    context_data, target_data, s_data = compute_context_vectors(lang, ft)
    knn_data, svc_data = train_classifiers(context_data, target_data)
    context_dev, instance_dev = parse_dev_data(lang, ft, s_data)
    test_classifier(lang, sys.argv[2:], 'knn', knn_data, context_dev, instance_dev)
    test_classifier(lang, sys.argv[2:], 'svc', svc_data, context_dev, instance_dev)
    
