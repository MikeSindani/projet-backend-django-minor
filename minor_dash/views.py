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
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication,
    TokenAuthentication,
)
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
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from django.db.models.functions import (
    ExtractMonth,
    ExtractDay,
    ExtractWeek,
    ExtractWeekDay,
    ExtractYear,
)
from django.db.models import F
from django.db.models import Count, Sum
from django.db.models.functions import TruncDay
from datetime import datetime
import calendar
from calendar import monthrange
from django.db.models import Count, Q, Sum, F
from django.db.models.functions import Coalesce
from django.db.models import DecimalField

# Create your views here.


### Vues des statistiques des differentes entrées
#
# Ces vues retournes les nombre des differentes entrées seulement chronologiquement(Year, Month, Day)
@api_view(["GET"])
def Statistique_stock_int_retrieve(request):
    period = request.query_params.get("period", "years")
    year = request.query_params.get("year", 2024)
    month = request.query_params.get("month", 1)
    categorie = request.query_params.get("category", "general")
    serializer = ""
    if categorie == "general":
        if period == "years":
            total_articles = (
                InventoryInto.objects.all()
                .annotate(year=ExtractYear("date_modification"))
                .values("year")
                .annotate(total=Sum("quantity"))
                .order_by("-year")
            )
            serializer = ArticleSerializerYear(total_articles, many=True)
        elif period == "month":
            total_articles = (
                InventoryInto.objects.filter(date_modification__year=year)
                .annotate(month=ExtractMonth("date_modification"))
                .values("month")
                .annotate(total=Sum("quantity"))
                .order_by("month")
            )
            serializer = ArticleSerializer(total_articles, many=True)
        elif period == "days":

            total_articles = (
                InventoryInto.objects.filter(date_modification__year=year, date_modification__month=month)
                .annotate(day=ExtractDay("date_modification"))
                .values("day")
                .annotate(total=Sum("quantity"))
                .order_by("day")
            )
            serializer = ArticleSerializerDay(total_articles, many=True)
    elif categorie == "expense":
            # Retrieve the latest setting to get the current currency
        latest_setting = Setting.objects.latest("id")
        current_currency = latest_setting.currency
            # Supposons que vous ayez un modèle Article avec une date de création
        if period == "days":
            total_articles = (
                InventoryInto.objects.filter(
                    date_modification__year=year,
                    date_modification__month=month,
                    currency_used_by_entreprise=current_currency,
                )
                .annotate(
                    day=ExtractDay("date_modification"),
                )
                .values("day")
                .annotate(total=Sum("price_used_by_entreprise"))
                .order_by("day")
            )
            print(total_articles)
            serializer = ArticleSerializerDay(total_articles, many=True)
        elif period == "month":
                # Supposons que vous ayez un modèle Article avec une date de création
               # Filter the InventoryInto objects by the current currency and the given year
            total_articles = (
                InventoryInto.objects.filter(
                    date_modification__year=year,
                    currency_used_by_entreprise=current_currency,  # Assuming InventoryInto has a 'currency' field
                )
                .annotate(month=ExtractMonth("date_modification"))
                .values("month")
                .annotate(total=Sum("price_used_by_entreprise"))
                .order_by("month")
            )

            serializer = ArticleSerializerMonth(total_articles, many=True)
        elif period == "years":

            total_articles = (
                InventoryInto.objects.filter(currency_used_by_entreprise=current_currency)
                .annotate(
                    year=ExtractYear("date_modification"),
                )
                .values("year")
                .annotate(total=Sum("price_used_by_entreprise"))
                .order_by("year")
            )
            serializer = ArticleSerializerYear(total_articles, many=True)
    elif categorie == "litre":
        # Retrieve the latest setting to get the current currency
        latest_setting = Setting.objects.latest('id')
        current_capacity = latest_setting.capacity
   
        if period == 'days':
            # Supposons que vous ayez un modèle Article avec une date de création
            total_articles = (
                InventoryInto.objects.filter(
                    date_modification__year=year, date_modification__month=month,unit=current_capacity
                )
                .annotate(
                    day=ExtractDay("date_modification"),
                )
                .values("day")
                .annotate(total=Sum("capacity"))
                .order_by("day")
            )
            print(total_articles)
            serializer = ArticleSerializerDay(total_articles, many=True)
        elif period == 'years':
             # Supposons que vous ayez un modèle Article avec une date de création
            total_articles = (
                InventoryInto.objects.filter(unit=current_capacity)
                .annotate(
                    year=ExtractYear("date_modification"),
                )
                .values("year")
                .annotate(total=Sum("capacity"))
                .order_by("year")
            )
            serializer = ArticleSerializerYear(total_articles, many=True)
        elif period == 'month':
            total_articles = (
                InventoryInto.objects.filter(unit=current_capacity)
                .annotate(
                    month=ExtractMonth("date_modification"),
                )
                .values("month")
                .annotate(total=Sum("capacity"))
                .order_by("month")
            )
            serializer = ArticleSerializerMonth(total_articles, many=True)

    data = serializer.data
    response_data = {
        "status": "success",
        "data": data,
        "message": "Data retrieved successfully",
    }

    return Response(response_data, status=status.HTTP_200_OK)

@api_view(["GET"])
def Statistique_stock_out_retrieve(request):

    # Supposons que vous ayez un modèle Article avec une date de création
    period = request.query_params.get("period", "years")
    year = request.query_params.get("year", 2024)
    month = request.query_params.get("month", 1)
    categorie = request.query_params.get("category", "general")
    serializer = ""
    if categorie == "general":     
        if period == "month":
            total_articles = (
                InventoryOut.objects.filter(date_modification__year=year)
                .annotate(
                    month=ExtractMonth("date_modification"),
                )
                .values("month")
                .annotate(total=Sum("quantity"))
                .order_by("month")
            )
            print(total_articles)
            serializer = ArticleSerializerMonth(total_articles, many=True)

        if period == "years":
            # Supposons que vous ayez un modèle Article avec une date de création
            total_articles = (
                InventoryOut.objects.all()
                .annotate(year=ExtractYear("date_modification"))
                .values("year")
                .annotate(total=Sum("quantity"))
                .order_by("year")
            )
            print(total_articles)
            serializer = ArticleSerializerYear(total_articles, many=True)

        if period == "days":
            total_articles = (
            InventoryOut.objects.filter(date_modification__year=year)
            .annotate(
                day=ExtractDay("date_modification"),
            )
            .values("day")
            .annotate(total=Sum("quantity"))
            .order_by("day")
        )
            print(total_articles)
            serializer = ArticleSerializerDay(total_articles, many=True)
    elif categorie == "expense":
        # Retrieve the latest setting to get the current currency
        latest_setting = Setting.objects.latest('id')
        current_currency = latest_setting.currency
        if period == 'month': 
            # Supposons que vous ayez un modèle Article avec une date de création
            total_articles = (
                InventoryOut.objects.filter(date_modification__year=year,id_inventory_into__currency_used_by_entreprise=current_currency)
                .annotate(
                    month=ExtractMonth("date_modification"),
                )
                .values("month")
                .annotate(total=Sum("id_inventory_into__price_used_by_entreprise"))
                .order_by("month")
            )
            serializer = ArticleSerializerMonth(total_articles, many=True)
        elif period == 'years':
             # Supposons que vous ayez un modèle Article avec une date de création
            total_articles = (
                InventoryOut.objects.filter(id_inventory_into__currency_used_by_entreprise=current_currency)
                .annotate(
                    year=ExtractYear("date_modification"),
                )
                .values("year")
                .annotate(total=Sum("id_inventory_into__price_used_by_entreprise"))
                .order_by("year")
            )
            serializer = ArticleSerializerYear(total_articles, many=True)
        elif period == 'days':
            # Supposons que vous ayez un modèle Article avec une date de création
            total_articles = (
                InventoryOut.objects.filter(date_modification__year=year,id_inventory_into__currency_used_by_entreprise=current_currency,date_modification__month=month)
                .annotate(
                    day=ExtractDay("date_modification"),
                )
                .values("day")
                .annotate(total=Sum("id_inventory_into__price_used_by_entreprise"))
                .order_by("day")
            )
            serializer = ArticleSerializerYear(total_articles, many=True)
    elif categorie == 'litre':
        # Retrieve the latest setting to get the current currency
        latest_setting = Setting.objects.latest('id')
        current_capacity = latest_setting.capacity
        if period == 'month':
            # Supposons que vous ayez un modèle Article avec une date de création
            total_articles = (
                InventoryOut.objects.filter(date_modification__year=year,id_inventory_into__unit=current_capacity)
                .annotate(
                    month=ExtractMonth("date_modification"),
                )
                .values("month")
                .annotate(total=Sum("id_inventory_into__capacity"))
                .order_by("month")
            )
            serializer = ArticleSerializerMonth(total_articles, many=True)
        elif period == 'years':
            # Supposons que vous ayez un modèle Article avec une date de création
            total_articles = (
                InventoryOut.objects.filter(id_inventory_into__unit=current_capacity)
                .annotate(
                    year=ExtractYear("date_modification"),
                )
                .values("year")
                .annotate(total=Sum("id_inventory_into__capacity"))
                .order_by("year")
            )
            serializer = ArticleSerializerYear(total_articles, many=True)
        elif period == "days":
            # Supposons que vous ayez un modèle Article avec une date de création
            total_articles = (
                InventoryOut.objects.filter(
                    date_modification__year=year, date_modification__month=month,id_inventory_into__unit=current_capacity
                )
                .annotate(
                    day=ExtractDay("date_modification"),
                )
                .values("day")
                .annotate(total=Sum("id_inventory_into__capacity"))
                .order_by("day")
            )
            serializer = ArticleSerializerDay(total_articles, many=True)
    data = serializer.data
    response_data = {
        "status": "success",
        "data": data,
        "message": "Data retrieved successfully",
    }
    return Response(response_data, status=status.HTTP_200_OK)

@api_view(["GET"])
def Statistique_calendre_retrieve_week_and_day(request, filter_by, year, month):
    # Obtenez le premier jour du mois en cours
    date = datetime.now()

    if filter_by == "Days":
        # Obtenez le dernier jour du mois en cours
        start_of_month = datetime(year=year, month=month, day=1).replace(day=1)
        end_of_month = calendar.monthrange(start_of_month.year, start_of_month.month)
        end_of_month = start_of_month.replace(day=end_of_month[1])
        creation_days = (
            InventoryInto.objects.filter(
                date_modification__range=(start_of_month, end_of_month)
            )
            .annotate(
                day=ExtractDay("date_modification"),
            )
            .values("day")
            .order_by("day")
            .distinct()
        )
        print(creation_days)
        serializer = CalendreDaysListSerializer(creation_days, many=True)
        data = serializer.data
        total_data = len(serializer.data)

        response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "message": "Data retrieved successfully",
        }
    elif filter_by == "Week":
        # Obtenez le dernier jour du mois en cours
        start_of_month = datetime(year, month).replace(day=1)
        end_of_month = calendar.monthrange(start_of_month.year, start_of_month.month)
        end_of_month = start_of_month.replace(day=end_of_month[1])
        creation_days = (
            InventoryInto.objects.filter(
                date_modification__range=(start_of_month, end_of_month)
            )
            .annotate(
                week=ExtractWeek("date_modification"),
            )
            .values("week")
            .order_by("week")
            .distinct()
        )
        print(creation_days)
        serializer = CalendreweekListSerializer(creation_days, many=True)
        data = serializer.data
        total_data = len(serializer.data)

        response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "message": "Data retrieved successfully",
        }
    return Response(response_data, status=status.HTTP_200_OK)

@api_view(["GET"])
def Statistique_calendre_retrieve_year_and_month(request, filter_by, year):
    if filter_by == "Years":
        total_articles = (
            InventoryInto.objects.all()
            .annotate(year=ExtractYear("date_modification"))
            .values("year")
            .order_by("year")
            .distinct()
        )
        print(total_articles)
        serializer = CalendreYearListSerializer(total_articles, many=True)
        data = serializer.data
        total_data = len(serializer.data)

        response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "message": "Data retrieved successfully",
        }
    elif filter_by == "Month":
        total_articles = (
            InventoryInto.objects.filter(date_modification__year=year)
            .annotate(
                month=ExtractMonth("date_modification"),
            )
            .values("month")
            .order_by("month")
            .distinct()
        )
        print(total_articles)
        serializer = CalendreMonthListSerializer(total_articles, many=True)
        data = serializer.data
        total_data = len(serializer.data)
        response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "message": "Data retrieved successfully",
        }
    return Response(response_data, status=status.HTTP_200_OK)



# Ces vues retournes les nombre des differentes entrées chronologiquement et par catégorie
#
#
#
#
#
#



    # Supposons que vous ayez un modèle Article avec une date de création
    entries = (
        InventoryInto.objects.filter(
            date_modification__year=year, date_modification__month=month
        )
        .annotate(
            day=ExtractDay("date_modification"),
        )
        .values("day", "id_article__id_category__name")
        .annotate(total=Count("id"))
    )

    # Formater les données dans le format souhaité
    result = {}
    for entry in entries:
        category = entry["id_article__id_category__name"]
        day = entry["day"]
        total = entry["total"]
        if category not in result:
            result[category] = [{"day": day, "total": total}]

        elif category in result:
            result[category] += [{"day": day, "total": total}]
            # result[category]['total'] += total

    response_data = {
        "status": "success",
        "data": result,
        "count": len(result),
        "message": "Data retrieved successfully",
    }

    return Response(response_data, status=status.HTTP_200_OK)

#3333333333333333333333333333333333333333333333333333333333333333333333
#
# list statistique by category 
#
#3333333333333333333333333333333333333333333333333333333333333#########
@api_view(["GET"])
def Statistique_total_stock_int_retrieve_month_category_list(request, year):

     # Obtenir le nombre d'articles disponibles et indisponibles, la quantité totale entrée et sortie, et le prix total pour chaque catégorie pour l'année spécifiée
        results = (
            Inventory.objects
            .filter(
                Q(inventoryinto__date_modification__year=year) |  # Filtre par année de création des entrées
                Q(inventoryinto__inventoryout__date_modification__year=year)  # Filtre par année de création des sorties
            ).annotate(
                available_count=Coalesce(
                    Count(
                        'inventoryinto',
                        filter=Q(inventoryinto__inventoryout__isAvailable=True),
                        distinct=True
                    ),
                    0
                ),
                unavailable_count=Coalesce(
                    Count(
                        'inventoryinto',
                        filter=Q(inventoryinto__inventoryout__isAvailable=False),
                        distinct=True
                    ),
                    0
                ),
                total_quantity_in=Coalesce(
                    Sum('inventoryinto__quantity'),
                    0
                ),
                total_quantity_out=Coalesce(
                    Sum('inventoryinto__inventoryout__quantity'),
                    0
                ),
                total_price=Coalesce(
                    Sum(F('inventoryinto__quantity') * F('inventoryinto__price')), 
                    0,
                    output_field=DecimalField()
                ),capacity_out = Coalesce(
                    Sum(F('inventoryinto__capacity') * F('inventoryinto__inventoryout__quantity')), 0,
                    output_field=DecimalField()
                ),
                numbres_of_pieces_out=Coalesce(Sum(F('inventoryinto__numbres_of_pieces') * F('inventoryinto__inventoryout__quantity')), 0,
                    output_field=DecimalField()
                ),
                year=Coalesce(
                        ExtractYear(F('inventoryinto__date_modification')),
                        ExtractYear(F('inventoryinto__inventoryout__date_modification'))
                        ,0
                    ),
                month=Coalesce(
                        ExtractMonth(F('inventoryinto__date_modification')),
                        ExtractMonth(F('inventoryinto__inventoryout__date_modification'))
                        ,0
                    ),
                day=Coalesce(
                        ExtractDay(F('inventoryinto__date_modification')),
                        ExtractDay(F('inventoryinto__inventoryout__date_modification'))
                        ,0
                    ),
                week=Coalesce(
                        ExtractWeekDay(F('inventoryinto__date_modification')),
                        ExtractWeekDay(F('inventoryinto__inventoryout__date_modification'))
                        ,0
                    )

            )
            .values('id_category__name','year','month','day','week', 'available_count', 'unavailable_count', 'total_quantity_in', 'total_quantity_out', 'total_price', 'inventoryinto__capacity', 'inventoryinto__weight', 'capacity_out','numbres_of_pieces_out','inventoryinto__numbres_of_pieces')
        )

        # Sérialiser les résultats
        serializer = InventorySummarybyYearsAndCategorySerializer(results, many=True)
        data = serializer.data 

        response_data = {
        "status": "success",
        "data": data,
        "message": "Data retrieved successfully",
        }
        return Response(response_data, status=status.HTTP_200_OK)

@api_view(["GET"])
def Statistique_total_stock_int_retrieve_year_category_list(request):

        # Obtenir le nombre d'articles disponibles et indisponibles, la quantité totale entrée et sortie, et le prix total pour chaque catégorie pour l'année spécifiée
        results = (
            Inventory.objects.all()
            .annotate(
                year=Coalesce(
                        ExtractYear(F('inventoryinto__date_modification')),
                        ExtractYear(F('inventoryinto__inventoryout__date_modification'))
                        ,0
                    ),
                month=Coalesce(
                        ExtractMonth(F('inventoryinto__date_modification')),
                        ExtractMonth(F('inventoryinto__inventoryout__date_modification'))
                        ,0
                    ),
                day=Coalesce(
                        ExtractDay(F('inventoryinto__date_modification')),
                        ExtractDay(F('inventoryinto__inventoryout__date_modification'))
                        ,0
                    ),
                week=Coalesce(
                        ExtractWeekDay(F('inventoryinto__date_modification')),
                        ExtractWeekDay(F('inventoryinto__inventoryout__date_modification'))
                        ,0
                    ),
                available_count=Coalesce(
                    Count(
                        'inventoryinto',
                        filter=Q(inventoryinto__inventoryout__isAvailable=True),
                        distinct=True
                    ),
                    0
                ),
                unavailable_count=Coalesce(
                    Count(
                        'inventoryinto',
                        filter=Q(inventoryinto__inventoryout__isAvailable=False),
                        distinct=True
                    ),
                    0
                ),
                total_quantity_in=Coalesce(
                    Sum('inventoryinto__quantity'),
                    0
                ),
                total_quantity_out=Coalesce(
                    Sum('inventoryinto__inventoryout__quantity'),
                    0
                ),
                total_price=Coalesce(
                    Sum(F('inventoryinto__quantity') * F('inventoryinto__price')), 
                    0,
                    output_field=DecimalField()
                ),capacity_out = Coalesce(
                    Sum(F('inventoryinto__capacity') * F('inventoryinto__inventoryout__quantity')), 0,
                    output_field=DecimalField()
                ),
                numbres_of_pieces_out=Coalesce(Sum(F('inventoryinto__numbres_of_pieces') * F('inventoryinto__inventoryout__quantity')), 0,
                    output_field=DecimalField()
                )

            )
            .values('id_category__name','year','month','day','week', 'available_count', 'unavailable_count', 'total_quantity_in', 'total_quantity_out', 'total_price', 'inventoryinto__capacity', 'inventoryinto__weight', 'capacity_out','numbres_of_pieces_out','inventoryinto__numbres_of_pieces')
        )

        # Sérialiser les résultats
        serializer = InventorySummarybyYearsAndCategorySerializer(results, many=True)
        data = serializer.data 

        response_data = {
        "status": "success",
        "data": data,
        "message": "Data retrieved successfully",
        }
        return Response(response_data, status=status.HTTP_200_OK)

@api_view(["GET"])
def Statistique_total_stock_int_retrieve_day_category_list(request, year, month):
     # Obtenir le nombre d'articles disponibles et indisponibles, la quantité totale entrée et sortie, et le prix total pour chaque catégorie pour l'année spécifiée
        results = (
            Inventory.objects
            .filter(
                Q(inventoryinto__date_modification__year=year,inventoryinto__date_modification__month=month) |  # Filtre par année de création des entrées
                Q(inventoryinto__inventoryout__date_modification__year=year,inventoryinto__inventoryout__date_modification__month=month)  # Filtre par année de création des sorties
            ).annotate(
                available_count=Coalesce(
                    Count(
                        'inventoryinto',
                        filter=Q(inventoryinto__inventoryout__isAvailable=True),
                        distinct=True
                    ),
                    0
                ),
                unavailable_count=Coalesce(
                    Count(
                        'inventoryinto',
                        filter=Q(inventoryinto__inventoryout__isAvailable=False),
                        distinct=True
                    ),
                    0
                ),
                total_quantity_in=Coalesce(
                    Sum('inventoryinto__quantity'),
                    0
                ),
                total_quantity_out=Coalesce(
                    Sum('inventoryinto__inventoryout__quantity'),
                    0
                ),
                total_price=Coalesce(
                    Sum(F('inventoryinto__quantity') * F('inventoryinto__price')), 
                    0,
                    output_field=DecimalField()
                ),capacity_out = Coalesce(
                    Sum(F('inventoryinto__capacity') * F('inventoryinto__inventoryout__quantity')), 0,
                    output_field=DecimalField()
                ),
                numbres_of_pieces_out=Coalesce(Sum(F('inventoryinto__numbres_of_pieces') * F('inventoryinto__inventoryout__quantity')), 0,
                    output_field=DecimalField()
                ),
                year=Coalesce(
                        ExtractYear(F('inventoryinto__date_modification')),
                        ExtractYear(F('inventoryinto__inventoryout__date_modification'))
                        ,0
                    ),
                month=Coalesce(
                        ExtractMonth(F('inventoryinto__date_modification')),
                        ExtractMonth(F('inventoryinto__inventoryout__date_modification'))
                    ),
                day=Coalesce(
                        ExtractDay(F('inventoryinto__date_modification')),
                        ExtractDay(F('inventoryinto__inventoryout__date_modification'))
                    ),
                week=Coalesce(
                        ExtractWeekDay(F('inventoryinto__date_modification')),
                        ExtractWeekDay(F('inventoryinto__inventoryout__date_modification'))
                    ),

            )
            .values('id_category__name','year','month','day','week', 'available_count', 'unavailable_count', 'total_quantity_in', 'total_quantity_out', 'total_price', 'inventoryinto__capacity', 'inventoryinto__weight', 'capacity_out','numbres_of_pieces_out','inventoryinto__numbres_of_pieces')
        )

        # Sérialiser les résultats
        serializer = InventorySummarybyYearsAndCategorySerializer(results, many=True)
        data = serializer.data 

        response_data = {
        "status": "success",
        "data": data,
        "message": "Data retrieved successfully",
        }
        return Response(response_data, status=status.HTTP_200_OK)

##########################################################################


#3333333333333333333333333333333333333333333333333333333333333333333333
#
# list statistique by article
#
#3333333333333333333333333333333333333333333333333333333333333#########
@api_view(["GET"])
def Statistique_total_stock_int_retrieve_month_article_list(request, year):

     # Obtenir le nombre d'articles disponibles et indisponibles, la quantité totale entrée et sortie, et le prix total pour chaque catégorie pour l'année spécifiée
        results = (
            Inventory.objects
            .filter(
                Q(inventoryinto__date_modification__year=year) |  # Filtre par année de création des entrées
                Q(inventoryinto__inventoryout__date_modification__year=year)  # Filtre par année de création des sorties
            ).annotate(
                available_count=Coalesce(
                    Count(
                        'inventoryinto',
                        filter=Q(inventoryinto__inventoryout__isAvailable=True),
                        distinct=True
                    ),
                    0
                ),
                unavailable_count=Coalesce(
                    Count(
                        'inventoryinto',
                        filter=Q(inventoryinto__inventoryout__isAvailable=False),
                        distinct=True
                    ),
                    0
                ),
                total_quantity_in=Coalesce(
                    Sum('inventoryinto__quantity'),
                    0
                ),
                total_quantity_out=Coalesce(
                    Sum('inventoryinto__inventoryout__quantity'),
                    0
                ),
                total_price=Coalesce(
                    Sum(F('inventoryinto__quantity') * F('inventoryinto__price_used_by_entreprise')), 
                    0,
                    output_field=DecimalField()
                ),capacity_out = Coalesce(
                    Sum(F('inventoryinto__capacity') * F('inventoryinto__inventoryout__quantity')), 0,
                    output_field=DecimalField()
                ),
                numbres_of_pieces_out=Coalesce(Sum(F('inventoryinto__numbres_of_pieces') * F('inventoryinto__inventoryout__quantity')), 0,
                    output_field=DecimalField()
                ),
                year=Coalesce(
                        ExtractYear(F('inventoryinto__date_modification')),
                        ExtractYear(F('inventoryinto__inventoryout__date_modification'))
                        ,0
                    ),
                month=Coalesce(
                        ExtractMonth(F('inventoryinto__date_modification')),
                        ExtractMonth(F('inventoryinto__inventoryout__date_modification'))
                        ,0
                    ),
                day=Coalesce(
                        ExtractDay(F('inventoryinto__date_modification')),
                        ExtractDay(F('inventoryinto__inventoryout__date_modification'))
                        ,0
                    ),
                week=Coalesce(
                        ExtractWeekDay(F('inventoryinto__date_modification')),
                        ExtractWeekDay(F('inventoryinto__inventoryout__date_modification'))
                        ,0
                    )

            )
            .order_by('-month')
            .values('designation', 'available_count','year','day','month','week', 'unavailable_count', 'total_quantity_in', 'total_quantity_out', 'total_price', 'inventoryinto__capacity', 'inventoryinto__weight', 'capacity_out','numbres_of_pieces_out','inventoryinto__numbres_of_pieces')
        )

        # Sérialiser les résultats
        serializer = InventorySummaryByArticleSerializer(results, many=True)
        data = serializer.data 

        response_data = {
        "status": "success",
        "data": data,
        "message": "Data retrieved successfully",
        }
        return Response(response_data, status=status.HTTP_200_OK)

@api_view(["GET"])
def Statistique_total_stock_int_retrieve_year_article_list(request):

        # Obtenir le nombre d'articles disponibles et indisponibles, la quantité totale entrée et sortie, et le prix total pour chaque catégorie pour l'année spécifiée
        results = (
            Inventory.objects.all()
            .annotate(
                available_count=Coalesce(
                    Count(
                        'inventoryinto',
                        filter=Q(inventoryinto__inventoryout__isAvailable=True),
                        distinct=True
                    ),
                    0
                ),
                unavailable_count=Coalesce(
                    Count(
                        'inventoryinto',
                        filter=Q(inventoryinto__inventoryout__isAvailable=False),
                        distinct=True
                    ),
                    0
                ),
                total_quantity_in=Coalesce(
                    Sum('inventoryinto__quantity'),
                    0
                ),
                total_quantity_out=Coalesce(
                    Sum('inventoryinto__inventoryout__quantity'),
                    0
                ),
                total_price=Coalesce(
                    Sum(F('inventoryinto__quantity') * F('inventoryinto__price_used_by_entreprise')), 
                    0,
                    output_field=DecimalField()
                ),capacity_out = Coalesce(
                    Sum(F('inventoryinto__capacity') * F('inventoryinto__inventoryout__quantity')), 0,
                    output_field=DecimalField()
                ),
                numbres_of_pieces_out=Coalesce(Sum(F('inventoryinto__numbres_of_pieces') * F('inventoryinto__inventoryout__quantity')), 0,
                    output_field=DecimalField()
                ),
                year=Coalesce(
                        ExtractYear(F('inventoryinto__date_modification')),
                        ExtractYear(F('inventoryinto__inventoryout__date_modification'))
                        ,0
                    ),
                month=Coalesce(
                        ExtractMonth(F('inventoryinto__date_modification')),
                        ExtractMonth(F('inventoryinto__inventoryout__date_modification'))
                        ,0
                    ),
                day=Coalesce(
                        ExtractDay(F('inventoryinto__date_modification')),
                        ExtractDay(F('inventoryinto__inventoryout__date_modification'))
                        ,0
                    ),
                week=Coalesce(
                        ExtractWeekDay(F('inventoryinto__date_modification')),
                        ExtractWeekDay(F('inventoryinto__inventoryout__date_modification'))
                        ,0
                    )

            )
             .order_by('-year')
            .values('designation', 'available_count','year','day','month','week', 'unavailable_count', 'total_quantity_in', 'total_quantity_out', 'total_price', 'inventoryinto__capacity', 'inventoryinto__weight', 'capacity_out','numbres_of_pieces_out','inventoryinto__numbres_of_pieces')
        )

        # Sérialiser les résultats
        serializer = InventorySummaryByArticleSerializer(results, many=True)
        data = serializer.data 

        response_data = {
        "status": "success",
        "data": data,
        "message": "Data retrieved successfully",
        }
        return Response(response_data, status=status.HTTP_200_OK)


@api_view(["GET"])
def Statistique_total_stock_int_retrieve_day_article_list(request, year, month):
     # Obtenir le nombre d'articles disponibles et indisponibles, la quantité totale entrée et sortie, et le prix total pour chaque catégorie pour l'année spécifiée
        results = (
            Inventory.objects
            .filter(
                Q(inventoryinto__date_modification__year=year,inventoryinto__date_modification__month=month) |  # Filtre par année de création des entrées
                Q(inventoryinto__inventoryout__date_modification__year=year,inventoryinto__inventoryout__date_modification__month=month)  # Filtre par année de création des sorties
            ).annotate(
                available_count=Coalesce(
                    Count(
                        'inventoryinto',
                        filter=Q(inventoryinto__inventoryout__isAvailable=True),
                        distinct=True
                    ),
                    0
                ),
                unavailable_count=Coalesce(
                    Count(
                        'inventoryinto',
                        filter=Q(inventoryinto__inventoryout__isAvailable=False),
                        distinct=True
                    ),
                    0
                ),
                total_quantity_in=Coalesce(
                    Sum('inventoryinto__quantity'),
                    0
                ),
                total_quantity_out=Coalesce(
                    Sum('inventoryinto__inventoryout__quantity'),
                    0
                ),
                total_price=Coalesce(
                    Sum(F('inventoryinto__quantity') * F('inventoryinto__price_used_by_entreprise')), 
                    0,
                    output_field=DecimalField()
                ),capacity_out = Coalesce(
                    Sum(F('inventoryinto__capacity') * F('inventoryinto__inventoryout__quantity')), 0,
                    output_field=DecimalField()
                ),
                numbres_of_pieces_out=Coalesce(Sum(F('inventoryinto__numbres_of_pieces') * F('inventoryinto__inventoryout__quantity')), 0,
                    output_field=DecimalField()
                ),
                year=Coalesce(
                        ExtractYear(F('inventoryinto__date_modification')),
                        ExtractYear(F('inventoryinto__inventoryout__date_modification'))
                        ,0
                    ),
                month=Coalesce(
                        ExtractMonth(F('inventoryinto__date_modification')),
                        ExtractMonth(F('inventoryinto__inventoryout__date_modification'))
                        ,0
                    ),
                day=Coalesce(
                        ExtractDay(F('inventoryinto__date_modification')),
                        ExtractDay(F('inventoryinto__inventoryout__date_modification'))
                        ,0
                    ),
                week=Coalesce(
                        ExtractWeekDay(F('inventoryinto__date_modification')),
                        ExtractWeekDay(F('inventoryinto__inventoryout__date_modification'))
                        ,0
                    )

            )
             .order_by('-day')
            .values('designation', 'available_count','year','day','month','week', 'unavailable_count', 'total_quantity_in', 'total_quantity_out', 'total_price', 'inventoryinto__capacity', 'inventoryinto__weight', 'capacity_out','numbres_of_pieces_out','inventoryinto__numbres_of_pieces')
        )

        # Sérialiser les résultats
        serializer = InventorySummaryByArticleSerializer(results, many=True)
        data = serializer.data 

        response_data = {
        "status": "success",
        "data": data,
        "message": "Data retrieved successfully",
        }
        return Response(response_data, status=status.HTTP_200_OK)

##########################################################################

@api_view(["GET"])
def Statistique_price_stock_int_retrieve_year(request):
    # Retrieve the latest setting to get the current currency
    latest_setting = Setting.objects.latest("id")
    current_currency = latest_setting.currency
    # Supposons que vous ayez un modèle Article avec une date de création
    total_articles = (
        InventoryInto.objects.filter(currency_used_by_entreprise=current_currency)
        .annotate(
            year=ExtractYear("date_modification"),
        )
        .values("year", "id_article__id_category__name")
        .annotate(total=Sum("price_used_by_entreprise"))
        .order_by("year")
    )
    serializer = ArticlePriceSerializerYear(total_articles, many=True)
    data = serializer.data
    total_data = len(serializer.data)

    response_data = {
        "status": "success",
        "data": data,
        "count": total_data,
        "message": "Data retrieved successfully",
    }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(["GET"])
def Statistique_price_stock_int_retrieve_day(request, year, month):
    # Retrieve the latest setting to get the current currency
    latest_setting = Setting.objects.latest("id")
    current_currency = latest_setting.currency
    # Supposons que vous ayez un modèle Article avec une date de création
    total_articles = (
        InventoryInto.objects.filter(
            date_modification__year=year,
            date_modification__month=month,
            currency_used_by_entreprise=current_currency,
        )
        .annotate(
            day=ExtractDay("date_modification"),
        )
        .values("day", "id_article__id_category__name")
        .annotate(total=Sum("price_used_by_entreprise"))
        .order_by("day")
    )
    print(total_articles)
    serializer = ArticlePriceSerializerDay(total_articles, many=True)
    data = serializer.data
    total_data = len(serializer.data)

    response_data = {
        "status": "success",
        "data": data,
        "count": total_data,
        "message": "Data retrieved successfully",
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


@api_view(["GET"])
def Statistique_price_stock_int_retrieve_month_article(request, year, article):
    # Retrieve the latest setting to get the current currency
    latest_setting = Setting.objects.latest('id')
    current_currency = latest_setting.currency
    # Supposons que vous ayez un modèle Article avec une date de création
    total_articles = (
        InventoryInto.objects.filter(
            date_modification__year=year, id_article__designation=article,currency_used_by_entreprise=current_currency
        )
        .annotate(
            month=ExtractMonth("date_modification"),
        )
        .values("month", "id_article__id_category__name")
        .annotate(total=Sum("price_used_by_entreprise"))
        .order_by("month")
    )
    print(total_articles)
    serializer = ArticlePriceSerializer(total_articles, many=True)
    data = serializer.data
    total_data = len(serializer.data)

    response_data = {
        "status": "success",
        "data": data,
        "count": total_data,
        "message": "Data retrieved successfully",
    }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(["GET"])
def Statistique_price_stock_int_retrieve_year_article(request, article):
    # Retrieve the latest setting to get the current currency
    latest_setting = Setting.objects.latest('id')
    current_currency = latest_setting.currency

    # Supposons que vous ayez un modèle Article avec une date de création
    total_articles = (
        InventoryInto.objects.filter(id_article__designation=article,currency_used_by_entreprise=current_currency)
        .annotate(
            year=ExtractYear("date_modification"),
        )
        .values("year", "id_article__id_category__name")
        .annotate(total=Sum("price_used_by_entreprise"))
        .order_by("year")
    )
    print(total_articles)
    serializer = ArticlePriceSerializerYear(total_articles, many=True)
    data = serializer.data
    total_data = len(serializer.data)

    response_data = {
        "status": "success",
        "data": data,
        "count": total_data,
        "message": "Data retrieved successfully",
    }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(["GET"])
def Statistique_price_stock_int_retrieve_day_article(request, year, month, article):
    # Retrieve the latest setting to get the current currency
    latest_setting = Setting.objects.latest('id')
    current_currency = latest_setting.currency
    # Supposons que vous ayez un modèle Article avec une date de création
    total_articles = (
        InventoryInto.objects.filter(
            date_modification__year=year,
            date_modification__month=month,
            id_article__designation=article,
            currency_used_by_entreprise=current_currency
        )
        .annotate(
            day=ExtractDay("date_modification"),
        )
        .values("day", "id_article__id_category__name")
        .annotate(total=Sum("price_used_by_entreprise"))
        .order_by("day")
    )
    print(total_articles)
    serializer = ArticlePriceSerializerDay(total_articles, many=True)
    data = serializer.data
    total_data = len(serializer.data)

    response_data = {
        "status": "success",
        "data": data,
        "count": total_data,
        "message": "Data retrieved successfully",
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


@api_view(["GET"])
def Statistique_price_stock_int_retrieve_month_category(request, year, category):
    # Retrieve the latest setting to get the current currency
    latest_setting = Setting.objects.latest('id')
    current_currency = latest_setting.currency
    # Supposons que vous ayez un modèle Article avec une date de création
    total_articles = (
        InventoryInto.objects.filter(
            date_modification__year=year, id_article__id_category__name=category,currency_used_by_entreprise=current_currency
        )
        .annotate(
            month=ExtractMonth("date_modification"),
        )
        .values("month", "id_article__id_category__name")
        .annotate(total=Sum("price_used_by_entreprise"))
        .order_by("month")
    )
    print(total_articles)
    serializer = ArticlePriceSerializer(total_articles, many=True)
    data = serializer.data
    total_data = len(serializer.data)

    response_data = {
        "status": "success",
        "data": data,
        "count": total_data,
        "message": "Data retrieved successfully",
    }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(["GET"])
def Statistique_price_stock_int_retrieve_year_category(request, category):
# Retrieve the latest setting to get the current currency
    latest_setting = Setting.objects.latest('id')
    current_currency = latest_setting.currency
    # Supposons que vous ayez un modèle Article avec une date de création
    total_articles = (
        InventoryInto.objects.filter(id_article__id_category__name=category,currency_used_by_entreprise=current_currency)
        .annotate(
            year=ExtractYear("date_modification"),
        )
        .values("year", "id_article__id_category__name")
        .annotate(total=Sum("price_used_by_entreprise"))
        .order_by("year")
    )
    print(total_articles)
    serializer = ArticlePriceSerializerYear(total_articles, many=True)
    data = serializer.data
    total_data = len(serializer.data)

    response_data = {
        "status": "success",
        "data": data,
        "count": total_data,
        "message": "Data retrieved successfully",
    }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(["GET"])
def Statistique_price_stock_int_retrieve_day_category(request, year, month, category):
    # Retrieve the latest setting to get the current currency
    latest_setting = Setting.objects.latest('id')
    current_currency = latest_setting.currency
    total_articles = (
        InventoryInto.objects.filter(
            date_modification__year=year,
            date_modification__month=month,
            id_article__id_category__name=category,
            currency_used_by_entreprise=current_currency
        )
        .annotate(
            day=ExtractDay("date_modification"),
        )
        .values("day", "id_article__id_category__name")
        .annotate(total=Sum("price_used_by_entreprise"))
        .order_by("day")
    )
    print(total_articles)
    serializer = ArticlePriceSerializerDay(total_articles, many=True)
    data = serializer.data
    total_data = len(serializer.data)

    response_data = {
        "status": "success",
        "data": data,
        "count": total_data,
        "message": "Data retrieved successfully",
    }
    return Response(response_data, status=status.HTTP_200_OK)


################################################################ Pour les littres


### Vues des statistiques des differentes sorties
#
#






class SettingViewSet(viewsets.ModelViewSet):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer
    # a ajouter manuelement partout
    # pagination_class = CustomPagination
    # authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().last()
        serializer = self.get_serializer(queryset)
        data = serializer.data
        total_data = 1  # Get the total number of data

        response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "message": "Data retrieved successfully",
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # id_UserAgent=request.user)
            return Response(
                {
                    "status": "success",
                    "data": serializer.data,
                    "message": "Data added successfully",
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {
                    "status": "error",
                    "data": serializer.errors,
                    "message": "Data error!",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  # id_UserAgent=request.user)
            return Response(
                {
                    "status": "success",
                    "data": serializer.data,
                    "message": "Data updated successfully",
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "status": "error",
                    "data": serializer.errors,
                    "message": "Update error!",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # instance.id_UserAgent= request.user
        instance.save()
        instance.delete()
        return Response(
            {"status": "success", "message": "Data deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class Statistique_maintenance_machine_list_retrieve(APIView):
    def get(self, request, format=None):
        # Annotate the queryset with planned and actual counts
        serializer = ""
        queryset = ''
        period = request.query_params.get('period', 'years')
        type = request.query_params.get('type','article')
        month = request.query_params.get('month')
        year = request.query_params.get('year')
        print(period)
        period = str(period)
        
        if period == 'days':
            if type == 'article':
                queryset = Machine.objects.values(
                'categorie__nom' # Grouper par catégorie de machine
                ).filter(diagnostics__date_modification__year=year, diagnostics__date_modification__month=month).annotate(
                planned=Count('planifiermaintenance'),
                actual=Count('diagnostics', filter=Q(diagnostics__isDiagnostic=True, diagnostics__isRepair=False)),
                total=F('planned') + F('actual'),
                category_machine = F('categorie__nom'),
                name_machine = F('nom'),
                type_de_maintenance=F('diagnostics__typeMaintenance'),
                year=ExtractYear('diagnostics__date_modification'), 
                month=ExtractMonth('diagnostics__date_modification'), 
                day=ExtractDay('diagnostics__date_modification')).values('year','month', 'day','nom', 'planned', 'actual',"type_de_maintenance",'total',"category_machine","name_machine").order_by('-year')
            elif type == 'category':
                queryset = CategorieMachine.objects.filter(machine__diagnostics__date_modification__year=year, 
                machine__date_creation__month=month).annotate(
                planned=Count('machine__planifiermaintenance'),
                actual=Count('machine__diagnostics', filter=Q(machine__diagnostics__isDiagnostic=True, machine__diagnostics__isRepair=False)),
                total=F('planned') + F('actual'),
                type_de_maintenance=F('machine__diagnostics__typeMaintenance'),
                year=ExtractYear('machine__diagnostics__date_modification'), 
                month=ExtractMonth('machine__diagnostics__date_modification'), 
                day=ExtractDay('machine__diagnostics__date_modification')).values('year','month', 'day','nom', 'planned', 'actual',"type_de_maintenance",'total',).order_by('-year')

        elif period == 'month':
            if type == 'article':
                queryset = Machine.objects.filter(diagnostics__date_modification__year=year).annotate(
                planned=Count('planifiermaintenance'),
                actual=Count('diagnostics', filter=Q(diagnostics__isDiagnostic=True, diagnostics__isRepair=False)),
                total=F('planned') + F('actual'),
                category_machine = F('categorie__nom'),
                name_machine = F('nom'),
                type_de_maintenance=F('diagnostics__typeMaintenance')
            ).annotate(year=ExtractYear('diagnostics__date_modification'), month=ExtractMonth('diagnostics__date_modification'), day=ExtractDay('diagnostics__date_modification')).values('year', 'month', 'day','nom', 'planned', 'actual',"type_de_maintenance",'total',"category_machine","name_machine").order_by('-year')
            elif type == 'category':
                queryset = CategorieMachine.objects.filter(machine__diagnostics__date_modification__year=year).annotate(
                planned=Count('machine__planifiermaintenance'),
                actual=Count('machine__diagnostics', filter=Q(machine__diagnostics__isDiagnostic=True, machine__diagnostics__isRepair=False)),
                total=F('planned') + F('actual'),
                type_de_maintenance=F('machine__diagnostics__typeMaintenance'),
                year=ExtractYear('machine__diagnostics__date_modification'), 
                month=ExtractMonth('machine__diagnostics__date_modification'), 
                day=ExtractDay('machine__diagnostics__date_modification')).values('year', 'month', 'day','nom', 'planned', 'actual',"type_de_maintenance",'total',).order_by('-year')

        elif period == 'years':
            if type == 'article':
                queryset = Machine.objects.filter().annotate(
                planned=Count('planifiermaintenance'),
                actual=Count('diagnostics', filter=Q(diagnostics__isDiagnostic=True, diagnostics__isRepair=False)),
                total=F('planned') + F('actual'),
                category_machine = F('categorie__nom'),
                name_machine = F('nom'),
                type_de_maintenance=F('diagnostics__typeMaintenance')
            ).annotate(year=ExtractYear('date_modification'), month=ExtractMonth('date_modification'), day=ExtractDay('date_modification')).values('year', 'month', 'day','nom', 'planned', 'actual',"type_de_maintenance",'total',"category_machine","name_machine").order_by('-year')
            elif type == 'category':
                queryset = CategorieMachine.objects.filter().annotate(
                planned=Count('machine__planifiermaintenance'),
                actual=Count('machine__diagnostics', filter=Q(machine__diagnostics__isDiagnostic=True, machine__diagnostics__isRepair=False)),
                total=F('planned') + F('actual'),
                type_de_maintenance=F('machine__diagnostics__typeMaintenance'),
                year=ExtractYear('machine__diagnostics__date_modification'), 
                month=ExtractMonth('machine__diagnostics__date_modification'), 
                day=ExtractDay('machine__diagnostics__date_modification')).values(
                'year', 'month', 'day','nom', 'planned', 'actual',"type_de_maintenance",'total',).order_by('-year')
        else:
            return Response({"error": "Invalid period parameter."}, status=400)
        
        if type == "article":
            serializer = MachineStatisticsSerializerForArticle(queryset, many=True)
        elif type == "category":
            serializer = MachineStatisticsSerializerForCategory(queryset, many=True)

        data = serializer.data
        response_data = {
        "status": "success",
        "data": data,
        "message": "Data retrieved successfully",
        }
        return Response(response_data)

class DiagnosticsStatisticsView(APIView):
    def get(self, request):
        serializer = ""
        queryset = ''
        period = request.query_params.get('period', 'years')
        year = request.query_params.get('year')
        print(period)
        period = str(period)
        if period == 'days':
            month = request.query_params.get('month')
            queryset = Diagnostics.objects.filter(date_modification__year=year, date_creation__month=month,isDiagnostic=True).annotate(day=ExtractDay('date_modification')).values('day').annotate(count=Count('id')).order_by('-day')
            serializer = ValuesbyDaysPeriodSerializer(queryset, many=True)
        elif period == 'month':
            queryset = Diagnostics.objects.filter(date_modification__year=year,isDiagnostic=True).annotate(month=ExtractMonth('date_modification')).values('month').annotate(count=Count('id')).order_by('-month')
            serializer = ValuesbyMonthPeriodSerializer(queryset, many=True)
        elif period == 'years':
            queryset = Diagnostics.objects.filter(isDiagnostic=True).annotate(year=ExtractYear('date_modification')).values('year').annotate(count=Count('id')).order_by('-year')
            serializer = ValuesbyYearsPeriodSerializer(queryset, many=True)
        else:
            return Response({"error": "Invalid period parameter."}, status=400)
        
        data = serializer.data 
        response_data = {
        "status": "success",
        "data": data,
        "message": "Data retrieved successfully",
        }
        return Response(response_data, status=status.HTTP_200_OK)

# Assurez-vous que ce sérialiseur existe

class PlanifierMaintenanceStatisticsView(APIView):
    def get(self, request):
        serializer = ""
        period = request.query_params.get('period', 'day')
        if period == 'days':
            year = request.query_params.get('year')
            month = request.query_params.get('month')
            queryset = PlanifierMaintenance.objects.filter(date_modification__year=year, date_creation__month=month).annotate(day=ExtractDay('date_modification')).values('day').annotate(count=Count('id')).order_by('-day')
            serializer = ValuesbyDaysPeriodSerializer(queryset, many=True)
        elif period == 'month':
            year = request.query_params.get('year')
            queryset = PlanifierMaintenance.objects.filter(date_modification__year=year).annotate(month=ExtractMonth('date_modification')).values('month').annotate(count=Count('id')).order_by('-month')
            serializer = ValuesbyMonthPeriodSerializer(queryset, many=True)
        elif period == 'years':
            queryset = PlanifierMaintenance.objects.all().annotate(year=ExtractYear('date_modification')).values('year').annotate(count=Count('id')).order_by('-year')
            serializer = ValuesbyYearsPeriodSerializer(queryset, many=True)
        else:
            return Response({"error": "Invalid period parameter."}, status=400)
        
        data = serializer.data  
        response_data = {
        "status": "success",
        "data": data,
        "message": "Data retrieved successfully",
        }
        return Response(response_data, status=status.HTTP_200_OK)
class RepairStatisticsView(APIView):
    def get(self, request):
        serializer = ""
        period = request.query_params.get('period', 'days')
        if period == 'days':
            year = request.query_params.get('year')
            month = request.query_params.get('month')
            queryset = Diagnostics.objects.filter(date_modification__year=year, date_creation__month=month,isRepair=True).annotate(day=ExtractDay('date_modification')).values('day').annotate(count=Count('id')).order_by('-day')
            serializer = ValuesbyDaysPeriodSerializer(queryset, many=True)  
        elif period == 'month':
            year = request.query_params.get('year')
            queryset = Diagnostics.objects.filter(date_modification__year=year,isRepair=True).annotate(month=ExtractMonth('date_modification')).values('month').annotate(count=Count('id')).order_by('-month')
            serializer = ValuesbyMonthPeriodSerializer(queryset, many=True)  
        elif period == 'years':
            queryset = Diagnostics.objects.filter(isRepair=True).annotate(year=ExtractYear('date_modification')).values('year').annotate(count=Count('id')).order_by('-year')
            serializer = ValuesbyYearsPeriodSerializer(queryset, many=True)  
        else:
            return Response({"error": "Invalid period parameter."}, status=400)
        
        # Utilisez le sérialiseur adapté au modèle PlanifierMaintenance
        data = serializer.data  
        response_data = {
        "status": "success",
        "data": data,
        "message": "Data retrieved successfully",
        }
        return Response(response_data, status=status.HTTP_200_OK)
