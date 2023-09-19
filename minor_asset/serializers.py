from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CategorieMachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategorieMachine
        fields = ["id",'nom', 'description', 'date_creation', 'time_created', 'date_modification', 'time_modified'] 


class MachineSerializer(serializers.ModelSerializer):
    categorie = CategorieMachineSerializer()  # Nested serializer
    class Meta:
        model = Machine
        exclude = ['image']
class MachineSerializerTwo(serializers.ModelSerializer):
    categorie = serializers.PrimaryKeyRelatedField(queryset=CategorieMachine.objects.all())
    class Meta:
        model = Machine
        exclude = ['image']


class AdresseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adresse
        fields = '__all__'

class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class TeamSerializer(serializers.ModelSerializer):
    supervisor = serializers.PrimaryKeyRelatedField(queryset=Agent.objects.all())
    assistant = serializers.PrimaryKeyRelatedField(queryset=Agent.objects.all())
    class Meta:
        model = Team
        fields = ['name', 'team_type', 'supervisor', 'assistant', 'date_creation', 'time_created', 'date_modification', 'time_modified']
        
class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = '__all__'


class MachineCountSerializer(serializers.Serializer):
    total_categorieMachine = serializers.IntegerField()
    total_machine = serializers.IntegerField()


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id','name', 'description', 'date_creation', 'time_created', 'date_modification', 'time_modified']

class CategoryInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryInventory
        fields = '__all__'
