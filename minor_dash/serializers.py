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