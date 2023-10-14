from django.db import models
from users.models import *
import random
import string

# Create your models here.
class CategorieMachine(models.Model):
    # Les attributs du modèle
    nom = models.CharField(max_length=50,null=True, blank=True,unique=True)
    description = models.TextField(null=True, blank=True)
    # date et time pour creat et modified 
    date_creation = models.DateTimeField(auto_now_add=True)
    time_created = models.TimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    time_modified = models.TimeField(auto_now=True)

    # Une méthode pour afficher le nom de la catégorie
    def __str__(self):
        return self.nom

class Machine(models.Model):
    image = models.ImageField(upload_to='articles/', null=True, blank=True)
    nom = models.CharField(max_length=250)
    marque = models.CharField(max_length=250)
    modele = models.CharField(max_length=250)
    annee_fabrique = models.IntegerField()
    immatriculation = models.CharField(max_length=20,null=True, blank=True,default="no immatriculation")

    categorie = models.ForeignKey(CategorieMachine, on_delete=models.SET_NULL, null=True)
    
    date_creation = models.DateTimeField(auto_now_add=True)
    time_created = models.TimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    time_modified = models.TimeField(auto_now=True)

    def __str__(self):
        return f"{self.nom} ({self.marque} {self.modele} )"

class Adresse(models.Model):
    # Les attributs du modèle
    rue = models.CharField(max_length=100,null=True, blank=True)
    numero = models.IntegerField( null=True, blank=True)
    ville = models.CharField(max_length=50 , null=True, blank=True)
    pays = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)

    # Une méthode pour afficher l'adresse sous forme de chaîne de caractères
    def __str__(self):
        return f"{self.rue} {self.numero}, {self.ville}, {self.pays}"
#cree un model viewset + son sterialiser + son url router + son ajout dans la page admin django


class Client(models.Model):
    # Les attributs du modèle
    nom = models.CharField(max_length=250,null=True, blank=True)
    phone1 = models.CharField(max_length=10,null=True, blank=True,unique=True)
    phone2 = models.CharField(max_length=10, blank=True,unique=True)
    email = models.EmailField()
    asset_code = models.ForeignKey("Machine", on_delete=models.SET_NULL, null=True) #asset code 
   
    # Les attributs du modèle
    rue = models.CharField(max_length=100,null=True, blank=True)
    numero = models.IntegerField( null=True, blank=True)
    quarter = models.CharField(max_length=150 , null=True, blank=True)
    commune = models.CharField(max_length=150 , null=True, blank=True)
    ville = models.CharField(max_length=50 , null=True, blank=True)
    pays = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    # date et time pour creat et modified 
    date_creation = models.DateTimeField(auto_now_add=True)
    time_created = models.TimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    time_modified = models.TimeField(auto_now=True)

    # Une méthode pour afficher le nom complet de l'agent
    def __str__(self):
        return f"{self.nom} {self.prenom} {self.postnom}"


class Provider(models.Model):
    name = models.CharField(max_length=100)
    phone1 = models.CharField(max_length=10,unique=True)
    phone2 = models.CharField(max_length=10, blank=True,unique=True)
    web_site = models.CharField(max_length=250, blank=True,unique=True)
    email = models.EmailField(null=True, blank=True,unique=True)
    # Les attributs du modèle
    rue = models.CharField(max_length=100,null=True, blank=True)
    numero = models.IntegerField()
    quarter = models.CharField(max_length=150 , null=True, blank=True)
    commune = models.CharField(max_length=150 , null=True, blank=True)
    ville = models.CharField(max_length=50 , null=True, blank=True)
    pays = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    
    # date et time pour creat et modified 
    date_creation = models.DateTimeField(auto_now_add=True)
    time_created = models.TimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    time_modified = models.TimeField(auto_now=True)

    def __str__(self):
        return self.name 

class Location(models.Model):
    name = models.CharField(max_length=100,unique=True)
    description = models.TextField(null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    time_created = models.TimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    time_modified = models.TimeField(auto_now=True)
    def __str__(self):
        return self.name   
class CategoryInventory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    id_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)

    date_creation = models.DateTimeField(auto_now_add=True,null=True)
    time_created = models.TimeField(auto_now_add=True,null=True)
    date_modification = models.DateTimeField(auto_now=True,null=True)
    time_modified = models.TimeField(auto_now=True,null=True)

    def __str__(self):
        return self.name 
    
'''
cree un model viewset + son sterialiser + son url router + son ajout dans la page admin django.
'''


class Inventory(models.Model):
    designation = models.CharField(max_length=250,null=True, blank=True)
    unit = models.CharField(max_length=20,null=True, blank=True)
    capacity = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    currency = models.CharField(max_length=20,null=True, blank=True)
    id_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    id_provider = models.ForeignKey(Provider, on_delete=models.SET_NULL, null=True, blank=True)
    id_category = models.ForeignKey(CategoryInventory, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='articles/', null=True, blank=True)
    code_bar = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(blank=True)
    # date et time pour creat et modified 
    date_creation = models.DateTimeField(auto_now_add=True)
    time_created = models.TimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True) 
    time_modified = models.TimeField(auto_now=True)
    def __str__(self):
        return self.designation


class InventoryInto(models.Model):
    quantity = models.IntegerField(null=True, blank=True)
    id_article = models.ForeignKey(Inventory, on_delete=models.SET_NULL, null=True, blank=True)
    userOrNew = models.CharField(max_length=20,null=True, blank=True)
    unit = models.CharField(max_length=20,null=True, blank=True)
    capacity = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True)
    
    # date et time pour creat et modified 
    date_creation = models.DateTimeField(auto_now_add=True)
    time_created = models.TimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    time_modified = models.TimeField(auto_now=True)
    # on verfier si la quantite est plein on met a true
    #isFull  = models.BooleanField(null=True, blank=True,default=False)
    

class InventoryOut(models.Model):
    quantity = models.IntegerField()
    id_inventory_into = models.ForeignKey("InventoryInto", on_delete=models.SET_NULL, null=True)
    id_agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True)
    id_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # UserAgent doit etre partout
    
    # date et time pour creat et modified 
    date_creation = models.DateTimeField(auto_now_add=True)
    time_created = models.TimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    time_modified = models.TimeField(auto_now=True)
    # on verfier si la quantite est plein on met a true
    #isFull  = models.BooleanField(null=True, blank=True,default=False)

class PlanifierRepair(models.Model):
    PRIORITE_CHOICES = [
        ('haut', 'Haut'),
        ('normal', 'Normal'),
        ('basse', 'Basse'),
    ]
    
    id_machine = models.ForeignKey("Machine", on_delete=models.SET_NULL, null=True)
    date_of_taking_action = models.DateTimeField()
    breakdown_description = models.CharField(max_length=200)
    action = models.CharField(max_length=200)
    target_running_date = models.DateTimeField() 
    priorite = models.CharField(max_length=10, choices=PRIORITE_CHOICES, blank=True)
    comments = models.TextField(null=True, blank=True)
    
    # date et time pour creat et modified 
    date_creation = models.DateTimeField(auto_now_add=True)
    time_created = models.TimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    time_modified = models.TimeField(auto_now=True)

class PlanifierMaintenance(models.Model):
    PRIORITE_CHOICES = [
        ('haut', 'Haut'),
        ('normal', 'Normal'),
        ('basse', 'Basse'),
    ]
    
    id_machine = models.ForeignKey('Machine', on_delete=models.SET_NULL, null=True)
    priority = models.CharField(max_length=10, choices=PRIORITE_CHOICES)
    date_of_taking_action = models.DateField()
    time_of_taking_action = models.TimeField()
    comments = models.TextField(null=True, blank=True)
    
    # date et time pour creat et modified 
    date_creation = models.DateTimeField(auto_now_add=True)
    time_created = models.TimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    time_modified = models.TimeField(auto_now=True)

class PlanifierTeam(models.Model):
    id_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    
    # date et time pour creat et modified 
    date_creation = models.DateTimeField(auto_now_add=True)
    time_created = models.TimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    time_modified = models.TimeField(auto_now=True)


class Remind(models.Model):
    id_planifierRepair = models.ForeignKey(PlanifierRepair, on_delete=models.SET_NULL, null=True, blank=True)
    id_planifierMaintenance = models.ForeignKey(PlanifierMaintenance, on_delete=models.SET_NULL, null=True, blank=True)
    datetime_remind = models.DateTimeField(null=True, blank=True)
    day = models.CharField(max_length=1,null=True, blank=True) 
    # date et time pour creat et modified 
    date_creation = models.DateTimeField(auto_now_add=True)
    time_created = models.TimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    time_modified = models.TimeField(auto_now=True)


def generate_work_order():
    return ''.join(random.choices(string.digits, k=6))


# Ce modèle représente une catégorie de panne
class CategoriePanne(models.Model):
    # Ce champ contient le nom de la catégorie
    nom = models.CharField(max_length=100,unique=True)
    # Ce champ contient la description de la catégorie
    description = models.TextField(blank=True)
    
     # date et time pour creat et modified 
    date_creation = models.DateTimeField(auto_now_add=True)
    time_created = models.TimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    time_modified = models.TimeField(auto_now=True)

    def __str__(self):
        return self.nom

# Ce modèle représente un code de panne
class CodePanne(models.Model):
    # Ce champ contient le système concerné par la panne
    code = models.CharField(max_length=100,unique=True)
    # Ce champ contient la description de la panne
    description = models.TextField(blank=True)
    # Ce champ contient un commentaire optionnel sur la panne
    comment = models.TextField(blank=True)
    # Ce champ contient la clé étrangère vers la catégorie de panne
    id_categorie_panne = models.ForeignKey(CategoriePanne, on_delete=models.SET_NULL, null=True,blank=True)
    
     # date et time pour creat et modified 
    date_creation = models.DateTimeField(auto_now_add=True)
    time_created = models.TimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    time_modified = models.TimeField(auto_now=True)

    def __str__(self):
        return self.code + " - " + self.description

class WorkOrder(models.Model):
    work_order = models.CharField(max_length=6, default=generate_work_order, primary_key=True)
    id_machine = models.ForeignKey(Machine, on_delete=models.SET_NULL, null=True)
    id_inventaire = models.ForeignKey(Inventory, on_delete=models.SET_NULL, null=True, blank=True)
    id_code_panne = models.ForeignKey(CodePanne, on_delete=models.SET_NULL, null=True)
    
     # date et time pour creat et modified 
    date_creation = models.DateTimeField(auto_now_add=True)
    time_created = models.TimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    time_modified = models.TimeField(auto_now=True)

# Ce modèle représente un diagnostic effectué sur une machine
class Diagnostics(models.Model):
    PRIORITE_CHOICES = [
        ('haut', 'Haut'),
        ('normal', 'Normal'),
        ('basse', 'Basse'),
    ]
    # Ce champ contient la clé étrangère vers le work order associé au diagnostic
    id_work_order = models.ForeignKey(WorkOrder, on_delete=models.SET_NULL, null=True)
    # Ce champ contient la clé étrangère vers la machine diagnostiquée
    id_machine = models.ForeignKey(Machine, on_delete=models.SET_NULL, null=True)
    # Ce champ contient le roster du diagnostic
    roster = models.CharField(max_length=100,null=True,blank=True)
    # Ce champ contient le commentaire du diagnostic
    comment = models.TextField(null=True,blank=True)
    # Ce champ contient le type de maintenance effectué
    typeMaintenance = models.CharField(max_length=100)
    # Ce champ contient la date de la panne
    breakdown_date = models.DateField()
    # Ce champ contient l'heure de la panne
    breakdown_time = models.TimeField()
    # Ce champ contient la date du début de la réparation
    start_repair_date = models.DateField(null=True,blank=True)
    # Ce champ contient l'heure du début de la réparation
    start_repair_time = models.TimeField(null=True,blank=True)
    # Ce champ contient la date de fin de la réparation
    end_repair_date = models.DateField(null=True,blank=True)
    # Ce champ contient l'heure de fin de la réparation
    end_repair_time = models.TimeField(null=True,blank=True)
    # Ce champ contient la priorité du diagnostic
    priority = models.CharField(max_length=10, choices=PRIORITE_CHOICES)
    # Ce champ contient le temps en heures décimales du diagnostic
    time_decimal_hour = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    # Ce champ contient le kilométrage de la panne en entier
    km_panne = models.IntegerField()
    # Ce champ contient le kilométrage en service en entier
    km_en_service = models.IntegerField()
    # Ce champ contient la quantité de fuel consommée
    fuel = models.DecimalField(max_digits=10, decimal_places=2)
    # Ce champ contient la quantité de cooling consommée
    cooling = models.DecimalField(max_digits=10, decimal_places=2)
    # Ce champ contient la quantité de grease consommée
    grease = models.DecimalField(max_digits=10, decimal_places=2)
    # Ce champ contient la quantité d'engin oil consommée
    engin_oil = models.DecimalField(max_digits=10, decimal_places=2)
    # Ce champ contient la quantité d'hydraulic oil consommée
    hydraulic_oil = models.DecimalField(max_digits=10, decimal_places=2)
    # Ce champ contient la quantité de transmission oil consommée
    transmission_oil = models.DecimalField(max_digits=10, decimal_places=2)
    # Ce champ contient le coût du diagnostic
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    # Ce champ contient la clé étrangère vers l'équipe qui a effectué le diagnostic
    id_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    # Ce champ contient la date du début du diagnostic
    start_diag_date = models.DateField()
    # Ce champ contient l'heure du début du diagnostic
    start_diag_time = models.TimeField()
    # Ce champ contient l'heure de fin du diagnostic
    end_diag_time = models.TimeField()
    # Ce champ contient la date de fin du diagnostic
    end_diag_date = models.DateField()

    Brake_fuite = models.CharField(max_length=100,null=True,blank=True)
 
    poids = models.CharField(max_length=100,null=True,blank=True)
    capacity = models.CharField(max_length=100,null=True,blank=True)
    currency = models.CharField(max_length=100,null=True,blank=True)
    distance = models.CharField(max_length=100,null=True,blank=True)
    
     # date et time pour creat et modified 
    date_creation = models.DateTimeField(auto_now_add=True)
    time_created = models.TimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    time_modified = models.TimeField(auto_now=True)
    

class TrackingPieces(models.Model):
    # Ce champ contient le nom de la catégorie
    id_machine = models.ForeignKey(Machine, on_delete=models.SET_NULL, null=True)
    id_inventory_out = models.ManyToManyField(InventoryOut)
    id_work_order = models.ForeignKey(WorkOrder, on_delete=models.SET_NULL, null=True)
    
     # date et time pour creat et modified 
    date_creation = models.DateTimeField(auto_now_add=True)
    time_created = models.TimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    time_modified = models.TimeField(auto_now=True)

    def __str__(self):
        return self.id_machine




