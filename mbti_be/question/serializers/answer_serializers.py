from rest_framework import serializers
from ..models import Answer

class AnswerSerializer(serializers.ModelSerializer):
    # question = QuestionSerializer()  # Nested serializer for question
    question = serializers.CharField(source='question.question_text', read_only=True)
    class Meta:
        model = Answer
        fields = ('answer_id', 'question_id', 'answer_text', 'type', 'question')
        
    def get_question(self, obj):
        return obj.question.question_text