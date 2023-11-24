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
    etat = serializers.SerializerMethodField()
    quantity_available = serializers.SerializerMethodField()

    class Meta:
        model = InventoryInto
        fields = '__all__'

    def get_id_article(self, obj):
        if obj.id_article.designation is None:
            return "No found"
        return f"{obj.id_article.designation}"

    def get_etat(self, obj):
        # Obtenez la somme totale de la quantité pour tous les objets InventoryOut qui ont le même id_inventory_into que l'instance actuelle
        total_quantity = InventoryOut.objects.filter(id_inventory_into=obj.id).aggregate(total=Sum('quantity'))['total']
        if total_quantity is None:
            total_quantity = 0
        if total_quantity >= obj.quantity:
            return "unavailable"
        return "available"
    def get_quantity_available(self, obj):
        # Obtenez la somme totale de la quantité pour tous les objets InventoryOut qui ont le même id_inventory_into que l'instance actuelle
        total_quantity = InventoryOut.objects.filter(id_inventory_into=obj.id).aggregate(total=Sum('quantity'))['total']
        if total_quantity is None:
            total_quantity = 0
        if total_quantity >= obj.quantity:
            return 0
        return obj.quantity - total_quantity 
    
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
        
class InventoryOutSerializerAvailable(serializers.ModelSerializer):
    id_inventory_into_name = serializers.SerializerMethodField()
    id_team = serializers.SerializerMethodField()
    id_agent = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    etat = serializers.SerializerMethodField()
    class Meta:
        model = InventoryOut
        fields = '__all__' 
    def get_user(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    def get_id_agent(self, obj):
        return f"{obj.id_agent.prenom} {obj.id_agent.nom}"
    def get_id_team(self, obj):
        return f"{obj.id_team.name}"
    def get_id_inventory_into_name(self, obj):
        return f"{obj.id_inventory_into}"
    def get_etat(self, obj):
        # Obtenez la somme totale de la quantité pour tous les objets InventoryOut qui ont le même id_inventory_into que l'instance actuelle
        total_quantity = InventoryOut.objects.filter(id_inventory_into=obj.id_inventory_into).aggregate(total=Sum('quantity'))['total']
        if total_quantity is None:
            total_quantity = 0
        if total_quantity >= obj.quantity:
            return "unavailable"
        return "available"


class TeamSerializer(serializers.ModelSerializer):
    team_name = serializers.SerializerMethodField()
    team_description = serializers.SerializerMethodField()
    team_supervisor = serializers.SerializerMethodField()
    team_assitance = serializers.SerializerMethodField()
    class Meta:
        model = Team
        fields = '__all__' 
    def get_team_name (self, obj):
        return f"{obj.name}" 
    def get_team_description (self, obj):
        return f"{obj.description}"
    def get_team_supervisor(self, obj):

        try:
            agent = Agent.objects.filter(team=obj.id,isSupervisor=True)[0]
        except:
            return f"No name found"
        return f"{agent.prenom} {agent.nom}"

    def get_team_assitance(self, obj):

        try:
            agent = Agent.objects.filter(team=obj.id,isAssistant=True)[0]
        except:
            return f"No name found"
        return f"{agent.prenom} {agent.nom}"

        
class TeamSerializerTwo(serializers.ModelSerializer):
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
    class Meta:
        model = WorkOrder
        fields = ["work_order","id_machine","id_machine_model","id_machine_marque","id_machine_immatriculation","date_creation","date_modification"]
    def get_id_machine(self, obj):
        return f"{obj.id_machine.nom}"
    def get_id_machine_model(self, obj):
        return f"{obj.id_machine.modele}"
    def get_id_machine_marque(self, obj):
        return f"{obj.id_machine.marque}"
    def get_id_machine_immatriculation(self, obj):
        return f"{obj.id_machine.immatriculation}"
class WorkOrderSerializerTwo(serializers.ModelSerializer):
    class Meta:
        model = WorkOrder
        fields = '__all__'

class WorkOrderSerializerforDetails(serializers.ModelSerializer):
    id_code_panne = CodePanneSerializer(many=True, read_only=True)
    class Meta:
        model = WorkOrder
        fields = ['id_code_panne']

class DiagnosticsSerializer(serializers.ModelSerializer):
    id_machine_name_full = serializers.SerializerMethodField()
    id_machine_name = serializers.SerializerMethodField()
    class Meta:
        model = Diagnostics
        fields = "__all__"
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


class InventoryOutSerializerForTracking(serializers.ModelSerializer):
    class Meta:
        model = InventoryOut
        fields = '__all__'  # or specify the fields you want to include
    
class TrackingPiecesSerializerforDetails(serializers.ModelSerializer):
    id_inventory_out = InventoryOutSerializer(many=True, read_only=True)
    class Meta:
        model = TrackingPieces
        fields = ['id_inventory_out']

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
    
class PlanifierMaintenanceForWebSockets(serializers.ModelSerializer):
    titre = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    priority = serializers.SerializerMethodField()
    date_of_taking_action = serializers.SerializerMethodField()
    time_of_taking_action = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    application = serializers.SerializerMethodField()
    genre = serializers.SerializerMethodField()
    class Meta:
        model = Remind
        fields = '__all__'
    def get_titre(self, obj):
        return f"[Now][Maintenance] schedule for maintenace machine named {obj.id_machine.nom} and ID {obj.id_machine.id}" 
    def get_description(self, obj):
        return f"This schedule has been scheduled for {obj.date_of_taking_action} {obj.time_of_taking_action} with a {obj.priority} priority  priority" 
    def get_priority(self, obj):
        return f"{obj.priority}"   
    def get_date_of_taking_action(self, obj):
        return f"{obj.date_of_taking_action}"
    def get_time_of_taking_action(self, obj):
        return f"{obj.time_of_taking_action}"
    def get_type(self, obj):
        return "Planned"
    def get_application(self, obj):
        return "Asset"
    def get_genre(self, obj):
        return "Maintenance"
    

class RemindSerializer(serializers.ModelSerializer):
    id_machine = serializers.SerializerMethodField()
    priority = serializers.SerializerMethodField()
    date_of_taking_action = serializers.SerializerMethodField()
    time_of_taking_action = serializers.SerializerMethodField()
    class Meta:
        model = Remind
        fields = '__all__'

    def get_id_machine(self, obj):
        return f"{obj.id_planifierMaintenance.id_machine.nom}" 
    def get_priority(self, obj):
        return f"{obj.id_planifierMaintenance.priority}"
    def get_date_of_taking_action(self, obj):
        return f"{obj.id_planifierMaintenance.date_of_taking_action}"
    def get_time_of_taking_action(self, obj):
        return f"{obj.id_planifierMaintenance.time_of_taking_action}"
   
class RemindSerializerForWebSockets(serializers.ModelSerializer):
    titre = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    priority = serializers.SerializerMethodField()
    date_of_taking_action = serializers.SerializerMethodField()
    time_of_taking_action = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    application = serializers.SerializerMethodField()
    genre = serializers.SerializerMethodField()
    class Meta:
        model = Remind
        fields = '__all__'
    def get_titre(self, obj):
        return f"[At {obj.day} Hour][Maintenance] schedule for maintenace machine named {obj.id_planifierMaintenance.id_machine.nom} and ID {obj.id_planifierMaintenance.id_machine.id}" 
    def get_description(self, obj):
         return f"This schedule has been scheduled for {obj.id_planifierMaintenance.date_of_taking_action} {obj.id_planifierMaintenance.time_of_taking_action} with a {obj.id_planifierMaintenance.priority}  priority" 
        
    def get_priority(self, obj):
        return f"{obj.id_planifierMaintenance.priority}"
    def get_date_of_taking_action(self, obj):
        return f"{obj.id_planifierMaintenance.date_of_taking_action}"
    def get_time_of_taking_action(self, obj):
        return f"{obj.id_planifierMaintenance.time_of_taking_action}"
    def get_type(self, obj):
        return "Remind"
    def get_application(self, obj):
        return "Asset"
    def get_genre(self, obj):
        return "Maintenance"
    
class RemindSerializerTwo(serializers.ModelSerializer):
    id_planifierMaintenance = serializers.PrimaryKeyRelatedField(queryset=PlanifierMaintenance.objects.all())
    #id_PlanifierTeam = serializers.PrimaryKeyRelatedField(queryset=PlanifierTeam.objects.all())
    class Meta:
        model = Remind
        fields = '__all__'

class PlanifierRepairSerializer(serializers.ModelSerializer):
    id_machine = serializers.SerializerMethodField()
    class Meta:
        model = PlanifierRepair
        fields = '__all__'
    def get_id_machine(self, obj):
        return f"{obj.id_machine.nom}" 
class PlanifierRepairSerializerTwo(serializers.ModelSerializer):
    id_machine = serializers.PrimaryKeyRelatedField(queryset=Machine.objects.all())
    class Meta:
        model = PlanifierRepair
        fields = '__all__'
class PlanifierRepairSerializerForWebSockets(serializers.ModelSerializer):
    titre = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    application = serializers.SerializerMethodField()
    genre = serializers.SerializerMethodField()
    class Meta:
        model = PlanifierRepair
        fields = '__all__'
    def get_titre(self, obj):
        return f"[Now][Repair] schedule for repair machine name {obj.id_machine.nom} and ID {obj.id_machine.id}" 
    def get_description(self, obj):
        return f"breakdown_description:{obj.breakdown_description} target running at {obj.target_running_date}{obj.target_running_time}with a {obj.priority} priority" 
    def get_priority(self, obj):
        return f"{obj.priority}"
    def get_type(self, obj):
        return "Planned"
    def get_application(self, obj):
        return "Asset"
    def get_genre(self, obj):
        return "Repair"
    
   
class RemindRepairSerializer(serializers.ModelSerializer):
        class Meta:
            model = RemindRepair
            fields = '__all__'
class RemindRepairSerializerForWebSockets(serializers.ModelSerializer):
    titre = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    priority = serializers.SerializerMethodField()
    date_of_taking_action = serializers.SerializerMethodField()
    time_of_taking_action = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    application = serializers.SerializerMethodField()
    genre = serializers.SerializerMethodField()
    class Meta:
        model = RemindRepair
        fields = '__all__'
    def get_titre(self, obj):
        return f"[At {obj.day} Hour][Repair] Callback for repair machine named {obj.id_PlanifierRepair.id_machine.nom} and id{obj.id_PlanifierRepair.id_machine.id}" 
    def get_description(self, obj):
        return f"This schedule has been scheduled for {obj.id_PlanifierRepair.date_of_taking_action} {obj.id_PlanifierRepair.time_of_taking_action} with a {obj.id_PlanifierRepair.priority} priority" 
    def get_priority(self, obj):
        return f"{obj.id_PlanifierRepair.priority}"
    def get_date_of_taking_action(self, obj):
        return f"{obj.id_PlanifierRepair.date_of_taking_action}"
    def get_time_of_taking_action(self, obj):
        return f"{obj.id_PlanifierRepair.time_of_taking_action}"
    def get_type(self, obj):
        return "Remind"
    def get_application(self, obj):
        return "Asset"
    def get_genre(self, obj):
        return "Repair"

class PlanifierTeamSerializerTwo(serializers.ModelSerializer):
    id_team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())
    class Meta:
        model = PlanifierTeam
        fields = '__all__'

class PlanifierTeamSerializer(serializers.ModelSerializer):
    team_name = serializers.SerializerMethodField()
    team_description = serializers.SerializerMethodField()
    team_supervisor = serializers.SerializerMethodField()
    team_assitance = serializers.SerializerMethodField()
    class Meta:
        model = PlanifierTeam
        fields = '__all__'
    def get_team_name (self, obj):
        return f"{obj.id_team.name}" 
    def get_team_description (self, obj):
        return f"{obj.id_team.description}" 
    def get_team_supervisor(self, obj):

        try:
            agent = Agent.objects.filter(team=obj.id_team.id,isSupervisor=True)[0]
            return f"{agent.nom}  {agent.prenom}"
        except:
            return f"no name found"
        

    def get_team_assitance(self, obj):
        try:
            agent = Agent.objects.filter(team=obj.id_team.id,isAssistant=True)[0]
            return f"{agent.nom}  {agent.prenom}"
        except:
            return f"No name found"
        
class PlanifierTeamForWebSockets(serializers.ModelSerializer):
    titre = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    priority = serializers.SerializerMethodField()
    date_of_taking_action = serializers.SerializerMethodField()
    time_of_taking_action = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    application = serializers.SerializerMethodField()
    genre = serializers.SerializerMethodField()
    team_supervisor = serializers.SerializerMethodField()
    team_assitance = serializers.SerializerMethodField()
    class Meta:
        model = PlanifierTeam
        fields = '__all__'
    def get_titre(self, obj):
        return f"[Now][Team] schedule for team name {obj.id_team.name} and ID {obj.id_team.id}" 
    def get_description(self, obj):
        name_supervisor = ""
        name_ajoint = ''
        try:
            agent = Agent.objects.filter(team=obj.id_team.id,isSupervisor=True)[0]
            name_supervisor = f"{agent.nom}  {agent.prenom}"
        except:
            name_supervisor = f"no name found"

        try:
            agent = Agent.objects.filter(team=obj.id_team.id,isAssistant=True)[0]
            name_ajoint = f"{agent.nom}  {agent.prenom}"
        except:
            name_ajoint = f"No name found"
        
        if obj.day == "1000":
            return f"This schedule has been scheduled for {obj.date_of_taking_action} {obj.time_of_taking_action} with supervisor name: {name_supervisor} and ajoint {name_ajoint}."
        if obj.day != "1000":
            return f"This schedule has been scheduled for {obj.day} with supervisor name: {name_supervisor} and ajoint {name_ajoint}."
         
    def get_priority(self, obj):
        return f"normal"   
    def get_date_of_taking_action(self, obj):
        return f"{obj.date_of_taking_action}"
    def get_time_of_taking_action(self, obj):
        return f"{obj.time_of_taking_action}"
    def get_type(self, obj):
        return "Planned"
    def get_genre(self, obj):
        return "Team"
    def get_application(self, obj):
        return "Asset"
    def get_team_description (self, obj):
        return f"{obj.id_team.description}" 
    def get_team_supervisor(self, obj):

        try:
            agent = Agent.objects.filter(team=obj.id_team.id,isSupervisor=True)[0]
            return f"{agent.nom}  {agent.prenom}"
        except:
            return f"no name found"
        

    def get_team_assitance(self, obj):
        try:
            agent = Agent.objects.filter(team=obj.id_team.id,isAssistant=True)[0]
            return f"{agent.nom}  {agent.prenom}"
        except:
            return f"No name found"

class RemindTeamSerializer(serializers.ModelSerializer):
    id_PlanifierTeam = serializers.PrimaryKeyRelatedField(queryset=PlanifierTeam.objects.all())
    class Meta:
        model = RemindTeam
        fields = '__all__'

class RemindTeamSerializerSpecialGet(serializers.ModelSerializer):
    team_name = serializers.SerializerMethodField()
    team_description = serializers.SerializerMethodField()
    team_supervisor = serializers.SerializerMethodField()
    team_assitance = serializers.SerializerMethodField()

    class Meta:
        model = RemindTeam
        fields = '__all__'
    def get_team_name (self, obj):
        return f"{obj.id_PlanifierTeam.id_team.name}" 
    def get_team_description (self, obj):
        return f"{obj.id_PlanifierTeam.id_team.description}" 
    def get_team_supervisor(self, obj):
        agent = ""
        try:
            agent = Agent.objects.get(team=obj.id_PlanifierTeam.id_team.id,isSupervisor=True)
        except:
            return f"{obj.id_PlanifierTeam.id_team.id}"
        return f"{agent.nom}  {agent.prenom}"

    def get_team_assitance(self, obj):
        agent = ""
        try:
            agent = Agent.objects.get(team=obj.id_PlanifierTeam.id_team.id,isAssistant=True)
            print(obj.id_team)
        except:
            return f"No name found"
        return f"{agent.nom}  {agent.prenom}"
    
    

class RemindTeamForWebSockets(serializers.ModelSerializer):
    titre = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    priority = serializers.SerializerMethodField()
    date_of_taking_action = serializers.SerializerMethodField()
    time_of_taking_action = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    genre = serializers.SerializerMethodField()
    application = serializers.SerializerMethodField()
    team_supervisor = serializers.SerializerMethodField()
    team_assitance = serializers.SerializerMethodField()
    class Meta:
        model = RemindTeam
        fields = '__all__'
    def get_titre(self, obj):
        return f"[At {obj.hours} Hour][Team] schedule for team name {obj.id_PlanifierTeam.id_team.name} and ID {obj.id_PlanifierTeam.id_team.id}" 
    def get_description(self, obj):
        name_supervisor = ""
        name_ajoint = ''
        try:
            agent = Agent.objects.filter(team=obj.id_PlanifierTeam.id_team.id,isSupervisor=True)[0]
            name_supervisor = f"{agent.nom}  {agent.prenom}"
        except:
            name_supervisor = f"no name found"

        try:
            agent = Agent.objects.filter(team=obj.id_PlanifierTeam.id_team.id,isAssistant=True)[0]
            name_ajoint = f"{agent.nom}  {agent.prenom}"
        except:
            name_ajoint = f"No name found"
        
        if obj.day == "1000":
            return f"This schedule has been scheduled for {obj.id_PlanifierTeam.date_of_taking_action} {obj.id_PlanifierTeam.time_of_taking_action} with supervisor name: {name_supervisor} and ajoint {name_ajoint}."
        if obj.day != "1000":
            return f"This schedule has been scheduled for {obj.id_PlanifierTeam.day} with supervisor name: {name_supervisor} and ajoint {name_ajoint}."
    def get_date_of_taking_action(self, obj):
        return f"{obj.id_team.date_of_taking_action}"
    def get_time_of_taking_action(self, obj):
        return f"{obj.id_team.time_of_taking_action}"
    def get_type(self, obj):
            return "Remind"
    def get_application(self, obj):
            return "Asset"
    def get_genre(self, obj):
        return "Team"
         

class InventorySerializerForWebSockets(serializers.ModelSerializer):
    etat = serializers.SerializerMethodField()
    titre = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    priority = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    application = serializers.SerializerMethodField()
    genre = serializers.SerializerMethodField()
    class Meta:
        model = InventoryInto
        fields = '__all__' 
    def get_titre(self, obj):
        return f"[unavailable][Stock] schedule for stock product  ID {obj.id_article.id} and NAME {obj.id_article.designation} " 
    def get_description(self, obj):
        return f"Be sure to replace the product as it is finished in the stock" 
        
    def get_priority(self, obj):
        return f"normal"  
    def get_type(self, obj):
            return "Stock"
    def get_application(self, obj):
            return "Asset"
    def get_etat(self, obj):
        # Obtenez la somme totale de la quantité pour tous les objets InventoryOut qui ont le même id_inventory_into que l'instance actuelle
        total_quantity = InventoryOut.objects.filter(id_inventory_into=obj.id).aggregate(total=Sum('quantity'))['total']
        if total_quantity is None:
            total_quantity = 0
        if total_quantity >= obj.quantity:
            return "unavailable"
        return "available"
    def get_genre(self, obj):
        return "Into"