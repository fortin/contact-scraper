
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
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.decomposition import PCA, KernelPCA


sig_path = "data/sig"
nosig_path = "data/nosig"


# cv = CountVectorizer()
tfidf_vectorizer = TfidfVectorizer()
# transformer = TfidfTransformer()
svc_clf = LinearSVC()
lr = LogisticRegression()
svc = SVC(gamma='scale')
rf = RandomForestClassifier()
gnb = GaussianNB()
qda = QuadraticDiscriminantAnalysis()
ab = AdaBoostClassifier()
mlp = MLPClassifier(hidden_layer_sizes=(10000, 10000, 10000, 10000), solver='adam', activation='relu', learning_rate='constant')
kn = KNeighborsClassifier()
gauss = GaussianProcessClassifier()
pca = PCA(n_components=1000)
kpca = KernelPCA(kernel="rbf", fit_inverse_transform=True, gamma=10)



def read_files(path):
    # train_set = []
    for root, dir_names, file_names in os.walk(path):
        for path in dir_names:
            read_files(os.path.join(root, path))
        for file_name in file_names:
            file_path = os.path.join(root, file_name)
            if os.path.isfile(file_path):
                df = {}
                with open(file_path, 'r', encoding="latin-1") as data:
                    df[file_name[:-4]] = pd.read_csv(data, sep="\n", encoding='utf-8')
                    df = pd.DataFrame.to_dense(df)
                    # df
                    # data_set=str(data.read())
                    print(df)                # train_set.append(data_set)
    return df

sig_corpus = read_files(sig_path)
nosig_corpus = read_files(nosig_path)

# for each file loaded from /sig, append a 1 to y, and 0 from nosig
# y = [1]*len(sig_corpus) + [0]*len(nosig_corpus)
#
# corpus = sig_corpus + nosig_corpus
#
# X = tfidf_vectorizer.fit_transform(corpus).todense()
# print(X.shape)

# lr.fit(X, y)
# svc_clf.fit(X, y)
# svc.fit(X, y)
# rf.fit(X, y)
# gnb.fit(X, y)
# ab.fit(X, y)
# qda.fit(X, y)
# ab.fit(X, y)
mlp.fit(X, y)
# kn.fit(X, y)
# gauss.fit(X, y)
# scores = []
#
# X_kpca = kpca.fit_transform(X)
# X_back = kpca.inverse_transform(X_kpca)
# X_pca = pca.fit_transform(X)
#
# for k in range(10):
#     X_train, X_test, y_train, y_test = train_test_split(X_back, y, test_size=0.33)
#     mlp.fit(X_train, y_train)
    # svc_clf.score(X_test, y_test) ###STORE THIS!!!
    # scores.append(mlp.score(X_test, y_test))

# dfPCA = pd.DataFrame(X, y)
# print(sum(lr.predict(X)))

# print(scores)
# conf = confusion_matrix(y, mlp.predict(X_back))
# pca_conf = confusion_matrix(y, mlp.predict(X_pca))
# print(conf)
# print(pca_conf)
# plt.imshow(conf, cmap='binary', interpolation='None')
# plt.show()
# print( f"{ np.mean(scores) } +/- {np.var(scores)}" )
# pca.fit_transform(dfPCA)

# plt.plot(pca.explained_variance_ratio_)
# plt.show()
# print(kpca.explained_variance_ratio_)
# print(kpca.singular_values_)
# print(pca.explained_variance_ratio_)
# print(pca.singular_values_)


# df = pd.DataFrame(pca.components_, columns=list(dfPCA.columns))
#
# df = df[0:4].to_csv('pca_dump.csv')


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
