from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *
from django.urls  import include

urlpatterns = [
    path('get-statistique_stock_int_month/<int:year>/', Statistique_total_stock_int_retrieve_month),
    path('get-statistique_stock_int_year/', Statistique_total_stock_int_retrieve_year),
    path('get-statistique_stock_int_day/<int:year>/<int:month>/', Statistique_total_stock_int_retrieve_day),
    path('get-list_in_calendre_week_and_day/<str:filter_by>/<int:year>/<int:month>/', Statistique_calendre_retrieve_week_and_day),
    path('get-list_in_calendre_month_and_year/<str:filter_by>/<int:year>/', Statistique_calendre_retrieve_year_and_month),
    path('get-statistique_stock_out_month/<int:year>/', Statistique_total_stock_out_retrieve_month),
    path('get-statistique_stock_out_year/', Statistique_total_stock_out_retrieve_year),
    path('get-statistique_stock_out_day/<int:year>/<int:month>/', Statistique_total_stock_out_retrieve_day),
]