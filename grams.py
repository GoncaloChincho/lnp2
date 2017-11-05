
# coding: utf-8

# In[1]:

import re
import nltk
from nltk import word_tokenize
from nltk.util import ngrams
from collections import Counter


# In[46]:

word = 'aposta'
if word == 'aposta':
    final_filename = 'apostaAnotado.final'
    unigrams_path = 'apostaUNIGRAMAS.txt'
    bigrams_path = 'apostaBIGRAMAS.txt'
else:
    final_filename = 'foremAnotado.final'
    unigrams_path = 'foremUNIGRAMAS.txt'
    bigrams_path = 'foremBIGRAMAS.txt'


# In[3]:

def list_uniq(list):
    uniq = []
    for el in list:
        if not el in uniq:
            uniq.append(el)
    return uniq


# In[113]:

#ngrams should be a dictionary -> {'the vaporwave': 50, 'kill jill': 542}
def ngrams_to_file(word,ngram_counts,n):
    if n == 1:
        filename = word + 'Unigramas.txt'
    elif n == 2:
        filename += word + 'Bigramas.txt' 
    else:
        return 'Bad n!'

    file = open(filename,'w')

    for ngram in ngram_counts:
        if n == 2:
            ngram_write = ngram[0] + ' ' + ngram[1]
        else:
            ngram_write = ngram
        
        file.write(ngram_write + '\t' + str(ngram_counts[ngram] + 1) + '\n')


# In[5]:

file = open(final_filename,'r')
text =(file.read()).lower()
text_words = nltk.word_tokenize(text)


# # Unigrams

# In[71]:

vocab = list_uniq(text_words)
vocab.append('<UNK>')
n_tokens = len(vocab)


# In[72]:

unigram_counts = Counter()


for token in vocab:
    unigram_counts[token] = 0

for text_word in text_words:
    unigram_counts[text_word] += 1


# In[114]:

ngrams_to_file(word,unigram_counts,1)


# # Bigrams

# In[61]:

bigrams = []
for i in range(len(vocab) - 1):
    bigrams.append((vocab[i],vocab[i]))
    for j in range(i + 1,len(vocab)):
        bigrams.append((vocab[i],vocab[j]))
        bigrams.append((vocab[j],vocab[i]))


# In[49]:

text_bigrams = list(ngrams(text_words,2))


# In[50]:

bigram_counts = Counter()

for bigram in bigrams:
    bigram_counts[bigram] = 0

for text_bigram in text_bigrams:
    bigram_counts[text_bigram] += 1


# In[115]:

ngrams_to_file(word,bigram_counts,2)


# In[56]:




# In[32]:




# In[16]:




# In[28]:




# In[33]:




# In[ ]:



