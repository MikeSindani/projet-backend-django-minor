from rest_framework import serializers
from .models import *
from users.models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db.models import Sum

class CategorieMachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategorieMachine
        fields = ["id",'nom', 'description', 'date_creation', 'time_created', 'date_modification', 'time_modified'] 


class MachineSerializer(serializers.ModelSerializer):
    categorie = serializers.SerializerMethodField()
    categorie_desc = serializers.SerializerMethodField()
      # Nested serializer
    class Meta:
        model = Machine
        fields = ["id",'nom', 'marque',"modele","annee_fabrique","categorie","categorie_desc","immatriculation", 'date_creation', 'time_created', 'date_modification', 'time_modified'] 
    def get_categorie(self, obj):
        return f"{obj.categorie.nom}"
    def get_categorie_desc(self, obj):
        return f"{obj.categorie.description}"
class MachineSerializerTwo(serializers.ModelSerializer):
    categorie = serializers.PrimaryKeyRelatedField(queryset=CategorieMachine.objects.all())
    class Meta:
        model = Machine
        exclude = ['image']


class AdresseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adresse
        fields = '__all__'
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name', 'team_type', 'date_creation', 'time_created', 'date_modification', 'time_modified']

class AgentSerializer(serializers.ModelSerializer):
    team = serializers.SerializerMethodField()
    #user = serializers.SerializerMethodField()
    class Meta:
        model = Agent
        exclude = ["image","postnom"]  
    '''def get_user(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"'''
    def get_team(self, obj):
        return f"{obj.team.name}"
class AgentSerializerTwo(serializers.ModelSerializer):
    team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())
    #user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Agent
        exclude = ["image","postnom"]       
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
    id_article = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = InventoryInto
        fields = '__all__'

    def get_id_article(self, obj):
        return f"{obj.id_article.designation}"

    def get_status(self, obj):
        # Obtenez la somme totale de la quantité pour tous les objets InventoryOut qui ont le même id_inventory_into que l'instance actuelle
        total_quantity = InventoryOut.objects.filter(id_inventory_into=obj.id).aggregate(total=Sum('quantity'))['total']
        if total_quantity is None:
            total_quantity = 0
        if total_quantity > obj.quantity:
            return "unavailable"
        return "available"
class InventoryIntoSerializerTwo(serializers.ModelSerializer):
    id_article = serializers.PrimaryKeyRelatedField(queryset=Inventory.objects.all())
    class Meta:
        model = InventoryInto
        fields = '__all__'



class InventoryOutSerializer(serializers.ModelSerializer):
    id_inventory_into = serializers.SerializerMethodField()
    id_team = serializers.SerializerMethodField()
    id_agent = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    class Meta:
        model = InventoryOut
        fields = '__all__'
    def get_user(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    def get_id_agent(self, obj):
        return f"{obj.id_agent.prenom} {obj.id_agent.nom}"
    def get_id_team(self, obj):
        return f"{obj.id_team.name}"
    def get_id_inventory_into(self, obj):
        return f"{obj.id_inventory_into.id_article.designation}"
    def validate(self, data):
        # Obtenez la somme totale de la quantité pour tous les objets Movie
        total_quantity = InventoryOut.objects.filter(id_inventory_into=data['id_inventory_into']).aggregate(total=Sum('quantity'))['total']

        # Vérifiez si la quantité de la nouvelle donnée est supérieure à la somme totale
        if data['quantity'] > total_quantity:
            raise serializers.ValidationError('Quantity inventory out cannot be greater than quantity inventory into')
    
class InventoryOutSerializerTwo(serializers.ModelSerializer):
    id_inventory_into = serializers.PrimaryKeyRelatedField(queryset=InventoryInto.objects.all())
    id_team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())
    id_agent = serializers.PrimaryKeyRelatedField(queryset=Agent.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = InventoryOut
        fields = '__all__' 

   
        
class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__' 


class CategoriePanneSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriePanne
        fields = '__all__'

class CodePanneSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodePanne
        fields = '__all__'

class WorkOrderSerializer(serializers.ModelSerializer):
    id_machine = serializers.SerializerMethodField()
    id_machine_model = serializers.SerializerMethodField()
    id_machine_marque = serializers.SerializerMethodField()
    id_machine_immatriculation = serializers.SerializerMethodField()
    id_code_panne = serializers.SerializerMethodField()
    id_code_panne_description = serializers.SerializerMethodField()
    id_code_panne_categorie = serializers.SerializerMethodField()
    class Meta:
        model = WorkOrder
        fields = ["id_code_panne_categorie","id_code_panne","id_code_panne_description","work_order","id_machine","id_machine_model","id_machine_marque","id_machine_immatriculation","date_creation","date_modification"]
    def get_id_machine(self, obj):
        return f"{obj.id_machine.nom}"
    def get_id_machine_model(self, obj):
        return f"{obj.id_machine.modele}"
    def get_id_machine_marque(self, obj):
        return f"{obj.id_machine.marque}"
    def get_id_machine_immatriculation(self, obj):
        return f"{obj.id_machine.immatriculation}"
    def get_id_code_panne(self, obj):
        return f"{obj.id_code_panne.code}"
    def get_id_code_panne_description(self, obj):
        return f"{obj.id_code_panne.description}"
    def get_id_code_panne_categorie(self, obj):
        return f"{obj.id_code_panne.id_categorie_panne.nom}"
class WorkOrderSerializerTwo(serializers.ModelSerializer):
    class Meta:
        model = WorkOrder
        fields = '__all__'



class DiagnosticsSerializer(serializers.ModelSerializer):
    id_machine_name_full = serializers.SerializerMethodField()
    id_code_panne = serializers.SerializerMethodField()
    id_machine_name = serializers.SerializerMethodField()
    class Meta:
        model = Diagnostics
        fields = [
            "id",
            "id_code_panne",
            'id_work_order',
            'id_machine',
            'id_machine_name',
            'id_machine_name_full',
            'roster',
            'comment',
            'typeMaintenance',
            'breakdown_date',
            'breakdown_time',
            'start_repair_date',
            'start_repair_time',
            'end_repair_date',
            'end_repair_time',
            'priority',
            'time_decimal_hour',
            'km_panne',
            'km_en_service',
            'fuel',
            'cooling',
            'grease',
            'engin_oil',
            'hydraulic_oil',
            'transmission_oil',
            'cost',
            'id_team',
            'start_diag_date',
            'start_diag_time',
            'end_diag_time',
            'end_diag_date',
            'Brake_fuite',
            'poids',
            'capacity',
            'currency',
            'distance',
            'date_creation',
            'time_created',
            'date_modification',
            'time_modified'
              ]
    def get_id_code_panne(self, obj):
        return f"{obj.id_work_order.id_code_panne.code}"
    def get_id_machine_name_full(self, obj):
        return f"{obj.id_machine.marque}  {obj.id_machine.nom}"
    def get_id_machine_name(self, obj):
        return f"{obj.id_machine.nom}"
class DiagnosticsSerializerTwo(serializers.ModelSerializer):
    id_machine = serializers.PrimaryKeyRelatedField(queryset=Machine.objects.all())
    id_work_order = serializers.PrimaryKeyRelatedField(queryset=WorkOrder.objects.all())

    class Meta:
        model = Diagnostics
        exclude = ["roster","time_decimal_hour",'start_repair_date', 'start_repair_time', 'end_repair_date', 'end_repair_time']

class TrackingPiecesSerializer(serializers.ModelSerializer):
    id_machine = serializers.PrimaryKeyRelatedField(queryset=Machine.objects.all())
    id_work_order = serializers.PrimaryKeyRelatedField(queryset=WorkOrder.objects.all())
    id_inventory_out = serializers.PrimaryKeyRelatedField(many=True, queryset=InventoryOut.objects.all())
    class Meta:
        model = TrackingPieces
        fields = "__all__"

class PlanifierMaintenanceSerializerTwo(serializers.ModelSerializer):
    class Meta:
        model = PlanifierMaintenance
        fields = '__all__'
class PlanifierMaintenanceSerializer(serializers.ModelSerializer):
    id_machine = serializers.SerializerMethodField()
    class Meta:
        model = PlanifierMaintenance
        fields = '__all__'
    def get_id_machine(self, obj):
        return f"{obj.id_machine.nom}"

class RemindSerializer(serializers.ModelSerializer):
    id_planifierMaintenance = serializers.PrimaryKeyRelatedField(queryset=PlanifierMaintenance.objects.all())
    class Meta:
        model = Remind
        fields = '__all__'
