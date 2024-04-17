import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np

X = joblib.load('/Users/rezaaar/Development/django-rest/mbti_be/ml_model/X_P1.sav') 
y = joblib.load('/Users/rezaaar/Development/django-rest/mbti_be/ml_model/y_P1.sav')

cntizer = CountVectorizer(analyzer="word",max_features=1000, min_df = 0.01)
X_cnt = cntizer.fit_transform(X)

tfizer = TfidfTransformer()
X_tfidf =  tfizer.fit_transform(X_cnt).toarray()
X = X_tfidf

'''
Dataset Baru
'''
# user_input = "mendengar dan memahami" #S
# user_input = "memahami apa yang dibicarakan " #S
# user_input = "Berusaha mengerti apa yg disampaikan dan memahami maksud dr informasi yg diberikan" #N
# user_input = "jika informasi tsb mnurut saya pnting, maka sy akan bahagia mendengarnya" #S
user_input = "memastikan informasi benar adanya atau tidak dan brusaha untuk menyaring informasi yang ada" #N

my_X_cnt = cntizer.transform(np.array([user_input]))

my_X_tfidf =  tfizer.transform(my_X_cnt).toarray()

result = []
model = joblib.load('/Users/rezaaar/Development/django-rest/mbti_be/ml_model/clf_P1.sav')
y_pred = model.predict(my_X_tfidf)
result.append(y_pred[0])

if result == [0] :
  result_output = 'N'
else :
  result_output = 'S'

print(user_input)
print("The result is : ", result_output)