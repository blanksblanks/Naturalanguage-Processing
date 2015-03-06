from providedcode.transitionparser import TransitionParser
from providedcode.dependencycorpusreader import DependencyCorpusReader
'''from providedcode.evaluate import DependencyEvaluator
from featureextractor import FeatureExtractor
from transition import Transition'''

from providedcode.dependencygraph import DependencyGraph
import sys

if __name__ == '__main__':

        tp = TransitionParser.load(sys.argv[1])

            data = DependencyCorpusReader('./', sys.stdin).parsed_sents()
            parsed = tp.parse(testdata)
                for p in prased:
                    print p.to_conll(10).encode('utf-8')
                    print('\n')
