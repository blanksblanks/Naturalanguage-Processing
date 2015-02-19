Name: Nina Baculinao
Uni: nb2406

COMS 4705 Natural Language Processing
Assignment 1 Readme

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

2)

    $ python perplexity.py A2.uni.txt Brown_train.txt
    The perplexity is 1104.83292814

    $ python perplexity.py A2.bi.txt Brown_train.txt
    The perplexity is 57.2215464238

    $ python perplexity.py A2.tri.txt Brown_train.txt
    The perplexity is 5.89521267642

3)

    $ python perplexity.py A3.txt Brown_train.txt
    The perplexity is 13.0759217039

4) Briefly comment on any differences in performance between the models with
and without linear interpolation. Use the perplexity output to support your
conclusions.

  • Average branching factor in predicting the next word
  • Lower is better (lower perplexity -> higher probability)
      Perplexity is like a branching factor

5) Both “Sample1.txt” and “Sample2.txt” contain sets of sentences; one
  of the files is an excerpt of the Brown dataset. Use your model to
  score the sentences in both files. Our code outputs the scores of each
  into “Sample1_scored.txt” and “Sample2_scored.txt”. Run the perplexity
  script on both output files and include the output in your report. Use
  these results to make an argument for which sample belongs to the
  Brown dataset.

 Perplexity Across Distributions
• What happens if you train a model on English and do it on French?
It won't work
    ○ if you want to train a language model, you have to train it on
    a homogenous set - within language, and even within genres
        ○ there is a metric that tells you how different the
        distribution is called cross-entropy


    $ python perplexity.py Sample1_scored.txt Sample1.txt
    The perplexity is 11.6492786046

    $ python perplexity.py Sample2_scored.txt Sample2.txt
    The perplexity is 1611241155.03

=====================================================================
Part B - Part of Speech Tagging (runtime < 5 minutes)
=====================================================================

5) POS% of my HMM tagger

    $ python pos.py B5.txt Brown_tagged_dev.txt
    Percent correct tags: 93.6921615938

6) POS% of NLTK's trigram tagger with backoffs

    $ python pos.py B6.txt Brown_tagged_dev.txt
    Percent correct tags: 95.3123637315

