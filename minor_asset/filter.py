from django_filters.rest_framework import FilterSet
from .models import CategorieMachine
   
class CategorieMachineFilter(FilterSet):
       class Meta:
           model = CategorieMachine
           fields = '__all__'  # Remplacez 'nom' par le nom de votre champ
