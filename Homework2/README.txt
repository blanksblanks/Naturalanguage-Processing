Name: Nina Baculinao
Uni: nb2406

COMS 4705 Natural Language Processing
Assignment 2 Readme

Note README.txt contains the exact same content as the markdown version README.md.

---------------------------------------------------------------------
1) Dependency Graphs

a. The visualized dependency graph of a sentence from each of the English, Danish, Korean, and Swedish training data sets can be found in the Homework 2 directory.

b. According to Nivre in "Algorithms for Deterministic Incremental
Dependency Parsing"" dependency graph G = (V, A) is projective if and only if,
for every arc (i, l, j) ∈ A and node k ∈ V, if i < k < j or j < k < i then
there is a subset of arcs {(i, l1, i1), (i1, l2, i2), ... (ik−1, lk, ik )} ∈ A
such that ik = k. In plain English, none of the arcs should cross each other in
a projective graph, i.e. if there exists an arc (i, l, j) where w_i is the
dependent word and w_j is the head word, then there shouldn't exist a) any arcs
with a dependent word less than w_i and head word less than w_j, because their
arcs would intersect, or b) any arcs with a dependent word greater than w_i and
head word greater than w_j because these conditions would create intersection
of the arcs. Our model is only trained on projective sentences as the
unconstrained problem of parsing non-projective sentences is NP-hard.

Some of these training sentences do not have projective dependency graphs
(about 10% of the Swedish data set, for example). Therefore, we use a function
providedcode/transition.py to determine if a dependency graph is projective.

    @staticmethod
    def _is_projective(depgraph):
        """
        Checks if a dependency graph is projective
        """
        arc_list = set()
        for key in depgraph.nodes:
            node = depgraph.nodes[key]
            if 'head' in node:
                childIdx = node['address'] // j for dependent wj
                parentIdx = node['head'] // i for head wi
                arc_list.add((parentIdx, childIdx)) // add (i, j)

        for (parentIdx, childIdx) in arc_list:
            # Ensure that childIdx < parentIdx
            if childIdx > parentIdx: // swap if j > i so j < i
                temp = childIdx
                childIdx = parentIdx
                parentIdx = temp
            for k in range(childIdx + 1, parentIdx): // for any k bt j...i
                for m in range(len(depgraph.nodes)): // for any node m
                    if (m < childIdx) or (m > parentIdx): // any m < j and > i
                        if (k, m) in arc_list: // this arc crosses
                            return False
                        if (m, k) in arc_list:
                            return False
        # print arc_list
        return True
        
Discussion: To check if a dependency graph of a sentence is projective, we
first create a unique set of all the arcs in the dependency graph. This list is
generated by traversing all the nodes in the dependency graph and adding the
tuple (i, j) to the arc list if the node has an identified head, and i, j
represent the node's head (parentIdx) and node's address (childIdx). After we
have the completed arc_list, we traverse every (i, j) pairing, swapping i with
j if j > i so that j < i, i.e. the childIdx is always less than the parentIdx.
After that, we check all the nodes k in the range between the i and j (parent
and child) indexes, and all the nodes m  > i and m < j (outside the parent and
child indexes), to check if there exist any arcs in the arc list that have the
tuple identity (k, m) or (m, k). If there exist any arcs like that, then the
graph is not projective, because that arc from k to m or m to k would intersect
with the arc from i to j.

c. Projective and non-projective sentence examples:

"She ate icecream with joy." (projective)

This sentence is projective because the verb "ate" has three dependencies,
"she", "icecream" and "with joy" (where joy modifies with). None of the
connecting arcs cross paths, so this is projective.

"You shouldn't put icecream into the freezer that is already melted."
(non-projective)

The above sentence is non-projective because the prepositional phrase "into the
freezer" is part of the complement of the verb "put", while the relative clause
"that is already melted" modifies the noun "icecream." So the arc connecting
"put" to "into" will cross the arc connecting "icecream" and "that is already
melted." 

---------------------------------------------------------------------
2) Manipulating Configurations

a. The four operations left_arc, right_arc, shift and reduce are fully
implemented in transition.py as a key part of the Nivre dependency parser is
manipulating the parser configuration.

b. The bad features model only contains the following features for extraction:

    Stack[0] word, features and left and rightmost dependencies
    

    Buffer[0] word, features and left and rightmost dependencies

The performance of parser using the provided badfeatures.model is, as can be
expected, quite bad. These features extracted in the feature model are not very
informative as they are, especially as a word is much less informative to
possible dependencies than the word's part of speech (ctag and tag attributes
in the list of features)

The standard metrics unlabeled attachment score and labeled attachment score
(the former assesses whether the output has the correct head and dependency
arcs, while the latter additionally measures the accuracy of the labels of each
arc) are all below 25% and practically 0% LAS accuracy for English, Danish and
Korean. 

Swedish:
UAS: 0.229038040231
LAS: 0.125473013344

English:
UAS: 0.0518518518519 
LAS: 0.0

Danish:
UAS: 0.123552894212 
LAS: 0.00718562874251

Korean:
UAS: 0.115488605639 
LAS: 0.0

---------------------------------------------------------------------
3) Dependency Parsing

a.  

Code format | CoNLL format| Description
------------|-------------|-------------
address     | ID          | Integer token identifier
word        | FORM        | Word or punctuation
lemma       | LEMMA       | Stem of token
ctag        | CPOSTAG     | Coarse-grained POS tag
tag         | POSTAG      | Fine-grained POS tag
feats       | FEATS       | Additional syntactic features
head        | HEAD        | Token's head
rel         | DEPREL      | Token's dependency relation to its head
deps        | -           | Dictionary of token's dependencies by their POS : ID
-           | PHEAD       | Projective head of token
-           | PDEPREL     | and its dependency relation

Final feature model: two target tokens (STK[0], BUF[0]) + a few lookahead tokens

address      | word | lemma | ctag | tag | feats | head (word) | rel | ldep, rdep
------------:|:----:|:-----:|:----:|:---:|:-----:|:-----------:|:---:|:----------:
STK[0]       |  x   |   +   |  +   |  +  |   x   |      -      |  -  |    x   x
STK[1]       |      |       |  +   |  +  |       |             |     |
BUF[0]       |  x   |   +   |  +   |  +  |   x   |      -      |  -  |    x   x
BUF[1]       |  +   |   +   |  +   |  +  |   +   |             |     |
BUF[2]       |      |       |  +   |  +  |       |             |     |
BUF[3]       |      |       |  +   |  +  |       |             |     |

Discussion: As mentioned previously, the bad model in the feature extractor had
certain features in their model previously (marked 'x' in the table above).
After specifying new features for the model (marked '+' in the table above),
the performance of the feature extractor improved vastly. I removed the rel and
head features because the information wouldn't be included later (marked '-' in
the table above.) The feature model I used is based on a standard feature model
as described in the book Dependency Parsing by Kubler, McDonald and Nivre. I
will describe the implementation, complexity and performance of three of my
feature additions below, from most to less influential (in terms of improving
performance of the feature model).

```
For implementation, talk about how you implemented the feature. For complexity,
think about big O - i.e., in relation to the number of words in the sentence.
For performance, you could give the LAS scores with and without it. 

1) absolute performance of the combination of features on the three languages you have test data for
2) a qualitative estimation of the marginal performance of a feature, i.e.
which feature appears to be most/least influential 3) why you think a given
feature is useful in a linguistic sense, and whether that is reflected in its
quantitative performance.
``` 1: Part of speech tags. I added tag and ctag to the feagtures extracted
from stack[0] and buffer[0]. Part of the This greatly improved performance,
boosting nearly all of the language to 50% accuracy. Knowing the fine-grained
part of speech tags and coarse-grained part of speech tags was very effective,
though the performance without coarse-grained ctags was almost the same as
performance with them - the improvement with coarse-grained tags was so slight
that I hesitated before deciding to continue to include this in the feature
model. Part of speech tags are extremely useful from the linguistic sentence
for determining more likely bigrams and trigrams in dependency parsing, as can
be seen by this big jump in accuracy. I hesitated between removing either the
coarse-grained or fine grained tag but settled on leaving the coarse grained
first as you can parse much more quickly with a simple grammar because the
grammar constant is smaller and you restrict the search of the expensive
refined model to exploring projected labels that the simple grammar likes. In
terms of implementation, it was a matter of extracting the tags so this feature
took place in constant time.

2: Lookahead tokens. I added a lookahead token on buffer (the second element -
buffer[1]), which contains remaining input words, and extracted word, lemma,
ctag, tag and feats for it. This raised accuracy by almost 10%. In addition, I
added a few more less important but possibly useful lookahead tokens in
stack[1] (the list of partially processed words) and buffer[2] and buffer[3].
Since these were likely less immediately relevant, I only looked up tags and
ctags for them, disregarding the words and lemmas because lemmas were
relatively less important than tag information, so this could possibly reduce
the noise. Access to these additional tokens and lookup of their tag features
should happen in constant time. 

3: Lemma added to complement word, feats and left/right dependencies for
buffer[0] and stack[0]. I also added lemma to the next token in both the stack
and the buffer. Word, feats and left/right dependencies were not very
informative by themselves, but the addition of lemma served to improve accuracy
for each language. As lemma is the stem of the token, this additional
information seemed a good complement for the original feature of just word in
the form it appears in the text. Originally, I had also included an extractor
of the word and lemma of the head of the token but since head information would
not always be available later I removed that aspect of the feature model,
together with possible information stored in the arcs as rel. This helped boost
the performance of the feature extractor as well, though not as much as part of
speech tags. The extraction of this feature also took constant time.

I generated trained models for English, Danish, Swedish, and Korean data sets,
and save the trained model for later evaluation. All the trained models and
conll files can be found in the main directory of Homework 2. The absolute
performance of  the combination of features on the three test data languages
(plus English, which only had a bank of less than 20 words) are as follows.

Language | WithOUT head/rel tags | With head/rel tags
---------|-----------------------|---------------------
Swedish: | UAS: 0.782314280024   | UAS: 0.886476797451
         | LAS: 0.665206134236   | LAS: 0.872137024497
Danish:  | UAS: 0.79620758483    | UAS: 0.862874251497
         | LAS: 0.707185628743   | LAS: 0.852095808383
Korean:  | UAS: 0.749710312862   | UAS: 0.853997682503
         | LAS: 0.620702974121   | LAS: 0.852838933951
English: | UAS: 0.762962962963   | UAS: 0.837037037037
         | LAS: 0.718518518519   | LAS: 0.834567901235
         
                     
c. The arc-eager shift reduce parser, in its simplest and most efficient
version, uses a greedy deterministic procedure to derive a single dependency
graph and in terms of computational complexity takes linear time in relation to
the number of sentences to parse - this is assuming each transition can be
predicted and executed in constant O(1) time (Nivre). This model maintains that
time as all the feature extractors do happen in cosntant time. The arc-eager
shift reduce parser, like other parsers, is implemented as a search for a
transition sequence that derives the optimal parse tree for a given sentence.
However, it does have a few tradeoffs compared other parsers like CKY parsers.
Arc eager shift-reduce parsing can make wrong turns and need to backtrack -
generally it does not deal well with ambiguity. When there is a shift-reduce
ambiguity in the arc-eager system, the oracle prediction makes an assumption
and automatically chooses shift. Another limitation is the lack of guarantees
when applying the oracle to a configuration that does not belong to the
canonical transition sequence - in this case the oracle prediction is as
expected suboptimal. Especially considering the limited size of the feature
space in our libsvm model and the fact we have limited our training data to 200
sentences, in some cases less than 200 because within these 200 we only look at
the projective ones. In a sense, the arc eager shift-reduce parser highlights
again that accuracy depends on the tradeoff between a high-complexity model
which may over-fit the data and a large-margin which will incorrectly classify
some training data in the interest of better generalization.

---------------------------------------------------------------------
4) Parser executable

a. Instructions for running parse.py:

```
cat englishfile | python parse.py english.model > englishfile.conll 
```
---------------------------------------------------------------------
INCLUDED DELIVERABLES (can all be found in the main directory of hw2)

1. Dependency graph plots
    a. $HW2_ROOT/figure_en.png - image of a sentence from English training data
    b. $HW2_ROOT/figure_da.png - image of a sentence from Danish training data
    c. $HW2_ROOT/figure_ko.png - image of a sentence from Korean training data
    d. $HW2_ROOT/figure_sw.png - image of a sentence from Swedish training data
2. Transitions between configurations
    a. $HW2_ROOT/transition.py
3. Feature extractor
    a. $HW2_ROOT/featureextractor.py
4. Trained model files
    a. $HW2_ROOT/english.model - trained TransitionParser for English
    b. $HW2_ROOT/danish.model - trained TransitionParser for Danish    
    c. $HW2_ROOT/korean.model - trained TransitionParser for Korean
    d. $HW2_ROOT/swedish.model - trained TransitionParser for Swedish
5. Standard parser
    a. $HW2_ROOT/parse.py - parser program
6. README file containing results and discussions
    a. $HW_ROOT/README.txt
