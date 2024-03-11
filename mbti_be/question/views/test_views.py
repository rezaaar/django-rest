from ml_model.utils import predict
from rest_framework.views import APIView
from rest_framework.response import Response
import joblib
import pickle

model = joblib.load('/Users/rezaaar/Development/django-rest/mbti_be/ml_model/model_IE1.joblib')

class PredictView(APIView):
    def get(self, request):
        res = model.predict('Sendirian')
        # res = predict([32, 60000])
        return Response(res)

