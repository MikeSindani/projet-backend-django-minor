from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import include

from rest_framework.routers import DefaultRouter, SimpleRouter


router = SimpleRouter()
router.register("settings", SettingViewSet, basename="settings")
router.register('tracking_piecestest', TrackingPiecesViewSetTest,basename="test")


urlpatterns = [
    ############################################################
    # Urls des diagnostics statistique , planned and maintenance
    path('diagnostics/statistics/', DiagnosticsStatisticsView.as_view(), name='diagnostics-statistics'),
    path('plannedMaintenance/statistics/', PlanifierMaintenanceStatisticsView.as_view(), name='plannedMaintenance-statistics'),
    path('repair/statistics/', RepairStatisticsView.as_view(), name='repair-statistics'),
    path('diagnostics/statistics/list/', Statistique_maintenance_machine_list_retrieve.as_view(), name='maintenance_machine-statistics'),
    path('stock/statistics/list/', Statistique_stock_list_retrieve.as_view(), name='maintenance_machine-statistics'),
    # for stock graphique generel, price , litre by period day, month , years.
    path("stock/int/statistics/",Statistique_stock_int_retrieve,name="Statistique_stock_int_retrieve" ),
    path("stock/out/statistics/",Statistique_stock_out_retrieve,name="Statistique_stock_out_retrieve" ),
     path('machine_data/', MachineData, name='machine_data'),
    ############################################################
    # Urls des différents entrées
    #
    path("", include(router.urls), name="api-root"),
    ### reucpere les annees et mois 
     path(
        "get-list_in_calendre_week_and_day/<str:filter_by>/<int:year>/<int:month>/",
        Statistique_calendre_retrieve_week_and_day,
        name="statistique_calendre_week_and_day",
    ),
    path(
        "get-list_in_calendre_month_and_year/<str:filter_by>/<int:year>/",
        Statistique_calendre_retrieve_year_and_month,
        name="statistique_calendre_month_and_year",
    ),
    #############################################################################################
    # Par catégories by list 
    path(
        "stock/int/statistique/by_category/list/",
        Statistique_total_stock_int_retrieve_by_category_list,
        name="statistique_stock_int_by_category",
    ),
    #############################################################################################
    #############################################################################################
    # Par articles by list 
    path(
        "get-statistique_stock_int_month_articles_list/<int:year>/",
        Statistique_total_stock_int_retrieve_month_article_list,
        name="statistique_stock_int_month_article",
    ),
    path(
        "get-statistique_stock_int_year_articles_list/",
        Statistique_total_stock_int_retrieve_year_article_list,
        name="statistique_stock_int_year_article",
    ),
    path(
        "get-statistique_stock_int_day_articles_list/<int:year>/<int:month>/",
        Statistique_total_stock_int_retrieve_day_article_list,
        name="statistique_stock_int_day_article",
    ),
    #############################################################################################
    path(
        "get-statistique_price_stock_int_year/",
        Statistique_price_stock_int_retrieve_year,
        name="statistique_price_stock_int_year",
    ),
    path(
        "get-statistique_price_stock_int_day/<int:year>/<int:month>/",
        Statistique_price_stock_int_retrieve_day,
        name="statistique_price_stock_int_day",
    ),
    path(
        "get-statistique_price_stock_int_month_article/<int:year>/<str:article>/",
        Statistique_price_stock_int_retrieve_month_article,
        name="statistique_price_stock_int_month_article",
    ),
    path(
        "get-statistique_price_stock_int_year_article/<str:article>/",
        Statistique_price_stock_int_retrieve_year_article,
        name="statistique_price_stock_int_year_article",
    ),
    path(
        "get-statistique_price_stock_int_day_article/<int:year>/<int:month>/<str:article>/",
        Statistique_price_stock_int_retrieve_day_article,
        name="statistique_price_stock_int_day_article",
    ),
    path(
        "get-statistique_price_stock_int_month_category/<int:year>/<str:category>/",
        Statistique_price_stock_int_retrieve_month_category,
        name="statistique_price_stock_int_month_category",
    ),
    path(
        "get-statistique_price_stock_int_year_category/<str:category>/",
        Statistique_price_stock_int_retrieve_year_category,
        name="statistique_price_stock_int_year_category",
    ),
    path(
        "get-statistique_price_stock_int_day_category/<int:year>/<int:month>/<str:category>/",
        Statistique_price_stock_int_retrieve_day_category,
        name="statistique_price_stock_int_day_category",
    ),
]
