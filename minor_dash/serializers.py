from .models import Setting
from rest_framework import serializers
from minor_asset.models import *
from users.models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db.models import Sum

def number_to_month(num):
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    if num >= 1 and num <= 12:
        return months[num - 1]
    else:
        return "Invalid month number"
# Serializers for Articles by total
#
#
#
#

class ArticleSerializer(serializers.ModelSerializer):
  month = serializers.DateField()
  total = serializers.IntegerField()

  def to_representation(self, instance):
      return {
          'months': number_to_month(instance['month']),
          'value': instance['total']
      }

class ArticleCategoryGeneralSerializer(serializers.ModelSerializer):
  month = serializers.DateField()
  category = serializers.CharField()
  total = serializers.IntegerField()

  def to_representation(self, instance):
      return {
          'months': number_to_month(instance['month']),
          'value': instance['total'],
          'category': instance['category'],
      }

class ArticleSerializerYear(serializers.ModelSerializer):
  years = serializers.DateField()
  value = serializers.IntegerField()

  def to_representation(self, instance):
      return {
          'years': instance['year'],
          'value': instance['total']
      }

class ArticleSerializerDay(serializers.ModelSerializer):
  days = serializers.DateField()
  value = serializers.IntegerField()

  def to_representation(self, instance):
      return {
          'days': instance['day'],
          'value': instance['total']
      }
class ArticleSerializerMonth(serializers.ModelSerializer):
  month = serializers.DateField()
  value = serializers.IntegerField()

  def to_representation(self, instance):
      return {
          'months':  number_to_month(instance['month']),
          'value': instance['total']
      }

# Serializers for Articles by price
#
#
#
#
class ArticlePriceSerializer(serializers.ModelSerializer):
  total = serializers.DecimalField(max_digits=10, decimal_places=4)
  month = serializers.DateField()
  id_article__designation = serializers.CharField()
  id_article__id_category = serializers.CharField()
  
  def to_representation(self, instance):
      return {
          'months': number_to_month(instance['month']),
          'value': instance['total'],
          'titre': instance['id_article__id_category__name'],
      }

class ArticlePriceSerializerYear(serializers.ModelSerializer):
  total = serializers.DecimalField(max_digits=10, decimal_places=4)
  year = serializers.DateField()
  id_article__id_category__name = serializers.CharField()
  
  def to_representation(self, instance):
      return {
          'years': instance['year'],
          'value': instance['total'],
          'titre': instance['id_article__id_category__name'],
      }


class ArticlePriceSerializerDay(serializers.ModelSerializer):
  total = serializers.DecimalField(max_digits=10, decimal_places=4)
  day = serializers.DateField()
  id_article__id_category__name = serializers.CharField()
  
  def to_representation(self, instance):
      return {
          'days': instance['day'],
          'value': instance['total'],
          'titre': instance['id_article__id_category__name'],
      }
      
      


class ArticlePriceOutSerializer(serializers.ModelSerializer):
  total = serializers.DecimalField(max_digits=10, decimal_places=4)
  month = serializers.DateField()
  id_inventory_into__id_article__id_category__name = serializers.CharField()
  
  def to_representation(self, instance):
      return {
          'months': number_to_month(instance['month']),
          'value': instance['total'],
          'titre': instance['id_inventory_into__id_article__id_category__name'],
      }

class ArticlePriceOutSerializerYear(serializers.ModelSerializer):
  total = serializers.DecimalField(max_digits=10, decimal_places=4)
  year = serializers.DateField()
  id_inventory_into__id_article__id_category__name = serializers.CharField()
  
  def to_representation(self, instance):
      return {
          'years': instance['year'],
          'value': instance['total'],
          'titre': instance['id_inventory_into__id_article__id_category__name'],
      }


class ArticlePriceOutSerializerDay(serializers.ModelSerializer):
  total = serializers.DecimalField(max_digits=10, decimal_places=4)
  day = serializers.DateField()
  id_inventory_into__id_article__id_category__name = serializers.CharField()
  
  def to_representation(self, instance):
      return {
          'days': instance['day'],
          'value': instance['total'],
          'titre': instance['id_inventory_into__id_article__id_category__name'],
      }
    


# Serializers for Articles by litre
#
#
#
#
class ArticleLitreSerializer(serializers.ModelSerializer):
  litre = serializers.DecimalField(max_digits=10, decimal_places=4)
  month = serializers.DateField()

  def to_representation(self, instance):
      return {
          'months': number_to_month(instance['month']),
          'value': instance['litre']
      }

class ArticleLitreSerializerYear(serializers.ModelSerializer):
  litre = serializers.DecimalField(max_digits=10, decimal_places=4)
  year = serializers.DateField()

  def to_representation(self, instance):
      return {
          'years': instance['year'],
          'value': instance['litre']
      }

class ArticleLitreSerializerDay(serializers.ModelSerializer):
  litre = serializers.DecimalField(max_digits=10, decimal_places=4)
  day = serializers.DateField()

  def to_representation(self, instance):
      return {
          'days': instance['day'],
          'value': instance['litre']
      }




class CalendreDaysListSerializer(serializers.ModelSerializer):
  day = serializers.DateField()
  def to_representation(self, instance):
      return {
          'days': instance['day'],
          'label': f"{instance['day']}",
      }
class CalendreMonthListSerializer(serializers.ModelSerializer):
  month = serializers.DateField()
  def to_representation(self, instance):
      return {
           'months': number_to_month(instance['month']),
           'label': f"{instance['month']}",
      }
class CalendreweekListSerializer(serializers.ModelSerializer):
  week = serializers.DateField()
  def to_representation(self, instance):
      return {
           'weeks': instance['week'],
           'label': f"{instance['week']}",
      }
  
class CalendreYearListSerializer(serializers.ModelSerializer):
  year = serializers.DateField()
  def to_representation(self, instance):
      return {
           'years': instance['year'],
           'label': f"{instance['year']}",
      }
      

class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = '__all__'


class InventorySummarybyYearsAndCategorySerializer(serializers.Serializer):
    category_name = serializers.CharField(source='id_category__name')
    available_count = serializers.IntegerField()
    unavailable_count = serializers.IntegerField()
    total_quantity_in = serializers.IntegerField()
    total_quantity_out = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=20, decimal_places=2)
   
    capacity_in = serializers.DecimalField(max_digits=20, decimal_places=3, source='inventoryinto__capacity')
    weight_in = serializers.DecimalField(max_digits=20, decimal_places=3, source='inventoryinto__weight')
    capacity_out = serializers.DecimalField(max_digits=20, decimal_places=3)
    numbres_of_pieces_int = serializers.IntegerField(source='inventoryinto__numbres_of_pieces')
    numbres_of_pieces_out = serializers.IntegerField()
    year = serializers.IntegerField()
    month = serializers.IntegerField()
    day = serializers.IntegerField()
    week = serializers.IntegerField()
    #weight_out = serializers.DecimalField()

    class Meta:
        fields = ['category_name','year','day','month','week','available_count', 'unavailable_count', 'total_quantity_in', 'total_quantity_out', 'total_price','numbres_of_pieces_int','numbres_of_pieces_out', 'capacity_in', 'weight_in', 'capacity_out']

    

class InventorySummaryByArticleSerializer(serializers.Serializer):
    article_name = serializers.CharField(source='designation')
    available_count = serializers.IntegerField()
    unavailable_count = serializers.IntegerField()
    total_quantity_in = serializers.IntegerField()
    total_quantity_out = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=20, decimal_places=2)
   
    capacity_in = serializers.DecimalField(max_digits=20, decimal_places=3, source='inventoryinto__capacity')
    weight_in = serializers.DecimalField(max_digits=20, decimal_places=3, source='inventoryinto__weight')
    capacity_out = serializers.DecimalField(max_digits=20, decimal_places=3)
    numbres_of_pieces_int = serializers.IntegerField(source='inventoryinto__numbres_of_pieces')
    numbres_of_pieces_out = serializers.IntegerField()
    year = serializers.IntegerField()
    month = serializers.IntegerField()
    day = serializers.IntegerField()
    week = serializers.IntegerField()
    #weight_out = serializers.DecimalField()

    class Meta:
        fields = ['article_name','year','day','month','week', 'available_count', 'unavailable_count', 'total_quantity_in', 'total_quantity_out', 'total_price','numbres_of_pieces_int','numbres_of_pieces_out', 'capacity_in', 'weight_in', 'capacity_out']

    
class DiagnosticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnostics
        fields = ['typeMaintenance']

class MachineStatisticsSerializerForArticle(serializers.ModelSerializer):
    name_machine = serializers.CharField(max_length=200)
    category_machine = serializers.CharField(max_length=200)
    planned = serializers.IntegerField()
    actual = serializers.IntegerField()
    total = serializers.IntegerField()
    type_de_maintenance = serializers.CharField(max_length=200)
    year = serializers.IntegerField()
    month = serializers.IntegerField()
    day = serializers.IntegerField()
    class Meta:
        model = Machine
        fields = ['nom', 'planned', 'actual',"type_de_maintenance",'total',"category_machine","name_machine",'year', 'month', 'day']
    

class MachineStatisticsSerializerForCategory(serializers.ModelSerializer):
    planned = serializers.IntegerField()
    actual = serializers.IntegerField()
    total = serializers.IntegerField()
    type_de_maintenance = serializers.CharField(max_length=200)
    year = serializers.IntegerField()
    month = serializers.IntegerField()
    day = serializers.IntegerField()
    class Meta:
        model = CategorieMachine
        fields = ['nom', 'planned', 'actual',"type_de_maintenance",'total','year', 'month', 'day']

class DiagnosticsStatisticsViewSerializer(serializers.ModelSerializer):
  year= serializers.DateField()
  month = serializers.DateField()
  day = serializers.DateField()
  def to_representation(self, instance):
      return {
           'years': instance['year'],
           'months': number_to_month(instance['month']),
           'days': instance['day'],
           'value': f"{instance['count']}",
      }
class PlanifierMaintenanceSerializer(serializers.ModelSerializer):
  year= serializers.DateField()
  month = serializers.DateField()
  day = serializers.DateField()
  def to_representation(self, instance):
      return {
           'years': instance['year'],
           'months': number_to_month(instance['month']),
           'days': instance['day'],
           'value': f"{instance['count']}",
      }
  
class ValuesbyYearsPeriodSerializer(serializers.ModelSerializer):
  year= serializers.DateField()
  def to_representation(self, instance):
      return {
           'years': instance['year'],
           'value': f"{instance['count']}",
      }
  
class ValuesbyDaysPeriodSerializer(serializers.ModelSerializer):
  year= serializers.DateField()
  month = serializers.DateField()
  day = serializers.DateField()
  def to_representation(self, instance):
      return {
           'days': instance['day'],
           'value': f"{instance['count']}",
      }
class ValuesbyMonthPeriodSerializer(serializers.ModelSerializer):
  month = serializers.DateField()
  def to_representation(self, instance):
      return {    
           'months': number_to_month(instance['month']),
           'value': f"{instance['count']}",
      }


class TrackingPiecesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackingPieces
        fields = '__all__'


class InventorySummarybyCategorySerializer(serializers.Serializer):
    id_category_name = serializers.CharField(source='id_category__name')
    available_count = serializers.IntegerField()
    unavailable_count = serializers.IntegerField()
    total_quantity_in = serializers.IntegerField()
    total_quantity_out = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=20, decimal_places=2)
    capacity = serializers.DecimalField(max_digits=20, decimal_places=3, source='inventoryinto__capacity')
    weight = serializers.DecimalField(max_digits=20, decimal_places=3, source='inventoryinto__weight')
    capacity_out = serializers.DecimalField(max_digits=20, decimal_places=3)
    numbres_of_pieces_out = serializers.IntegerField()
    numbres_of_pieces = serializers.IntegerField(source='inventoryinto__numbres_of_pieces')

    class Meta:
        fields = ['id_category_name', 'available_count', 'unavailable_count', 'total_quantity_in', 'total_quantity_out', 'total_price', 'capacity', 'weight', 'capacity_out', 'numbres_of_pieces_out', 'numbres_of_pieces']
class MachineDataSerializer(serializers.ModelSerializer):
    planned = serializers.ListField(child=serializers.IntegerField())
    actual = serializers.ListField(child=serializers.IntegerField())
    #total = serializers.IntegerField()
    year = serializers.ListField(child=serializers.IntegerField())
    nom = serializers.CharField()  # Not an integer, but a string

    class Meta:
        model = Machine
        fields = ['nom', 'planned', 'actual', 'year']