from .models import Setting
from rest_framework import serializers
from minor_asset.models import *
from users.models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db.models import Sum


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
          'month': instance['month'],
          'total': instance['total']
      }

class ArticleCategoryGeneralSerializer(serializers.ModelSerializer):
  month = serializers.DateField()
  category = serializers.CharField()
  total = serializers.IntegerField()

  def to_representation(self, instance):
      return {
          'month': instance['month'],
          'total': instance['total'],
          'category': instance['category'],
      }

class ArticleSerializerYear(serializers.ModelSerializer):
  year = serializers.DateField()
  total = serializers.IntegerField()

  def to_representation(self, instance):
      return {
          'year': instance['year'],
          'total': instance['total']
      }

class ArticleSerializerDay(serializers.ModelSerializer):
  day = serializers.DateField()
  total = serializers.IntegerField()

  def to_representation(self, instance):
      return {
          'day': instance['day'],
          'total': instance['total']
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
          'month': instance['month'],
          'total': instance['total'],
          'titre': instance['id_article__id_category__name'],
      }

class ArticlePriceSerializerYear(serializers.ModelSerializer):
  total = serializers.DecimalField(max_digits=10, decimal_places=4)
  year = serializers.DateField()
  id_article__id_category__name = serializers.CharField()
  
  def to_representation(self, instance):
      return {
          'year': instance['year'],
          'total': instance['total'],
          'titre': instance['id_article__id_category__name'],
      }


class ArticlePriceSerializerDay(serializers.ModelSerializer):
  total = serializers.DecimalField(max_digits=10, decimal_places=4)
  day = serializers.DateField()
  id_article__id_category__name = serializers.CharField()
  
  def to_representation(self, instance):
      return {
          'day': instance['day'],
          'total': instance['total'],
          'titre': instance['id_article__id_category__name'],
      }
      
      


class ArticlePriceOutSerializer(serializers.ModelSerializer):
  total = serializers.DecimalField(max_digits=10, decimal_places=4)
  month = serializers.DateField()
  id_inventory_into__id_article__id_category__name = serializers.CharField()
  
  def to_representation(self, instance):
      return {
          'month': instance['month'],
          'total': instance['total'],
          'titre': instance['id_inventory_into__id_article__id_category__name'],
      }

class ArticlePriceOutSerializerYear(serializers.ModelSerializer):
  total = serializers.DecimalField(max_digits=10, decimal_places=4)
  year = serializers.DateField()
  id_inventory_into__id_article__id_category__name = serializers.CharField()
  
  def to_representation(self, instance):
      return {
          'year': instance['year'],
          'total': instance['total'],
          'titre': instance['id_inventory_into__id_article__id_category__name'],
      }


class ArticlePriceOutSerializerDay(serializers.ModelSerializer):
  total = serializers.DecimalField(max_digits=10, decimal_places=4)
  day = serializers.DateField()
  id_inventory_into__id_article__id_category__name = serializers.CharField()
  
  def to_representation(self, instance):
      return {
          'day': instance['day'],
          'total': instance['total'],
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
          'month': instance['month'],
          'litre': instance['litre']
      }

class ArticleLitreSerializerYear(serializers.ModelSerializer):
  litre = serializers.DecimalField(max_digits=10, decimal_places=4)
  year = serializers.DateField()

  def to_representation(self, instance):
      return {
          'year': instance['year'],
          'litre': instance['litre']
      }

class ArticleLitreSerializerDay(serializers.ModelSerializer):
  litre = serializers.DecimalField(max_digits=10, decimal_places=4)
  day = serializers.DateField()

  def to_representation(self, instance):
      return {
          'day': instance['day'],
          'litre': instance['litre']
      }




class CalendreDaysListSerializer(serializers.ModelSerializer):
  day = serializers.DateField()
  def to_representation(self, instance):
      return {
          'value': instance['day'],
          'label': f"{instance['day']}",
      }
class CalendreMonthListSerializer(serializers.ModelSerializer):
  month = serializers.DateField()
  def to_representation(self, instance):
      return {
           'value': instance['month'],
           'label': f"{instance['month']}",
      }
class CalendreweekListSerializer(serializers.ModelSerializer):
  week = serializers.DateField()
  def to_representation(self, instance):
      return {
           'value': instance['week'],
           'label': f"{instance['week']}",
      }
  
class CalendreYearListSerializer(serializers.ModelSerializer):
  year = serializers.DateField()
  def to_representation(self, instance):
      return {
           'value': instance['year'],
           'label': f"{instance['year']}",
      }
      

class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = '__all__'