# -*- coding: utf-8 -*-
# Data Analysis
import pandas as pd
import numpy as np
from sklearn.svm import SVC
import re
import string
from sklearn.preprocessing import LabelEncoder
from nltk import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import ADASYN

# loading data
df = pd.read_csv('/Users/rezaaar/Development/django-rest/mbti_be/ml_model/data1_1.csv')

# Text Processing
df['Indikator'] = df['Indikator'].str.lower()

# data cleansing

def data_clean(indikator) :
  #remove tab. new line, and back slice
  indikator = indikator.replace('\\t'," ").replace('\\n'," ").replace('\\u'," ").replace('\\',"")
  #remove non ASCII (emoticon,dll)
  indikator = indikator.encode('ascii', 'replace').decode('ascii')
  #remove mention, link, hashtag
  indikator = ' '.join(re.sub("([@#][A-Za-z0-9]+)|(\w+:\/\/\S+)"," ", indikator).split())
  #remove number
  indikator = re.sub(r"\d+", "", indikator)
  #remove punctuation
  indikator = indikator.translate(str.maketrans("","",string.punctuation))
  #remove whitespace leading & trailing
  indikator =  indikator.strip()
  #remove multiple white spacew into single white space
  indikator = re.sub('\s+', ' ', indikator)
  #remove single char
  indikator = re.sub(r"\b[a-zA-Z]\b", "", indikator)

  return indikator

df['Indikator_clean'] = df['Indikator'].apply(data_clean)
  #NLTK word tokenize
  
def word_tokenize_wrapper(indikator) :
  return word_tokenize(indikator)

df['Indikator_tokens'] = df['Indikator_clean'].apply(word_tokenize_wrapper)

normalizad_word = pd.read_csv("/Users/rezaaar/Development/django-rest/mbti_be/ml_model/normalisasi1.csv")

normalizad_word_dict = {}

for index, row in normalizad_word.iterrows():
  if row.iloc[0] not in normalizad_word_dict:
    normalizad_word_dict[row.iloc[0]] = row.iloc[1]

def normalized_term(document):
    return [normalizad_word_dict[term] if term in normalizad_word_dict else term for term in document]

df['Indikator_normalized'] = df['Indikator_tokens'].apply(normalized_term)

df['Indikator_normalized'].head()

stop_list = ["saya","akan","dan","dengan","yang","di","lalu","jika","secara"]

def stopword_removal (indikator):
  filtering = stop_list
  x = []
  data = []
  def my_func (x) :
    if x in filtering :
      return False
    else :
      return True

  fit = filter(my_func,indikator)
  for x in fit :
    data.append(x)
  return data

df['indikator_filter'] = df['Indikator_normalized'].apply(stopword_removal)

# Stemming

def stemming(indikator) :
  factory = StemmerFactory()
  stemmer = factory.create_stemmer()

  do = []
  for w in indikator :
    dt = stemmer.stem(w)
    do.append(dt)
  d_clean = " ".join(do)
  return d_clean

df['indikator_stemming'] = df['indikator_filter'].apply(stemming)

#tokenize data stemming
 #NLTK word tokenize
def stemmed_tokenizing(indikator) :
  return word_tokenize(indikator)

df['indikator_stemmed_tokens'] = df['indikator_stemming'].apply(stemmed_tokenizing)

"""# Feature extraction"""

# Feature extraction packages
# import sklearn

data_clean = df.astype({'Tipe' : 'category'})
data_clean = df.astype({'indikator_stemmed_tokens' : 'string'})


for idx in data_clean.index:
 if(len(data_clean["indikator_stemming"][idx]) == 0):
  data_clean = data_clean.drop(index=idx)

# Inisialisasi objek TfidfVectorizer
tfidf_vectorizer = TfidfVectorizer()

# Melakukan pembobotan TF-IDF pada kolom "indikator"
X = tfidf_vectorizer.fit_transform(data_clean['indikator_stemmed_tokens'])


# encoding label
enc = LabelEncoder()
data_clean['type of encoding'] = enc.fit_transform(data_clean['Tipe'])

y = data_clean['type of encoding']

"""# Splitting Data"""

if X.shape[0] != y.shape[0]:
  print("X and y rows are mismatched, check dataset again")

pd.DataFrame(X,y)

# Splitting data

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=12, shuffle=True)
"""# Predict Testing"""

list_indikator = np.array(data_clean['indikator_stemmed_tokens'])
list_tipe = np.array(data_clean['type of encoding'])

cntizer = CountVectorizer(analyzer="word",max_features=1000, min_df = 0.01)
X_cnt = cntizer.fit_transform(list_indikator)

tfizer = TfidfTransformer()
X_tfidf =  tfizer.fit_transform(X_cnt).toarray()

# Posts in tf-idf representation
X = X_tfidf

'''
dataset Baru
'''
# user_input = "berkenalan" #E
# user_input = "berkenalan" #E
# user_input = "Memikirkan terlebih dahulu/memastikan bahwa orang tersebut benar"" tidak berniat jahat" #I
# user_input = "mengajak berbicara" #E
user_input = "memastikan atau mengajak satu teman lagi untuk bertemu " #I

my_X_cnt = cntizer.transform(np.array([user_input]))
my_X_tfidf =  tfizer.transform(my_X_cnt).toarray()

result = []

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25,  stratify=y,random_state=12)

adasyn = ADASYN()  # Add this line to define the ADASYN object

X_train_adasyn, y_train_adasyn = adasyn.fit_resample(X_train, y_train)

model = SVC(C = 143, class_weight='balanced', gamma='auto', kernel='rbf')
model.fit(X_train_adasyn, y_train_adasyn)

y_pred = model.predict(my_X_tfidf)
result.append(y_pred[0])

if result == [0] :
  result_output = 'E'
else :
  result_output = 'I'

print(user_input)
print("The result is : ", result_output)

"""# Saving Model"""