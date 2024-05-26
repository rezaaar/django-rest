from rest_framework.response import Response
from rest_framework import status, generics
from ..serializers.personality_serializers import PersonalitySerializer
from ..serializers.major_serializers import MajorSerializer
from ..models import Personality, Major

class PersonalityListCreateView(generics.ListCreateAPIView):
    queryset = Personality.objects.all()
    serializer_class = PersonalitySerializer
    
    def list (self, request):
        queryset = self.get_queryset()
        serializer = PersonalitySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class PersonlityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Personality.objects.all()
    serializer_class = PersonalitySerializer