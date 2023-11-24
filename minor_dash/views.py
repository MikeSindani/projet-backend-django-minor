from django.shortcuts import render
from rest_framework import viewsets
from minor_asset.models import *
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from minor_asset.filter import *
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from rest_framework import generics, authentication
from rest_framework import permissions
from rest_framework.views import APIView
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from datetime import timedelta
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.db.models import Count
from django.db.models.functions import ExtractMonth,ExtractDay,ExtractWeek,ExtractWeekDay,ExtractYear
from django.db.models import F
from django.db.models import Count
from django.db.models.functions import TruncDay
from datetime import datetime
import calendar
from calendar import monthrange
# Create your views here.


### Vues des statistiques des differentes entrées
# 
#  
@api_view(['GET'])
def Statistique_total_stock_int_retrieve_month(request, year):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryInto.objects.filter(
    date_creation__year=2023).annotate(
    month=ExtractMonth('date_creation'),).values('month').annotate(total=Count('quantity')).order_by('month')
    print(total_articles)
    serializer = ArticleSerializer(total_articles, many=True)
    data = serializer.data
    total_data = len(serializer.data)

    response_data = {
        "status": "success",
        "data": data,
        "count": total_data,
        "message": "Data retrieved successfully"
    }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def Statistique_total_stock_int_retrieve_year(request):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryInto.objects.all().annotate(year=ExtractYear('date_creation'),).values('year').annotate(total=Count('quantity')).order_by('year')
    print(total_articles)
    serializer = ArticleSerializerYear(total_articles, many=True)
    data = serializer.data
    total_data = len(serializer.data)

    response_data = {
        "status": "success",
        "data": data,
        "count": total_data,
        "message": "Data retrieved successfully"
    }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def Statistique_total_stock_int_retrieve_day(request, year, month):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryInto.objects.filter(
    date_creation__year=year, date_creation__month=month).annotate(
    day=ExtractDay('date_creation'),).values('day').annotate(total=Count('quantity')).order_by('day')
    print(total_articles)
    serializer = ArticleSerializerDay(total_articles, many=True)
    data = serializer.data
    total_data = len(serializer.data)

    response_data = {
        "status": "success",
        "data": data,
        "count": total_data,
        "message": "Data retrieved successfully"
    }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def Statistique_calendre_retrieve_week_and_day(request,filter_by,year,month):
    # Obtenez le premier jour du mois en cours
    date = datetime.now()
    
    if(filter_by == "Days"):
         # Obtenez le dernier jour du mois en cours
        start_of_month = datetime(year,month).replace(day=1)
        end_of_month = calendar.monthrange(start_of_month.year, start_of_month.month)
        end_of_month = start_of_month.replace(day=end_of_month[1])
        creation_days = InventoryInto.objects.filter(
        date_creation__range=(start_of_month, end_of_month)
        ).annotate(
        day=ExtractDay('date_creation'),
        ).values(
        'day'
        ).order_by('day').distinct()
        print(creation_days)
        serializer = CalendreDaysListSerializer(creation_days, many=True)
        data = serializer.data
        total_data = len(serializer.data)

        response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "message": "Data retrieved successfully"
        }
    elif(filter_by == "Week"):
         # Obtenez le dernier jour du mois en cours
        start_of_month = datetime(year,month).replace(day=1)
        end_of_month = calendar.monthrange(start_of_month.year, start_of_month.month)
        end_of_month = start_of_month.replace(day=end_of_month[1])
        creation_days = InventoryInto.objects.filter(
        date_creation__range=(start_of_month, end_of_month)
        ).annotate(
        week=ExtractWeek('date_creation'),
        ).values(
        'week'
        ).order_by('week').distinct()
        print(creation_days)
        serializer = CalendreweekListSerializer(creation_days, many=True)
        data = serializer.data
        total_data = len(serializer.data)

        response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "message": "Data retrieved successfully"
        }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def Statistique_calendre_retrieve_year_and_month(request,filter_by,year):
    if(filter_by == "Years"):
        total_articles = InventoryInto.objects.all().annotate(year=ExtractYear('date_creation')).values('year').order_by('year').distinct()
        print(total_articles)
        serializer = CalendreYearListSerializer(total_articles, many=True)
        data = serializer.data
        total_data = len(serializer.data)

        response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "message": "Data retrieved successfully"}
    elif(filter_by == "Month"):
        total_articles = InventoryInto.objects.filter(
        date_creation__year=year).annotate(
        month=ExtractMonth('date_creation'),).values('month').order_by('month').distinct()
        print(total_articles)
        serializer = CalendreMonthListSerializer(total_articles, many=True)
        data = serializer.data
        total_data = len(serializer.data)
        response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "message": "Data retrieved successfully"
        }
    return Response(response_data, status=status.HTTP_200_OK)



### Vues des statistiques des differentes sorties
# 
# 

@api_view(['GET'])
def Statistique_total_stock_out_retrieve_month(request, year):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryOut.objects.filter(
    date_creation__year=year).annotate(
    month=ExtractMonth('date_creation'),).values('month').annotate(total=Count('quantity')).order_by('month')
    print(total_articles)
    serializer = ArticleSerializer(total_articles, many=True)
    data = serializer.data
    total_data = len(serializer.data)

    response_data = {
        "status": "success",
        "data": data,
        "count": total_data,
        "message": "Data retrieved successfully"
    }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def Statistique_total_stock_out_retrieve_year(request):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryOut.objects.all().annotate(year=ExtractYear('date_creation'),).values('year').annotate(total=Count('quantity')).order_by('year')
    print(total_articles)
    serializer = ArticleSerializerYear(total_articles, many=True)
    data = serializer.data
    total_data = len(serializer.data)

    response_data = {
        "status": "success",
        "data": data,
        "count": total_data,
        "message": "Data retrieved successfully"
    }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def Statistique_total_stock_out_retrieve_day(request, year, month):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryOut.objects.filter(
    date_creation__year=year, date_creation__month=month).annotate(
    day=ExtractDay('date_creation'),).values('day').annotate(total=Count('quantity')).order_by('day')
    print(total_articles)
    serializer = ArticleSerializerDay(total_articles, many=True)
    data = serializer.data
    total_data = len(serializer.data)

    response_data = {
        "status": "success",
        "data": data,
        "count": total_data,
        "message": "Data retrieved successfully"
    }
    return Response(response_data, status=status.HTTP_200_OK)







