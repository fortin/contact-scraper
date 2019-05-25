import re
import os
import sys
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import csv

path = "/Users/antonio/pCloud Drive/My Documents/Linguistics/corpora/enron-email/maildir/arnold-j/sent"

cv = CountVectorizer(lowercase=True)
tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True)
tfidf_transformer.fit(word_count_vector)

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

# def build_data_frame(path, classification):
#     rows = []
#     index = []
#     for file_name, text in read_files(path):
#         rows.append({'text': text, 'class': classification})
#         index.append(file_name)
#
#     data_frame = DataFrame(rows, index=index)
#     return data_frame


corpus = read_files(path)

X = cv.fit_transform(corpus)

feature_names = cv.get_feature_names()
vectors = X.toarray()



#
# pd.DataFrame(vectors).to_csv("foo.csv")
