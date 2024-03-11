from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status, generics
from ..serializers.answer_serializers import AnswerSerializer
from ..models import Answer
# from ...ml_model.utils import predict

class CustomPageNumberPagination(PageNumberPagination):
    def get_page_size(self, request):
        if 'page_size' in request.query_params:
            return min(int(request.query_params['page_size']), 100)  # limit max page size to 100
        return self.page_size

class AnswerListCreateView(generics.ListCreateAPIView):
    serializer_class = AnswerSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        question_id = self.request.query_params.get('question_id', None)
        if question_id is not None:
            return Answer.objects.filter(question_id=question_id).order_by('answer_id')
        return Answer.objects.all().order_by('answer_id')
    
    def list (self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class AnswerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer