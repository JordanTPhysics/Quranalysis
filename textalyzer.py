# -*- coding: utf-8 -*-
"""
Created on Sat Sep 30 15:03:49 2023

@author: jorda
"""

import nltk, re, numpy as np, pandas as pd
from nltk.tokenize import word_tokenize as wt#, sent_tokenize as st

import gensim
import string
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
import gensim.corpora
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.dates

import os

quran = pd.read_csv('quran-simple.txt', sep="|", header=None)
quran.columns = ['Surah', 'Ayah', 'Content']

quran.drop(quran.index[6236:], inplace=True)

quran['Surah'] = pd.to_numeric(quran['Surah'], downcast = 'integer')

quran['Ayah'] = pd.to_numeric(quran['Ayah'], downcast = 'integer')


def unique_words(sura, neg=0):
    if neg==0:
        selection = quran[quran['Surah']==sura].Content.str.split().tolist()
    else:
        selection = quran[quran['Surah']!=sura].Content.str.split().tolist()
    flat_list = [item for aya in selection for item in aya]
    return set(flat_list)

#this function uses the above one to find words only used in this surah
def unique(sura):
    return (sorted(list(set(unique_words(sura))-set(unique_words(sura,1)))))

surahs = quran.groupby('Surah')['Content'].apply(list).tolist()

surah_tokenized = [wt(" ".join(x)) for x in surahs]

#takes a 2d list of chapters and tokenized words, returns a dict of each word frequency
def word_dictionary(book):
    result = {}
    for chapter in book:
        for word in chapter:
            if word in result:
                result[word] += 1
            else:
                result[word] = 1
                
    return result

word_frequency = word_dictionary(surah_tokenized)

sorted_words = dict(sorted(word_frequency.items(),
                           key=lambda item: item[1],
                           reverse=True))

words, frequencies = sorted_words.items()

# Create a bar chart
plt.bar(words, frequencies)
plt.xlabel('Words')
plt.ylabel('Frequencies')
plt.title('Word Frequencies')

# Rotate x-axis labels for better readability (optional)
plt.xticks(rotation=45)

# Show the plot
plt.tight_layout()  # Ensures labels are not cut off
plt.show()





