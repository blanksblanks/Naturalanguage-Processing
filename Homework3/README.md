Name: Nina Baculinao
Uni: nb2406

COMS 4705 Natural Language Processing
Assignment 3 Report

Note report.txt contains the exact same content as the markdown version README.md.

---------------------------------------------------------------------

0. Ran baseline.py, which simply took the most frequently appearing senses and labeled all appearances of that word accordingly. The output was scored accordingly:

Fine-grained score for "English.baseline" using key "data/English-dev.key":
    precision: 0.535 (1061.00 correct of 1985.00 in total)
    attempted: 100.00 % (1985.00 attempted of 1985.00 in total)

Fine-grained score for "Spanish.baseline" using key "data/Spanish-dev.key":
    precision: 0.684 (1441.00 correct of 2107.00 in total)
    attempted: 100.00 % (2107.00 attempted of 2107.00 in total)

Fine-grained score for "Catalan.baseline" using key "data/Catalan-dev.key":
    precision: 0.678 (768.00 correct of 1133.00 in total)
    attempted: 100.00 % (1133.00 attempted of 1133.00 in total)

1. For this step I computed context vectors for each instance of a word using language-train.xml as training data and a default window size of k=10 (where the context consists of all words within k distance of word w). The context vector for each lexelt varied from vectors of length 298 (use) and length 1987 (add.v). The vectors had the characteristic of being very sparse with lots of 0's and a few 1's.  

2. For this step, support vector machines come into play by performing optimization to find a hyperplane with the largest margin that separates training examples into classes, where a test example is classified depending on the side of the hyerplane it lies in. Using the scikit-learn library's neighbors.KNeighborsClassifier class and svm.LinearSVC class, I trained two separate classifiers for the three languages with their respective language-test.xml data. The results of testing on the dev data follow in the next paragraph.

3. According to scorer2:

ENGLISH:
 KNN:
  precision: 0.566 (1124.00 correct of 1985.00 attempted)
  attempted: 100.00 % (1985.00 attempted of 1985.00 in total)
 SVC:
  precision: 0.620 (1230.00 correct of 1985.00 attempted)
  attempted: 100.00 % (1985.00 attempted of 1985.00 in total)

SPANISH:
 KNN:
  precision: 0.700 (1474.00 correct of 2107.00 attempted)
  attempted: 100.00 % (2107.00 attempted of 2107.00 in total)
 SVC:
  precision: 0.783 (1650.00 correct of 2107.00 in total)
  attempted: 100.00 % (2107.00 attempted of 2107.00 in total)

CATALAN:
 KNN:
  precision: 0.703 (797.00 correct of 1133.00 attempted)
  attempted: 100.00 % (1133.00 attempted of 1133.00 in total)
 SVC:
  precision: 0.824 (934.00 correct of 1133.00 attempted)
  attempted: 100.00 % (1133.00 attempted of 1133.00 in total)

To sum it up in a table:

----------------------------------------------------------------------------------
|                         | English          | Spanish       | Catalan           |
|-------------------------|------------------|---------------|-------------------|
| Baseline                | 0.535            | 0.684         | 0.678             |
| Context vectors only    | 0.566 / 0.620    | 0.700 / 0.783 | 0.703 / 0.824     |
----------------------------------------------------------------------------------

In the case of all languages, the Linear SVC Support Vector Machine performed better than KNN (0.620 vs. 0.566 for English, 0.783 vs. 0.700 for Spanish, and 0.824 vs. 0.703 for Catalan). All the classifiers attempted to classify 100% of their respective language-dev.xml data. Additionally, all the precision scores of the context vectors approach out-perform the baseline of picking just the most frequently occurring sense, even the KNN (0.566 English KNN > 0.535 baseline), and the simprovement is seen across Spanish and Catalan.

4. For this step I tried to extract better features than just taking all the words in the window, and then redid the classification. In this section I will discuss the different approaches and how much they improved/worsened performance.

a) Remove stop words, do stemming, etc. I also tried removing punctuation and capitalization in this preprocessing step to extract better features

------------------------------------------------------------------------------------
|                           | English          | Spanish       | Catalan           |
|---------------------------|------------------|---------------|-------------------|
| 0_No preprocessing        | 0.566 / 0.620    | 0.700 / 0.783 | 0.703 / 0.824     |
| 1_Remove stop words       | 0.525 / 0.615    | 0.682 / 0.787 | - unavailable     |
| 2_Stem tokens             | 0.564 / 0.623    | 0.701 / 0.795 | 0.705 / 0.824     |
| 12_Combination            | 0.531 / 0.620    | 0.690 / 0.791 | - unavailable (1) |
------------------------------------------------------------------------------------

I performed removing stop words and stemming tokens separately, and then together. Above is a table that sums up the effects of each type of preprocessing. The two numbers in each column represent KNN / SVC. For the most part, I look at SVC classifier values because they have better performance, but I will discuss KNN values once in a while.

STOP WORDS: Note that for English, performance drops (0.620 -> 0.615 for LinearSVC) when we filter out stop words, that is, high-frequency words like “the”, “to” and “also” that contain little lexical content and whose presence in a text may not be all that helpful to distinguish the text from another text. However, for English, we seem to be losing useful information to disambiguate the words. On the other hand, performance increases when we remove stop words in Spanish (0.783 -> 0.787). For English and Spanish, I used the stopwords from NLTK's Wordlist Corpora, but NLTK did not have a list of stop words for Catalan, so this type of preprocessing is only done on English and Spanish.

TLDR; Stop words: bad for English, slightly good for Spanish, N/A for Catalan

STEM TOKENS: To stem tokens, I used the Porter Stemmer. For English, there is a slight increase in performance for LinearSVC (0.620 -> 0.623) yet a slight decrease for KNN (0.566 -> 0.564) so I consider it an inconclusive results as to whether this is a good way to extract better features in English. For Spanish, there is a pretty good increase (0.783 -> 0.795)) and for Catalan the results are the same (0.824 -> 0.824)

TLDR; Stem tokens: inconclusive for English, good for Spanish, inconclusive for Catalan

COMBINATION: For English, the mild increase in performance by stemming tokens is canceled out by the mild decrease in performance, giving us the same result that we have without preprocessing (0.620) For Spanish, stemming tokens alone performs better than the combination (0.795 vs. 0.791). And for Catalan, the combination is unavailable because NLTK does not have a stop list for it.

TLDR; Combo: unhelpful for English, worse than just stemming for Spanish, N/A for Catalan

-----------------------------------------------------------------------------------
|                       | English           | Spanish          | Catalan          |
-----------------------------------------------------------------------------------
| 0_No preprocessing    | 0.566 / 0.620     | 0.700 / 0.783    | 0.703 / 0.824    |
-----------------------------------------------------------------------------------
| 3x_Remove punctuation | 0.547 / 0.618     | 0.699 / 0.789    | 0.708 / 0.820    |
-----------------------------------------------------------------------------------
| 3_Remove punc & caps  | 0.558 / 0.621 +   | 0.698 / 0.790    | 0.714 / 0.824 +  |
-----------------------------------------------------------------------------------
| 123_Combination       | 0.540 / 0.620     | 0.668 / 0.795 +  | N/A              |
-----------------------------------------------------------------------------------

+ in the table indicates this was the best results for this part so far

REMOVE PUNCTUATION AND CAPITALIZATION: Removing punctuation produced worse results for English and Catalan, but once we removed punctuation and capitalization, this produced slightly better results for English, Spanish and the same result for Catalan, so I considered this a good preprocessing step. For Spanish, the combination of removing stop words, stemming words and was the best combination for it.
To sum it up: English benefited from removing punctuation and capitalization, Spanish benefited from removing stop words, stemming words and removing punctuation and capitalization, Catalan stayed the same after removing puncutation and capitalization but since removing them created shorter feature vectors I considered this a benefit.

b) Add more features by obtaining the synonyms, hyponyms and hypernyms of a word in WordNet.

------------------------------------------------------------------------------------
|                           | English          | Spanish        | Catalan          |
------------------------------------------------------------------------------------
| 0_No preprocessing        | 0.566 / 0.620    | 0.700 / 0.783  | 0.703 / 0.824    |
------------------------------------------------------------------------------------
| 4_Syn + hyper + hyponyms  | 0.497 / 0.598    | - unavailable  | - unavailable    |
------------------------------------------------------------------------------------

I used WordNet to find all possible synonyms, hyponyms and hypernyms to the feature set. For a simplified example, if we have the token ‘dog', then synonyms according to WordNet's synsets could be [u'andiron', u'frump', u'pawl', u'frank', u'dog', u'chase', u'cad']. Hyponyms and hypernyms could be [u'basenji', u'corgi', u'cur', u'dalmatian', u'griffon', u'lapdog', u'leonberg', u'newfoundland', u'pooch', u'poodle', u'pug', u'puppy', u'spitz', u'canine']. I only counted the words that did not have underscores (indicating that this word was actually made of two tokens). Once we had that list of synonyms, hypernyms and hyponyms, we added it to the vector. The same preprocessing was required for dev data. The final results were, as was somewhat expected, worse (0.620 -> 0.598). Not only did we add preprocessing time, we also generated these incredibly long and sparse vectors.

A better way to do it perhaps would have been to generate sets of synoyms and consider each set a single feature in the vector. For example, if the word ‘frigid' appeared in the training set, and ‘cold' appeared later, then both could be added to the same feature set. However, the route I took above was Di's suggested implementation on Piazza, and it's interesting as well to examine why this approach fails to provide any meaningful linguistic information to help disambiguate a word sense.

Note: this step was only undertaken for English, because Open Multilingual WordNet was not available, so we could not do this for Spanish and Catalan. I strongly suspect that it would not have produced more favorable results anyway. 

c) Compute relevance scores

---------------------------------------------------------------------------
| Threshold value         | Relevance     | PMI           | Chi           |
---------------------------------------------------------------------------
| percent = 0.25          | 0.462 / 0.536 | -             | -             |
---------------------------------------------------------------------------
| percent = 0.50          | 0.471 / 0.537 | -             | -             |
---------------------------------------------------------------------------
| percent = 1.0           | 0.475 / 0.552 | -             | -             |
---------------------------------------------------------------------------
| top = 20                | 0.524 / 0.544 | -             | -             |
---------------------------------------------------------------------------
| top = 30                | 0.529 / 0.549 | -             | -             |
---------------------------------------------------------------------------
| top = 50                | 0.545 / 0.570 | -             | -             |
---------------------------------------------------------------------------
| top = 100               | 0.547 / 0.576 | -             | -             |
---------------------------------------------------------------------------
| top = 250               | 0.549 / 0.602 | -             | -             |
---------------------------------------------------------------------------
| top = 300               | 0.551 / 0.610 | 0.551 / 0.597 | 0.566 / 0.620 |
---------------------------------------------------------------------------
| thresh = avg prob (lex) | 0.322 / 0.607 | 0.539 / 0.588 | 0.472 / 0.538 |
---------------------------------------------------------------------------
| thresh = -2.0           | 0.555 / 0.609 | -             | -             |
---------------------------------------------------------------------------

RELEVANCE SCORES: For this step, I computed the relevance score log(p(s|c) / p(!s|c)) where p(s|c) is the probability word w has sense s when context word c appears and p(!s|c) is the probability word doesn't have sense s when the context word c appears. Therefore, for a sense s of word w and a word c in the window of w, we computed the ‘relevance score' of c with s. After that, I sorted all these context words c by their relevance score, so that the final set of features is the union of all the top context window words for each sense that I kept.

I played with many threshold values, but finally had to conclude that this step only diminished performance. I tried counting only the top # of words for each sense, I tried the top percentages for each sense, I also tried a threshold value of the average relevance score for every lexelt and an arbitarily chosen threshold score of -2.0 based on my own observations of the relevance scores being generated. Recall that my own context vectors baseline is 0.620. The more inclusive I made the threshold, the longer the context vectors, and the closer it would approach that value. For example “activate.v” had an original vector length of 1670. If I shortened it to a vector length of 113 with the top relevance scoring pairs for each lexelt, it would perform correspondingly worse than a newly generated vector of length 1479 with less strict threshold values. Some vectors only had original vectors of length 300, so choosing the top 300 relevance scores for each sense would not even change the vectors, giving closer scores to our original 0.620.  Overall, the relevance score was not a useful feature extraction method.

d) Trying pointwise mutual information and chi-square for extracting features

-------------------------------------------------------------------------------------
|                         | English          | Spanish          | Catalan           |
-------------------------------------------------------------------------------------
| 0_No preprocessing      | 0.566 / 0.620     | 0.700 / 0.783    | 0.703 / 0.824    |
-------------------------------------------------------------------------------------
| 5_Relevance scores      | 0.322 / 0.607     | 0.500 / 0.776    | 0.568 / 0.818    |
-------------------------------------------------------------------------------------
| 6_Pointwise mutual info | 0.539 / 0.588     | 0.687 / 0.746    | 0.682 / 0.773    |
-------------------------------------------------------------------------------------
| 7_Chi square            | 0.472 / 0.538     | 0.691 / 0.711    | 0.682 / 0.730    |
-------------------------------------------------------------------------------------

POINTWISE MUTUAL INFORMATION: I calculated the PMI as described in class as log p(s,c) / p(s)p(c) = log p(s|c) / p(s) where in this case s is the sense and and c is the word in the context window that appears with it.

CHI SQUARE: I calculated chi square by the formula: [(obs - exp) * (obs - exp)]/ exp where exp = s/t * c/t * t (and t is the number of instances in total for the lexelt) and obs is just the observed instances that s and c actually appear together. 

For all of these, I used the average of scores across a lexelt for all senses as the threshold for cutting off features. Relevance scores performed the best and closest to the original in the case of relevance scores. So none of these turned out to be helpful feature extraction methods. 

5. Adjust the window size k

------------------------------------------------------------
| k  | English         | Spanish         | Catalan         |
------------------------------------------------------------
| 2  | 0.582 / 0.628   | 0.741 / 0.782   | 0.757 / 0.820   |
------------------------------------------------------------
| 3  | 0.590 / 0.640 + | 0.735 / 0.785   | 0.767 / 0.821   |
------------------------------------------------------------
| 4  | 0.582 / 0.630   | 0.729 / 0.784   | 0.742 / 0.812   |
------------------------------------------------------------
| 5  | 0.574 / 0.633   | 0.717 / 0.786   | 0.741 / 0.803   |
------------------------------------------------------------
| 6  | 0.571 / 0.618   | 0.717 / 0.793 + | 0.745 / 0.807   |
------------------------------------------------------------
| 7  | 0.544 / 0.618   | 0.710 / 0.776   | 0.733 / 0.804   |
------------------------------------------------------------
| 8  | 0.506 / 0.606   | 0.707 / 0.780   | 0.721 / 0.808   |
------------------------------------------------------------
| 9  | 0.546 / 0.616   | 0.704 / 0.783   | 0.699 / 0.811   |
------------------------------------------------------------
| 10 | 0.566 / 0.620   | 0.700 / 0.783   | 0.703 / 0.824 + |
------------------------------------------------------------
| 12 | 0.567 / 0.614   | 0.689 / 0.774   | 0.717 / 0.821   |
------------------------------------------------------------

+ indicates the best performers in this part

WINDOW SIZE: Surprisingly, this turned out to have the effect one would have hoped for with the relevance scores/chi square/PMI methods. It shortened the vectors for each lexelt and improved performance. Interestingly different languages, the range of relevant nearby words containing important linguistic information for disambiguation varies. For English, k=3 increased performance the best (0.640 precision compared to 0.620 for k=10). For Spanish, k=6 (0.793 compared to 0.783). And for Catalan, the original window size k=10 (0.824). 

6. Find the best combination of the feature extracting approaches and use the classifier that gives better results

--------------------------------------------------------
| Key | Feature                                        |
--------------------------------------------------------
| 1   | Remove stop words                              |
--------------------------------------------------------
| 2   | Stem tokens                                    |
--------------------------------------------------------
| 3   | Remove punctuation and capitalization          |
--------------------------------------------------------
| 3#  | Remove punctuation, capitalization and numbers |
--------------------------------------------------------

----------------------------------------------------------------------
| Ft  | k  | English           | Spanish          | Catalan          |
----------------------------------------------------------------------
| 3   | 3  | 0.589 / 0.642 +++ | 0.720 / 0.795    | 0.756 / 0.824    |
----------------------------------------------------------------------
| 23  | 3  |   -   / 0.631     |   -   /   -      |  -   / 0.819     |
----------------------------------------------------------------------
| 3   | 6  |   -   /   -       | 0.710 / 0.796    |  -   /   -       |
----------------------------------------------------------------------
| 23  | 6  |   -   /   -       | 0.720 / 0.812    |  -   /   -       |
----------------------------------------------------------------------
| 123 | 6  |   -   /   -       | 0.717 / 0.793    | N/A              |
----------------------------------------------------------------------
| 23  | 10 |   -   /   -       |  -   /   -       |  -   / 0.828     |
----------------------------------------------------------------------
| 3#  | 3  |   -   / 0.640     |  -   /   -       |  -   /   -       |
----------------------------------------------------------------------
| 23# | 6  |   -   /   -       |  -   / 0.813 +++ |  -   /   -       |
----------------------------------------------------------------------
| 23# | 10 |   -   /   -       |  -   /   -       |  -   / 0.831 +++ |
----------------------------------------------------------------------

+++  indicates the best performers overall in this last step

I experimented with the better results from part 4a) and my findings with different k-values. I didn't use information for synsets, relevance scores, PMI or chi square because they my experiences with them had only detracted from the original performance. While k for Spanish and Catalan are different, they undergo the same preprocessing procedures, which is interesting and perhaps due to their closer linguistic similarity with each other compared to with English. It turns out the best results for this training and development data are:

English: k=3, remove punctuation and capitalization
Spanish: k=6, stem tokens, remove punctuation, capitalization and numbers
Catalan: k=10, stem tokens, remove punctuation, capitalization and numbers

In the appendix at the end of this report you can find all the trials listed in table form (basically a compilation of all the smaller tables that I have shown up to this point) I ran in order to reach these results.

---------------------------------------------------------------------

SUMMARY OF FINAL FEATURE EXTRACTING APPROACHES FOR ENGLISH, SPANISH AND CATALAN:

For each training and development example, we are provided a few sentences as the surrounding context. For the best combination of feature extracting approaches, I first consider all single words (unigrams) in the surrounding context window of words that are within k distance of (preceding and following) the word to be disambiguated (and these words can be in different sentences). Depending on the language, k is set to a different value. After several trials, I have set k=3 for English, k=6 for Spanish and k=10 for Catalan. During the preprocessing, all tokens in the set context window are converted to lowercase. For English, only punctuation is removed, and in the case of Spanish and Catalan, all tokens that do not contain an alphabet character (punctuation and numbers) are removed. Spanish and Catalan also have all their tokens replaced by their morphological root forms using a Porter stemmer. Each remaining token contributes one feature to our final context vector. In a training (or test) example, the feature corresponding to is set to the number of times it appears in that example. 

The final results:

Fine-grained score for "English.answer" using key "data/English-dev.key":
 precision: 0.642 (1274.00 correct of 1985.00 attempted)
 recall: 0.642 (1274.00 correct of 1985.00 in total)
 attempted: 100.00 % (1985.00 attempted of 1985.00 in total)

Fine-grained score for "Spanish.answer" using key "data/Spanish-dev.key":
 precision: 0.813 (1712.00 correct of 2107.00 attempted)
 recall: 0.813 (1712.00 correct of 2107.00 in total)
 attempted: 100.00 % (2107.00 attempted of 2107.00 in total)

Fine-grained score for "Catalan.answer" using key "data/Catalan-dev.key":
 precision: 0.831 (941.00 correct of 1133.00 attempted)
 recall: 0.831 (941.00 correct of 1133.00 in total)
 attempted: 100.00 % (1133.00 attempted of 1133.00 in total)

---------------------------------------------------------------------

INCLUDED DELIVERABLES (can all be found in the main directory of hw3):

[x] main.py
[x] English.answer
[x] Spanish.answer
[x] Catalan.answer
[x] report.txt

---------------------------------------------------------------------

APPENDIX OF ALL EXPERIMENTS AND RESULTS:

--------------------------------------------------------
| Key | Feature                                        |
--------------------------------------------------------
| -1  | Baseline                                       |
--------------------------------------------------------
| 0   | Compute context vectors with no preprocessing  |
--------------------------------------------------------
| 1   | Remove stop words                              |
--------------------------------------------------------
| 2   | Stem tokens                                    |
--------------------------------------------------------
| 3x  | Remove punctuation                             |
--------------------------------------------------------
| 3   | Remove punctuation and capitalization          |
--------------------------------------------------------
| 3#  | Remove punctuation, capitalization and numbers |
--------------------------------------------------------
| 4   | Add list of synonyms, hypernyms and hyponyms   |
--------------------------------------------------------
| 5   | Compute relevance scores                       |
--------------------------------------------------------
| 6   | Compute PMI                                    |
--------------------------------------------------------
| 7   | Compute Chi-square                             |
--------------------------------------------------------

----------------------------------------------------------------------
| ft  | k  | English           | Spanish          | Catalan          |
----------------------------------------------------------------------
| -1  |    | 0.535 *           | 0.684            | 0.678            |
----------------------------------------------------------------------
| 0   | 10 | 0.566 / 0.620 **  | 0.700 / 0.783    | 0.703 / 0.824 +  |
----------------------------------------------------------------------
| 1   | 10 | 0.525 / 0.615     | 0.682 / 0.787    | N/A              |
----------------------------------------------------------------------
| 2   | 10 | 0.564 / 0.623     | 0.701 / 0.795    | 0.705 / 0.824 +  |
----------------------------------------------------------------------
| 12  | 10 | 0.531 / 0.620     | 0.690 / 0.791    | N/A              |
----------------------------------------------------------------------
| 3x  | 10 | 0.547 / 0.618     | 0.699 / 0.789    | 0.708 / 0.820    |
----------------------------------------------------------------------
| 3   | 10 | 0.558 / 0.621 +   | 0.698 / 0.790    | 0.714 / 0.824 +  |
----------------------------------------------------------------------
| 123 | 10 | 0.540 / 0.620     | 0.668 / 0.795 +  | N/A              |
----------------------------------------------------------------------
| 4   | 10 | 0.497 / 0.532     | N/A              | N/A              |
----------------------------------------------------------------------
| 5   | 10 | 0.322 / 0.607     | 0.500 / 0.776    | 0.568 / 0.818    |
----------------------------------------------------------------------
| 6   | 10 | 0.539 / 0.588     | 0.687 / 0.746    | 0.682 / 0.773    |
----------------------------------------------------------------------
| 7   | 10 | 0.472 / 0.538     | 0.691 / 0.711    | 0.682 / 0.730    |
----------------------------------------------------------------------
| 0   | 2  | 0.582 / 0.628     | 0.741 / 0.782    | 0.757 / 0.820    |
----------------------------------------------------------------------
| 0   | 3  | 0.590 / 0.640 ++  | 0.735 / 0.785    | 0.767 / 0.821    |
----------------------------------------------------------------------
| 0   | 4  | 0.582 / 0.630     | 0.729 / 0.784    | 0.742 / 0.812    |
----------------------------------------------------------------------
| 0   | 5  | 0.574 / 0.633     | 0.717 / 0.786    | 0.741 / 0.803    |
----------------------------------------------------------------------
| 0   | 6  | 0.571 / 0.618     | 0.717 / 0.793 ++ | 0.745 / 0.807    |
----------------------------------------------------------------------
| 0   | 7  | 0.544 / 0.618     | 0.710 / 0.776    | 0.733 / 0.804    |
----------------------------------------------------------------------
| 0   | 8  | 0.506 / 0.606     | 0.707 / 0.780    | 0.721 / 0.808    |
----------------------------------------------------------------------
| 0   | 9  | 0.546 / 0.616     | 0.704 / 0.783    | 0.699 / 0.811    |
----------------------------------------------------------------------
| 0   | 10 | 0.566 / 0.620     | 0.700 / 0.783    | 0.703 / 0.824 ++ |
----------------------------------------------------------------------
| 0   | 12 | 0.567 / 0.614     | 0.689 / 0.774    | 0.717 / 0.821    |
----------------------------------------------------------------------
| 3   | 3  | 0.589 / 0.642 +++ | 0.720 / 0.795    | 0.756 / 0.824    |
----------------------------------------------------------------------
| 23  | 3  | -   / 0.631       | -   /   -        | -   / 0.819      |
----------------------------------------------------------------------
| 3   | 6  | -   /   -         | 0.710 / 0.796    | -   /   -        |
----------------------------------------------------------------------
| 23  | 6  | -   /   -         | 0.720 / 0.812    | -   /   -        |
----------------------------------------------------------------------
| 123 | 6  | -   /   -         | 0.717 / 0.793    | N/A              |
----------------------------------------------------------------------
| 23  | 10 | -   /   -         | -   /   -        | -   / 0.828      |
----------------------------------------------------------------------
| 3#  | 3  | -   / 0.640       | -   /   -        | -   /   -        |
----------------------------------------------------------------------
| 23# | 6  | -   /   -         | -   / 0.813 +++  | -   /   -        |
----------------------------------------------------------------------
| 23# | 10 | -   /   -         | -   /   -        | -    / 0.831 +++ |
----------------------------------------------------------------------

where +, ++, +++ represent the best performers in each progressive part

