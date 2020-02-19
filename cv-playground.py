import re
import os
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import email
from names_dataset import NameDataset

sig_path = "data/sig"
nosig_path = "data/nosig"

sig_test_path = "data/sig_test"
nosig_test_path = "data/nosig_test"

# cv = CountVectorizer()
m = NameDataset()

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

def body_extractor(path):
    """
    Extract body of email message from file.
    """
    # result = {}
    result = ""
    for root, dir_names, file_names in os.walk(path):
        for path in dir_names:
            read_files(os.path.join(root, path))
        for file_name in file_names:
            file_path = os.path.join(root, file_name)
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding='latin-1') as data:
                    result = data.read()
    msg = email.message_from_string(str_cleaner(result))
    body = ''
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))

        # skip any text/plain (txt) attachments
            if ctype == 'text/plain' or ctype == 'text/html' and 'attachment' not in cdispo:
                body = part.get_payload(decode=True) # decode
                break
    # not multipart - i.e. plain text, no attachments
    else:
        body = msg.get_payload(decode=True)
    # strip HTML and remove \r, \t, \n
    body = re.sub('<[^<]+?>', '', str(body)).replace('\\r', '\r').replace('\\n', '\n').replace('\\t', '')
    # is there a more general, additive way to do this?
    return(body)

def is_title(x):
    x = " ".join(x.casefold().strip().split())
    return x in job_titles['Job Title'].values

def is_title_sen(x):
    # loop through bigrams looking for job title
    bigram_vectorizer = CountVectorizer(ngram_range=(1, 3),
                                    token_pattern=r'\b\w+\b', min_df=1)
    analyze = bigram_vectorizer.build_analyzer()
    # print(sum(list(map(is_title, analyze(x)))))
    # print(analyze(x))# >= 1)
    return sum(list(map(is_title, analyze(x)))) >= 1

def is_first_name(x):
    x = " ".join(x.casefold().strip().split())
    # print(x)
    return x in first_names['First Name'].values

def is_first_name_sen(x):
    bigram_vectorizer = CountVectorizer(ngram_range=(1, 2),
                                    token_pattern=r'\b\w+\b', min_df=1)
    analyze = bigram_vectorizer.build_analyzer()
    # print(x + ': ' + str_cleaner(list(map(is_title, analyze(x)))))
    # print(analyze(x))# >= 1)
    return sum(list(map(is_first_name, analyze(x)))) >= 1

def is_last_name(x):
    x = " ".join(x.casefold().strip().split())
    return x in last_names['Last Name'].values

def is_last_name_sen(x):
    bigram_vectorizer = CountVectorizer(ngram_range=(1, 2),
                                    token_pattern=r'\b\w+\b', min_df=1)
    analyze = bigram_vectorizer.build_analyzer()
    print(x + ': ' + str_cleaner(list(map(is_title, analyze(x)))))
    # print(analyze(x))# >= 1)
    return sum(list(map(is_last_name, analyze(x)))) >= 1

sig_corpus = read_files(sig_path)
nosig_corpus = read_files(nosig_path)

first_names = pd.read_csv("/Users/antonio/miniconda3/envs/contact-scraper/lib/python3.7/site-packages/names_dataset/first_names.all.txt")

last_names = pd.read_csv("/Users/antonio/miniconda3/envs/contact-scraper/lib/python3.7/site-packages/names_dataset/last_names.all.txt")

job_titles = pd.read_csv('data/job_title_dictionary2.txt', encoding='latin-1')
sig_test_corpus = read_files(sig_test_path)
# nosig_test_corpus = read_files(nosig_test_path)
job_titles['Job Title'] = job_titles['Job Title'].apply(lambda x: x.casefold())

def str_cleaner(x):
    x = re.sub(r'[^@. a-zA-Z]', '', str(x))
    return x
# y = [1]*len(sig_corpus) + [0]*len(nosig_corpus)

# cv = CountVectorizer()
# tfidf_vectorizer = TfidfVectorizer()
#
# corpus = [sig_corpus, nosig_corpus]
# print(corpus)
# sys.exit()


# for line in body_extractor(sig_path):
#     for x in line:
#         cor = is_title(x)
#     print(cor)

# cor = [is_title_sen(line) for line in str_cleaner(corpus)]
# print(cor)

stc = str_cleaner(sig_test_corpus).split()
fname = [is_first_name_sen(line) for line in stc]
# name = [is_first_name_sen(line) for line in stc]
# print(name)
#
sys.exit()
# nm = m.search_last_name(line)
# print(line + ': ' + nm)

# print(is_title_sen(str(corpus)))
# print(is_title_sen('scary Monster'))
# print(is_title_sen('  TeAchEr   '))
# print(is_title_sen('Data     SCientist'))
#
# print(is_title_sen(body_extractor(my_file3)))
#
# print(is_title_sen('Ich    werde ein 3d scheisse'))
# print(is_title_sen('I am a      Data     scientist     '))
# print(is_title_sen('Calligrapher'))

# corpus = [sig_test_corpus, nosig_test_corpus]
# sys.exit()

result = []

for email in corpus:
    df = pd.DataFrame(columns=['line'])
    email = [x.replace("\n", "") for x in email]
    email = [x.replace("\t", "") for x in email]
    for line in email:
        df = df.append({'line': line}, ignore_index=True)
    result.append(df)

# cor = [line for line in email for email in corpus ]
# print(cor)
# all_rows = pd.concat([result[0], result[1]])
# print(result[1])

y = [1]*len(sig_corpus) + [0]*len(nosig_corpus)
# print(len(all_rows))
# print(len(y))
# sys.exit()

# corpus = sig_corpus + nosig_corpus
#
X = tfidf_vectorizer.fit_transform(corpus).todense()
#
cv.fit(X, y)

cv.fit(all_rows.values.ravel(), y)

# df of all features X
# df of all labels y
# if they are of the same length, fit(X, y) will work

def row_cv(x):
    print(pd.Series(np.array(cv.transform([x['line']]).todense())[0]))
    return 0 #pd.Series(np.array(cv.transform([x['line']]).todense())[0])


sig = result[0]
nosig =result[1]

q = sig.apply(row_cv, result_type='expand', axis=1)
r = nosig.apply(row_cv, result_type='expand', axis=1)
#
# v = q.rolling(4, center=True).sum()
# w = r.rolling(4, center=True).sum()
#
# print(v)
# print(w)
