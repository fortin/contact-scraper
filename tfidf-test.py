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

# aim: giant list of vectors
# x matrix like [ [1,3,2,45,3,34], [3,2,45,3,34,101], .... ]
# y matrix like [0 ,1, 1, 0 ,0 .....]
# TODO: 1 vector per email, tfidf'd with a vectorizer that has weights for the entire corpus
#

sig_path = "data/sig"
nosig_path = "data/nosig"

svc_clf = LinearSVC()
# cv = CountVectorizer()
tfidf_vectorizer = TfidfVectorizer()
# transformer = TfidfTransformer()
lr = LogisticRegression()

def read_files(path):
    train_set = []
    for root, dir_names, file_names in os.walk(path):
        for path in dir_names:
            read_files(os.path.join(root, path))
        for file_name in file_names:
            file_path = os.path.join(root, file_name)
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding="latin-1") as data:
                    data_set=str(data.read())
                    train_set.append(data_set)
    return train_set

sig_corpus = read_files(sig_path)
nosig_corpus = read_files(nosig_path)

# for each file loaded from /sig, append a 1 to y, and 0 from nosig
y = [1]*len(sig_corpus) + [0]*len(nosig_corpus)

corpus = sig_corpus + nosig_corpus

X = tfidf_vectorizer.fit_transform(corpus).todense()
lr.fit(X, y)
# svc_clf.fit(X, y)

scores = []

for k in range(10):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
    svc_clf.fit(X_train, y_train)
    # svc_clf.score(X_test, y_test) ###STORE THIS!!!
    scores.append(svc_clf.score(X_test, y_test))

print(sum(lr.predict(X)))

# print(scores)
# conf = confusion_matrix(y, lr.predict(X))
# print(conf)
# plt.imshow(conf, cmap='binary', interpolation='None')
# plt.show()
# print( f"{ np.mean(scores) } +/- {np.var(scores)}" )

# TODO: calculate confusion matrix

# set path to /sig, create corpus and set y to 1 * len(corpus)
# y = [1]*len(sig_corpus) + [0]*len(nosig_corpus)
# corpus = sig_corpus + nosig_corpus


# word_count_vector = cv.fit_transform(corpus)
#
# tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True)
# tfidf_transformer.fit(word_count_vector)

# count matrix
# count_vector=cv.transform(corpus)

# tf-idf scores
# tf_idf_vector=tfidf_transformer.transform(count_vector)

# first_document_vector=tf_idf_vector[0]
# feature_names = cv.get_feature_names()

#print the scores
# df = pd.DataFrame(first_document_vector.T.todense(), index=feature_names, columns=["tfidf"])
# df.sort_values(by=["tfidf"],ascending=False).to_csv("foo.csv")

# print idf values
# df_idf = pd.DataFrame(tfidf_transformer.idf_, index=cv.get_feature_names(),columns=["tf_idf_weights"])

# sort ascending
# df_idf.sort_values(by=['tf_idf_weights']).to_csv("bar.csv")
# print(word_count_vector.shape)
# print(tfidf_vectorizer.get_feature_names())
# print(X.toarray())
