from xml.dom import minidom
import json
import codecs
import sys
import unicodedata
from nltk.corpus import wordnet as wn
import nltk
from sklearn import datasets
from sklearn import svm
from sklearn import neighbors

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
			l = inst.getElementsByTagName('context')[0]
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

# 4
def replace_accented(input_str):
    nkfd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

# 2
def most_frequent_sense(language, sense_dict):
	data = parse_data('data/' + language + '-dev.xml')
	outfile = codecs.open(language + '.baseline', encoding = 'utf-8', mode = 'w')
        for lexelt, instances in sorted(data.iteritems(), key = lambda d: replace_accented(d[0].split('.')[0])):
            for instance_id, context in sorted(instances, key = lambda d: int(d[0].split('.')[-1])):
			sid = getFrequentSense(lexelt, sense_dict)
			outfile.write(replace_accented(lexelt + ' ' + instance_id + ' ' + sid + '\n'))
	outfile.close()

def compute_context_vectors(language):
        input_file = 'data/' + language + '-train.xml'
	xmldoc = minidom.parse(input_file)
	s_i_data = {}
        s_data = {}
        ans_data = {}
        context_data = []
        k = 10
	lex_list = xmldoc.getElementsByTagName('lexelt')
	for node in lex_list:
		lexelt = node.getAttribute('item')
		print 'lexelt', lexelt
                s_i_data[lexelt] = []
                ans_data[lexelt] = []
                s = []
                inst_list = node.getElementsByTagName('instance')
		for inst in inst_list:
			instance_id = inst.getAttribute('id')
                        l = inst.getElementsByTagName('context')[0]
			# context = (l.childNodes[0].nodeValue + l.childNodes[1].firstChild.nodeValue + l.childNodes[2].nodeValue).replace('\n', '')
                        pretokens = nltk.word_tokenize(l.childNodes[0].nodeValue)
                        posttokens = nltk.word_tokenize(l.childNodes[2].nodeValue)
                        tokens = pretokens[-k:]
                        tokens.extend(posttokens[:k])
                        print instance_id, 'tokens', tokens
                        s.extend(tokens)
                        # convert list to dictionary
                        s_i = {}
                        for token in tokens:
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
                        s_i_data[lexelt].append((instance_id, s_i))
                        # print 'data[lexelt]',  data[lexelt]
			# create list of answers
                        sense_id = inst.getElementsByTagName('answer')[0].getAttribute('senseid')
			ans_data[lexelt].append((instance_id, sense_id))
                s = list(set(s))
                s_data[lexelt] = s
                # print lexelt, 'SET!!!', s_data[lexelt]
                
                # calculate context vectors for each instance
		context_data[lexelt] = []
                for inst in s_i_data[lexelt]:
                        instance_id = inst[0]
                        s_i = inst[1]
                        vector = []
                        for idx in xrange(len(s)):
                              word = s[idx]
                              if word in s_i:
                                   vector.append(s_i[word])
                              else:
                                  vector.append(0)
                        context_data[lexelt].append((instance_id, vector))
                        # print 'context vector for', instance_id, vector
	return context_data, ans_data
        # reminder: context_vex[lexelt] = [] -> [(id, vector), (id, vector)]
        # print 'data', data


if __name__ == '__main__':
	if len(sys.argv) != 2:
		print 'Usage: python baseline.py [language]'
		sys.exit(0)
        # sense_dict = build_dict(sys.argv[1])
	# most_frequent_sense(sys.argv[1], sense_dict)
        vect_data, ans_data  = compute_context_vectors(sys.argv[1])
        print vect_data
        print ans_data
        clf = svm.SVC()
        list_of_context_vectors = []
        for lexelt in vect_data:
                vectors = vect_data[lexelt]
                list_of_context_vectors.append(vectors[1])
        for lexelt in ans_data:
                answers = vect_data[lexelt]
                list_of_answers.append(answers[1])
        clf.fit(list_of_context_vectors, list_of_answers)
