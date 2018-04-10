import pickle
from collections import Counter

import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import pandas as pd

OMIT = {"matplotlib", "Python", "Matplotlib", "python", "mac", "windows"}.union(set(stopwords.words('english')))

def dictionary(words):
    wordset = set(words)
    return {w:i for i, w in enumerate(words)}

def freq_dictionary(words, topn=1000):
    freqs = Counter(words)
    return {w[0]:(i,w[1]) for i, w in enumerate(freqs.most_common(topn))}
    
def stem(sentences):
    ps = PorterStemmer()
    for s in sentences:
        tokens = nltk.word_tokenize(" ".join(s))
        yield [ps.stem(w) for w in tokens if ps.stem(w) not in OMIT]
def sentence_extract(f):
    """
    Extract list of sentences as strings from SO csv
    Returns list of non-stop NOUNS
    """
    df = pd.read_csv(f)
    sentences = list(df['Title'])
    print(len(sentences))

    sentences_clean = []
    count = 0
    for s in sentences:
        count += 1
        print(f"reading {count}")
        # function to test if something is a noun
        tokenized = nltk.word_tokenize(s)
        is_noun = lambda pos: pos[:2] == 'NN'
        # do the nlp stuff
        nouns = [word.lower() for (word, pos) in nltk.pos_tag(tokenized) if\
            is_noun(pos) and word not in OMIT]
        sentences_clean.append(nouns)
    return sentences_clean

if __name__ == "__main__":
    sentences = sentence_extract("Data/stackoverflow.csv")
    print(len(sentences))
    # pickle.dump(sentences, open("sentences_clean.pickle", "wb"))
    # sentences = pickle.load(open("sentences_clean.pickle", "rb"))
    # print(sentences)
    # stemmed = stem(sentences)
    # words = [word for s in sentences for word in s]
    # freq_dic = freq_dictionary(words, topn=2000)
    # pickle.dump(freq_dic, open("freq_dict_2000.pickle", "wb"))
    # # pass
