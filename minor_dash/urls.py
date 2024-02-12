from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *
from django.urls  import include

from rest_framework.routers import DefaultRouter, SimpleRouter


router = SimpleRouter()
router.register('settings', SettingViewSet, basename='settings')


urlpatterns = [
    # Urls des differentes entrées
    #  
    path('', include(router.urls)),
    path('get-statistique_stock_int_month/<int:year>/', Statistique_total_stock_int_retrieve_month),
    path('get-statistique_stock_int_year/', Statistique_total_stock_int_retrieve_year),
    path('get-statistique_stock_int_day/<int:year>/<int:month>/', Statistique_total_stock_int_retrieve_day),
    
    #Par articles
    
    path('get-statistique_stock_int_month_article/<int:year>/<str:article>/', Statistique_total_stock_int_retrieve_month_article),
    path('get-statistique_stock_int_year_article/<str:article>/', Statistique_total_stock_int_retrieve_year_article),
    path('get-statistique_stock_int_day_article/<int:year>/<int:month>/<str:article>/', Statistique_total_stock_int_retrieve_day_article),

    path('get-statistique_stock_category_int_month/<int:year>/', Statistique_total_category_stock_int_retrieve_month),
    path('get-statistique_stock_category_int_year/', Statistique_total_category_stock_int_retrieve_year),
    path('get-statistique_stock_category_int_day/<int:year>/<int:month>/', Statistique_total_category_stock_int_retrieve_day),
    
    # Par categories
    
    path('get-statistique_stock_int_month_category/<int:year>/<str:category>/', Statistique_total_stock_int_retrieve_month_category),
    path('get-statistique_stock_int_year_category/<str:category>/', Statistique_total_stock_int_retrieve_year_category),
    path('get-statistique_stock_int_day_category/<int:year>/<int:month>/<str:category>/', Statistique_total_stock_int_retrieve_day_category),
    
    
    
    path('get-list_in_calendre_week_and_day/<str:filter_by>/<int:year>/<int:month>/', Statistique_calendre_retrieve_week_and_day),
    path('get-list_in_calendre_month_and_year/<str:filter_by>/<int:year>/', Statistique_calendre_retrieve_year_and_month),
    
    
    # Par prix
    path('get-statistique_price_general_stock_int_month/<int:year>/', Statistique_price_general_stock_int_retrieve_month),
    path('get-statistique_price_general_stock_int_year/', Statistique_price_general_stock_int_retrieve_year),
    path('get-statistique_price_general_stock_int_day/<int:year>/<int:month>/', Statistique_price_general_stock_int_retrieve_day),
    
    
    path('get-statistique_price_stock_int_month/<int:year>/', Statistique_price_stock_int_retrieve_month),
    path('get-statistique_price_stock_int_year/', Statistique_price_stock_int_retrieve_year),
    path('get-statistique_price_stock_int_day/<int:year>/<int:month>/', Statistique_price_stock_int_retrieve_day),

    path('get-statistique_price_stock_int_month_article/<int:year>/<str:article>/', Statistique_price_stock_int_retrieve_month_article),
    path('get-statistique_price_stock_int_year_article/<str:article>/', Statistique_price_stock_int_retrieve_year_article),
    path('get-statistique_price_stock_int_day_article/<int:year>/<int:month>/<str:article>/', Statistique_price_stock_int_retrieve_day_article),
    
    path('get-statistique_price_stock_int_month_category/<int:year>/<str:category>/', Statistique_price_stock_int_retrieve_month_category),
    path('get-statistique_price_stock_int_year_category/<str:category>/', Statistique_price_stock_int_retrieve_year_category),
    path('get-statistique_price_stock_int_day_category/<int:year>/<int:month>/<str:category>/', Statistique_price_stock_int_retrieve_day_category),

    
    # Par litre
    path('get-statistique_littre_general_stock_int_month/<int:year>/', Statistique_littre_general_stock_int_retrieve_month),
    path('get-statistique_littre_general_stock_int_year/', Statistique_littre_general_stock_int_retrieve_year),
    path('get-statistique_littre_general_stock_int_day/<int:year>/<int:month>/', Statistique_littre_general_stock_int_retrieve_day),
    
   
    path('get-statistique_littre_stock_int_month/<int:year>/', Statistique_littre_stock_int_retrieve_month),
    path('get-statistique_littre_stock_int_year/', Statistique_littre_stock_int_retrieve_year),
    path('get-statistique_littre_stock_int_day/<int:year>/<int:month>/', Statistique_littre_stock_int_retrieve_day),

    path('get-statistique_littre_stock_int_month_article/<int:year>/<str:article>/', Statistique_littre_stock_int_retrieve_month_article),
    path('get-statistique_littre_stock_int_year_article/<str:article>/', Statistique_littre_stock_int_retrieve_year_article),
    path('get-statistique_littre_stock_int_day_article/<int:year>/<int:month>/<str:article>/', Statistique_littre_stock_int_retrieve_day_article),

    path('get-statistique_littre_stock_int_month_category/<int:year>/<str:category>/', Statistique_littre_stock_int_retrieve_month_category),
    path('get-statistique_littre_stock_int_year_category/<str:category>/', Statistique_littre_stock_int_retrieve_year_category),
    path('get-statistique_littre_stock_int_day_category/<int:year>/<int:month>/<str:category>/', Statistique_littre_stock_int_retrieve_day_category),

    
    
    
    
    
    # Urls des differentes sorties
    
    # Par general
    path('get-statistique_stock_out_month/<int:year>/', Statistique_total_stock_out_retrieve_month),
    path('get-statistique_stock_out_year/', Statistique_total_stock_out_retrieve_year),
    path('get-statistique_stock_out_day/<int:year>/<int:month>/', Statistique_total_stock_out_retrieve_day),
    
    
    # Par articles
    path('get-statistique_stock_out_month_article/<int:year>/<str:article>/', Statistique_total_stock_out_retrieve_month_article),
    path('get-statistique_stock_out_year_article/<str:article>/', Statistique_total_stock_out_retrieve_year_article),
    path('get-statistique_stock_out_day_article/<int:year>/<int:month>/<str:article>/', Statistique_total_stock_out_retrieve_day_article),
 
    # Par categories
    path('get-statistique_stock_category_out_month/<int:year>/', Statistique_total_category_stock_out_retrieve_month),
    path('get-statistique_stock_category_out_year/', Statistique_total_category_stock_out_retrieve_year),
    path('get-statistique_stock_category_out_day/<int:year>/<int:month>/', Statistique_total_category_stock_out_retrieve_day),
    
    path('get-statistique_stock_out_month_category/<int:year>/<str:category>/', Statistique_total_stock_out_retrieve_month_category),
    path('get-statistique_stock_out_year_category/<str:category>/', Statistique_total_stock_out_retrieve_year_category),
    path('get-statistique_stock_out_day_category/<int:year>/<int:month>/<str:category>/', Statistique_total_stock_out_retrieve_day_category),
    
    
    # Par prix
    path('get-statistique_price_general_stock_out_month/<int:year>/', Statistique_price_general_stock_out_retrieve_month),
    path('get-statistique_price_general_stock_out_year/', Statistique_price_general_stock_out_retrieve_year),
    path('get-statistique_price_general_stock_out_day/<int:year>/<int:month>/', Statistique_price_general_stock_out_retrieve_day),
    
    
    path('get-statistique_price_stock_out_month/<int:year>/', Statistique_price_stock_out_retrieve_month),
    path('get-statistique_price_stock_out_year/', Statistique_price_stock_out_retrieve_year),
    path('get-statistique_price_stock_out_day/<int:year>/<int:month>/', Statistique_price_stock_out_retrieve_day),

    path('get-statistique_price_stock_out_month_article/<int:year>/<str:article>/', Statistique_price_stock_out_retrieve_month_article),
    path('get-statistique_price_stock_out_year_article/<str:article>/', Statistique_price_stock_out_retrieve_year_article),
    path('get-statistique_price_stock_out_day_article/<int:year>/<int:month>/<str:article>/', Statistique_price_stock_out_retrieve_day_article),
    path('get-statistique_price_stock_out_month_category/<int:year>/<str:category>/', Statistique_price_stock_out_retrieve_month_category),
    path('get-statistique_price_stock_out_year_category/<str:category>/', Statistique_price_stock_out_retrieve_year_category),
    path('get-statistique_price_stock_out_day_category/<int:year>/<int:month>/<str:category>/', Statistique_price_stock_out_retrieve_day_category),
    
    
    #Par littre
    path('get-statistique_littre_general_stock_out_month/<int:year>/', Statistique_littre_general_stock_out_retrieve_month),
    path('get-statistique_littre_general_stock_out_year/', Statistique_littre_general_stock_out_retrieve_year),
    path('get-statistique_littre_general_stock_out_day/<int:year>/<int:month>/', Statistique_littre_general_stock_out_retrieve_day),
    
    path('get-statistique_littre_stock_out_month/<int:year>/', Statistique_littre_stock_out_retrieve_month),
    path('get-statistique_littre_stock_out_year/', Statistique_littre_stock_out_retrieve_year),
    path('get-statistique_littre_stock_out_day/<int:year>/<int:month>/', Statistique_littre_stock_out_retrieve_day),
    path('get-statistique_littre_stock_out_month_category/<int:year>/<str:category>/', Statistique_littre_stock_out_retrieve_month_category),
    path('get-statistique_littre_stock_out_year_category/<str:category>/', Statistique_littre_stock_out_retrieve_year_category),
    path('get-statistique_littre_stock_out_day_category/<int:year>/<int:month>/<str:category>/', Statistique_littre_stock_out_retrieve_day_category),
    path('get-statistique_littre_stock_out_month_article/<int:year>/<str:article>/', Statistique_littre_stock_out_retrieve_month_article),
    path('get-statistique_littre_stock_out_year_article/<str:article>/', Statistique_littre_stock_out_retrieve_year_article),
    path('get-statistique_littre_stock_out_day_article/<int:year>/<int:month>/<str:article>/', Statistique_littre_stock_out_retrieve_day_article),
    
    
]