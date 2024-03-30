# -*- coding: utf-8 -*-
"""
Created on Sat Sep 30 15:03:49 2023

@author: jorda
"""

import nltk, re, numpy as np, pandas as pd

import string
from snowballstemmer import stemmer
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.dates
import os

from util import QURAN_CHAPTERS as titles

FIG_SIZE = (10, 15)

quran = pd.read_csv('quran-simple.txt', sep="|", header=None)
quran.columns = ['Surah', 'Ayah', 'Content']

#%%
quran.drop(quran.index[6236:], inplace=True)

stemmer_arabii = stemmer('arabic')

quran['Surah'] = pd.to_numeric(quran['Surah'], downcast = 'integer')
quran['Ayah'] = pd.to_numeric(quran['Ayah'], downcast = 'integer')
#%%
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

surah_ayat = quran.groupby('Surah')['Content'].apply(list).tolist()
surahs = [' '.join(surah) for surah in surah_ayat]
surah_tokens = [s.split(' ') for s in surahs]

def remove_tashkeel(text):
    # Define a regular expression pattern to match diacritics
    pattern = re.compile('[\u0617-\u061A\u064B-\u0652]')
    
    # Use the sub() method to replace matched diacritics with an empty string
    text = re.sub(pattern, '', text)
    
    return text

ayahs_no_tash = [remove_tashkeel(a) for s in surah_ayat for a in s]

surahs_no_tash = list(map(remove_tashkeel, surahs))
no_tash_tokens = [x.split(' ') for x in surahs_no_tash]

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

def surah_dictionary(ayah, return_dict = False):
    result = {}
    for word in ayah:
        if word in result:
            result[word] += 1
        else:
            result[word] = 1
            
    if return_dict:
        return result
    return [(word, count) for count, word in result.items()]


def freqdist(word_dict, title):

    fig = plt.figure(3, FIG_SIZE)
    plt.gcf().subplots_adjust(bottom=0.15) # to avoid x-ticks cut-off
    fdist = nltk.FreqDist(word_dict)
    fdist.plot(20, cumulative=False, title=f'{title} FreqDist', show=False)

    fig.savefig(f'static/figures/{title}FreqDist.png', bbox_inches = "tight")
    plt.clf()
    
    return fig

word_freq = [surah_dictionary(surah, False) for surah in no_tash_tokens]

def surahsFrequencyPlots(surah_tokens):    
    for idx, surah in enumerate(surah_tokens):
        freqdist(surah, titles[idx])
    

stemmed = [stemmer_arabii.stemWords(surah) for surah in no_tash_tokens]
stemmed_surahs = [" ".join(surah) for surah in stemmed]
quran_dict = word_dictionary(stemmed)

df_surahs = pd.DataFrame({'Chapter': titles,
                          'noTashkeel': surahs_no_tash,
                          'normal': surahs,
                          'stemmer': stemmed})


def root_search(word, quran):
    pattern = re.compile(r'\b\w*{}\w*\b'.format(re.escape(word)))
    
    # Find all matches in the text
    matches = pattern.findall(quran)
    
    return matches
    


def root_dictionary(word, quran):
    matches = root_search(word, quran)
    
    result = {}
    for word in matches:
        if word in result:
            result[word] += 1
        else:
            result[word] = 1
    return result
#%%   
def find_and_label_root(word, quran):
    filtered_instances = []
    for no, surah in enumerate(quran, start=1):  
        print(no, surah)
        for verse_num, verse in enumerate(surah, start=1):
            pattern = re.compile(r'\b\w*{}\w*\b'.format(re.escape(word)))
            matches = pattern.findall(verse)

            for match in matches:
                filtered_instances.append((no, verse_num, match))
    return filtered_instances


    