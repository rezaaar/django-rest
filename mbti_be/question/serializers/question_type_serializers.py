from rest_framework import serializers
from ..models import QuestionType

class QuestionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionType
        fields = '__all__'  # Include all fields