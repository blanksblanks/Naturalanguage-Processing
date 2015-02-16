Name: Nina Baculinao
Uni: nb2406

COMS 4705 Natural Language Processing
Assignment 1 Readme

Runtime information

nb2406@delhi:~/hidden/5281122421/Homework1$ time python solutionsA.py

real  0m53.909s
user  0m50.939s
sys 0m0.308s

real  7m5.337s
user  7m1.430s
sys 0m0.288s`:

nb2406@paris:~/hidden/5281122421/Homework1$ python perplexity.py A2.uni.txt
Brown_train.txt
The perplexity is 1104.83292814
nb2406@paris:~/hidden/5281122421/Homework1$ python perplexity.py A2.bi.txt
Brown_train.txt
The perplexity is 57.2215464238
nb2406@paris:~/hidden/5281122421/Homework1$ python perplexity.py A2.tri.txt
Brown_train.txt
The perplexity is 5.89521267642
nb2406@paris:~/hidden/5281122421/Homework1$ python perplexity.py A3.txt
Brown_train.txt
The perplexity is 13.0759217039

A 5)
nb2406@sofia:~/hidden/5281122421/Homework1$ python perplexity.py
Sample1_scored.txt Sample1.txt
The perplexity is 11.6492786046
nb2406@sofia:~/hidden/5281122421/Homework1$ python perplexity.py
Sample2_scored.txt Sample2.txt
The perplexity is 1611241155.03

perf(solutionsB.py): reduce runtime avg ~26 to 1m26 (more)
 - by removing python's built-in count method and writing own
  - fix: double 'STOP' production in replace_rare method so words match tag
    indices
     - feat: accurately calculate emission probabilities

5B:
real  12m29.693s
user  4m12.736s
sys 0m16.577s
nb2406@tokyo:~/hidden/5281122421/Homework1$ python pos B5.txt
Brown_tagged_dev.txt
python: can't open file 'pos': [Errno 2] No such file or directory
nb2406@tokyo:~/hidden/5281122421/Homework1$ python pos.py B5.txt
Brown_tagged_dev.txt
Percent correct tags: 93.6921615938
