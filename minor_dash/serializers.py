from rest_framework import serializers
from minor_asset.models import *
from users.models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db.models import Sum

class ArticleSerializer(serializers.ModelSerializer):
  month = serializers.DateField()
  total = serializers.IntegerField()

  def to_representation(self, instance):
      return {
          'month': instance['month'],
          'total': instance['total']
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