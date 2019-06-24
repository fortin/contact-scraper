
import re
import os
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.decomposition import PCA, KernelPCA
from email.parser import HeaderParser
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.decomposition import PCA, KernelPCA
from email.parser import HeaderParser


sig_path = "data/sig"
nosig_path = "data/nosig"

sig_test_path = "data/sig_test"
nosig_test_path = "data/nosig_test"

# cv = CountVectorizer()
# tfidf_vectorizer = TfidfVectorizer()
# tfidf_vectorizer = TfidfVectorizer()
# transformer = TfidfTransformer()
# svc_clf = LinearSVC()
# lr = LogisticRegression()
# svc = SVC(gamma='scale')
# rf = RandomForestClassifier()
# gnb = GaussianNB()
# qda = QuadraticDiscriminantAnalysis()
# ab = AdaBoostClassifier()
# mlp = MLPClassifier(hidden_layer_sizes=(10000, 10000, 10000, 10000), solver='adam', activation='relu', learning_rate='constant')
# kn = KNeighborsClassifier()
# gauss = GaussianProcessClassifier()
# pca = PCA(n_components=1000)
# kpca = KernelPCA(kernel="rbf", fit_inverse_transform=True, gamma=10)

# svc_clf = LinearSVC()
# lr = LogisticRegression()
# svc = SVC(gamma='scale')
# rf = RandomForestClassifier()
# gnb = GaussianNB()
# qda = QuadraticDiscriminantAnalysis()
# ab = AdaBoostClassifier()
# mlp = MLPClassifier(hidden_layer_sizes=(10000, 10000, 10000, 10000), solver='adam', activation='relu', learning_rate='constant')
# kn = KNeighborsClassifier()
# gauss = GaussianProcessClassifier()
# pca = PCA(n_components=1000)
# kpca = KernelPCA(kernel="rbf", fit_inverse_transform=True, gamma=10)
#


def read_files(path):
    # train_set = []
    result = {}
    for root, dir_names, file_names in os.walk(path):
        for path in dir_names:
            read_files(os.path.join(root, path))
        for file_name in file_names:
            file_path = os.path.join(root, file_name)
            if os.path.isfile(file_path):
                # df = {}
                # with open(file_path, 'r', encoding="latin-1") as data:
                #     df[file_name[:-4]] = pd.read_csv(data, sep="\n", encoding='utf-8')
                #     df = pd.DataFrame.to_dense(df)
                #     # df
                #     # data_set=str(data.read())
                #     print(df)                # train_set.append(data_set)
                # df = pd.DataFrame()
                with open(file_path, 'r', encoding='latin-1') as data:
                    result[file_name.split('.')[0]] = data.readlines()
    return result

def hit_word_feature(df, w, r):
    # df[f'{w}_feat'] = df[['line']].apply( lambda x: w in x['line'] )
    df[f'{w}_feat'] = df['line'].apply( lambda x: w in x )
    df[f'{w}_feat'] = df[f'{w}_feat'].rolling(r).sum().fillna(0).astype(bool)
    return df

def process_files(d):
    result = {}
    for k, v in d.items():
        df = pd.DataFrame()
        parser = HeaderParser()
        v = [x.replace("\n", "") for x in v]
        # v = [[x] for x in ",".join(str(x) for x in v).split("': ')]
        # v['From: '.split('From: ')[0]] = v
        print(v)
        sys.exit()
        h = parser.parsestr(v)
        from_header = h['From:']
        for line in v:
            df = df.append({'line': line}, ignore_index=True)
        df = hit_word_feature(df, from_header, 3)
        result[file_name.split('.')[0]] = df
    return(result)

# sig_corpus = process_files(read_files(sig_path))
# nosig_corpus = process_files(read_files(nosig_path))

# def from_extractor(df):
#     df['From'] = df['line'].str.extract("From: (.+?)\n")
#     return df['From'].dropna()

# sig_corpus = read_files(sig_path)
# nosig_corpus = read_files(nosig_path)

sig_test_corpus = process_files(read_files(sig_test_path))
# nosig_test_corpus = read_files(nosig_test_path)

# corpus = sig_corpus + nosig_corpus
print(type(sig_test_corpus))
# pat = '\n\n'
# hit_words = ('\n')
# email = '/Users/antonio/Documents/Dropbox/Code/Python/Contact-Scraper/data/dasovich-j/dasovich-j-246.txt'
#
# with open(email, 'r') as f:
# print(h.items())
#
#
sys.exit()


# f = from_extractor(list(sig_test_corpus.values())[0])
# f = f.to_string(index=False, header=False)
#
# from_info = dict()
#
# for line in f:
#     from_info[f] = line
#
# print(from_info)
# print(sig_test_corpus.values[0])
# print(hit_word_feature(list(sig_test_corpus.values())[0], hit_words, 3))

# for line in f:
    # print(line)
# for h in hit_words:


# for each file loaded from /sig, append a 1 to y, and 0 from nosig
# y = [1]*len(sig_corpus) + [0]*len(nosig_corpus)
#
# corpus = sig_corpus + nosig_corpus
#
# X = tfidf_vectorizer.fit_transform(corpus).todense()
#
