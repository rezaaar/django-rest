from rest_framework import serializers
from ..models import Question

class QuestionSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='question_type.type', read_only=True)
    class Meta:
        model = Question
        fields = ('question_id', 'question_type', 'question_text', 'level', 'type')
    