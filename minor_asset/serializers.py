from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CategorieMachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategorieMachine
        fields = ["id",'nom', 'description', 'date_creation', 'time_created', 'date_modification', 'time_modified'] 


class MachineSerializer(serializers.ModelSerializer):
    categorie = serializers.StringRelatedField()  # Nested serializer
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
        exclude = ["image","prenom","postnom"]

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
    id_location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
    class Meta:
        model = CategoryInventory
        fields = '__all__'
class InventorySerializer(serializers.ModelSerializer):
    id_location =  serializers.StringRelatedField()
    id_provider =  serializers.StringRelatedField()
    id_category =  serializers.StringRelatedField()
    class Meta:
        model = Inventory
        exclude = ['image']

class InventorySerializerTwo(serializers.ModelSerializer):
    id_location =  serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
    id_provider =  serializers.PrimaryKeyRelatedField(queryset=Provider.objects.all())
    id_category =  serializers.PrimaryKeyRelatedField(queryset=CategoryInventory.objects.all())

    class Meta:
        model = Inventory
        exclude = ['image']

class InventoryIntoSerializer(serializers.ModelSerializer):
    id_article = serializers.StringRelatedField()
    class Meta:
        model = InventoryInto
        fields = '__all__'
class InventoryIntoSerializerTwo(serializers.ModelSerializer):
    id_article = serializers.PrimaryKeyRelatedField(queryset=Inventory.objects.all())
    class Meta:
        model = InventoryInto
        fields = '__all__'
        
class InventoryOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryOut
        fields = ['quantity', 'id_article', 'id_agent', 'id_team', 'date_creation', 'time_created', 'date_modification', 'time_modified']

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__' 