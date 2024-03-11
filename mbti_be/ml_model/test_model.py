# diimport dulu terrr semua depedencies nya terr
import pandas as pd
# import pickle as pkl
# prepro depedencies
import re
import string
from sklearn.preprocessing import LabelEncoder
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.tokenize import word_tokenize
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
# data cleansing
# Import word_tokennize & FreqDist from NLTK
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
# Feature extraction packages


from sklearn.feature_extraction.text import TfidfVectorizer
# model algorithm
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from imblearn.over_sampling import ADASYN
from imblearn.over_sampling import ADASYN

# load data
data = pd.read_csv('/Users/rezaaar/Development/django-rest/mbti_be/ml_model/data1_1.csv')

# preprocessing the data -> cleanse the data & convert feature dtype as a vector/numbers yagesya biar bisa dipahami sama mesinnya brok.
data['Indikator'] = data['Indikator'].str.lower()
pd.DataFrame(data['Indikator'])

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
data['Indikator_clean'] = data['Indikator'].apply(data_clean)
  #NLTK word tokenize
def word_tokenize_wrapper(indikator) :
  return word_tokenize(indikator)

data['Indikator_tokens'] = data['Indikator_clean'].apply(word_tokenize_wrapper)

normalizad_word = pd.read_csv("/Users/rezaaar/Development/django-rest/mbti_be/ml_model/normalisasi1.csv")

normalizad_word_dict = {}

for index, row in normalizad_word.iterrows():
    if row[0] not in normalizad_word_dict:
        normalizad_word_dict[row[0]] = row[1]

def normalized_term(document):
    return [normalizad_word_dict[term] if term in normalizad_word_dict else term for term in document]

data['Indikator_normalized'] = data['Indikator_tokens'].apply(normalized_term)

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

data['indikator_filter'] = data['Indikator_normalized'].apply(stopword_removal)

# Stemming
def stemming(indikator) :
  factory = StemmerFactory()
  stemmer = factory.create_stemmer()

  do = []
  for w in indikator :
    dt = stemmer.stem(w)
    do.append(dt)

  data_clean = []
  d_clean = " ".join(do)
  return d_clean

data['indikator_stemming'] = data['indikator_filter'].apply(stemming)

#tokenize data stemming - NLTK word tokenize
def stemmed_tokenizing(indikator) :
  return word_tokenize(indikator)

data['indikator_stemmed_tokens'] = data['indikator_stemming'].apply(stemmed_tokenizing)

# Vectorize
data_clean = data.astype({'Tipe' : 'category'})
data_clean = data.astype({'indikator_stemmed_tokens' : 'string'})
# Inisialisasi objek TfidfVectorizer
tfidf_vectorizer = TfidfVectorizer()
# Melakukan pembobotan TF-IDF pada kolom "indikator"
X = tfidf_vectorizer.fit_transform(data_clean['indikator_stemmed_tokens'])
# encoding label
enc = LabelEncoder()
data_clean['type of encoding'] = enc.fit_transform(data_clean['Tipe'])
y = data_clean['type of encoding']

# Modeling
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25,  stratify=y,random_state=12)
adasyn = ADASYN(sampling_strategy = 'minority', n_neighbors = 5)
X_train_adasyn, y_train_adasyn = adasyn.fit_resample(X_train, y_train)
model = SVC(C = 143, class_weight='balanced', gamma='auto', kernel='rbf')
model.fit(X_train_adasyn, y_train_adasyn)