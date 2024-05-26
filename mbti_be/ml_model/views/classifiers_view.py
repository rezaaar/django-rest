from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np

@api_view(['POST'])
def PredictModel(request):
    type = request.data['type']
    answer = request.data['answer']
    
    if type not in ["E1", "E2", "E3", "J1", "J2", "J3", "P1", "P2", "P3", "T1", "T2", "T3",]:
        return Response("Invalid type", status=status.HTTP_400_BAD_REQUEST)
    
    X = joblib.load(f'ml_model/classifiers/{type}/X_{type}.sav')
    y = joblib.load(f'ml_model/classifiers/{type}/y_{type}.sav')
    model = joblib.load(f'ml_model/classifiers/{type}/clf_{type}.sav')
    
    cntizer = CountVectorizer(analyzer="word",max_features=1000, min_df = 0.01)
    X_cnt = cntizer.fit_transform(X)
    
    tfizer = TfidfTransformer()
    X_tfidf =  tfizer.fit_transform(X_cnt).toarray()
    X = X_tfidf
    
    my_X_cnt = cntizer.transform(np.array([answer]))
    my_X_tfidf =  tfizer.transform(my_X_cnt).toarray()
    
    result = []
    y_pred = model.predict(my_X_tfidf)
    result.append(y_pred[0])
    
    if result == [0] :
        result_output = 0
    else :
        result_output = 1
    
    return Response({"result": result_output}, status=status.HTTP_200_OK)