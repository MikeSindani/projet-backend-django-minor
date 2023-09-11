from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CategorieMachineViewSet


router = DefaultRouter()
router.register(r'categorie_machines', CategorieMachineViewSet)

urlpatterns = router.urls