from django.urls import include, path
from .views import questions_views, question_type_views, answer_views

urlpatterns = [
    
    path('question-type/', question_type_views.QuestionTypeListCreateView.as_view(), name='list-create-question-type'),
    path('question-type/<int:pk>/', question_type_views.QuestionTypeDetailView.as_view(), name='retrieve-update-delete-question-type'),
    
    path('questions/', questions_views.QuestionListCreateView.as_view(), name='list-create-question'),
    path('questions/<int:pk>/', questions_views.QuestionDetailView.as_view(), name='retrieve-update-delete-question'),
    
    path('answers/', answer_views.AnswerListCreateView.as_view(), name='list-create-answer'),
    path('answers/<int:pk>/', answer_views.AnswerDetailView.as_view(), name='retrieve-update-delete-answer'),
    path('answers/import/', answer_views.ImportDataAPIView.as_view(), name='import-answer'),
]