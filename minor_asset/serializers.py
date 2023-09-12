from rest_framework import serializers
from .models import CategorieMachine

class CategorieMachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategorieMachine
        fields = ["id",'nom', 'description', 'date_creation', 'time_created', 'date_modification', 'time_modified'] 