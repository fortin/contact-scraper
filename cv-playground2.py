import re
import os
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

sig_path = "data/sig"
nosig_path = "data/nosig"

sig_test_path = "data/sig_test"
nosig_test_path = "data/nosig_test"

cv = CountVectorizer()

def read_files(path):
    result = {}
    for root, dir_names, file_names in os.walk(path):
        for path in dir_names:
            read_files(os.path.join(root, path))
        for file_name in file_names:
            file_path = os.path.join(root, file_name)
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding='latin-1') as data:
                    result[file_name.split('.')[0]] = data.readlines()
    return result

def createfeats(x):

sig_corpus = read_files(sig_path)
nosig_corpus = read_files(nosig_path)

# print(sig_corpus)
# print(type(sig_corpus))
# print(nosig_corpus)
# print(type(nosig_corpus))
# sys.exit()
sig_test_corpus = read_files(sig_test_path)
nosig_test_corpus = read_files(nosig_test_path)

# corpus = {**sig_corpus, **nosig_corpus}
# print(corpus)
# sys.exit()
corpus = {**sig_test_corpus, **nosig_test_corpus}

result = []

for email in list(corpus.values()):
    df = pd.DataFrame(columns=['line'])
    email = [x.replace("\n", "") for x in email]
    email = [x.replace("\t", "") for x in email]
    for line in email:
        df = df.append({'line': line}, ignore_index=True)
    result.append(df)


# So in the detect step
# Ie what we are now doing
# We need to convert each email to a features df
# Prior to the concat
# So....
# To do that
# Create a function
# Which turns any single email df
# Into the features df
# Call it createfeats or something
# Then use [createfeats(x) for x in blah]
# Where blah is the list of the email df
# (I forgot the name, should be obvious)
# (exactly the things we were concat-ing just now)

print(result[1])
sys.exit()

all_rows = pd.concat(result)
# print(all_rows)
# sys.exit()

cv.fit(all_rows.values.ravel())

def row_cv(x):
    return pd.Series(np.array(cv.transform([x['line']]).todense())[0])

# email0 = result[0]

q = result[1].apply(row_cv, result_type='expand', axis=1)

r = q.rolling(4, center=True).sum()
print(r)

feats = [createfeats(x) for x in result]
