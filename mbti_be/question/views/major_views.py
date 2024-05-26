from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.pagination import PageNumberPagination
from ..serializers.major_serializers import MajorSerializer
from ..models import Major

class CustomPagination(PageNumberPagination):
    def get_page_size(self, request):
        if 'page_size' in request.query_params:
            return min(int(request.query_params['page_size']), 100)  # limit max page size to 100
        return self.page_size
    
class MajorListCreateView(generics.ListCreateAPIView):
    serializer_class = MajorSerializer
    pagination_class = CustomPagination
    
    def get_queryset(self):
        return Major.objects.all().order_by('major_id')
    
    def list (self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = MajorSerializer(self.paginate_queryset(queryset), many=True) # Serialize queryset
        return Response(serializer.data, status=status.HTTP_200_OK)

class MajorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Major.objects.all()
    serializer_class = MajorSerializer