import re
import os
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

path = "/Users/antonio/pCloud Drive/My Documents/Linguistics/corpora/enron-email/maildir/arnold-j/sent"

tfidf_vectorizer = TfidfVectorizer()
transformer = TfidfTransformer()

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
X = tfidf_vectorizer.fit_transform(corpus)

print(tfidf_vectorizer.get_feature_names())
print(X.toarray())
