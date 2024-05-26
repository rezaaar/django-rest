from rest_framework import serializers
from ..models import Personality

class PersonalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Personality
        fields = ('type', 'description','majors')