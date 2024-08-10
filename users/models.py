
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import date
from django.contrib.auth.models import Group, Permission
import uuid 

class Organisation(models.Model):
    TYPE = (
        ('MINOR', 'MINOR'),
        ('MECANIQUE', 'MECANIQUE'),
        # Add all the other currencies here
    )
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=True)
    name = models.CharField(max_length=250)
    type = models.CharField( max_length=250,choices=TYPE)
    trial = models.BooleanField()
    on_paid = models.BooleanField()
    date_to_paid = models.DateTimeField()
    data_until_paid = models.DateTimeField()
    # date et time pour creat et modified 
    date_creation = models.DateTimeField(auto_now_add=True)
    time_created = models.TimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    time_modified = models.TimeField(auto_now=True)

    def __str__(self):
        return f"nom:{self.name} type:{self.type} uuid:{self.id}"


class Team(models.Model):
    TYPE = (
        ('MAINTENANCE', 'MAINTENANCE'),
        ('INVENTAIRE', 'INVENTAIRE'),
        ('CONTROLEUR', 'CONTROLEUR'),
        ('OTHERS', 'OTHERS'),
        # Add all the other currencies here
    )
    name = models.CharField(max_length=100 ,null=True, blank=True,unique=True)
    team_type = models.CharField(max_length=20, choices=TYPE)
    description = models.TextField(blank=True)
    
    entreprise = models.ForeignKey("organisation", on_delete=models.SET_NULL, null=True)
    
    # date et time pour creat et modified 
    date_creation = models.DateTimeField(auto_now_add=True)
    time_created = models.TimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    time_modified = models.TimeField(auto_now=True)


class Agent(models.Model):
    APPS_USER = (
        ('ASSET', 'ASSET'),
        ('FLEET', 'FLEET'),
        # Add all the other currencies here
    )
    # Les attributs du modèle
    image = models.ImageField(upload_to='articles/', null=True, blank=True)
    nom = models.CharField(max_length=250)
    prenom = models.CharField(max_length=250)
    postnom = models.CharField(max_length=250)
    matricule = models.CharField(max_length=10, unique=True)
    phone1 = models.CharField(max_length=10)
    phone2 = models.CharField(max_length=10, blank=True)
    email = models.EmailField(null=True, blank=True,unique=True)
    # Les attributs du modèle
    rue = models.CharField(max_length=100,null=True, blank=True)
    numero = models.IntegerField(null=True, blank=True)
    quarter = models.CharField(max_length=150 , null=True, blank=True)
    commune = models.CharField(max_length=150 , null=True, blank=True)
    ville = models.CharField(max_length=50 , null=True, blank=True)
    pays = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.CharField(max_length=10,null=True, blank=True)
    # id de l'equipe 
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team')
    entreprise = models.ForeignKey("organisation", on_delete=models.SET_NULL,null=True)

    isSupervisor = models.BooleanField(default=False)
    isAssistant = models.BooleanField(default=False)
    isAgent = models.BooleanField(default=True)

    user_apps_type = models.CharField(max_length=20, choices=APPS_USER)
    # date et time pour creat et modified 
    date_creation = models.DateTimeField(auto_now_add=True)
    time_created = models.TimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    time_modified = models.TimeField(auto_now=True)

    # Une méthode pour afficher le nom complet de l'agent
    def __str__(self):
        return f"{self.nom} {self.prenom} {self.postnom}"

# Create your models here.
class User(AbstractUser):
  PROFIL = (
        ('ADMIN', 'ADMIN'),
        ('INVENTORY', 'INVENTORY'),
        ('MAINTENANCE', 'MAINTENANCE'),
        ('CONTROLEUR', 'CONTROLEUR'),
        # Add all the other currencies here
    )
  # Pas besoin de définir le champ username
  email = models.EmailField('email address', unique = True)
  poste = models.CharField(max_length = 50, blank = True, null = True)
  profil = models.CharField(max_length=20, choices=PROFIL, blank = True, null = True)
  agent = models.OneToOneField(Agent, on_delete=models.CASCADE,blank = True, null = True)

  entreprise = models.ForeignKey("organisation", on_delete=models.SET_NULL,null=True)

  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = ['password'] 
  def __str__(self):
      return "{} - {}".format(self.username,self.email)

  groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name="users_groups",
        related_query_name="user",
        help_text=
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ,
    )

  user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name="users_permissions",
        related_query_name="user",
        help_text='Specific permissions for this user.',
    )
