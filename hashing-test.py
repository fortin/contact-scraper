import re
import os
import sys
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import pandas as pd

path = "/Users/antonio/pCloud Drive/My Documents/Linguistics/corpora/enron-email/maildir/arnold-j/sent"

NEWLINE = '\n'
hash_vectorizer = HashingVectorizer(n_features=4**6)
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
                past_header, lines = False, []
                with open(file_path, 'r', encoding="latin-1") as data:
                    for line in data:
                        if past_header:
                            data_set=str(data.read())
                            train_set.append(data_set)
                        elif line == NEWLINE:
                            past_header = True
        return train_set

corpus = read_files(path)
cv = CountVectorizer()
word_count_vector = cv.fit_transform(corpus)
count_vector=cv.transform(corpus)

# tfidf_transformer=TfidfTransformer(smooth_idf=False,use_idf=False)
transformer.fit(word_count_vector)
tf_idf_vector=transformer.transform(count_vector)
# B = hash_vectorizer.build_analyzer()
feature_names = cv.get_feature_names()
X = hash_vectorizer.fit_transform(corpus)

# print idf values - not hash but still
df_hash = pd.DataFrame(transformer.idf_,index=cv.get_feature_names(),columns=["hash_weights"])

# sort ascending
df_hash.sort_values(by=['hash_weights']).to_csv("hash.csv")
# print(B)
# print(X.toarray())
