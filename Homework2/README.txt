Name: Nina Baculinao
Uni: nb2406

COMS 4705 Natural Language Processing
Assignment 2 Readme

---------------------------------------------------------------------
1) Dependency Graphs
---------------------------------------------------------------------


---------------------------------------------------------------------
2) Manipulating Configurations
---------------------------------------------------------------------

Swedish:
This is not a very good feature extractor!
UAS: 0.229038040231
LAS: 0.125473013344

English:
This is not a very good feature extractor!
UAS: 0.0518518518519 
LAS: 0.0

Danish:
This is not a very good feature extractor!
UAS: 0.123552894212 
LAS: 0.00718562874251

Korean:
This is not a very good feature extractor!
UAS: 0.115488605639 
LAS: 0.0

After adding FORM, LEMMA, POSTAG, FEATS feature model:
Swedish:
UAS: 0.504879506074 
LAS: 0.364070902211
------
Swedish:
After adding the rest of the feature model:
UAS: 0.785301732723 
LAS: 0.6721768572

English:
UAS: 0.083950617284 
LAS: 0.0

Danish:
UAS: 0.0644710578842 
LAS: 0.0

Korean:
UAS: 0.115488605639 
LAS: 0.0
 Number of training examples : 200
 Number of valid (projective) examples : 200
Training support vector machine...
done!
UAS: 0.731942835071 
LAS: 0.598686751642
Danish:
 Number of training examples : 200
 Number of valid (projective) examples : 174
Training support vector machine...
done!
UAS: 0.79500998004 
LAS: 0.714371257485

after checking form of its head
UAS: 0.813173652695 
LAS: 0.732734530938
