from rest_framework import serializers
from ..models import Answer

class AnswerSerializer(serializers.ModelSerializer):
    # question_text = serializers.CharField(source='question.question_text', read_only=True)
    question = serializers.SerializerMethodField()

    def get_question(self, obj):
        question_text = obj.question_id.question_text[:50]
        if len(obj.question_id.question_text) > 30:
            question_text += "..."
        return question_text
    
    class Meta:
        model = Answer
        fields = ('answer_id', 'question_id', 'answer_text', 'type_result', 'question')
        