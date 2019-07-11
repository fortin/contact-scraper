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
                    raw_emails = data.readlines()
        return raw_emails

sig_corpus = read_files(sig_path)
nosig_corpus = read_files(nosig_path)

# sig_test_corpus = read_files(sig_test_path)
# nosig_test_corpus = read_files(nosig_test_path)

corpus = [sig_corpus, nosig_corpus]

# corpus = [sig_test_corpus, nosig_test_corpus]

result = []

for email in corpus:
    df = pd.DataFrame(columns=['line'])
    email = [x.replace("\n", "") for x in email]
    email = [x.replace("\t", "") for x in email]
    for line in email:
        df = df.append({'line': line}, ignore_index=True)
    result.append(df)

all_rows = pd.concat([result[0], result[1]])

cv.fit(all_rows.values.ravel())

def row_cv(x):
    return pd.Series(np.array(cv.transform([x['line']]).todense())[0])

email0 = result[0]

q = email0.apply(row_cv, result_type='expand', axis=1)

r = q.rolling(4, center=True).sum()
print(r)
