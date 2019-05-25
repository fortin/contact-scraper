import re
import os
import sys
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import pandas as pd
import csv

path = "/Users/antonio/pCloud Drive/My Documents/Linguistics/corpora/enron-email/maildir/skilling-j/sent"

cv = CountVectorizer()
tfidf_vectorizer = TfidfVectorizer()
# transformer = TfidfTransformer()

def read_files(path):
    # TODO skip headers?
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

corpus = read_files(path)
# X = tfidf_vectorizer.fit_transform(corpus)
# this step generates word counts for the words in your docs

word_count_vector = cv.fit_transform(corpus)

tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True)
tfidf_transformer.fit(word_count_vector)

# count matrix
count_vector=cv.transform(corpus)

# tf-idf scores
tf_idf_vector=tfidf_transformer.transform(count_vector)

first_document_vector=tf_idf_vector[0]
feature_names = cv.get_feature_names()

#print the scores
df = pd.DataFrame(first_document_vector.T.todense(), index=feature_names, columns=["tfidf"])
df.sort_values(by=["tfidf"],ascending=False).to_csv("foo.csv")

# print idf values
df_idf = pd.DataFrame(tfidf_transformer.idf_, index=cv.get_feature_names(),columns=["tf_idf_weights"])

# sort ascending
df_idf.sort_values(by=['tf_idf_weights']).to_csv("bar.csv")
# print(word_count_vector.shape)
# print(tfidf_vectorizer.get_feature_names())
# print(X.toarray())
