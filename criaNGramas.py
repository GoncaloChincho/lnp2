
# coding: utf-8

# In[19]:

import re
import nltk
from nltk import word_tokenize
from nltk.util import ngrams
from collections import Counter


# In[49]:

word = 'aposta'
if word == 'aposta':
    folder = 'apostaStuff\\'
    final_filename = folder + 'apostaAnotado.final'
else:
    folder = 'foremIrSerStuff\\'
    final_filename = folder + 'foremAnotado.final'


# In[21]:

def list_uniq(list):
    uniq = []
    for el in list:
        if not el in uniq:
            uniq.append(el)
    return uniq


# In[52]:

#ngrams should be a dictionary -> {'the vaporwave': 0.43241, 'kill jill': 0.12313}
def ngrams_to_file(word,ngrams,n):
    print(word)
    if word == 'aposta':
        filename = 'apostaStuff\\aposta'
    else:
        filename = 'foremIrSerStuff\\forem'
        
    if n == 1:
        filename += 'Unigramas.txt'
    elif n == 2:
        filename += 'Bigramas.txt'
        
    else:
        return 'Bad n!'
    file = open(filename,'w')
    for ngram in ngrams:
        file.write(ngram + '\t' + str(ngrams[ngram]) + '\n')


# In[23]:

file = open(final_filename,'r')
text =(file.read()).lower()
text_words = nltk.word_tokenize(text)


# # Unigrams

# In[24]:

tokens = list_uniq(text_words)
n_tokens = len(tokens)


# In[45]:

unigram_counts = {}
unigram_probs = {}

for token in tokens:
    unigram_counts[token] = 0
    unigram_probs[token] = 0

for wordy in text_words:
    unigram_counts[wordy] += 1

for unigram in unigram_counts:
    unigram_probs[unigram] = unigram_counts[unigram]/n_tokens


# In[53]:

ngrams_to_file(word,unigram_probs,1)


# # Bigrams

# In[97]:

bigrams = ngrams(text_words,2)


# In[103]:

(bigrams)


# In[ ]:



