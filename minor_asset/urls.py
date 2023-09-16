from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *
from django.urls  import include


router = DefaultRouter()
router.register(r'categorie_machines', CategorieMachineViewSet)
router.register(r'machines', MachineViewSet)
router.register(r'agents', AgentViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'providers', ProviderViewSet)

urlpatterns = [
    path('machine-count/', MachineCountView.as_view(), name='machine-count'),
    path('categorie-machine-count/', CategorieMachineCountView.as_view(), name='machine-categorie-count'),
    path('', include(router.urls)),
]