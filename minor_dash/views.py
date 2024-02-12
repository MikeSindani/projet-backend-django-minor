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
from django.db.models import Count,Sum
from django.db.models.functions import TruncDay
from datetime import datetime
import calendar
from calendar import monthrange
# Create your views here.


### Vues des statistiques des differentes entrées
# 
# Ces vues retournes les nombre des differentes entrées seulement chronologiquement(Year, Month, Day)  
@api_view(['GET'])
def Statistique_total_stock_int_retrieve_month(request, year):
    total_articles = InventoryInto.objects.filter(
        date_modification__year=year
    ).annotate(
    month=ExtractMonth('date_modification')).values('month').annotate(
        total=Sum('quantity')
    ).order_by('month')

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
    total_articles = InventoryInto.objects.all().annotate(year=ExtractYear('date_modification'),).values('year').annotate(total=Sum('quantity')).order_by('year')
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
    date_modification__year=year, date_modification__month=month).annotate(
    day=ExtractDay('date_modification'),).values('day').annotate(total=Sum('quantity')).order_by('day')
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




# Ces vues retournes les nombre des differentes entrées chronologiquement et par article
# 
# 
# 
# 
# 
#   

@api_view(['GET'])
def Statistique_total_stock_int_retrieve_month_article(request, year, article):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryInto.objects.filter(
    date_modification__year=year, id_article__designation=article).annotate(
    month=ExtractMonth('date_modification'),).values('month').annotate(total=Sum('quantity')).order_by('month')
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
def Statistique_total_stock_int_retrieve_year_article(request, article):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryInto.objects.filter(id_article__designation=article).annotate(year=ExtractYear('date_modification'),).values('year').annotate(total=Sum('quantity')).order_by('year')
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
def Statistique_total_stock_int_retrieve_day_article(request, year, month, article):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryInto.objects.filter(
    date_modification__year=year, date_modification__month=month, id_article__designation=article).annotate(
    day=ExtractDay('date_modification'),).values('day').annotate(total=Sum('quantity')).order_by('day')
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




# Ces vues retournes les nombre des differentes entrées chronologiquement et par catégorie
# 
# 
# 
# 
# 
#   

@api_view(['GET'])
def Statistique_total_category_stock_int_retrieve_month(request, year):

# Supposons que vous ayez un modèle Article avec une date de création
    entries = InventoryInto.objects.filter(date_modification__year=year).annotate(month=ExtractMonth('date_modification'),).values('month','id_article__id_category__name').annotate(total=Count('id'))

        # Formater les données dans le format souhaité
    result = {}
    print(entries)
    for entry in entries:
        category = entry['id_article__id_category__name']
        month = entry['month']
        total = entry['total']
        if category not in result:
            result[category] = [{'month': month, 'total': total}]
            
        elif category in result:
            result[category] += [{'month': month, 'total': total}]
            #result[category]['total'] += total
            
    response_data = {
        "status": "success",
        "data": result,
        "count": len(result),
        "message": "Data retrieved successfully"
    }
    
    return Response(response_data, status=status.HTTP_200_OK)



@api_view(['GET'])
def Statistique_total_category_stock_int_retrieve_year(request):

# Supposons que vous ayez un modèle Article avec une date de création
    entries = InventoryInto.objects.all().annotate(year=ExtractYear('date_modification'),).values('year','id_article__id_category__name').annotate(total=Count('id'))

        # Formater les données dans le format souhaité
    result = {}
    print(entries)
    for entry in entries:
        category = entry['id_article__id_category__name']
        year = entry['year']
        total = entry['total']
        if category not in result:
            result[category] = [{'year': year, 'total': total}]
            
        elif category in result:
            result[category] += [{'year': year, 'total': total}]
            #result[category]['total'] += total
            
    response_data = {
        "status": "success",
        "data": result,
        "count": len(result),
        "message": "Data retrieved successfully"
    }
    
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def Statistique_total_category_stock_int_retrieve_day(request, year, month):

# Supposons que vous ayez un modèle Article avec une date de création
    entries = InventoryInto.objects.filter(date_modification__year=year, date_modification__month=month).annotate(day=ExtractDay('date_modification'),).values('day','id_article__id_category__name').annotate(total=Count('id'))

        # Formater les données dans le format souhaité
    result = {}
    for entry in entries:
        category = entry['id_article__id_category__name']
        day = entry['day']
        total = entry['total']
        if category not in result:
            result[category] = [{'day': day, 'total': total}]
            
        elif category in result:
            result[category] += [{'day': day, 'total': total}]
            #result[category]['total'] += total
            
    response_data = {
        "status": "success",
        "data": result,
        "count": len(result),
        "message": "Data retrieved successfully"
    }
    
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def Statistique_total_stock_int_retrieve_month_category(request, year, category):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryInto.objects.filter(
    date_modification__year=year, id_article__id_category__name=category).annotate(
    month=ExtractMonth('date_modification'),).values('month').annotate(total=Sum('quantity')).order_by('month')
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
def Statistique_total_stock_int_retrieve_year_category(request, category):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryInto.objects.filter(id_article__id_category__name=category).annotate(year=ExtractYear('date_modification'),).values('year').annotate(total=Sum('quantity')).order_by('year')
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
def Statistique_total_stock_int_retrieve_day_category(request, year, month, category):
    total_articles = InventoryInto.objects.filter(
    date_modification__year=year, date_modification__month=month, id_article__id_category__name=category).annotate(
    day=ExtractDay('date_modification'),).values('day').annotate(total=Count('quantity')).order_by('day')
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
        start_of_month = datetime(year=year,month=month,day=1).replace(day=1)
        end_of_month = calendar.monthrange(start_of_month.year, start_of_month.month)
        end_of_month = start_of_month.replace(day=end_of_month[1])
        creation_days = InventoryInto.objects.filter(
        date_modification__range=(start_of_month, end_of_month)
        ).annotate(
        day=ExtractDay('date_modification'),
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
        date_modification__range=(start_of_month, end_of_month)
        ).annotate(
        week=ExtractWeek('date_modification'),
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
        total_articles = InventoryInto.objects.all().annotate(year=ExtractYear('date_modification')).values('year').order_by('year').distinct()
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
        date_modification__year=year).annotate(
        month=ExtractMonth('date_modification'),).values('month').order_by('month').distinct()
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





# ---------------------------------------------------------------- Pour les prix
# Ces vues retournes les nombre des differentes entrées seulement chronologiquement(Year, Month, Day)  

# Grand general

from django.db.models import Sum, ExtractMonth
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import InventoryInto, Setting
from .serializers import ArticleSerializer

@api_view(['GET'])
def Statistique_price_general_stock_int_retrieve_month(request, year):
    # Retrieve the latest setting to get the current currency
    latest_setting = Setting.objects.latest('id')
    current_currency = latest_setting.currency

    # Filter the InventoryInto objects by the current currency and the given year
    total_articles = InventoryInto.objects.filter(
        date_modification__year=year,
        currency=current_currency  # Assuming InventoryInto has a 'currency' field
    ).annotate(
        month=ExtractMonth('date_modification')
    ).values('month').annotate(
        total=Sum('price_used_by_entreprise')
    ).order_by('month')

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
def Statistique_price_general_stock_int_retrieve_year(request):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryInto.objects.all().annotate(year=ExtractYear('date_modification'),).values('year').annotate(total=Sum('price_used_by_entreprise')).order_by('year')
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
def Statistique_price_general_stock_int_retrieve_day(request, year, month):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryInto.objects.filter(
    date_modification__year=year, date_modification__month=month).annotate(
    day=ExtractDay('date_modification'),).values('day').annotate(total=Sum('price_used_by_entreprise')).order_by('day')
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





# Petit general
@api_view(['GET'])
def Statistique_price_stock_int_retrieve_month(request, year):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryInto.objects.filter(
    date_modification__year=2023).annotate(
    month=ExtractMonth('date_modification')).values('month', 'id_article__id_category__name').annotate(total=Sum('price_used_by_entreprise')).order_by('month')
    serializer = ArticlePriceSerializer(total_articles, many=True)
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
def Statistique_price_stock_int_retrieve_year(request):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryInto.objects.all().annotate(year=ExtractYear('date_modification'),).values('year', 'id_article__id_category__name').annotate(total=Sum('price_used_by_entreprise')).order_by('year')
    serializer = ArticlePriceSerializerYear(total_articles, many=True)
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
def Statistique_price_stock_int_retrieve_day(request, year, month):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryInto.objects.filter(
    date_modification__year=year, date_modification__month=month).annotate(
    day=ExtractDay('date_modification'),).values('day', 'id_article__id_category__name').annotate(total=Sum('price_used_by_entreprise')).order_by('day')
    print(total_articles)
    serializer = ArticlePriceSerializerDay(total_articles, many=True)
    data = serializer.data
    total_data = len(serializer.data)

    response_data = {
        "status": "success",
        "data": data,
        "count": total_data,
        "message": "Data retrieved successfully"
    }
    return Response(response_data, status=status.HTTP_200_OK)



################################################################ Pour les prix
# Ces vues retournes les nombre des differentes entrées chronologiquement et par article
# 
# 
# 
# 
# 
#   

@api_view(['GET'])
def Statistique_price_stock_int_retrieve_month_article(request, year, article):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryInto.objects.filter(
    date_modification__year=year, id_article__designation=article).annotate(
    month=ExtractMonth('date_modification'),).values('month', 'id_article__id_category__name').annotate(total=Sum('price_used_by_entreprise')).order_by('month')
    print(total_articles)
    serializer = ArticlePriceSerializer(total_articles, many=True)
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
def Statistique_price_stock_int_retrieve_year_article(request, article):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryInto.objects.filter(id_article__designation=article).annotate(year=ExtractYear('date_modification'),).values('year', 'id_article__id_category__name').annotate(total=Sum('price_used_by_entreprise')).order_by('year')
    print(total_articles)
    serializer = ArticlePriceSerializerYear(total_articles, many=True)
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
def Statistique_price_stock_int_retrieve_day_article(request, year, month, article):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryInto.objects.filter(
    date_modification__year=year, date_modification__month=month, id_article__designation=article).annotate(
    day=ExtractDay('date_modification'),).values('day', 'id_article__id_category__name').annotate(total=Sum('price_used_by_entreprise')).order_by('day')
    print(total_articles)
    serializer = ArticlePriceSerializerDay(total_articles, many=True)
    data = serializer.data
    total_data = len(serializer.data)

    response_data = {
        "status": "success",
        "data": data,
        "count": total_data,
        "message": "Data retrieved successfully"
    }
    return Response(response_data, status=status.HTTP_200_OK)


################################################################ Pour les prix

# Ces vues retournes les nombre des differentes entrées chronologiquement et par catégorie
# 
# 
# 
# 
# 
#   

@api_view(['GET'])
def Statistique_price_stock_int_retrieve_month_category(request, year, category):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryInto.objects.filter(
    date_modification__year=year, id_article__id_category__name=category).annotate(
    month=ExtractMonth('date_modification'),).values('month', 'id_article__id_category__name').annotate(total=Sum('price_used_by_entreprise')).order_by('month')
    print(total_articles)
    serializer = ArticlePriceSerializer(total_articles, many=True)
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
def Statistique_price_stock_int_retrieve_year_category(request, category):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryInto.objects.filter(id_article__id_category__name=category).annotate(year=ExtractYear('date_modification'),).values('year', 'id_article__id_category__name').annotate(total=Sum('price_used_by_entreprise')).order_by('year')
    print(total_articles)
    serializer = ArticlePriceSerializerYear(total_articles, many=True)
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
def Statistique_price_stock_int_retrieve_day_category(request, year, month, category):
    total_articles = InventoryInto.objects.filter(
    date_modification__year=year, date_modification__month=month, id_article__id_category__name=category).annotate(
    day=ExtractDay('date_modification'),).values('day', 'id_article__id_category__name').annotate(total=Sum('price_used_by_entreprise')).order_by('day')
    print(total_articles)
    serializer = ArticlePriceSerializerDay(total_articles, many=True)
    data = serializer.data
    total_data = len(serializer.data)

    response_data = {
        "status": "success",
        "data": data,
        "count": total_data,
        "message": "Data retrieved successfully"
    }
    return Response(response_data, status=status.HTTP_200_OK)


################################################################ Pour les littres

# Grand general

@api_view(['GET'])
def Statistique_littre_general_stock_int_retrieve_month(request, year):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryInto.objects.filter(
    date_modification__year=year).annotate(
    month=ExtractMonth('date_modification')).values('month').annotate(total=Sum('capacity')).order_by('month')
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
def Statistique_littre_general_stock_int_retrieve_year(request):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryInto.objects.all().annotate(year=ExtractYear('date_modification'),).values('year').annotate(total=Sum('capacity')).order_by('year')
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
def Statistique_littre_general_stock_int_retrieve_day(request, year, month):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryInto.objects.filter(
    date_modification__year=year, date_modification__month=month).annotate(
    day=ExtractDay('date_modification'),).values('day').annotate(total=Sum('capacity')).order_by('day')
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





# Petit general
@api_view(['GET'])
def Statistique_littre_stock_int_retrieve_month(request, year):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryInto.objects.filter(
    date_modification__year=year).annotate(
    month=ExtractMonth('date_modification')).values('month', 'id_article__id_category__name').annotate(total=Sum('capacity')).order_by('month')
    serializer = ArticlePriceSerializer(total_articles, many=True)
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
def Statistique_littre_stock_int_retrieve_year(request):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryInto.objects.all().annotate(year=ExtractYear('date_modification'),).values('year', 'id_article__id_category__name').annotate(total=Sum('capacity')).order_by('year')
    serializer = ArticlePriceSerializerYear(total_articles, many=True)
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
def Statistique_littre_stock_int_retrieve_day(request, year, month):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryInto.objects.filter(
    date_modification__year=year, date_modification__month=month).annotate(
    day=ExtractDay('date_modification'),).values('day', 'id_article__id_category__name').annotate(total=Sum('capacity')).order_by('day')
    print(total_articles)
    serializer = ArticlePriceSerializerDay(total_articles, many=True)
    data = serializer.data
    total_data = len(serializer.data)

    response_data = {
        "status": "success",
        "data": data,
        "count": total_data,
        "message": "Data retrieved successfully"
    }
    return Response(response_data, status=status.HTTP_200_OK)


# Selon l'article

@api_view(['GET'])
def Statistique_littre_stock_int_retrieve_month_article(request, year, article):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryInto.objects.filter(
    date_modification__year=year, id_article__designation=article).annotate(
    month=ExtractMonth('date_modification'),).values('month', 'id_article__id_category__name').annotate(total=Sum('capacity')).order_by('month')
    print(total_articles)
    serializer = ArticlePriceSerializer(total_articles, many=True)
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
def Statistique_littre_stock_int_retrieve_year_article(request, article):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryInto.objects.filter(id_article__designation=article).annotate(year=ExtractYear('date_modification'),).values('year', 'id_article__id_category__name').annotate(total=Sum('capacity')).order_by('year')
    print(total_articles)
    serializer = ArticlePriceSerializerYear(total_articles, many=True)
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
def Statistique_littre_stock_int_retrieve_day_article(request, year, month, article):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryInto.objects.filter(
    date_modification__year=year, date_modification__month=month, id_article__designation=article).annotate(
    day=ExtractDay('date_modification'),).values('day', 'id_article__id_category__name').annotate(total=Sum('capacity')).order_by('day')
    print(total_articles)
    serializer = ArticlePriceSerializerDay(total_articles, many=True)
    data = serializer.data
    total_data = len(serializer.data)

    response_data = {
        "status": "success",
        "data": data,
        "count": total_data,
        "message": "Data retrieved successfully"
    }
    return Response(response_data, status=status.HTTP_200_OK)


# Selon la catégorie

@api_view(['GET'])
def Statistique_littre_stock_int_retrieve_month_category(request, year, category):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryInto.objects.filter(
    date_modification__year=year, id_article__id_category__name=category).annotate(
    month=ExtractMonth('date_modification'),).values('month', 'id_article__id_category__name').annotate(total=Sum('capacity')).order_by('month')
    print(total_articles)
    serializer = ArticlePriceSerializer(total_articles, many=True)
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
def Statistique_littre_stock_int_retrieve_year_category(request, category):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryInto.objects.filter(id_article__id_category__name=category).annotate(year=ExtractYear('date_modification'),).values('year', 'id_article__id_category__name').annotate(total=Sum('capacity')).order_by('year')
    print(total_articles)
    serializer = ArticlePriceSerializerYear(total_articles, many=True)
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
def Statistique_littre_stock_int_retrieve_day_category(request, year, month, category):
    total_articles = InventoryInto.objects.filter(
    date_modification__year=year, date_modification__month=month, id_article__id_category__name=category).annotate(
    day=ExtractDay('date_modification'),).values('day', 'id_article__id_category__name').annotate(total=Sum('capacity')).order_by('day')
    print(total_articles)
    serializer = ArticlePriceSerializerDay(total_articles, many=True)
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
        start_of_month = datetime(year=year,month=month,day=1).replace(day=1)
        end_of_month = calendar.monthrange(start_of_month.year, start_of_month.month)
        end_of_month = start_of_month.replace(day=end_of_month[1])
        creation_days = InventoryInto.objects.filter(
        date_modification__range=(start_of_month, end_of_month)
        ).annotate(
        day=ExtractDay('date_modification'),
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
        date_modification__range=(start_of_month, end_of_month)
        ).annotate(
        week=ExtractWeek('date_modification'),
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
        total_articles = InventoryInto.objects.all().annotate(year=ExtractYear('date_modification')).values('year').order_by('year').distinct()
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
        date_modification__year=year).annotate(
        month=ExtractMonth('date_modification'),).values('month').order_by('month').distinct()
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

#############




### Vues des statistiques des differentes sorties
# 
# 

@api_view(['GET'])
def Statistique_total_stock_out_retrieve_month(request, year):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryOut.objects.filter(
    date_modification__year=year).annotate(
    month=ExtractMonth('date_modification'),).values('month').annotate(total=Sum('quantity')).order_by('month')
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
    total_articles = InventoryOut.objects.all().annotate(year=ExtractYear('date_modification')).values('year').annotate(total=Sum('quantity')).order_by('year')
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
    date_modification__year=year, date_modification__month=month).annotate(
    day=ExtractDay('date_modification'),).values('day').annotate(total=Sum('quantity')).order_by('day')
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





# Ces vues retournes les nombre des differentes sorties chronologiquement et par article
# 
# 
# 
# 
# 
#   

@api_view(['GET'])
def Statistique_total_stock_out_retrieve_month_article(request, year, article):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryOut.objects.filter(
    date_modification__year=year, id_inventory_into__id_article__designation=article).annotate(
    month=ExtractMonth('date_modification'),).values('month').annotate(total=Sum('quantity')).order_by('month')
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
def Statistique_total_stock_out_retrieve_year_article(request, article):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryOut.objects.filter(id_inventory_into__id_article__designation=article).annotate(year=ExtractYear('date_modification'),).values('year').annotate(total=Sum('quantity')).order_by('year')
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
def Statistique_total_stock_out_retrieve_day_article(request, year, month, article):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryOut.objects.filter(
    date_modification__year=year, date_modification__month=month, id_inventory_into__id_article__designation=article).annotate(
    day=ExtractDay('date_modification'),).values('day').annotate(total=Sum('quantity')).order_by('day')
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
def Statistique_total_category_stock_out_retrieve_month(request, year):

# Supposons que vous ayez un modèle Article avec une date de création
    entries = InventoryOut.objects.filter(date_modification__year=year).annotate(month=ExtractMonth('date_modification'),).values('month','id_inventory_into__id_article__id_category__name').annotate(total=Count('id'))

        # Formater les données dans le format souhaité
    result = {}
    print(entries)
    for entry in entries:
        category = entry['id_inventory_into__id_article__id_category__name']
        month = entry['month']
        total = entry['total']
        if category not in result:
            result[category] = [{'month': month, 'total': total}]
            
        elif category in result:
            result[category] += [{'month': month, 'total': total}]
            #result[category]['total'] += total
    
    response_data = {
        "status": "success",
        "data": result,
        "count": len(result),
        "message": "Data retrieved successfully"
    }
    
    return Response(response_data, status=status.HTTP_200_OK)



@api_view(['GET'])
def Statistique_total_category_stock_out_retrieve_year(request):

# Supposons que vous ayez un modèle Article avec une date de création
    entries = InventoryOut.objects.all().annotate(year=ExtractYear('date_modification'),).values('year','id_inventory_into__id_article__id_category__name').annotate(total=Count('id'))

        # Formater les données dans le format souhaité
    result = {}
    print(entries)
    for entry in entries:
        category = entry['id_inventory_into__id_article__id_category__name']
        year = entry['year']
        total = entry['total']
        if category not in result:
            result[category] = [{'year': year, 'total': total}]
            
        elif category in result:
            result[category] += [{'year': year, 'total': total}]
            #result[category]['total'] += total
            
    response_data = {
        "status": "success",
        "data": result,
        "count": len(result),
        "message": "Data retrieved successfully"
    }
    
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def Statistique_total_category_stock_out_retrieve_day(request, year, month):

# Supposons que vous ayez un modèle Article avec une date de création
    entries = InventoryOut.objects.filter(date_modification__year=year, date_modification__month=month).annotate(day=ExtractDay('date_modification'),).values('day','id_inventory_into__id_article__id_category__name').annotate(total=Count('id'))

        # Formater les données dans le format souhaité
    result = {}
    for entry in entries:
        category = entry['id_inventory_into__id_article__id_category__name']
        day = entry['day']
        total = entry['total']
        if category not in result:
            result[category] = [{'day': day, 'total': total}]
            
        elif category in result:
            result[category] += [{'day': day, 'total': total}]
            #result[category]['total'] += total
            
    response_data = {
        "status": "success",
        "data": result,
        "count": len(result),
        "message": "Data retrieved successfully"
    }
    
    return Response(response_data, status=status.HTTP_200_OK)
   
   

@api_view(['GET'])
def Statistique_total_stock_out_retrieve_month_category(request, year, category):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryOut.objects.filter(
    date_modification__year=year, id_inventory_into__id_article__id_category__name=category).annotate(
    month=ExtractMonth('date_modification'),).values('month').annotate(total=Sum('quantity')).order_by('month')
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
def Statistique_total_stock_out_retrieve_year_category(request, category):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryOut.objects.filter(id_inventory_into__id_article__id_category__name=category).annotate(year=ExtractYear('date_modification'),).values('year').annotate(total=Sum('quantity')).order_by('year')
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
def Statistique_total_stock_out_retrieve_day_category(request, year, month, category):
    total_articles = InventoryOut.objects.filter(
    date_modification__year=year, date_modification__month=month, id_inventory_into__id_article__id_category__name=category).annotate(
    day=ExtractDay('date_modification'),).values('day').annotate(total=Sum ('quantity')).order_by('day')
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


################################################################ Pour les prix

# Ces vues retournes les nombre des differentes entrées chronologiquement et par catégorie
# 
# 
# 
# 
# 
# 

# Sorties General
#
#

# Grand general
@api_view(['GET'])
def Statistique_price_general_stock_out_retrieve_month(request, year):
    
# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryOut.objects.filter(date_modification__year=year).annotate(month=ExtractMonth('date_modification'),).values('month').annotate(total=Sum('id_inventory_into__price_used_by_entreprise')).order_by('month')
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
def Statistique_price_general_stock_out_retrieve_year(request):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryOut.objects.all().annotate(year=ExtractYear('date_modification'),).values('year').annotate(total=Sum('id_inventory_into__price_used_by_entreprise')).order_by('year')
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
def Statistique_price_general_stock_out_retrieve_day(request, year, month):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryOut.objects.filter(date_modification__year=year, date_modification__month=month).annotate(day=ExtractDay('date_modification'),).values('day').annotate(total=Sum('id_inventory_into__price_used_by_entreprise')).order_by('day')
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






# Petit general

@api_view(['GET'])
def Statistique_price_stock_out_retrieve_month(request, year):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryOut.objects.filter(date_modification__year=year).annotate(month=ExtractMonth('date_modification'),).values('month', 'id_inventory_into__id_article__id_category__name').annotate(total=Sum('id_inventory_into__price_used_by_entreprise')).order_by('month')
    serializer = ArticlePriceOutSerializer(total_articles, many=True)
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
def Statistique_price_stock_out_retrieve_year(request):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryOut.objects.all().annotate(year=ExtractYear('date_modification'),).values('year', 'id_inventory_into__id_article__id_category__name').annotate(total=Sum('id_inventory_into__price_used_by_entreprise')).order_by('year')
    serializer = ArticlePriceOutSerializerYear(total_articles, many=True)
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
def Statistique_price_stock_out_retrieve_day(request, year, month):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryOut.objects.filter(date_modification__year=year, date_modification__month=month).annotate(day=ExtractDay('date_modification'),).values('day', 'id_inventory_into__id_article__id_category__name').annotate(total=Sum('id_inventory_into__price_used_by_entreprise')).order_by('day')
    serializer = ArticlePriceOutSerializerDay(total_articles, many=True)
    data = serializer.data
    total_data = len(serializer.data)

    response_data = {
        "status": "success",
        "data": data,
        "count": total_data,
        "message": "Data retrieved successfully"
    }
    return Response(response_data, status=status.HTTP_200_OK)

  
  
# Sorties par categories
#
#

@api_view(['GET'])
def Statistique_price_stock_out_retrieve_month_category(request, year, category):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryOut.objects.filter(
    date_modification__year=year, id_inventory_into__id_article__id_category__name=category).annotate(month=ExtractMonth('date_modification'),).values('month', 'id_inventory_into__id_article__id_category__name').annotate(total=Sum('id_inventory_into__price_used_by_entreprise')).order_by('month')
    print(total_articles)
    serializer = ArticlePriceOutSerializer(total_articles, many=True)
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
def Statistique_price_stock_out_retrieve_year_category(request, category):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryOut.objects.filter(id_inventory_into__id_article__id_category__name=category).annotate(year=ExtractYear('date_modification'),).values('year', 'id_inventory_into__id_article__id_category__name').annotate(total=Sum('id_inventory_into__price_used_by_entreprise')).order_by('year')
    print(total_articles)
    serializer = ArticlePriceOutSerializerYear(total_articles, many=True)
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
def Statistique_price_stock_out_retrieve_day_category(request, year, month, category):
    total_articles = InventoryOut.objects.filter(
    date_modification__year=year, date_modification__month=month, id_inventory_into__id_article__id_category__name=category).annotate(day=ExtractDay('date_modification'),).values('day', 'id_inventory_into__id_article__id_category__name').annotate(total=Sum('id_inventory_into__price_used_by_entreprise')).order_by('day')
    print(total_articles)
    serializer = ArticlePriceOutSerializerDay(total_articles, many=True)
    data = serializer.data
    total_data = len(serializer.data)

    response_data = {
        "status": "success",
        "data": data,
        "count": total_data,
        "message": "Data retrieved successfully"
    }
    return Response(response_data, status=status.HTTP_200_OK)



# Par articles

@api_view(['GET'])
def Statistique_price_stock_out_retrieve_month_article(request, year, article):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryOut.objects.filter(
    date_modification__year=year, id_inventory_into__id_article__designation=article).annotate(
    month=ExtractMonth('date_modification'),).values('month', 'id_inventory_into__id_article__id_category__name').annotate(total=Sum('id_inventory_into__price_used_by_entreprise')).order_by('month')
    print(total_articles)
    serializer = ArticlePriceOutSerializer(total_articles, many=True)
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
def Statistique_price_stock_out_retrieve_year_article(request, article):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryOut.objects.filter(id_inventory_into__id_article__designation=article).annotate(year=ExtractYear('date_modification'),).values('year', 'id_inventory_into__id_article__id_category__name').annotate(total=Sum('id_inventory_into__price_used_by_entreprise')).order_by('year')
    print(total_articles)
    serializer = ArticlePriceOutSerializerYear(total_articles, many=True)
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
def Statistique_price_stock_out_retrieve_day_article(request, year, month, article):
    total_articles = InventoryOut.objects.filter(
    date_modification__year=year, date_modification__month=month, id_inventory_into__id_article__designation=article).annotate(
    day=ExtractDay('date_modification'),).values('day', 'id_inventory_into__id_article__id_category__name').annotate(total=Sum('id_inventory_into__price_used_by_entreprise')).order_by('day')
    print(total_articles)
    serializer = ArticlePriceOutSerializerDay(total_articles, many=True)
    data = serializer.data
    total_data = len(serializer.data)

    response_data = {
        "status": "success",
        "data": data,
        "count": total_data,
        "message": "Data retrieved successfully"
    }
    return Response(response_data, status=status.HTTP_200_OK)







################################################################ Pour les littres


# Par General 

# Par grand géneral

@api_view(['GET'])
def Statistique_littre_general_stock_out_retrieve_month(request, year):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryOut.objects.filter(date_modification__year=year).annotate(month=ExtractMonth('date_modification'),).values('month').annotate(total=Sum('id_inventory_into__capacity')).order_by('month')
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
def Statistique_littre_general_stock_out_retrieve_year(request):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryOut.objects.all().annotate(year=ExtractYear('date_modification'),).values('year').annotate(total=Sum('id_inventory_into__capacity')).order_by('year')
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
def Statistique_littre_general_stock_out_retrieve_day(request, year, month):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryOut.objects.filter(date_modification__year=year, date_modification__month=month).annotate(day=ExtractDay('date_modification'),).values('day').annotate(total=Sum('id_inventory_into__capacity')).order_by('day')
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




# Par petit general

@api_view(['GET'])
def Statistique_littre_stock_out_retrieve_month(request, year):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryOut.objects.filter(date_modification__year=year).annotate(month=ExtractMonth('date_modification'),).values('month', 'id_inventory_into__id_article__id_category__name').annotate(total=Sum('id_inventory_into__capacity')).order_by('month')
    serializer = ArticlePriceOutSerializer(total_articles, many=True)
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
def Statistique_littre_stock_out_retrieve_year(request):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryOut.objects.all().annotate(year=ExtractYear('date_modification'),).values('year', 'id_inventory_into__id_article__id_category__name').annotate(total=Sum('id_inventory_into__capacity')).order_by('year')
    serializer = ArticlePriceOutSerializerYear(total_articles, many=True)
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
def Statistique_littre_stock_out_retrieve_day(request, year, month):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryOut.objects.filter(date_modification__year=year, date_modification__month=month).annotate(day=ExtractDay('date_modification'),).values('day', 'id_inventory_into__id_article__id_category__name').annotate(total=Sum('id_inventory_into__capacity')).order_by('day')
    serializer = ArticlePriceOutSerializerDay(total_articles, many=True)
    data = serializer.data
    total_data = len(serializer.data)

    response_data = {
        "status": "success",
        "data": data,
        "count": total_data,
        "message": "Data retrieved successfully"
    }
    return Response(response_data, status=status.HTTP_200_OK)



# Par categorie


@api_view(['GET'])
def Statistique_littre_stock_out_retrieve_month_category(request, year, category):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryOut.objects.filter(
    date_modification__year=year, id_inventory_into__id_article__id_category__name=category).annotate(month=ExtractMonth('date_modification'),).values('month', 'id_inventory_into__id_article__id_category__name').annotate(total=Sum('id_inventory_into__capacity')).order_by('month')
    print(total_articles)
    serializer = ArticlePriceOutSerializer(total_articles, many=True)
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
def Statistique_littre_stock_out_retrieve_year_category(request, category):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryOut.objects.filter(id_inventory_into__id_article__id_category__name=category).annotate(year=ExtractYear('date_modification'),).values('year', 'id_inventory_into__id_article__id_category__name').annotate(total=Sum('id_inventory_into__capacity')).order_by('year')
    print(total_articles)
    serializer = ArticlePriceOutSerializerYear(total_articles, many=True)
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
def Statistique_littre_stock_out_retrieve_day_category(request, year, month, category):
    total_articles = InventoryOut.objects.filter(
    date_modification__year=year, date_modification__month=month, id_inventory_into__id_article__id_category__name=category).annotate(day=ExtractDay('date_modification'),).values('day', 'id_inventory_into__id_article__id_category__name').annotate(total=Sum('id_inventory_into__capacity')).order_by('day')
    print(total_articles)
    serializer = ArticlePriceOutSerializerDay(total_articles, many=True)
    data = serializer.data
    total_data = len(serializer.data)

    response_data = {
        "status": "success",
        "data": data,
        "count": total_data,
        "message": "Data retrieved successfully"
    }
    return Response(response_data, status=status.HTTP_200_OK)



# Par article

def Statistique_littre_stock_out_retrieve_month_article(request, year, article):
    
# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryOut.objects.filter(
    date_modification__year=year, id_inventory_into__id_article__designation=article).annotate(
    month=ExtractMonth('date_modification'),).values('month', 'id_inventory_into__id_article__id_category__name').annotate(total=Sum('id_inventory_into__capacity')).order_by('month')
    print(total_articles)
    serializer = ArticlePriceOutSerializer(total_articles, many=True)
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
def Statistique_littre_stock_out_retrieve_year_article(request, article):

# Supposons que vous ayez un modèle Article avec une date de création
    total_articles = InventoryOut.objects.filter(id_inventory_into__id_article__designation=article).annotate(year=ExtractYear('date_modification'),).values('year', 'id_inventory_into__id_article__id_category__name').annotate(total=Sum('id_inventory_into__capacity')).order_by('year')
    print(total_articles)
    serializer = ArticlePriceOutSerializerYear(total_articles, many=True)
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
def Statistique_littre_stock_out_retrieve_day_article(request, year, month, article):
    total_articles = InventoryOut.objects.filter(
    date_modification__year=year, date_modification__month=month, id_inventory_into__id_article__designation=article).annotate(
    day=ExtractDay('date_modification'),).values('day', 'id_inventory_into__id_article__id_category__name').annotate(total=Sum('id_inventory_into__capacity')).order_by('day')
    print(total_articles)
    serializer = ArticlePriceOutSerializerDay(total_articles, many=True)
    data = serializer.data
    total_data = len(serializer.data)

    response_data = {
        "status": "success",
        "data": data,
        "count": total_data,
        "message": "Data retrieved successfully"
    }
    return Response(response_data, status=status.HTTP_200_OK)








class SettingViewSet(viewsets.ModelViewSet):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer
    # a ajouter manuelement partout 
    #pagination_class = CustomPagination
    #authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]
    #permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().last()
        serializer = self.get_serializer(queryset)
        data = serializer.data
        total_data = 1  # Get the total number of data

        response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "message": "Data retrieved successfully"
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()#id_UserAgent=request.user)
                return Response({"status": "success", "data": serializer.data, "message": "Data added successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": "error", "data": serializer.errors, "message": "Data error!"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()#id_UserAgent=request.user)
                return Response({"status": "success", "data": serializer.data, "message": "Data updated successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": serializer.errors, "message": "Update error!"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
            instance = self.get_object()
            #instance.id_UserAgent= request.user
            instance.save()
            instance.delete()
            return Response({"status": "success", "message": "Data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)





