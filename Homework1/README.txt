Name: Nina Baculinao
Uni: nb2406

COMS 4705 Natural Language Processing
Assignment 1 Readme & Report

=====================================================================
Runtime Information
=====================================================================

Part A - Language Model: < 1 minute

real  0m55.728s
user  0m52.791s
sys     0m0.444s

Part B - Part of Speech Tagging: < 5 minutes

real  4m16.207s
user  4m4.203s
sys   0m1.240s

Note: By removing Python's built-in count method in step 3, I was able to
reduce the runtime average of 26 minutes to 1 minute (up to that point).

=====================================================================
Part A - Language Model (runtime < 1 minute)
=====================================================================

Note: All perplexity.py and pos.py values must be included. Analysis must
demonstrate understanding of perplexity as a measure of a language model and
POS% as a a measure of tagger.

2) Perplexity values for unigram, bigram and trigram models respectively

    $ python perplexity.py A2.uni.txt Brown_train.txt
    The perplexity is 1104.83292814

    $ python perplexity.py A2.bi.txt Brown_train.txt
    The perplexity is 57.2215464238

    $ python perplexity.py A2.tri.txt Brown_train.txt
    The perplexity is 5.89521267642

3) Perplexity value for linear interpolation of the last three n-gram models

    $ python perplexity.py A3.txt Brown_train.txt
    The perplexity is 13.0759217039

4) Perplexity is the most common intrinsic evaluation metric for N-gram
language models. The idea behind it is it that when given two probabilistic
models, the better one is whichever model assigns a higher probability to
the test (hence more accurately predicts the test set) (Jurafsky & Martin).
Therefore, the lower the perplexity is, the better, as that correlates with
higher probability. More formally, the perplexity is based on computing the
probability of the test set, normalized by the number of words, and
therefore it is related inversely to the likelihood of the test sequence
according to the model. As stated in lecture, we can think of perplexity
as the average branching factor in predicting the next word. The more
information the N-gram model gives us about the word sequence, the lower the
perplexity. As we can see from the values above, the trigram model performs
better than bigram model and the bigram model performs better than the
unigram model. This is to be expected as additional information correlates
with less perplexity and lower branching factor. However, when we compare
the performance of linear interpolation, we find that it out-performs the
unigram and bigram models, but performs less well compared to the trigram
model. Since this form of linear interpolation simply takes equally weighted
values of lambda  to interpolate the last three n-gram models, it finds an
average between the three taggers rather than approximating the best set of
lambdas. Therefore in terms of performance, from best to last we have:
trigram model, linear interpolation with equal lambda parameters, bigram
model and unigram model, where the trigram and linear interpolation models
perform much better than the other two models, particularly the unigram
model, which has a perplexity of over 1000.

It is worth noting that since we tested the different N-gram models on the
same training set that we trained on, instead of training on a new test set
that contains all new test sentences that were not in the training set,
some of probabilities are too high and cause inaccuracy in the perplexity.
However, since we just want to compare these different language models, the
relative perplexity values between the different models still give us a good
idea of their performance.

5) When we use our linear interpolation model to score the "Sample1" and
"Sample2" text files, and compare their relative perplexities of their
Sample and Sample_scored files, it is quite easy to infer that "Sample1" is
the excerpt of the Brown dataset, while "Sample2" is not. We already know
that the perplexity of the linear interpolation model tested on the same
training set we trained is 13.08, which is quite close 11.65 perplexity
value of what I can assume is our Brown excerpt in the Sample1 file.
Sample2 on the other hand, has an exceedingly high perplexity of
1611241155.03. This is even higher than the unigram perplexity on the same
training set. Because it is such an exceedingly high perplexity, we can
hypothesize that this set may not be in English at all. When I open the
file, indeed it is not English, so the language model has no chance of even
guessing what kind of characters go into a word, let alone what word follows
another. Sample2 shows us what happens to perplexity across distribution; if
you train a model on English and then test it on another language, it will
not work. If we want to train a language model and be able to test it, it
needs to be done on a homogenous set - within languages, and even within
genres. One important metric for telling us how different the distribution
is is called cross-entropy, but for now these perplexity values are telling
enough for us to figure out which of these Samples could belong to the
training set - undoubtedly Sample1.

    $ python perplexity.py Sample1_scored.txt Sample1.txt
    The perplexity is 11.6492786046

    $ python perplexity.py Sample2_scored.txt Sample2.txt
    The perplexity is 1611241155.03

=====================================================================
Part B - Part of Speech Tagging (runtime < 5 minutes)
=====================================================================

Taggers are evaluated by comparing their output from a test set to human
labels for that test set (Jurafsky & Martin). In this case, we compare %
correct part-of-speech tags produced by our machine taggers with human labels
for that tag set ("Brown_tagged_dev.txt"). In the case of our HMM tagger, which
implements the Viterbi algorithm, 93.69% of tags matched the human tagged
or 'correct' set - this seems quite good. It seems that calculating emission
probabilities and trigram probabilities in the sequence with smoothing for
rare words is  fairlyn effective way of tagging parts of speech. However, when we
iompare that 95.31% correct tags the NLTK trigram tagger with backoffs -
from trigram to bigram to default 'NOUN' tags -  came up with, we realize
the HMM tagger could still use some improvement. What improvements to make
could be decided after an error analysis to pinpoint areas where the tagger
does not perform well.

5) POS% of my HMM tagger

    $ python pos.py B5.txt Brown_tagged_dev.txt
    Percent correct tags: 93.6921615938

6) POS% of NLTK's trigram tagger with backoffs

    $ python pos.py B6.txt Brown_tagged_dev.txt
    Percent correct tags: 95.3123637315

