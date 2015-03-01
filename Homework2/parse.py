'''import random
from providedcode import dataset'''
from providedcode.transitionparser import TransitionParser
'''from providedcode.evaluate import DependencyEvaluator
from featureextractor import FeatureExtractor
from transition import Transition'''

from providedcode.dependencygraph import DependencyGraph
import sys

if __name__ == '__main__':

    tp = TransitionParser.load(sys.argv[1])

    for line in sys.stdin:
        sentence = DependencyGraph.from_sentence(line)
        parsed = tp.parse([sentence])
        print parsed[0].to_conll(10).encode('utf-8')

