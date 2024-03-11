from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.pagination import PageNumberPagination
from ..serializers.question_serializers import QuestionSerializer
from ..models import Question

# Custom pagination class
class CustomPagination(PageNumberPagination):
    def get_page_size(self, request):
        if 'page_size' in request.query_params:
            return min(int(request.query_params['page_size']), 100)  # limit max page size to 100
        return self.page_size

class QuestionListCreateView(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer # Use question serializer
    pagination_class = CustomPagination # Use custom pagination class
    
    def get_queryset(self): # Get queryset based on question type
        question_type_id = self.request.query_params.get('type', None)
        if question_type_id is not None:
            return Question.objects.filter(question_type=question_type_id).order_by('question_id')
        return Question.objects.all().order_by('question_id')
    
    def list (self, request): # List questions
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data) 
        serializer = QuestionSerializer(self.paginate_queryset(queryset), many=True) # Serialize queryset
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer