from django.shortcuts import render
from rest_framework import viewsets
from .models import CategorieMachine
from .serializers import CategorieMachineSerializer
# Create your views here.

class CategorieMachineViewSet(viewsets.ModelViewSet):
    queryset = CategorieMachine.objects.all()
    serializer_class = CategorieMachineSerializer


  
