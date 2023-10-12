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
router.register(r'locations', LocationViewSet)
router.register(r'category-inventory', CategoryInventoryViewSet)
router.register(r'inventory', InventoryViewSet)
router.register(r'inventory-into', InventoryIntoViewSet, basename='inventory-into')
router.register(r'inventory-out', InventoryOutViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'categoriepanne', CategoriePanneViewSet)
router.register(r'codepanne', CodePanneViewSet)
router.register(r'workorder', WorkOrderViewSet)
router.register(r'diagnostics', DiagnosticsViewSet)



urlpatterns = [
    path('machine-count/', MachineCountView.as_view(), name='machine-count'),
    path('categorie-machine-count/', CategorieMachineCountView.as_view(), name='machine-categorie-count'),
    path('provider_count/', ProviderCountView.as_view(), name='provider_count'),
    path('inventory_count/', InventoryCountView.as_view(), name='inventory_count'),
    path('inventory_out_count/', InventoryOutCountView.as_view(), name='inventory_out_count'),
    path('inventory_in_count/', InventoryIntoCountView.as_view(), name='inventory_in_count'),
    path('workorder_count_current/', WorkOrderCurrentCountView.as_view(), name='workorder_count_current'),
    path('workorder_count_week/', WorkOrderWeekCountView.as_view(), name='workorder_count_week'),
    path('workorder_count_month/', WorkOrderMounthCountView.as_view(), name='workorder_count_mounth'),
    path('diagnostics_count_current/', DiagnosticsCurrentCountView.as_view(), name='diagnostics_count_current'),
    path('diagnostics_count_week/', DiagnosticsWeekCountView.as_view(), name='diagnostics_count_week'),
    path('diagnostics_count_month/', DiagnosticsMounthCountView.as_view(), name='diagnostics_count_mounth'),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('', include(router.urls)),
]