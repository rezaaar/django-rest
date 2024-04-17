from django.urls import include, path
from .views import classifiers_view

urlpatterns = [
    path('predict/', classifiers_view.PredictModel, name='predict-classifier'),
]