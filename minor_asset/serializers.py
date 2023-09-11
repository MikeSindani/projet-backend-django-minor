from rest_framework import serializers
from .models import CategorieMachine

class CategorieMachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategorieMachine
        fields = ['nom', 'description']
