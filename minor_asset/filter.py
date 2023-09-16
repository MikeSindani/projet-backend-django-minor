from django_filters.rest_framework import FilterSet
from .models import *
   
class CategorieMachineFilter(FilterSet):
       class Meta:
           model = CategorieMachine
           fields = '__all__'
class MachineFilter(FilterSet):
    class Meta:
        model = Machine
        fields = ['nom', 'marque', 'modele', 'annee_fabrique', 'categorie']
class ClientFilter(FilterSet):
    class Meta:
        model = Client
        fields = '__all__'
  # Remplacez 'nom' par le nom de votre champ
class ProviderFilter(FilterSet):
    class Meta:
        model = Provider
        fields = '__all__'
