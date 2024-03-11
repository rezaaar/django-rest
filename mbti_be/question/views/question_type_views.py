from rest_framework.response import Response
from rest_framework import status, generics
from ..serializers.question_type_serializers import QuestionTypeSerializer
from ..models import QuestionType

class QuestionTypeListCreateView(generics.ListCreateAPIView):
    queryset = QuestionType.objects.all()
    serializer_class = QuestionTypeSerializer
    
    def list (self, request):
        queryset = self.get_queryset()
        serializer = QuestionTypeSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class QuestionTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = QuestionType.objects.all()
    serializer_class = QuestionTypeSerializer