from rest_framework import serializers
from ..models import Major

class MajorSerializer(serializers.ModelSerializer):
    # personality_type = serializers.CharField(source='personality.type', read_only=True)
    class Meta:
        model = Major
        fields = ('major_id', 'major_name', 'type')