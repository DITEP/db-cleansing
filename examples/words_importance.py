"""
This script is intended to show the usage of word2vec for
our use-case
"""
import pandas as pd
import matplotlib.pyplot as plt

from gensim.models import word2vec
from sklearn.manifold import TSNE
from preprocessing.text2vec.transformers import HTMLParser


path = '../data/reports.csv'

df = pd.read_csv(path, sep=';').head(1000)
parser = HTMLParser(strategy='tokens')
X = parser.transform(df)

w2v = word2vec.Word2Vec(X,
                        size=128,
                        window=8,
                        sample=0.1)


