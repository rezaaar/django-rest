from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status, generics
from ..serializers.answer_serializers import AnswerSerializer
from ..models import Answer, Question
import csv
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
        serializer = AnswerSerializer(self.paginate_queryset(queryset), many=True) # Serialize queryset
        # serializer = AnswerSerializer(self.paginate_queryset(queryset), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class AnswerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

class ImportDataAPIView(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        # data = request.POST
        csv_file = request.FILES.get('csv_file')
        question_id = Question.objects.get(question_id=request.data.get('question_id'))
        if csv_file is None:
            return Response({'error': 'No CSV file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            decoded_file = csv_file.read().decode('utf-8-sig')
            reader = csv.DictReader(decoded_file.splitlines(), delimiter=',')
            for row in reader:
                # Assuming the CSV file has columns 'question_id' and 'answer_text'
                answer_text = row.get('Indikator')
                type = row.get('Tipe'),
                type = type[0] # Get the first element of the tuple (since it's a single value)
                # Create a new Answer object and save it to the database
                answer = Answer(question_id=question_id, answer_text=answer_text, type_result=type)
                if(answer_text == ''):
                    continue
                answer.save()
            return Response({'message': 'CSV file imported successfully'}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)