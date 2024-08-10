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
from .models import Machine
from .serializers import MachineDataSerializer
from django.db.models.functions import Concat


# Create your views here.
def funct__id__entreprise(request):
    user = request.user
    userModel = User.objects.get(id=user.id)
    user__organisation__id = ""
    if userModel.entreprise:
        if userModel.entreprise.id:
            user__organisation__id = userModel.entreprise.id
    return user__organisation__id


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
    user__organisation__id = funct__id__entreprise(request=request)
    if categorie == "general":
        if period == "years":
            total_articles = (
                InventoryInto.objects.filter(entreprise__id=user__organisation__id)
                .annotate(year=ExtractYear("date_modification"))
                .values("year")
                .annotate(total=Sum("quantity"))
                .order_by("-year")
            )
            serializer = ArticleSerializerYear(total_articles, many=True)
        elif period == "month":
            total_articles = (
                InventoryInto.objects.filter(
                    date_modification__year=year, entreprise__id=user__organisation__id
                )
                .annotate(month=ExtractMonth("date_modification"))
                .values("month")
                .annotate(total=Sum("quantity"))
                .order_by("month")
            )
            serializer = ArticleSerializer(total_articles, many=True)
        elif period == "days":

            total_articles = (
                InventoryInto.objects.filter(
                    date_modification__year=year, date_modification__month=month
                )
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
                    entreprise__id=user__organisation__id,
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
                    currency_used_by_entreprise=current_currency,
                    entreprise__id=user__organisation__id,  # Assuming InventoryInto has a 'currency' field
                )
                .annotate(month=ExtractMonth("date_modification"))
                .values("month")
                .annotate(total=Sum("price_used_by_entreprise"))
                .order_by("month")
            )

            serializer = ArticleSerializerMonth(total_articles, many=True)
        elif period == "years":

            total_articles = (
                InventoryInto.objects.filter(
                    currency_used_by_entreprise=current_currency,
                    entreprise__id=user__organisation__id,
                )
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
        latest_setting = Setting.objects.latest("id")
        current_capacity = latest_setting.capacity

        if period == "days":
            # Supposons que vous ayez un modèle Article avec une date de création
            total_articles = (
                InventoryInto.objects.filter(
                    date_modification__year=year,
                    date_modification__month=month,
                    unit=current_capacity,
                    entreprise__id=user__organisation__id,
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
        elif period == "years":
            # Supposons que vous ayez un modèle Article avec une date de création
            total_articles = (
                InventoryInto.objects.filter(
                    unit=current_capacity, entreprise__id=user__organisation__id
                )
                .annotate(
                    year=ExtractYear("date_modification"),
                )
                .values("year")
                .annotate(total=Sum("capacity"))
                .order_by("year")
            )
            serializer = ArticleSerializerYear(total_articles, many=True)
        elif period == "month":
            total_articles = (
                InventoryInto.objects.filter(
                    unit=current_capacity, entreprise__id=user__organisation__id
                )
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
    user__organisation__id = funct__id__entreprise(request=request)
    if categorie == "general":
        if period == "month":
            total_articles = (
                InventoryOut.objects.filter(
                    date_modification__year=year, entreprise__id=user__organisation__id
                )
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
                InventoryOut.objects.filter(entreprise__id=user__organisation__id)
                .annotate(year=ExtractYear("date_modification"))
                .values("year")
                .annotate(total=Sum("quantity"))
                .order_by("year")
            )
            print(total_articles)
            serializer = ArticleSerializerYear(total_articles, many=True)

        if period == "days":
            total_articles = (
                InventoryOut.objects.filter(
                    date_modification__year=year, entreprise__id=user__organisation__id
                )
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
        latest_setting = Setting.objects.latest("id")
        current_currency = latest_setting.currency
        if period == "month":
            # Supposons que vous ayez un modèle Article avec une date de création
            total_articles = (
                InventoryOut.objects.filter(
                    date_modification__year=year,
                    id_inventory_into__currency_used_by_entreprise=current_currency,
                    entreprise__id=user__organisation__id,
                )
                .annotate(
                    month=ExtractMonth("date_modification"),
                )
                .values("month")
                .annotate(total=Sum("id_inventory_into__price_used_by_entreprise"))
                .order_by("month")
            )
            serializer = ArticleSerializerMonth(total_articles, many=True)
        elif period == "years":
            # Supposons que vous ayez un modèle Article avec une date de création
            total_articles = (
                InventoryOut.objects.filter(
                    id_inventory_into__currency_used_by_entreprise=current_currency,
                    entreprise__id=user__organisation__id,
                )
                .annotate(
                    year=ExtractYear("date_modification"),
                )
                .values("year")
                .annotate(total=Sum("id_inventory_into__price_used_by_entreprise"))
                .order_by("year")
            )
            serializer = ArticleSerializerYear(total_articles, many=True)
        elif period == "days":
            # Supposons que vous ayez un modèle Article avec une date de création
            total_articles = (
                InventoryOut.objects.filter(
                    date_modification__year=year,
                    id_inventory_into__currency_used_by_entreprise=current_currency,
                    date_modification__month=month,
                    entreprise__id=user__organisation__id,
                )
                .annotate(
                    day=ExtractDay("date_modification"),
                )
                .values("day")
                .annotate(total=Sum("id_inventory_into__price_used_by_entreprise"))
                .order_by("day")
            )
            serializer = ArticleSerializerYear(total_articles, many=True)
    elif categorie == "litre":
        # Retrieve the latest setting to get the current currency
        latest_setting = Setting.objects.filter(
            entreprise__id=user__organisation__id
        ).latest("id")
        current_capacity = latest_setting.capacity
        if period == "month":
            # Supposons que vous ayez un modèle Article avec une date de création
            total_articles = (
                InventoryOut.objects.filter(
                    date_modification__year=year,
                    id_inventory_into__unit=current_capacity,
                    entreprise__id=user__organisation__id,
                )
                .annotate(
                    month=ExtractMonth("date_modification"),
                )
                .values("month")
                .annotate(total=Sum("id_inventory_into__capacity"))
                .order_by("month")
            )
            serializer = ArticleSerializerMonth(total_articles, many=True)
        elif period == "years":
            # Supposons que vous ayez un modèle Article avec une date de création
            total_articles = (
                InventoryOut.objects.filter(
                    id_inventory_into__unit=current_capacity,
                    entreprise__id=user__organisation__id,
                )
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
                    date_modification__year=year,
                    date_modification__month=month,
                    id_inventory_into__unit=current_capacity,
                    entreprise__id=user__organisation__id,
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
    user__organisation__id = funct__id__entreprise(request=request)
    if filter_by == "Days":
        # Obtenez le dernier jour du mois en cours
        start_of_month = datetime(year=year, month=month, day=1).replace(day=1)
        end_of_month = calendar.monthrange(start_of_month.year, start_of_month.month)
        end_of_month = start_of_month.replace(day=end_of_month[1])
        creation_days = (
            InventoryInto.objects.filter(
                date_modification__range=(start_of_month, end_of_month),
                entreprise__id=user__organisation__id,
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
                date_modification__range=(start_of_month, end_of_month),
                entreprise__id=user__organisation__id,
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
    user__organisation__id = funct__id__entreprise(request=request)
    if filter_by == "Years":
        total_articles = (
            InventoryInto.objects.filter(entreprise__id=user__organisation__id)
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
            InventoryInto.objects.filter(date_modification__year=year,entreprise__id=user__organisation__id,)
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


# 3333333333333333333333333333333333333333333333333333333333333333333333
#']
# list statistique by category
#
# 3333333333333333333333333333333333333333333333333333333333333#########
@api_view(["GET"])
def Statistique_total_stock_int_retrieve_by_category_list(request):
    period = request.query_params.get("period", "years")
    year = request.query_params.get("year")
    month = request.query_params.get("month")
    user__organisation__id = funct__id__entreprise(request=request)
    print(year)
    print(period)
    print(request.user)
    period = str(period)
    serializer = []
    data = ""
    if period == "month":
        # Obtenir le nombre d'articles disponibles et indisponibles, la quantité totale entrée et sortie, et le prix total pour chaque catégorie pour l'année spécifiée
        results = (
            Inventory.objects.filter(
                Q(
                    inventoryinto__date_modification__year=year
                )  # Filtre par année de création des entrées
                | Q(inventoryinto__inventoryout__date_modification__year=year),
                entreprise__id=user__organisation__id,  # Filtre par année de création des sorties
            )
            .annotate(
                available_count=Coalesce(
                    Count(
                        "inventoryinto",
                        filter=Q(inventoryinto__inventoryout__isAvailable=True),
                        distinct=True,
                    ),
                    0,
                ),
                unavailable_count=Coalesce(
                    Count(
                        "inventoryinto",
                        filter=Q(inventoryinto__inventoryout__isAvailable=False),
                        distinct=True,
                    ),
                    0,
                ),
                total_quantity_in=Coalesce(Sum("inventoryinto__quantity"), 0),
                total_quantity_out=Coalesce(
                    Sum("inventoryinto__inventoryout__quantity"), 0
                ),
                total_price=Coalesce(
                    Sum(F("inventoryinto__quantity") * F("inventoryinto__price")),
                    0,
                    output_field=DecimalField(),
                ),
                capacity_out=Coalesce(
                    Sum(
                        F("inventoryinto__capacity")
                        * F("inventoryinto__inventoryout__quantity")
                    ),
                    0,
                    output_field=DecimalField(),
                ),
                numbres_of_pieces_out=Coalesce(
                    Sum(
                        F("inventoryinto__numbres_of_pieces")
                        * F("inventoryinto__inventoryout__quantity")
                    ),
                    0,
                    output_field=DecimalField(),
                ),
                year=Coalesce(
                    ExtractYear(F("inventoryinto__date_modification")),
                    ExtractYear(F("inventoryinto__inventoryout__date_modification")),
                    0,
                ),
                month=Coalesce(
                    ExtractMonth(F("inventoryinto__date_modification")),
                    ExtractMonth(F("inventoryinto__inventoryout__date_modification")),
                    0,
                ),
                day=Coalesce(
                    ExtractDay(F("inventoryinto__date_modification")),
                    ExtractDay(F("inventoryinto__inventoryout__date_modification")),
                    0,
                ),
                week=Coalesce(
                    ExtractWeekDay(F("inventoryinto__date_modification")),
                    ExtractWeekDay(F("inventoryinto__inventoryout__date_modification")),
                    0,
                ),
            )
            .values(
                "id_category__name",
                "year",
                "month",
                "day",
                "week",
                "available_count",
                "unavailable_count",
                "total_quantity_in",
                "total_quantity_out",
                "total_price",
                "inventoryinto__capacity",
                "inventoryinto__weight",
                "capacity_out",
                "numbres_of_pieces_out",
                "inventoryinto__numbres_of_pieces",
            )
        )

        # Sérialiser les résultats
        serializer = InventorySummarybyYearsAndCategorySerializer(results, many=True)

    if period == "years":
        # Obtenir le nombre d'articles disponibles et indisponibles, la quantité totale entrée et sortie, et le prix total pour chaque catégorie pour l'année spécifiée

        # Assuming Inventory, InventoryInto, and InventoryOut are your models
        # and they have the necessary relationships and fields as per your query`

        results = (
            Inventory.objects.filter(entreprise__id=user__organisation__id)
            .annotate(
                available_count=Coalesce(
                    Count(
                        "inventoryinto",
                        filter=Q(inventoryinto__inventoryout__isAvailable=True),
                        distinct=True,
                    ),
                    0,
                ),
                unavailable_count=Coalesce(
                    Count(
                        "inventoryinto",
                        filter=Q(inventoryinto__inventoryout__isAvailable=False),
                        distinct=True,
                    ),
                    0,
                ),
                total_quantity_in=Coalesce(Sum("inventoryinto__quantity"), 0),
                total_quantity_out=Coalesce(
                    Sum("inventoryinto__inventoryout__quantity"), 0
                ),
                total_price=Coalesce(
                    Sum(F("inventoryinto__quantity") * F("inventoryinto__price")),
                    0,
                    output_field=DecimalField(),
                ),
                capacity_out=Coalesce(
                    Sum(
                        F("inventoryinto__capacity")
                        * F("inventoryinto__inventoryout__quantity")
                    ),
                    0,
                    output_field=DecimalField(),
                ),
                numbres_of_pieces_out=Coalesce(
                    Sum(
                        F("inventoryinto__numbres_of_pieces")
                        * F("inventoryinto__inventoryout__quantity")
                    ),
                    0,
                    output_field=DecimalField(),
                ),
                year=Coalesce(
                    ExtractYear(F("inventoryinto__date_modification")),
                    ExtractYear(F("inventoryinto__inventoryout__date_modification")),
                    0,
                ),
                month=Coalesce(
                    ExtractMonth(F("inventoryinto__date_modification")),
                    ExtractMonth(F("inventoryinto__inventoryout__date_modification")),
                    0,
                ),
                day=Coalesce(
                    ExtractDay(F("inventoryinto__date_modification")),
                    ExtractDay(F("inventoryinto__inventoryout__date_modification")),
                    0,
                ),
                week=Coalesce(
                    ExtractWeekDay(F("inventoryinto__date_modification")),
                    ExtractWeekDay(F("inventoryinto__inventoryout__date_modification")),
                    0,
                ),
            )
            .values(
                "id_category_name",
                "year",
                "month",
                "day",
                "week",
                "available_count",
                "unavailable_count",
                "total_quantity_in",
                "total_quantity_out",
                "total_price",
                "inventoryinto__capacity",
                "inventoryinto__weight",
                "capacity_out",
                "numbres_of_pieces_out",
                "inventoryinto__numbres_of_pieces",
            )
        )
        # print(results)
        # Créer un dictionnaire pour stocker les totaux par catégorie
        totals_by_category = {}
        # Parcourir les résultats et calculer les totaux pour chaque catégorie
        for result in results:
            category_name = result["id_category_name"]
            if category_name not in totals_by_category:
                # Initialiser les totaux pour cette catégorie si elle n'existe pas déjà
                totals_by_category[category_name] = {
                    "total_quantity_in": 0,
                    "total_quantity_out": 0,
                    "total_price": 0,
                    "total_capacity_out": 0,
                    "total_numbres_of_pieces_out": 0,
                }
            # Mettre à jour les totaux pour cette catégorie
            totals_by_category[category_name]["total_quantity_in"] += result[
                "total_quantity_in"
            ]
            totals_by_category[category_name]["total_quantity_out"] += result[
                "total_quantity_out"
            ]
            totals_by_category[category_name]["total_price"] += result["total_price"]
            totals_by_category[category_name]["total_capacity_out"] += result[
                "capacity_out"
            ]
            totals_by_category[category_name]["total_numbres_of_pieces_out"] += result[
                "numbres_of_pieces_out"
            ]

        print(totals_by_category.values())
        # Sérialiser les résultats
        serializer = InventorySummarybyCategorySerializer(
            totals_by_category.values(), many=True
        )

    if period == "days":
        # Obtenir le nombre d'articles disponibles et indisponibles, la quantité totale entrée et sortie, et le prix total pour chaque catégorie pour l'année spécifiée
        results = (
            Inventory.objects.filter(
                Q(
                    inventoryinto__date_modification__year=year,
                    inventoryinto__date_modification__month=month,
                )
                | Q(
                    inventoryinto__inventoryout__date_modification__year=year,
                    inventoryinto__inventoryout__date_modification__month=month,
                ),
                entreprise__id=user__organisation__id,
            )
            .annotate(
                available_count=Coalesce(
                    Count(
                        "inventoryinto",
                        filter=Q(inventoryinto__inventoryout__isAvailable=True),
                        distinct=True,
                    ),
                    0,
                ),
                unavailable_count=Coalesce(
                    Count(
                        "inventoryinto",
                        filter=Q(inventoryinto__inventoryout__isAvailable=False),
                        distinct=True,
                    ),
                    0,
                ),
                total_quantity_in=Coalesce(Sum("inventoryinto__quantity"), 0),
                total_quantity_out=Coalesce(
                    Sum("inventoryinto__inventoryout__quantity"), 0
                ),
                total_price=Coalesce(
                    Sum(F("inventoryinto__quantity") * F("inventoryinto__price")),
                    0,
                    output_field=DecimalField(),
                ),
                capacity_out=Coalesce(
                    Sum(
                        F("inventoryinto__capacity")
                        * F("inventoryinto__inventoryout__quantity")
                    ),
                    0,
                    output_field=DecimalField(),
                ),
                numbres_of_pieces_out=Coalesce(
                    Sum(
                        F("inventoryinto__numbres_of_pieces")
                        * F("inventoryinto__inventoryout__quantity")
                    ),
                    0,
                    output_field=DecimalField(),
                ),
            )
            .values(
                "id_category__name",
                "available_count",
                "unavailable_count",
                "total_quantity_in",
                "total_quantity_out",
                "total_price",
                "inventoryinto__capacity",
                "inventoryinto__weight",
                "capacity_out",
                "numbres_of_pieces_out",
                "inventoryinto__numbres_of_pieces",
            )
        )

        # Sérialiser les résultats
        serializer = InventorySummarybyCategorySerializer(results, many=True)

    data = serializer.data
    response_data = {
        "status": "success",
        "data": data,
        "message": "Data retrieved successfully",
    }
    return Response(response_data, status=status.HTTP_200_OK)


##########################################################################


# 3333333333333333333333333333333333333333333333333333333333333333333333
#
# list statistique by article
#
# 3333333333333333333333333333333333333333333333333333333333333#########
@api_view(["GET"])
def Statistique_total_stock_int_retrieve_month_article_list(request, year):
    user__organisation__id = funct__id__entreprise(request=request)
    # Obtenir le nombre d'articles disponibles et indisponibles, la quantité totale entrée et sortie, et le prix total pour chaque catégorie pour l'année spécifiée
    results = (
        Inventory.objects.filter(
            Q(
                inventoryinto__date_modification__year=year
            )  # Filtre par année de création des entrées
            | Q(inventoryinto__inventoryout__date_modification__year=year),
            entreprise__id=user__organisation__id,  # Filtre par année de création des sorties
        )
        .annotate(
            available_count=Coalesce(
                Count(
                    "inventoryinto",
                    filter=Q(inventoryinto__inventoryout__isAvailable=True),
                    distinct=True,
                ),
                0,
            ),
            unavailable_count=Coalesce(
                Count(
                    "inventoryinto",
                    filter=Q(inventoryinto__inventoryout__isAvailable=False),
                    distinct=True,
                ),
                0,
            ),
            total_quantity_in=Coalesce(Sum("inventoryinto__quantity"), 0),
            total_quantity_out=Coalesce(
                Sum("inventoryinto__inventoryout__quantity"), 0
            ),
            total_price=Coalesce(
                Sum(
                    F("inventoryinto__quantity")
                    * F("inventoryinto__price_used_by_entreprise")
                ),
                0,
                output_field=DecimalField(),
            ),
            capacity_out=Coalesce(
                Sum(
                    F("inventoryinto__capacity")
                    * F("inventoryinto__inventoryout__quantity")
                ),
                0,
                output_field=DecimalField(),
            ),
            numbres_of_pieces_out=Coalesce(
                Sum(
                    F("inventoryinto__numbres_of_pieces")
                    * F("inventoryinto__inventoryout__quantity")
                ),
                0,
                output_field=DecimalField(),
            ),
            year=Coalesce(
                ExtractYear(F("inventoryinto__date_modification")),
                ExtractYear(F("inventoryinto__inventoryout__date_modification")),
                0,
            ),
            month=Coalesce(
                ExtractMonth(F("inventoryinto__date_modification")),
                ExtractMonth(F("inventoryinto__inventoryout__date_modification")),
                0,
            ),
            day=Coalesce(
                ExtractDay(F("inventoryinto__date_modification")),
                ExtractDay(F("inventoryinto__inventoryout__date_modification")),
                0,
            ),
            week=Coalesce(
                ExtractWeekDay(F("inventoryinto__date_modification")),
                ExtractWeekDay(F("inventoryinto__inventoryout__date_modification")),
                0,
            ),
        )
        .order_by("-month")
        .values(
            "designation",
            "available_count",
            "year",
            "day",
            "month",
            "week",
            "unavailable_count",
            "total_quantity_in",
            "total_quantity_out",
            "total_price",
            "inventoryinto__capacity",
            "inventoryinto__weight",
            "capacity_out",
            "numbres_of_pieces_out",
            "inventoryinto__numbres_of_pieces",
        )
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
    user__organisation__id = funct__id__entreprise(request=request)
    # Obtenir le nombre d'articles disponibles et indisponibles, la quantité totale entrée et sortie, et le prix total pour chaque catégorie pour l'année spécifiée
    results = (
        Inventory.objects.filter(entreprise__id=user__organisation__id)
        .annotate(
            available_count=Coalesce(
                Count(
                    "inventoryinto",
                    filter=Q(inventoryinto__inventoryout__isAvailable=True),
                    distinct=True,
                ),
                0,
            ),
            unavailable_count=Coalesce(
                Count(
                    "inventoryinto",
                    filter=Q(inventoryinto__inventoryout__isAvailable=False),
                    distinct=True,
                ),
                0,
            ),
            total_quantity_in=Coalesce(Sum("inventoryinto__quantity"), 0),
            total_quantity_out=Coalesce(
                Sum("inventoryinto__inventoryout__quantity"), 0
            ),
            total_price=Coalesce(
                Sum(
                    F("inventoryinto__quantity")
                    * F("inventoryinto__price_used_by_entreprise")
                ),
                0,
                output_field=DecimalField(),
            ),
            capacity_out=Coalesce(
                Sum(
                    F("inventoryinto__capacity")
                    * F("inventoryinto__inventoryout__quantity")
                ),
                0,
                output_field=DecimalField(),
            ),
            numbres_of_pieces_out=Coalesce(
                Sum(
                    F("inventoryinto__numbres_of_pieces")
                    * F("inventoryinto__inventoryout__quantity")
                ),
                0,
                output_field=DecimalField(),
            ),
            year=Coalesce(
                ExtractYear(F("inventoryinto__date_modification")),
                ExtractYear(F("inventoryinto__inventoryout__date_modification")),
                0,
            ),
            month=Coalesce(
                ExtractMonth(F("inventoryinto__date_modification")),
                ExtractMonth(F("inventoryinto__inventoryout__date_modification")),
                0,
            ),
            day=Coalesce(
                ExtractDay(F("inventoryinto__date_modification")),
                ExtractDay(F("inventoryinto__inventoryout__date_modification")),
                0,
            ),
            week=Coalesce(
                ExtractWeekDay(F("inventoryinto__date_modification")),
                ExtractWeekDay(F("inventoryinto__inventoryout__date_modification")),
                0,
            ),
        )
        .order_by("-year")
        .values(
            "designation",
            "available_count",
            "year",
            "day",
            "month",
            "week",
            "unavailable_count",
            "total_quantity_in",
            "total_quantity_out",
            "total_price",
            "inventoryinto__capacity",
            "inventoryinto__weight",
            "capacity_out",
            "numbres_of_pieces_out",
            "inventoryinto__numbres_of_pieces",
        )
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
    user__organisation__id = funct__id__entreprise(request=request)
    # Obtenir le nombre d'articles disponibles et indisponibles, la quantité totale entrée et sortie, et le prix total pour chaque catégorie pour l'année spécifiée
    results = (
        Inventory.objects.filter(
            Q(
                inventoryinto__date_modification__year=year,
                inventoryinto__date_modification__month=month,
            )  # Filtre par année de création des entrées
            | Q(
                inventoryinto__inventoryout__date_modification__year=year,
                inventoryinto__inventoryout__date_modification__month=month,
            ),
            entreprise__id=user__organisation__id,  # Filtre par année de création des sorties
        )
        .annotate(
            available_count=Coalesce(
                Count(
                    "inventoryinto",
                    filter=Q(inventoryinto__inventoryout__isAvailable=True),
                    distinct=True,
                ),
                0,
            ),
            unavailable_count=Coalesce(
                Count(
                    "inventoryinto",
                    filter=Q(inventoryinto__inventoryout__isAvailable=False),
                    distinct=True,
                ),
                0,
            ),
            total_quantity_in=Coalesce(Sum("inventoryinto__quantity"), 0),
            total_quantity_out=Coalesce(
                Sum("inventoryinto__inventoryout__quantity"), 0
            ),
            total_price=Coalesce(
                Sum(
                    F("inventoryinto__quantity")
                    * F("inventoryinto__price_used_by_entreprise")
                ),
                0,
                output_field=DecimalField(),
            ),
            capacity_out=Coalesce(
                Sum(
                    F("inventoryinto__capacity")
                    * F("inventoryinto__inventoryout__quantity")
                ),
                0,
                output_field=DecimalField(),
            ),
            numbres_of_pieces_out=Coalesce(
                Sum(
                    F("inventoryinto__numbres_of_pieces")
                    * F("inventoryinto__inventoryout__quantity")
                ),
                0,
                output_field=DecimalField(),
            ),
            year=Coalesce(
                ExtractYear(F("inventoryinto__date_modification")),
                ExtractYear(F("inventoryinto__inventoryout__date_modification")),
                0,
            ),
            month=Coalesce(
                ExtractMonth(F("inventoryinto__date_modification")),
                ExtractMonth(F("inventoryinto__inventoryout__date_modification")),
                0,
            ),
            day=Coalesce(
                ExtractDay(F("inventoryinto__date_modification")),
                ExtractDay(F("inventoryinto__inventoryout__date_modification")),
                0,
            ),
            week=Coalesce(
                ExtractWeekDay(F("inventoryinto__date_modification")),
                ExtractWeekDay(F("inventoryinto__inventoryout__date_modification")),
                0,
            ),
        )
        .order_by("-day")
        .values(
            "designation",
            "available_count",
            "year",
            "day",
            "month",
            "week",
            "unavailable_count",
            "total_quantity_in",
            "total_quantity_out",
            "total_price",
            "inventoryinto__capacity",
            "inventoryinto__weight",
            "capacity_out",
            "numbres_of_pieces_out",
            "inventoryinto__numbres_of_pieces",
        )
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
    user__organisation__id = funct__id__entreprise(request=request)
    # Retrieve the latest setting to get the current currency
    latest_setting = Setting.objects.filter(
        entreprise__id=user__organisation__id
    ).latest("id")
    current_currency = latest_setting.currency
    # Supposons que vous ayez un modèle Article avec une date de création
    total_articles = (
        InventoryInto.objects.filter(
            currency_used_by_entreprise=current_currency,
            entreprise__id=user__organisation__id,
        )
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
    user__organisation__id = funct__id__entreprise(request=request)
    # Retrieve the latest setting to get the current currency
    latest_setting = Setting.objects.filter(
        entreprise__id=user__organisation__id
    ).latest("id")
    current_currency = latest_setting.currency
    # Supposons que vous ayez un modèle Article avec une date de création
    total_articles = (
        InventoryInto.objects.filter(
            date_modification__year=year,
            date_modification__month=month,
            currency_used_by_entreprise=current_currency,
            entreprise__id=user__organisation__id,
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
    latest_setting = Setting.objects.latest("id")
    current_currency = latest_setting.currency
    # Supposons que vous ayez un modèle Article avec une date de création
    total_articles = (
        InventoryInto.objects.filter(
            date_modification__year=year,
            id_article__designation=article,
            currency_used_by_entreprise=current_currency,
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
    latest_setting = Setting.objects.latest("id")
    current_currency = latest_setting.currency

    # Supposons que vous ayez un modèle Article avec une date de création
    total_articles = (
        InventoryInto.objects.filter(
            id_article__designation=article,
            currency_used_by_entreprise=current_currency,
        )
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
    latest_setting = Setting.objects.latest("id")
    current_currency = latest_setting.currency
    # Supposons que vous ayez un modèle Article avec une date de création
    total_articles = (
        InventoryInto.objects.filter(
            date_modification__year=year,
            date_modification__month=month,
            id_article__designation=article,
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
    latest_setting = Setting.objects.latest("id")
    current_currency = latest_setting.currency
    # Supposons que vous ayez un modèle Article avec une date de création
    total_articles = (
        InventoryInto.objects.filter(
            date_modification__year=year,
            id_article__id_category__name=category,
            currency_used_by_entreprise=current_currency,
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
    latest_setting = Setting.objects.latest("id")
    current_currency = latest_setting.currency
    # Supposons que vous ayez un modèle Article avec une date de création
    total_articles = (
        InventoryInto.objects.filter(
            id_article__id_category__name=category,
            currency_used_by_entreprise=current_currency,
        )
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
    latest_setting = Setting.objects.latest("id")
    current_currency = latest_setting.currency
    total_articles = (
        InventoryInto.objects.filter(
            date_modification__year=year,
            date_modification__month=month,
            id_article__id_category__name=category,
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


################################################################ Pour les littres


### Vues des statistiques des differentes sorties
#
#


class SettingViewSet(viewsets.ModelViewSet):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer
    # a ajouter manuelement partout
    # pagination_class = CustomPagination
    authentication_classes = [
        authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    ]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        # Récupérer l'utilisateur actuellement connecté
        user = self.request.user
        userModel = User.objects.get(id=user.id)
        user__organisation__id = ""
        if userModel.entreprise:
            if userModel.entreprise.id:
                user__organisation__id = userModel.entreprise.id
                print("categorie machine")
                print(user__organisation__id)

                # Filtrer les posts de blog appartenant à l'utilisateur et à son organisation
                return queryset.filter(entreprise__id=user__organisation__id)
        else:
            return queryset.all()

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
        queryset = ""
        period = request.query_params.get("period", "years")
        type = request.query_params.get("type", "article")
        month = request.query_params.get("month", 10)
        year = request.query_params.get("year", 2024)
        print(period)
        period = str(period)
        user__organisation__id = funct__id__entreprise(request=request)
        data: list = []

        if period == "days":
            if type == "article":
                try:
                    machines = list(
                        Machine.objects.filter(entreprise__id=user__organisation__id)
                        .values("nom")
                        .distinct()
                    )
                    machines = [dictionnaire["nom"] for dictionnaire in machines]
                    print(machines)
                except Machine.DoesNotExist:
                    return Response({"error": "Machines not found"}, status=404)

                def func_get_time(machine_name, year, month):
                    time_data = (
                        Diagnostics.objects.filter(
                            id_machine__nom=machine_name,
                            entreprise__id=user__organisation__id,
                            date_modification__year=year,
                            date_modification__month=month,
                        )
                        .values("date_modification__day")
                        .distinct()
                    )
                    time_data = [
                        dictionnaire["date_modification__day"]
                        for dictionnaire in time_data
                    ]
                    print(time_data)
                    return time_data

                def func_get_planned(machine_name, list_time):
                    data: list = []
                    for time in list_time:
                        planned_subquery = (
                            PlanifierMaintenance.objects.filter(
                                id_machine__nom=machine_name,
                                date_modification__day=time,
                                entreprise__id=user__organisation__id,
                            )
                            .annotate(presence_count=Count("id"))
                            .values("presence_count")
                            .distinct()
                        )
                        planned_subquery = [
                            dictionnaire["presence_count"]
                            for dictionnaire in planned_subquery
                        ]
                        for number in planned_subquery:
                            data.append(number)
                        print(data)

                    return data

                def func_get_actual(machine_name, list_time):
                    data: list = []
                    for time in list_time:
                        actual_subquery = (
                            Diagnostics.objects.filter(
                                id_machine__nom=machine_name,
                                date_modification__day=time,
                                isDiagnostic=True,
                                isRepair=False,
                                entreprise__id=user__organisation__id,
                            )
                            .annotate(presence_count=Count("id"))
                            .values("presence_count")
                            .distinct()
                        )
                        actual_subquery = [
                            dictionnaire["presence_count"]
                            for dictionnaire in actual_subquery
                        ]
                        for number in actual_subquery:
                            data.append(number)
                    return data

                for name in machines:
                    time = func_get_time(machine_name=name, year=year, month=month)
                    planned = func_get_planned(machine_name=name, list_time=time)
                    actual = func_get_actual(machine_name=name, list_time=time)
                    tmp = {
                        "name": name,
                        "datetime": time,
                        "planned": planned,
                        "actual": actual,
                        "total": len(planned) + len(actual),
                    }
                    data.append(tmp)
                print(data)
            elif type == "category":
                try:
                    machines = list(
                        CategorieMachine.objects.filter(
                            entreprise__id=user__organisation__id
                        )
                        .values("nom")
                        .distinct()
                    )
                    machines = [dictionnaire["nom"] for dictionnaire in machines]
                    print(machines)
                except CategorieMachine.DoesNotExist:
                    return Response({"error": "Machines not found"}, status=404)

                def func_get_time(machine_name, year, month):
                    time_data = (
                        Diagnostics.objects.filter(
                            id_machine__categorie__nom=machine_name,
                            entreprise__id=user__organisation__id,
                            date_modification__year=year,
                            date_modification__month=month,
                        )
                        .values("date_modification__day")
                        .distinct()
                    )
                    time_data = [
                        dictionnaire["date_modification__day"]
                        for dictionnaire in time_data
                    ]
                    print(time_data)
                    return time_data

                def func_get_planned(machine_name, list_time):
                    data: list = []
                    for time in list_time:
                        planned_subquery = (
                            PlanifierMaintenance.objects.filter(
                                id_machine__categorie__nom=machine_name,
                                date_modification__day=time,
                                entreprise__id=user__organisation__id,
                            )
                            .annotate(presence_count=Count("id"))
                            .values("presence_count")
                            .distinct()
                        )
                        planned_subquery = [
                            dictionnaire["presence_count"]
                            for dictionnaire in planned_subquery
                        ]
                        for number in planned_subquery:
                            data.append(number)
                        print(data)

                    return data

                def func_get_actual(machine_name, list_time):
                    data: list = []
                    for time in list_time:
                        actual_subquery = (
                            Diagnostics.objects.filter(
                                id_machine__categorie__nom=machine_name,
                                date_modification__day=time,
                                isDiagnostic=True,
                                isRepair=False,
                                entreprise__id=user__organisation__id,
                            )
                            .annotate(presence_count=Count("id"))
                            .values("presence_count")
                            .distinct()
                        )
                        actual_subquery = [
                            dictionnaire["presence_count"]
                            for dictionnaire in actual_subquery
                        ]
                        for number in actual_subquery:
                            data.append(number)
                    return data

                for name in machines:
                    time = func_get_time(machine_name=name, year=year, month=month)
                    planned = func_get_planned(machine_name=name, list_time=time)
                    actual = func_get_actual(machine_name=name, list_time=time)
                    tmp = {
                        "name": name,
                        "datetime": time,
                        "planned": planned,
                        "actual": actual,
                        "total": len(planned) + len(actual),
                    }
                    data.append(tmp)
                print(data)

        elif period == "month":
            if type == "article":
                try:
                    machines = list(
                        Machine.objects.filter(entreprise__id=user__organisation__id)
                        .values("nom")
                        .distinct()
                    )
                    machines = [dictionnaire["nom"] for dictionnaire in machines]
                    print(machines)
                except Machine.DoesNotExist:
                    return Response({"error": "Machines not found"}, status=404)

                def func_get_time(machine_name, year):
                    time_data = (
                        Diagnostics.objects.filter(
                            id_machine__nom=machine_name,
                            entreprise__id=user__organisation__id,
                            date_modification__year=year,
                        )
                        .values("date_modification__month")
                        .distinct()
                    )
                    time_data = [
                        dictionnaire["date_modification__month"]
                        for dictionnaire in time_data
                    ]
                    print(time_data)
                    return time_data

                def func_get_planned(machine_name, list_time):
                    data: list = []
                    for time in list_time:
                        planned_subquery = (
                            PlanifierMaintenance.objects.filter(
                                id_machine__nom=machine_name,
                                date_modification__month=time,
                                entreprise__id=user__organisation__id,
                            )
                            .annotate(presence_count=Count("id"))
                            .values("presence_count")
                            .distinct()
                        )
                        planned_subquery = [
                            dictionnaire["presence_count"]
                            for dictionnaire in planned_subquery
                        ]
                        for number in planned_subquery:
                            data.append(number)
                        print(data)

                    return data

                def func_get_actual(machine_name, list_time):
                    data: list = []
                    for time in list_time:
                        actual_subquery = (
                            Diagnostics.objects.filter(
                                id_machine__nom=machine_name,
                                date_modification__month=time,
                                isDiagnostic=True,
                                isRepair=False,
                                entreprise__id=user__organisation__id,
                            )
                            .annotate(presence_count=Count("id"))
                            .values("presence_count")
                            .distinct()
                        )
                        actual_subquery = [
                            dictionnaire["presence_count"]
                            for dictionnaire in actual_subquery
                        ]
                        for number in actual_subquery:
                            data.append(number)
                    return data

                for name in machines:
                    planned = func_get_planned(
                        machine_name=name,
                        list_time=func_get_time(machine_name=name, year=year),
                    )
                    actual = func_get_actual(
                        machine_name=name,
                        list_time=func_get_time(machine_name=name, year=year),
                    )
                    tmp = {
                        "name": name,
                        "datetime": func_get_time(machine_name=name, year=year),
                        "planned": planned,
                        "actual": actual,
                        "total": len(planned) + len(actual),
                    }
                    data.append(tmp)
                print(data)

            elif type == "category":
                try:
                    machines = list(
                        CategorieMachine.objects.filter(
                            entreprise__id=user__organisation__id
                        )
                        .values("nom")
                        .distinct()
                    )
                    machines = [dictionnaire["nom"] for dictionnaire in machines]
                    print(machines)
                except CategorieMachine.DoesNotExist:
                    return Response({"error": "Machines not found"}, status=404)

                def func_get_time(machine_name, year):
                    time_data = (
                        Diagnostics.objects.filter(
                            id_machine__categorie__nom=machine_name,
                            entreprise__id=user__organisation__id,
                            date_modification__year=year,
                        )
                        .values("date_modification__month")
                        .distinct()
                    )
                    time_data = [
                        dictionnaire["date_modification__month"]
                        for dictionnaire in time_data
                    ]
                    print(time_data)
                    return time_data

                def func_get_planned(machine_name, list_time):
                    data: list = []
                    for time in list_time:
                        planned_subquery = (
                            PlanifierMaintenance.objects.filter(
                                id_machine__categorie__nom=machine_name,
                                date_modification__month=time,
                                entreprise__id=user__organisation__id,
                            )
                            .annotate(presence_count=Count("id"))
                            .values("presence_count")
                            .distinct()
                        )
                        planned_subquery = [
                            dictionnaire["presence_count"]
                            for dictionnaire in planned_subquery
                        ]
                        for number in planned_subquery:
                            data.append(number)
                        print(data)

                    return data

                def func_get_actual(machine_name, list_time):
                    data: list = []
                    for time in list_time:
                        actual_subquery = (
                            Diagnostics.objects.filter(
                                id_machine__categorie__nom=machine_name,
                                date_modification__month=time,
                                isDiagnostic=True,
                                isRepair=False,
                                entreprise__id=user__organisation__id,
                            )
                            .annotate(presence_count=Count("id"))
                            .values("presence_count")
                            .distinct()
                        )
                        actual_subquery = [
                            dictionnaire["presence_count"]
                            for dictionnaire in actual_subquery
                        ]
                        for number in actual_subquery:
                            data.append(number)
                    return data

                for name in machines:
                    planned = func_get_planned(
                        machine_name=name,
                        list_time=func_get_time(machine_name=name, year=year),
                    )
                    actual = func_get_actual(
                        machine_name=name,
                        list_time=func_get_time(machine_name=name, year=year),
                    )
                    tmp = {
                        "name": name,
                        "datetime": func_get_time(machine_name=name, year=year),
                        "planned": planned,
                        "actual": actual,
                        "total": len(planned) + len(actual),
                    }
                    data.append(tmp)
                print(data)

        elif period == "years":
            if type == "article":
                try:
                    machines = list(
                        Machine.objects.filter(entreprise__id=user__organisation__id)
                        .values("nom")
                        .distinct()
                    )
                    machines = [dictionnaire["nom"] for dictionnaire in machines]
                    print(machines)
                except Machine.DoesNotExist:
                    return Response({"error": "Machines not found"}, status=404)

                def func_get_times(machine_name):
                    time_data = (
                        Diagnostics.objects.filter(
                            id_machine__nom=machine_name,
                            entreprise__id=user__organisation__id,
                        )
                        .values("date_modification__year")
                        .distinct()
                    )
                    time_data = [
                        dictionnaire["date_modification__year"]
                        for dictionnaire in time_data
                    ]
                    print(time_data)
                    return time_data

                def func_get_time(machine_name, year):
                    time_data = (
                        Diagnostics.objects.filter(
                            id_machine__nom=machine_name,
                            entreprise__id=user__organisation__id,
                            date_modification__year=year,
                        )
                        .values("date_modification__month")
                        .distinct()
                    )
                    time_data = [
                        dictionnaire["date_modification__year"]
                        for dictionnaire in time_data
                    ]
                    print(time_data)
                    return time_data

                def func_get_planned(machine_name, list_time):
                    data: list = []
                    for time in list_time:
                        planned_subquery = (
                            PlanifierMaintenance.objects.filter(
                                id_machine__nom=machine_name,
                                date_modification__year=time,
                                entreprise__id=user__organisation__id,
                            )
                            .annotate(presence_count=Count("id"))
                            .values("presence_count")
                            .distinct()
                        )
                        planned_subquery = [
                            dictionnaire["presence_count"]
                            for dictionnaire in planned_subquery
                        ]
                        for number in planned_subquery:
                            data.append(number)
                        print(data)
                    return data

                def func_get_actual(machine_name, list_time):
                    data: list = []
                    for time in list_time:
                        actual_subquery = (
                            Diagnostics.objects.filter(
                                id_machine__nom=machine_name,
                                date_modification__year=time,
                                isDiagnostic=True,
                                isRepair=False,
                                entreprise__id=user__organisation__id,
                            )
                            .annotate(presence_count=Count("id"))
                            .values("presence_count")
                            .distinct()
                        )
                        actual_subquery = [
                            dictionnaire["presence_count"]
                            for dictionnaire in actual_subquery
                        ]
                        for number in actual_subquery:
                            data.append(number)
                    return data

                for name in machines:
                    planned = func_get_planned(
                        machine_name=name, list_time=func_get_times(machine_name=name)
                    )
                    actual = func_get_actual(
                        machine_name=name, list_time=func_get_times(machine_name=name)
                    )
                    tmp = {
                        "name": name,
                        "datetime": func_get_times(machine_name=name),
                        "planned": planned,
                        "actual": actual,
                        "total": len(planned) + len(actual),
                    }
                    data.append(tmp)
                print(data)

            elif type == "category":

                try:
                    machines = list(
                        CategorieMachine.objects.filter(
                            entreprise__id=user__organisation__id
                        )
                        .values("nom")
                        .distinct()
                    )
                    machines = [dictionnaire["nom"] for dictionnaire in machines]
                    print(machines)
                except CategorieMachine.DoesNotExist:
                    return Response({"error": "Machines not found"}, status=404)

                def func_get_times(machine_name):
                    time_data = (
                        Diagnostics.objects.filter(
                            id_machine__categorie__nom=machine_name,
                            entreprise__id=user__organisation__id,
                        )
                        .values("date_modification__year")
                        .distinct()
                    )
                    time_data = [
                        dictionnaire["date_modification__year"]
                        for dictionnaire in time_data
                    ]
                    print(time_data)
                    return time_data

                def func_get_planned(machine_name, list_time):
                    data: list = []
                    for time in list_time:
                        planned_subquery = (
                            PlanifierMaintenance.objects.filter(
                                id_machine__categorie__nom=machine_name,
                                date_modification__year=time,
                                entreprise__id=user__organisation__id,
                            )
                            .annotate(presence_count=Count("id"))
                            .values("presence_count")
                            .distinct()
                        )
                        planned_subquery = [
                            dictionnaire["presence_count"]
                            for dictionnaire in planned_subquery
                        ]
                        for number in planned_subquery:
                            data.append(number)
                        print(data)

                    return data

                def func_get_actual(machine_name, list_time):
                    data: list = []
                    for time in list_time:
                        actual_subquery = (
                            Diagnostics.objects.filter(
                                id_machine__categorie__nom=machine_name,
                                date_modification__year=time,
                                isDiagnostic=True,
                                isRepair=False,
                                entreprise__id=user__organisation__id,
                            )
                            .annotate(presence_count=Count("id"))
                            .values("presence_count")
                            .distinct()
                        )
                        actual_subquery = [
                            dictionnaire["presence_count"]
                            for dictionnaire in actual_subquery
                        ]
                        for number in actual_subquery:
                            data.append(number)
                    return data

                for name in machines:
                    planned = func_get_planned(
                        machine_name=name, list_time=func_get_times(machine_name=name)
                    )
                    actual = func_get_actual(
                        machine_name=name, list_time=func_get_times(machine_name=name)
                    )
                    tmp = {
                        "name": name,
                        "datetime": func_get_times(machine_name=name),
                        "planned": planned,
                        "actual": actual,
                        "total": len(planned) + len(actual),
                    }
                    data.append(tmp)
                print(data)
        else:
            return Response({"error": "Invalid period parameter."}, status=400)

        """ if type == "article":
            serializer = MachineStatisticsSerializerForArticle(queryset, many=True)
        elif type == "category":
            serializer = MachineStatisticsSerializerForCategory(queryset, many=True)"""

        response_data = {
            "status": "success",
            "data": data,
            "message": "Data retrieved successfully",
        }
        return Response(response_data)


# pour le stock
#
#
class Statistique_stock_list_retrieve(APIView):
    def get(self, request, format=None):
        # Annotate the queryset with planned and actual counts
        serializer = ""
        queryset = ""
        period = request.query_params.get("period", "years")
        type = request.query_params.get("type", "article")
        month = request.query_params.get("month", 10)
        year = request.query_params.get("year", 2024)
        stock = request.query_params.get("stock", "in")
        user__organisation__id = funct__id__entreprise(request=request)
        data: list = []

        if period == "days":
            if stock == "in":
                if type == "article":
                    try:
                        db = list(
                            Inventory.objects.filter(entreprise__id=user__organisation__id)
                            .values("designation")
                            .distinct()
                        )
                        db = [dictionnaire["designation"] for dictionnaire in db]
                        print(db)
                    except Inventory.DoesNotExist:
                        return Response({"error": "Machines not found"}, status=404)
                    

                    def func_get_time(name, year, month):
                        time_data = (
                            InventoryInto.objects.filter(
                                id_article__designation=name,
                                entreprise__id=user__organisation__id,
                                date_modification__year=year,
                                date_modification__month=month,
                            )
                            .values("date_modification__day")
                            .distinct()
                        )
                        time_data = [
                            dictionnaire["date_modification__day"]
                            for dictionnaire in time_data
                        ]
                        print(time_data)
                        return time_data

                    def func_get_available(name, list_time):
                        data: list = []
                        for time in list_time:
                            subquery = (
                                InventoryInto.objects.filter(
                                    id_article__designation=name,
                                    date_modification__day=time,
                                    entreprise__id=user__organisation__id,
                                )
                                .annotate(
                                    available=Coalesce(
                                        Count(
                                            "id",
                                            filter=Q(inventoryout__isAvailable=True),
                                            distinct=True,
                                        ),
                                        0,
                                    ),
                                )
                                .values("available")
                                .distinct()
                            )
                            subquery = [dictionnaire["available"]for dictionnaire in subquery]
                            for number in subquery:
                                data.append(number)
                            print(data)

                        return data

                    def func_get_quantity(name, list_time):
                        data: list = []
                        for time in list_time:
                            subquery = (
                                InventoryInto.objects.filter(
                                    id_article__designation=name,
                                    date_modification__day=time,
                                    entreprise__id=user__organisation__id,
                                )
                                .annotate(
                                    quantity=Coalesce(Sum("quantity"), 0),
                                )
                                .values("quantity")
                                .distinct()
                            )
                            subquery = [
                                dictionnaire["quantity"] for dictionnaire in subquery
                            ]
                            for number in subquery:
                                data.append(number)
                            print(data)

                        return data

                    def func_get_capacity(name, list_time):
                        data: list = []
                        for time in list_time:
                            subquery = (
                                InventoryInto.objects.filter(
                                    id_article__designation=name,
                                    date_modification__day=time,
                                    entreprise__id=user__organisation__id,
                                )
                                .values("capacity")
                                .distinct()
                            )
                            subquery = [
                                dictionnaire["capacity"] for dictionnaire in subquery
                            ]
                            for number in subquery:
                                data.append(number)
                            print(data)
                        return data

                    def func_get_price(name, list_time):
                        data: list = []
                        for time in list_time:
                            subquery = (
                                InventoryInto.objects.filter(
                                    id_article__designation=name,
                                    date_modification__day=time,
                                    entreprise__id=user__organisation__id,
                                )
                                .annotate(
                                    price=Coalesce(
                                        Sum(
                                            F("quantity")
                                            * F("price_used_by_entreprise")
                                        ),
                                        0,
                                        output_field=DecimalField(),
                                    ),
                                )
                                .values("price")
                                .distinct()
                            )
                            subquery = [
                                dictionnaire["price"] for dictionnaire in subquery
                            ]
                            for number in subquery:
                                data.append(number)
                            print(data)
                        return data

                    def func_get_numbres_of_pieces(name, list_time):
                        data: list = []
                        for time in list_time:
                            subquery = (
                                InventoryInto.objects.filter(
                                    id_article__designation=name,
                                    date_modification__day=time,
                                    entreprise__id=user__organisation__id,
                                )
                                .values("numbres_of_pieces")
                                .distinct()
                            )
                            subquery = [
                                dictionnaire["numbres_of_pieces"]
                                for dictionnaire in subquery
                            ]
                            for number in subquery:
                                data.append(number)
                            print(data)
                        return data

                    def func_get_weight(name, list_time):
                        data: list = []
                        for time in list_time:
                            subquery = (
                                InventoryInto.objects.filter(
                                    id_article__designation=name,
                                    date_modification__day=time,
                                    entreprise__id=user__organisation__id,
                                )
                                .values('weight')
                                .distinct()
                            )
                            subquery = [
                                dictionnaire['weight'] for dictionnaire in subquery
                            ]
                            for number in subquery:
                                data.append(number)
                            print(data)
                        return data

                    for name in db:
                        time = func_get_time(name=name, year=year, month=month)
                        available = func_get_available(name=name, list_time=time)
                        quantity = func_get_quantity(name=name, list_time=time)
                        capacity = func_get_capacity(name=name, list_time=time)
                        weight = func_get_weight(name=name, list_time=time)
                        numbres_of_pieces = func_get_numbres_of_pieces(
                            name=name, list_time=time
                        )
                        price = func_get_price(name=name, list_time=time)
                        tmp = {
                            "name": name,
                            "datetime": time,
                            "available": available,
                            "quantity": quantity,
                            "capacity": capacity,
                            "weight": weight,
                            "numbres_of_pieces": numbres_of_pieces,
                            "price": price,
                        }
                        data.append(tmp)
                    print(data)
                elif type == "category":
                    try:
                        bd = list(
                            CategoryInventory.objects.filter(
                                entreprise__id=user__organisation__id
                            )
                            .values("name")
                            .distinct()
                        )
                        bd = [dictionnaire["name"] for dictionnaire in bd]
                        print(bd)
                    except CategoryInventory.DoesNotExist:
                        return Response({"error": "Machines not found"}, status=404)

                    def func_get_time(name, year, month):
                            time_data = (
                                InventoryInto.objects.filter(
                                    id_article__id_category__name=name,
                                    entreprise__id=user__organisation__id,
                                    date_modification__year=year,
                                    date_modification__month=month,
                                )
                                .values("date_modification__day")
                                .distinct()
                            )
                            time_data = [
                                dictionnaire["date_modification__day"]
                                for dictionnaire in time_data
                            ]
                            print(time_data)
                            return time_data

                    def func_get_available(name, list_time):
                            data: list = []
                            for time in list_time:
                                subquery = (
                                    InventoryInto.objects.filter(
                                        id_article__id_category__name=name,
                                        date_modification__day=time,
                                        entreprise__id=user__organisation__id,
                                    )
                                    .annotate(
                                        available_count=Coalesce(
                                            Count(
                                                "id",
                                                filter=Q(inventoryout__isAvailable=True),
                                                distinct=True,
                                            ),
                                            0,
                                        ),
                                    )
                                    .values("available_count")
                                    .distinct()
                                )
                                subquery = [
                                    dictionnaire["available_count"]
                                    for dictionnaire in subquery
                                ]
                                for number in subquery:
                                    data.append(number)
                                print(data)

                            return data

                    def func_get_quantity(name, list_time):
                            data: list = []
                            for time in list_time:
                                subquery = (
                                    InventoryInto.objects.filter(
                                        id_article__id_category__name=name,
                                        date_modification__day=time,
                                        entreprise__id=user__organisation__id,
                                    )
                                    .annotate(
                                        quantity=Coalesce(Sum("quantity"), 0),
                                    )
                                    .values("quantity")
                                    .distinct()
                                )
                                subquery = [
                                    dictionnaire["quantity"] for dictionnaire in subquery
                                ]
                                for number in subquery:
                                    data.append(number)
                                print(data)

                            return data

                    def func_get_capacity(name, list_time):
                            data: list = []
                            for time in list_time:
                                subquery = (
                                    InventoryInto.objects.filter(
                                        id_article__id_category__name=name,
                                        date_modification__day=time,
                                        entreprise__id=user__organisation__id,
                                    )
                                    .values("capacity")
                                    .distinct()
                                )
                                subquery = [
                                    dictionnaire["capacity"] for dictionnaire in subquery
                                ]
                                for number in subquery:
                                    data.append(number)
                                print(data)
                            return data

                    def func_get_price(name, list_time):
                            data: list = []
                            for time in list_time:
                                subquery = (
                                    InventoryInto.objects.filter(
                                        id_article__id_category__name=name,
                                        date_modification__day=time,
                                        entreprise__id=user__organisation__id,
                                    )
                                    .annotate(
                                        price=Coalesce(
                                            Sum(
                                                F("quantity")
                                                * F("price_used_by_entreprise")
                                            ),
                                            0,
                                            output_field=DecimalField(),
                                        ),
                                    )
                                    .values("price")
                                    .distinct()
                                )
                                subquery = [
                                    dictionnaire["price"] for dictionnaire in subquery
                                ]
                                for number in subquery:
                                    data.append(number)
                                print(data)
                            return data

                    def func_get_numbres_of_pieces(name, list_time):
                            data: list = []
                            for time in list_time:
                                subquery = (
                                    InventoryInto.objects.filter(
                                        id_article__id_category__name=name,
                                        date_modification__day=time,
                                        entreprise__id=user__organisation__id,
                                    )
                                    .values("numbres_of_pieces")
                                    .distinct()
                                )
                                subquery = [
                                    dictionnaire["numbres_of_pieces"]
                                    for dictionnaire in subquery
                                ]
                                for number in subquery:
                                    data.append(number)
                                print(data)
                            return data

                    def func_get_weight(name, list_time):
                            data: list = []
                            for time in list_time:
                                subquery = (
                                    InventoryInto.objects.filter(
                                        id_article__id_category__name=name,
                                        date_modification__day=time,
                                        entreprise__id=user__organisation__id,
                                    )
                                    .values('weight')
                                    .distinct()
                                )
                                subquery = [
                                    dictionnaire['weight'] for dictionnaire in subquery
                                ]
                                for number in subquery:
                                    data.append(number)
                                print(data)
                            return data

                    for name in bd:
                            time = func_get_time(name=name, year=year, month=month)
                            available = func_get_available(name=name, list_time=time)
                            quantity = func_get_quantity(name=name, list_time=time)
                            capacity = func_get_capacity(name=name, list_time=time)
                            weight = func_get_weight(name=name, list_time=time)
                            numbres_of_pieces = func_get_numbres_of_pieces(
                                name=name, list_time=time
                            )
                            price = func_get_price(name=name, list_time=time)
                            tmp = {
                                "name": name,
                                "datetime": time,
                                "available": available,
                                "quantity": quantity,
                                "capacity": capacity,
                                "weight": weight,
                                "numbres_of_pieces": numbres_of_pieces,
                                "price": price,
                            }
                            data.append(tmp)
                    print(data)
            if stock == "out":
                if type == "article":
                    try:
                        db = list(
                            Inventory.objects.filter(
                                entreprise__id=user__organisation__id
                            )
                            .values("designation")
                            .distinct()
                        )
                        db = [dictionnaire["designation"] for dictionnaire in db]
                        print(db)
                    except Inventory.DoesNotExist:
                        return Response({"error": "Machines not found"}, status=404)

                    def func_get_time(name, year, month):
                        time_data = (
                            InventoryOut.objects.filter(
                                id_inventory_into__id_article__designation=name,
                                entreprise__id=user__organisation__id,
                                date_modification__year=year,
                                date_modification__month=month,
                            )
                            .values("date_modification__day")
                            .distinct()
                        )
                        time_data = [
                            dictionnaire["date_modification__day"]
                            for dictionnaire in time_data
                        ]
                        print(time_data)
                        return time_data

                    def func_get_available(name, list_time):
                        data: list = []
                        for time in list_time:
                            subquery = (
                                InventoryInto.objects.filter(
                                    id_inventory_into__id_article__designation=name,
                                    date_modification__day=time,
                                    entreprise__id=user__organisation__id,
                                )
                                .annotate(
                                    available_count=Coalesce(
                                        Count(
                                            "id",
                                            filter=Q(inventoryout__isAvailable=True),
                                            distinct=True,
                                        ),
                                        0,
                                    ),
                                )
                                .values("available_count")
                                .distinct()
                            )
                            subquery = [
                                dictionnaire["available_count"]
                                for dictionnaire in subquery
                            ]
                            for number in subquery:
                                data.append(number)
                            print(data)

                        return data

                    def func_get_quantity(name, list_time):
                        data: list = []
                        for time in list_time:
                            subquery = (
                                InventoryOut.objects.filter(
                                    id_inventory_into__id_article__designation=name,
                                    date_modification__day=time,
                                    entreprise__id=user__organisation__id,
                                )
                                .annotate(
                                    quantity=Coalesce(Sum("quantity"), 0),
                                )
                                .values("quantity")
                                .distinct()
                            )
                            subquery = [
                                dictionnaire["quantity"] for dictionnaire in subquery
                            ]
                            for number in subquery:
                                data.append(number)
                            print(data)

                        return data

                    def func_get_capacity(name, list_time):
                        data: list = []
                        for time in list_time:
                            subquery = (
                                InventoryOut.objects.filter(
                                       id_inventory_into__id_article__designation=name,
                                    date_modification__day=time,
                                    entreprise__id=user__organisation__id,
                                )
                                .values("capacity")
                                .distinct()
                            )
                            subquery = [
                                dictionnaire["capacity"] for dictionnaire in subquery
                            ]
                            for number in subquery:
                                data.append(number)
                            print(data)
                        return data

                    def func_get_price(name, list_time):
                        data: list = []
                        for time in list_time:
                            subquery = (
                                InventoryOut.objects.filter(
                                       id_inventory_into__id_article__designation=name,
                                    date_modification__day=time,
                                    entreprise__id=user__organisation__id,
                                )
                                .annotate(
                                    price=Coalesce(
                                        Sum(
                                            F("quantity")
                                            * F("price_used_by_entreprise")
                                        ),
                                        0,
                                        output_field=DecimalField(),
                                    ),
                                )
                                .values("price")
                                .distinct()
                            )
                            subquery = [
                                dictionnaire["price"] for dictionnaire in subquery
                            ]
                            for number in subquery:
                                data.append(number)
                            print(data)
                        return data

                    def func_get_numbres_of_pieces(name, list_time):
                        data: list = []
                        for time in list_time:
                            subquery = (
                                InventoryOut.objects.filter(
                                       id_inventory_into__id_article__designation=name,
                                    date_modification__day=time,
                                    entreprise__id=user__organisation__id,
                                )
                                .values("numbres_of_pieces")
                                .distinct()
                            )
                            subquery = [
                                dictionnaire["numbres_of_pieces"]
                                for dictionnaire in subquery
                            ]
                            for number in subquery:
                                data.append(number)
                            print(data)
                        return data

                    def func_get_weight(name, list_time):
                        data: list = []
                        for time in list_time:
                            subquery = (
                                InventoryInto.objects.filter(
                                    id_inventory_into__id_article__designation=name,
                                    date_modification__day=time,
                                    entreprise__id=user__organisation__id,
                                )
                                .values('weight')
                                .distinct()
                            )
                            subquery = [
                                dictionnaire['weight'] for dictionnaire in subquery
                            ]
                            for number in subquery:
                                data.append(number)
                            print(data)
                        return data

                    for name in db:
                        time = func_get_time(name=name, year=year, month=month)
                        available = func_get_available(name=name, list_time=time)
                        quantity = func_get_quantity(name=name, list_time=time)
                        capacity = func_get_capacity(name=name, list_time=time)
                        weight = func_get_weight(name=name, list_time=time)
                        numbres_of_pieces = func_get_numbres_of_pieces(
                            name=name, list_time=time
                        )
                        price = func_get_price(name=name, list_time=time)
                        tmp = {
                            "name": name,
                            "datetime": time,
                            "available": available,
                            "quantity": quantity,
                            "capacity": capacity,
                            "weight": weight,
                            "numbres_of_pieces": numbres_of_pieces,
                            "price": price,
                        }
                        data.append(tmp)
                    print(data)
                elif type == "category":
                    try:
                        bd = list(
                            CategoryInventory.objects.filter(
                                entreprise__id=user__organisation__id
                            )
                            .values("name")
                            .distinct()
                        )
                        bd = [dictionnaire["name"] for dictionnaire in bd]
                        print(bd)
                    except CategoryInventory.DoesNotExist:
                        return Response({"error": "Machines not found"}, status=404)

                    def func_get_time(name, year, month):
                            time_data = (
                                InventoryOut.objects.filter(
                                    id_inventory_into__id_article__id_category__name=name,
                                    entreprise__id=user__organisation__id,
                                    date_modification__year=year,
                                    date_modification__month=month,
                                )
                                .values("date_modification__day")
                                .distinct()
                            )
                            time_data = [
                                dictionnaire["date_modification__day"]
                                for dictionnaire in time_data
                            ]
                            print(time_data)
                            return time_data

                    def func_get_available(name, list_time):
                            data: list = []
                            for time in list_time:
                                subquery = (
                                    InventoryOut.objects.filter(
                                        id_inventory_into__id_article__id_category__name=name,
                                        date_modification__day=time,
                                        entreprise__id=user__organisation__id,
                                    )
                                    .annotate(
                                        available_count=Coalesce(
                                            Count(
                                                "id",
                                                filter=Q(inventoryout__isAvailable=True),
                                                distinct=True,
                                            ),
                                            0,
                                        ),
                                    )
                                    .values("available_count")
                                    .distinct()
                                )
                                subquery = [
                                    dictionnaire["available_count"]
                                    for dictionnaire in subquery
                                ]
                                for number in subquery:
                                    data.append(number)
                                print(data)

                            return data

                    def func_get_quantity(name, list_time):
                            data: list = []
                            for time in list_time:
                                subquery = (
                                    InventoryOut.objects.filter(
                                        id_inventory_into__id_article__id_category__name=name,
                                        date_modification__day=time,
                                        entreprise__id=user__organisation__id,
                                    )
                                    .annotate(
                                        quantity=Coalesce(Sum("quantity"), 0),
                                    )
                                    .values("quantity")
                                    .distinct()
                                )
                                subquery = [
                                    dictionnaire["quantity"] for dictionnaire in subquery
                                ]
                                for number in subquery:
                                    data.append(number)
                                print(data)

                            return data

                    def func_get_capacity(name, list_time):
                            data: list = []
                            for time in list_time:
                                subquery = (
                                    InventoryOut.objects.filter(
                                        id_inventory_into__id_article__id_category__name=name,
                                        date_modification__day=time,
                                        entreprise__id=user__organisation__id,
                                    )
                                    .values("capacity")
                                    .distinct()
                                )
                                subquery = [
                                    dictionnaire["capacity"] for dictionnaire in subquery
                                ]
                                for number in subquery:
                                    data.append(number)
                                print(data)
                            return data

                    def func_get_price(name, list_time):
                            data: list = []
                            for time in list_time:
                                subquery = (
                                    InventoryOut.objects.filter(
                                        id_inventory_into__id_article__id_category__name=name,
                                        date_modification__day=time,
                                        entreprise__id=user__organisation__id,
                                    )
                                    .annotate(
                                        price=Coalesce(
                                            Sum(
                                                F("quantity")
                                                * F("price_used_by_entreprise")
                                            ),
                                            0,
                                            output_field=DecimalField(),
                                        ),
                                    )
                                    .values("price")
                                    .distinct()
                                )
                                subquery = [
                                    dictionnaire["price"] for dictionnaire in subquery
                                ]
                                for number in subquery:
                                    data.append(number)
                                print(data)
                            return data

                    def func_get_numbres_of_pieces(name, list_time):
                            data: list = []
                            for time in list_time:
                                subquery = (
                                    InventoryOut.objects.filter(
                                        id_inventory_into__id_article__id_category__name=name,
                                        date_modification__day=time,
                                        entreprise__id=user__organisation__id,
                                    )
                                    .values("numbres_of_pieces")
                                    .distinct()
                                )
                                subquery = [
                                    dictionnaire["numbres_of_pieces"]
                                    for dictionnaire in subquery
                                ]
                                for number in subquery:
                                    data.append(number)
                                print(data)
                            return data

                    def func_get_weight(name, list_time):
                            data: list = []
                            for time in list_time:
                                subquery = (
                                    InventoryOut.objects.filter(
                                        id_inventory_into__id_article__id_category__name=name,
                                        date_modification__day=time,
                                        entreprise__id=user__organisation__id,
                                    )
                                    .values('weight')
                                    .distinct()
                                )
                                subquery = [
                                    dictionnaire['weight'] for dictionnaire in subquery
                                ]
                                for number in subquery:
                                    data.append(number)
                                print(data)
                            return data

                    for name in bd:
                            time = func_get_time(name=name, year=year, month=month)
                            available = func_get_available(name=name, list_time=time)
                            quantity = func_get_quantity(name=name, list_time=time)
                            capacity = func_get_capacity(name=name, list_time=time)
                            weight = func_get_weight(name=name, list_time=time)
                            numbres_of_pieces = func_get_numbres_of_pieces(
                                name=name, list_time=time
                            )
                            price = func_get_price(name=name, list_time=time)
                            tmp = {
                                "name": name,
                                "datetime": time,
                                "available": available,
                                "quantity": quantity,
                                "capacity": capacity,
                                "weight": weight,
                                "numbres_of_pieces": numbres_of_pieces,
                                "price": price,
                            }
                            data.append(tmp)
                    print(data)
        elif period == "month":
            if stock == "in":
                if type == "article":
                    try:
                        db = list(
                            Inventory.objects.filter(entreprise__id=user__organisation__id)
                            .values("designation")
                            .distinct()
                        )
                        db = [dictionnaire["designation"] for dictionnaire in db]
                        print(db)
                    except Inventory.DoesNotExist:
                        return Response({"error": "Machines not found"}, status=404)
                    
                    
                    def func_get_time(name, year, month):
                            time_data = (
                                InventoryInto.objects.filter(
                                    id_article__designation=name,
                                    entreprise__id=user__organisation__id,
                                    date_modification__year=year,
                                )
                                .values("date_modification__month")
                                .distinct()
                            )
                            time_data = [
                                dictionnaire["date_modification__month"]
                                for dictionnaire in time_data
                            ]
                            print(time_data)
                            return time_data

                    def func_get_available(name, list_time):
                            data: list = []
                            for time in list_time:
                                subquery = (
                                    InventoryInto.objects.filter(
                                        id_article__designation=name,
                                        date_modification__month=time,
                                        entreprise__id=user__organisation__id,
                                    )
                                    .annotate(
                                    available=Coalesce(
                                        Count(
                                            "id",
                                            filter=Q(inventoryout__isAvailable=True),
                                            distinct=True,
                                        ),
                                        0,
                                    ),
                                   )
                                    .values("available")
                                    .distinct()
                                )
                                subquery = [
                                    dictionnaire["available"] for dictionnaire in subquery
                                ]
                                for number in subquery:
                                    data.append(number)
                                print(data)
                            return data

                    def func_get_quantity(name, list_time):
                            data: list = []
                            for time in list_time:
                                subquery = (
                                    InventoryInto.objects.filter(
                                        id_article__designation=name,
                                        date_modification__month=time,
                                        entreprise__id=user__organisation__id,
                                    )
                                    .values("quantity")
                                    .distinct()
                                )
                                subquery = [
                                    dictionnaire["quantity"] for dictionnaire in subquery
                                ]
                                for number in subquery:
                                    data.append(number)
                                print(data)
                            return data

                    def func_get_capacity(name, list_time): 
                            data: list = []
                            for time in list_time:
                                subquery = (
                                    InventoryInto.objects.filter(
                                        id_article__designation=name,
                                        date_modification__month=time,
                                        entreprise__id=user__organisation__id,
                                    )
                                    .values("capacity")
                                    .distinct()
                                )
                                subquery = [
                                    dictionnaire["capacity"] for dictionnaire in subquery
                                ]
                                for number in subquery:
                                    data.append(number)
                                print(data)
                            return data
                    
                    def func_get_weight(name, list_time):
                            data: list = []
                            for time in list_time:
                                subquery = (
                                    InventoryInto.objects.filter(
                                        id_article__designation=name,
                                        date_modification__month=time,
                                        entreprise__id=user__organisation__id,
                                    )
                                    .values('weight')
                                    .distinct()
                                )
                                subquery = [
                                    dictionnaire['weight'] for dictionnaire in subquery
                                ]
                                for number in subquery:
                                    data.append(number)
                                print(data)
                            return data
                    
                    def func_get_numbres_of_pieces(name, list_time):
                            data: list = []
                            for time in list_time:
                                subquery = (
                                    InventoryInto.objects.filter(
                                        id_article__designation=name,
                                        date_modification__month=time,
                                        entreprise__id=user__organisation__id,
                                    )
                                    .values("numbres_of_pieces")
                                    .distinct()
                                )
                                subquery = [
                                    dictionnaire["numbres_of_pieces"]
                                    for dictionnaire in subquery
                                ]
                                for number in subquery:
                                    data.append(number)
                                print(data)
                            return data
                    
                    def func_get_price(name, list_time):
                            data: list = []
                            for time in list_time:
                                subquery = (
                                    InventoryInto.objects.filter(
                                        id_article__designation=name,
                                        date_modification__month=time,
                                        entreprise__id=user__organisation__id,
                                    )
                                    .values("price")
                                    .distinct()
                                )
                                subquery = [
                                    dictionnaire["price"] for dictionnaire in subquery
                                ]
                                for number in subquery:
                                    data.append(number)
                                print(data)
                            return data

                    for name in db:
                            time = func_get_time(name=name, year=year, month=month)
                            available = func_get_available(name=name, list_time=time)
                            quantity = func_get_quantity(name=name, list_time=time)
                            capacity = func_get_capacity(name=name, list_time=time)
                            weight = func_get_weight(name=name, list_time=time)
                            numbres_of_pieces = func_get_numbres_of_pieces(
                                name=name, list_time=time
                            )
                            price = func_get_price(name=name, list_time=time)
                            tmp = {
                                "name": name,
                                "datetime": time,
                                "available": available,
                                "quantity": quantity,
                                "capacity": capacity,
                                "weight": weight,
                                "numbres_of_pieces": numbres_of_pieces,
                                "price": price,
                            }
                            data.append(tmp)
                    print(data)
                elif type == "category":
                    try:
                        bd = list(
                            CategoryInventory.objects.filter(
                                entreprise__id=user__organisation__id
                            )
                            .values("name")
                            .distinct()
                        )
                        bd = [dictionnaire["name"] for dictionnaire in bd]
                        print(bd)
                    except CategoryInventory.DoesNotExist:
                        return Response({"error": "Machines not found"}, status=404)
                    
                    def func_get_time(name, year, month):
                        time_data = (
                            InventoryInto.objects.filter(
                                id_article__id_category__name=name,
                                date_modification__year=year,
                                entreprise__id=user__organisation__id,
                            )
                            .values("date_modification__year")
                            .distinct()
                        )
                        time_data = [
                            dictionnaire["date_modification__year"]
                            for dictionnaire in time_data
                        ]
                        print(time_data)
                        return time_data

                    def func_get_available(name, list_time):    
                        data: list = []
                        for time in list_time:
                            subquery = (
                                InventoryInto.objects.filter(
                                    id_article__id_category__name=name,
                                    date_modification__year=time,
                                    entreprise__id=user__organisation__id,
                                )
                                .values("available")
                                .distinct()
                            )
                            subquery = [
                                dictionnaire["available"] for dictionnaire in subquery
                            ]
                            for number in subquery:
                                data.append(number)
                            print(data)
                        return data

                    def func_get_quantity(name, list_time):
                        data: list = []
                        for time in list_time:
                            subquery = (
                                InventoryInto.objects.filter(
                                    id_article__id_category__name=name,
                                    date_modification__year=time,
                                    entreprise__id=user__organisation__id,
                                )
                                .values("quantity")
                                .distinct()
                            )
                            subquery = [
                                dictionnaire["quantity"] for dictionnaire in subquery
                            ]
                            for number in subquery:
                                data.append(number)
                            print(data)
                        return data

                    def func_get_capacity(name, list_time):
                        data: list = []
                        for time in list_time:
                            subquery = (
                                InventoryInto.objects.filter(
                                    id_article__id_category__name=name,
                                    date_modification__year=time,
                                    entreprise__id=user__organisation__id,
                                )
                                .values("capacity")
                                .distinct()
                            )
                            subquery = [
                                dictionnaire["capacity"] for dictionnaire in subquery
                            ]
                            for number in subquery:
                                data.append(number)
                            print(data)
                        return data

                    def func_get_weight(name, list_time):
                        data: list = []
                        for time in list_time:
                            subquery = (
                                InventoryInto.objects.filter(
                                    id_article__id_category__name=name,
                                    date_modification__year=time,
                                    entreprise__id=user__organisation__id,
                                )
                                .values("weight")
                                .distinct()
                            )
                            subquery = [
                                dictionnaire["weight"] for dictionnaire in subquery
                            ]
                            for number in subquery:
                                data.append(number)
                            print(data)
                        return data
                    
                    def func_get_numbres_of_pieces(name, list_time):
                        data: list = []
                        for time in list_time:
                            subquery = (
                                InventoryInto.objects.filter(
                                    id_article__id_category__name=name,
                                    date_modification__year=time,
                                    entreprise__id=user__organisation__id,
                                )
                                .values("numbres_of_pieces")
                                .distinct()
                            )
                            subquery = [
                                dictionnaire["numbres_of_pieces"]
                                for dictionnaire in subquery
                            ]
                            for number in subquery:
                                data.append(number)
                            print(data)
                        return data
                    
                    def func_get_price(name, list_time):
                        data: list = []
                        for time in list_time:
                            subquery = (
                                InventoryInto.objects.filter(
                                    id_article__id_category__name=name,
                                    date_modification__year=time,
                                    entreprise__id=user__organisation__id,
                                )
                                .values("price")
                                .distinct()
                            )
                            subquery = [
                                dictionnaire["price"] for dictionnaire in subquery
                            ]
                            for number in subquery:
                                data.append(number)
                            print(data)
                        return data
                    
                    for name in bd:
                            time = func_get_time(name=name, year=year, month=month)
                            available = func_get_available(name=name, list_time=time)
                            quantity = func_get_quantity(name=name, list_time=time)
                            capacity = func_get_capacity(name=name, list_time=time)
                            weight = func_get_weight(name=name, list_time=time)
                            numbres_of_pieces = func_get_numbres_of_pieces(
                                name=name, list_time=time
                            )
                            price = func_get_price(name=name, list_time=time)
                            tmp = {
                                "name": name,
                                "datetime": time,
                                "available": available,
                                "quantity": quantity,
                                "capacity": capacity,
                                "weight": weight,
                                "numbres_of_pieces": numbres_of_pieces,
                                "price": price,
                            }
                            data.append(tmp)
                    print(data)
            if stock == "out":
                if type == "article":
                    try:
                        db = list(
                            Inventory.objects.filter(entreprise__id=user__organisation__id)
                            .values("designation")
                            .distinct()
                        )
                        db = [dictionnaire["designation"] for dictionnaire in db]
                        print(db)
                    except Inventory.DoesNotExist:
                        return Response({"error": "Machines not found"}, status=404)
                    
                    
                    def func_get_time(name, year, month):
                            time_data = (
                                InventoryOut.objects.filter(
                                    id_inventory_into__id_article__designation=name,
                                    entreprise__id=user__organisation__id,
                                    date_modification__year=year,
                                )
                                .values("date_modification__month")
                                .distinct()
                            )
                            time_data = [
                                dictionnaire["date_modification__month"]
                                for dictionnaire in time_data
                            ]
                            print(time_data)
                            return time_data

                    def func_get_available(name, list_time):
                            data: list = []
                            for time in list_time:
                                subquery = (
                                    InventoryOut.objects.filter(
                                        id_inventory_into__id_article__designation=name,
                                        date_modification__month=time,
                                        entreprise__id=user__organisation__id,
                                    )
                                    .annotate(
                                    available=Coalesce(
                                        Count(
                                            "id",
                                            filter=Q(isAvailable=True),
                                            distinct=True,
                                        ),
                                        0,
                                    ),
                                   )
                                    .values("available")
                                    .distinct()
                                )
                                subquery = [
                                    dictionnaire["available"] for dictionnaire in subquery
                                ]
                                for number in subquery:
                                    data.append(number)
                                print(data)
                            return data

                    def func_get_quantity(name, list_time):
                            data: list = []
                            for time in list_time:
                                subquery = (
                                    InventoryOut.objects.filter(
                                        id_inventory_into__id_article__designation=name,
                                        date_modification__month=time,
                                        entreprise__id=user__organisation__id,
                                    )
                                    .values("quantity")
                                    .distinct()
                                )
                                subquery = [
                                    dictionnaire["quantity"] for dictionnaire in subquery
                                ]
                                for number in subquery:
                                    data.append(number)
                                print(data)
                            return data

                    def func_get_capacity(name, list_time): 
                            data: list = []
                            for time in list_time:
                                subquery = (
                                    InventoryOut.objects.filter(
                                        id_inventory_into__id_article__designation=name,
                                        date_modification__month=time,
                                        entreprise__id=user__organisation__id,
                                    )
                                    .values("capacity")
                                    .distinct()
                                )
                                subquery = [
                                    dictionnaire["capacity"] for dictionnaire in subquery
                                ]
                                for number in subquery:
                                    data.append(number)
                                print(data)
                            return data
                    
                    def func_get_weight(name, list_time):
                            data: list = []
                            for time in list_time:
                                subquery = (
                                    InventoryOut.objects.filter(
                                        id_inventory_into__id_article__designation=name,
                                        date_modification__month=time,
                                        entreprise__id=user__organisation__id,
                                    )
                                    .values('weight')
                                    .distinct()
                                )
                                subquery = [
                                    dictionnaire['weight'] for dictionnaire in subquery
                                ]
                                for number in subquery:
                                    data.append(number)
                                print(data)
                            return data

                    def func_get_numbres_of_pieces(name, list_time):
                            data: list = []
                            for time in list_time:
                                subquery = (
                                    InventoryOut.objects.filter(
                                       id_inventory_into__id_article__designation=name,
                                        date_modification__month=time,
                                        entreprise__id=user__organisation__id,
                                    )
                                    .values("numbres_of_pieces")
                                    .distinct()
                                )
                                subquery = [
                                    dictionnaire["numbres_of_pieces"]
                                    for dictionnaire in subquery
                                ]
                                for number in subquery:
                                    data.append(number)
                                print(data)
                            return data
                    
                    def func_get_price(name, list_time):
                            data: list = []
                            for time in list_time:
                                subquery = (
                                    InventoryOut.objects.filter(
                                        id_inventory_into__id_article__designation=name,
                                        date_modification__month=time,
                                        entreprise__id=user__organisation__id,
                                    )
                                    .values("price")
                                    .distinct()
                                )
                                subquery = [
                                    dictionnaire["price"] for dictionnaire in subquery
                                ]
                                for number in subquery:
                                    data.append(number)
                                print(data)
                            return data

                    for name in db:
                            time = func_get_time(name=name, year=year, month=month)
                            available = func_get_available(name=name, list_time=time)
                            quantity = func_get_quantity(name=name, list_time=time)
                            capacity = func_get_capacity(name=name, list_time=time)
                            weight = func_get_weight(name=name, list_time=time)
                            numbres_of_pieces = func_get_numbres_of_pieces(
                                name=name, list_time=time
                            )
                            price = func_get_price(name=name, list_time=time)
                            tmp = {
                                "name": name,
                                "datetime": time,
                                "available": available,
                                "quantity": quantity,
                                "capacity": capacity,
                                "weight": weight,
                                "numbres_of_pieces": numbres_of_pieces,
                                "price": price,
                            }
                            data.append(tmp)
                    print(data)
                if  type == "categorie":
                    
                    try:
                        bd = list(
                            CategoryInventory.objects.filter(
                                entreprise__id=user__organisation__id
                            )
                            .values("name")
                            .distinct()
                        )
                        bd = [dictionnaire["name"] for dictionnaire in bd]
                        print(bd)
                    except CategoryInventory.DoesNotExist:
                        return Response({"error": "Machines not found"}, status=404)
                    
                    def func_get_time(name, year, month):
                        time_data = (
                             InventoryOut.objects.filter(
                                id_inventory_into__id_article__id_category_name=name,
                                entreprise__id=user__organisation__id,
                                date_modification__year=year,
                            )
                            .values("date_modification__month")
                            .distinct()
                        )
                        time_data = [
                            dictionnaire["date_modification__month"]
                            for dictionnaire in time_data
                        ]
                        print(time_data)
                        return time_data

                    def func_get_available(name, list_time):    
                        data: list = []
                        for time in list_time:
                            subquery = (
                                 InventoryOut.objects.filter(
                                    id_inventory_into__id_article__id_category_name=name,
                                    entreprise__id=user__organisation__id,
                                    date_modification__month=time,
                                )
                                .values("available")
                                .distinct()
                            )
                            subquery = [
                                dictionnaire["available"] for dictionnaire in subquery
                            ]
                            for number in subquery:
                                data.append(number)
                            print(data)
                        return data

                    def func_get_quantity(name, list_time):
                        data: list = []
                        for time in list_time:
                            subquery = (
                                 InventoryOut.objects.filter(
                                    id_inventory_into__id_article__id_category_name=name,
                                    entreprise__id=user__organisation__id,
                                    date_modification__month=time,
                                )
                                .values("quantity")
                                .distinct()
                            )
                            subquery = [
                                dictionnaire["quantity"] for dictionnaire in subquery
                            ]
                            for number in subquery:
                                data.append(number)
                            print(data)
                        return data

                    def func_get_capacity(name, list_time):
                        data: list = []
                        for time in list_time:
                            subquery = (
                                 InventoryOut.objects.filter(
                                    id_inventory_into__id_article__id_category_name=name,
                                    entreprise__id=user__organisation__id,
                                    date_modification__month=time,
                                )
                                .values("capacity")
                                .distinct()
                            )
                            subquery = [
                                dictionnaire["capacity"] for dictionnaire in subquery
                            ]
                            for number in subquery:
                                data.append(number)
                            print(data)
                        return data

                    def func_get_weight(name, list_time):
                        data: list = []
                        for time in list_time:
                            subquery = (
                                 InventoryOut.objects.filter(
                                    id_inventory_into__id_article__id_category_name=name,
                                    entreprise__id=user__organisation__id,
                                    date_modification__month=time,
                                )
                                .values("weight")
                                .distinct()
                            )
                            subquery = [
                                dictionnaire["weight"] for dictionnaire in subquery
                            ]
                            for number in subquery:
                                data.append(number)
                            print(data)
                        return data
                    
                    def func_get_numbres_of_pieces(name, list_time):
                        data: list = []
                        for time in list_time:
                            subquery = (
                                 InventoryOut.objects.filter(
                                    id_inventory_into__id_article__id_category_name=name,
                                    entreprise__id=user__organisation__id,
                                    date_modification__month=time,
                                )
                                .values("numbres_of_pieces")
                                .distinct()
                            )
                            subquery = [
                                dictionnaire["numbres_of_pieces"]
                                for dictionnaire in subquery
                            ]
                            for number in subquery:
                                data.append(number)
                            print(data)
                        return data
                    
                    def func_get_price(name, list_time):
                        data: list = []
                        for time in list_time:
                            subquery = (
                                InventoryOut.objects.filter(
                                    id_inventory_into__id_article__id_category_name=name,
                                    entreprise__id=user__organisation__id,
                                    date_modification__month=time,
                                )
                                .values("price")
                                .distinct()
                            )
                            subquery = [
                                dictionnaire["price"] for dictionnaire in subquery
                            ]
                            for number in subquery:
                                data.append(number)
                            print(data)
                        return data
                    
                    for name in bd:
                            time = func_get_time(name=name, year=year, month=month)
                            available = func_get_available(name=name, list_time=time)
                            quantity = func_get_quantity(name=name, list_time=time)
                            capacity = func_get_capacity(name=name, list_time=time)
                            weight = func_get_weight(name=name, list_time=time)
                            numbres_of_pieces = func_get_numbres_of_pieces(
                                name=name, list_time=time
                            )
                            price = func_get_price(name=name, list_time=time)
                            tmp = {
                                "name": name,
                                "datetime": time,
                                "available": available,
                                "quantity": quantity,
                                "capacity": capacity,
                                "weight": weight,
                                "numbres_of_pieces": numbres_of_pieces,
                                "price": price,
                            }
                            data.append(tmp)
                    print(data)
        elif period == "years":
            if stock == "in":
                if type == "article":
                    try:
                        db = list(
                            Inventory.objects.filter(entreprise__id=user__organisation__id)
                            .values("designation")
                            .distinct()
                        )
                        db = [dictionnaire["designation"] for dictionnaire in db]
                        print(db)
                    except Inventory.DoesNotExist:
                        return Response({"error": "Machines not found"}, status=404)
                    
                    def func_get_time(name, year, month):
                            time_data = (
                                InventoryInto.objects.filter(
                                    id_article__designation=name,
                                    entreprise__id=user__organisation__id,
                                )
                                .values("date_modification__year")
                                .distinct()
                            )
                            time_data = [
                                dictionnaire["date_modification__year"]
                                for dictionnaire in time_data
                            ]
                            print(time_data)
                            return time_data

                    def func_get_available(name, list_time):
                            data: list = []
                            for time in list_time:
                                subquery = (
                                    InventoryInto.objects.filter(
                                        id_article__designation=name,
                                        entreprise__id=user__organisation__id,
                                    ).annotate(
                                    available=Coalesce(
                                        Count(
                                            "id",
                                            filter=Q(inventoryout__isAvailable=True),
                                            distinct=True,
                                        ),
                                        0,
                                    ),
                                )
                                    .values("available")
                                    .distinct()
                                )
                                subquery = [
                                    dictionnaire["available"] for dictionnaire in subquery
                                ]
                                for number in subquery:
                                    data.append(number)
                                print(data)
                            return data

                    def func_get_quantity(name, list_time):
                            data: list = []
                            for time in list_time:
                                subquery = (
                                    InventoryInto.objects.filter(
                                        id_article__designation=name,
                                        entreprise__id=user__organisation__id,
                                    )
                                    .values("quantity")
                                    .distinct()
                                )
                                subquery = [
                                    dictionnaire["quantity"] for dictionnaire in subquery
                                ]
                                for number in subquery:
                                    data.append(number)
                                print(data)
                            return data

                    def func_get_capacity(name, list_time): 
                            data: list = []
                            for time in list_time:
                                subquery = (
                                    InventoryInto.objects.filter(
                                        id_article__designation=name,
                                        entreprise__id=user__organisation__id,
                                    )
                                    .values("capacity")
                                    .distinct()
                                )
                                subquery = [
                                    dictionnaire["capacity"] for dictionnaire in subquery
                                ]
                                for number in subquery:
                                    data.append(number)
                                print(data)
                            return data
                    
                    def func_get_weight(name, list_time):
                            data: list = []
                            for time in list_time:
                                subquery = (
                                    InventoryInto.objects.filter(
                                        id_article__designation=name,
                                        entreprise__id=user__organisation__id,
                                    )
                                    .values('weight')
                                    .distinct()
                                )
                                subquery = [
                                    dictionnaire['weight'] for dictionnaire in subquery
                                ]
                                for number in subquery:
                                    data.append(number)
                                print(data)
                            return data

                    def func_get_numbres_of_pieces(name, list_time):
                            data: list = []
                            for time in list_time:
                                subquery = (
                                    InventoryInto.objects.filter(
                                        id_article__designation=name,
                                        entreprise__id=user__organisation__id,
                                    )
                                    .values("numbres_of_pieces")
                                    .distinct()
                                )
                                subquery = [
                                    dictionnaire["numbres_of_pieces"]
                                    for dictionnaire in subquery
                                ]
                                for number in subquery:
                                    data.append(number)
                                print(data)
                            return data
                    
                    def func_get_price(name, list_time):
                            data: list = []
                            for time in list_time:
                                subquery = (
                                    InventoryInto.objects.filter(
                                        id_article__designation=name,
                                        entreprise__id=user__organisation__id,
                                    )
                                    .values("price")
                                    .distinct()
                                )
                                subquery = [
                                    dictionnaire["price"] for dictionnaire in subquery
                                ]
                                for number in subquery:
                                    data.append(number)
                                print(data)
                            return data

                    for name in db:
                            time = func_get_time(name=name, year=year, month=month)
                            available = func_get_available(name=name, list_time=time)
                            quantity = func_get_quantity(name=name, list_time=time)
                            capacity = func_get_capacity(name=name, list_time=time)
                            weight = func_get_weight(name=name, list_time=time)
                            numbres_of_pieces = func_get_numbres_of_pieces(
                                name=name, list_time=time
                            )
                            price = func_get_price(name=name, list_time=time)
                            tmp = {
                                "name": name,
                                "datetime": time,
                                "available": available,
                                "quantity": quantity,
                                "capacity": capacity,
                                "weight": weight,
                                "numbres_of_pieces": numbres_of_pieces,
                                "price": price,
                            }
                            data.append(tmp)
                    print(data)   
                if  type == "categorie":
                    
                    try:
                        bd = list(
                            CategoryInventory.objects.filter(
                                entreprise__id=user__organisation__id
                            )
                            .values("name")
                            .distinct()
                        )
                        bd = [dictionnaire["name"] for dictionnaire in bd]
                        print(bd)
                    except CategoryInventory.DoesNotExist:
                        return Response({"error": "Machines not found"}, status=404)
                    
                    def func_get_time(name, year, month):
                        time_data = (
                            InventoryInto.objects.filter(
                                id_article__id_category__name=name,
                                entreprise__id=user__organisation__id,
                            )
                            .values("date_modification__year")
                            .distinct()
                        )
                        time_data = [
                            dictionnaire["date_modification__year"]
                            for dictionnaire in time_data
                        ]
                        print(time_data)
                        return time_data

                    def func_get_available(name, list_time):    
                        data: list = []
                        for time in list_time:
                            subquery = (
                                InventoryInto.objects.filter(
                                    id_article__id_category__name=name,
                                    entreprise__id=user__organisation__id,
                                )
                                .values("available")
                                .distinct()
                            )
                            subquery = [
                                dictionnaire["available"] for dictionnaire in subquery
                            ]
                            for number in subquery:
                                data.append(number)
                            print(data)
                        return data

                    def func_get_quantity(name, list_time):
                        data: list = []
                        for time in list_time:
                            subquery = (
                                InventoryInto.objects.filter(
                                    id_article__id_category__name=name,
                                    entreprise__id=user__organisation__id,
                                )
                                .values("quantity")
                                .distinct()
                            )
                            subquery = [
                                dictionnaire["quantity"] for dictionnaire in subquery
                            ]
                            for number in subquery:
                                data.append(number)
                            print(data)
                        return data

                    def func_get_capacity(name, list_time):
                        data: list = []
                        for time in list_time:
                            subquery = (
                                InventoryInto.objects.filter(
                                    id_article__id_category__name=name,
                                    entreprise__id=user__organisation__id,
                                )
                                .values("capacity")
                                .distinct()
                            )
                            subquery = [
                                dictionnaire["capacity"] for dictionnaire in subquery
                            ]
                            for number in subquery:
                                data.append(number)
                            print(data)
                        return data

                    def func_get_weight(name, list_time):
                        data: list = []
                        for time in list_time:
                            subquery = (
                                InventoryInto.objects.filter(
                                    id_article__id_category__name=name,
                                    entreprise__id=user__organisation__id,
                                )
                                .values("weight")
                                .distinct()
                            )
                            subquery = [
                                dictionnaire["weight"] for dictionnaire in subquery
                            ]
                            for number in subquery:
                                data.append(number)
                            print(data)
                        return data
                    
                    def func_get_numbres_of_pieces(name, list_time):
                        data: list = []
                        for time in list_time:
                            subquery = (
                                InventoryInto.objects.filter(
                                    id_article__id_category__name=name,
                                    entreprise__id=user__organisation__id,
                                )
                                .values("numbres_of_pieces")
                                .distinct()
                            )
                            subquery = [
                                dictionnaire["numbres_of_pieces"]
                                for dictionnaire in subquery
                            ]
                            for number in subquery:
                                data.append(number)
                            print(data)
                        return data
                    
                    def funct_get_price(name, list_time):
                        data: list = []
                        for time in list_time:
                            subquery = (
                                InventoryInto.objects.filter(
                                    id_article__id_category__name=name,
                                    entreprise__id=user__organisation__id,
                                )
                                .values("price")
                                .distinct()
                            )
                            subquery = [
                                dictionnaire["price"] for dictionnaire in subquery
                            ]
                            for number in subquery:
                                data.append(number)
                            print(data)
                        return data
                    
                    for name in bd:
                            time = func_get_time(name=name, year=year, month=month)
                            available = func_get_available(name=name, list_time=time)
                            quantity = func_get_quantity(name=name, list_time=time)
                            capacity = func_get_capacity(name=name, list_time=time)
                            weight = func_get_weight(name=name, list_time=time)
                            numbres_of_pieces = func_get_numbres_of_pieces(
                                name=name, list_time=time
                            )
                            price = func_get_price(name=name, list_time=time)
                            tmp = {
                                "name": name,
                                "datetime": time,
                                "available": available,
                                "quantity": quantity,
                                "capacity": capacity,
                                "weight": weight,
                                "numbres_of_pieces": numbres_of_pieces,
                                "price": price,
                            }
                            data.append(tmp)
                    print(data)
            if stock == "out": 
                if type == "article": 
                    try:
                        db = list(
                            Inventory.objects.filter(entreprise__id=user__organisation__id)
                            .values("designation")
                            .distinct()
                        )
                        db = [dictionnaire["designation"] for dictionnaire in db]
                        print(db)
                    except Inventory.DoesNotExist:
                        return Response({"error": "Machines not found"}, status=404)
                    
                    def func_get_time(name, year, month):
                            time_data = (
                                InventoryOut.objects.filter(
                                    id_inventory_into__id_article__designation=name,
                                    entreprise__id=user__organisation__id,
                                )
                                .values("date_modification__year")
                                .distinct()
                            )
                            time_data = [
                                dictionnaire["date_modification__year"]
                                for dictionnaire in time_data
                            ]
                            print(time_data)
                            return time_data

                    def func_get_available(name, list_time):
                            data: list = []
                            for time in list_time:
                                subquery = (
                                    InventoryOut.objects.filter(
                                        id_inventory_into__id_article__designation=name,
                                        entreprise__id=user__organisation__id,
                                    ).annotate(
                                    available=Coalesce(
                                        Count(
                                            "id",
                                            filter=Q(isAvailable=True),
                                            distinct=True,
                                        ),
                                        0,
                                    ),
                                   )
                                    .values("available")
                                    .distinct()
                                )
                                subquery = [
                                    dictionnaire["available"] for dictionnaire in subquery
                                ]
                                for number in subquery:
                                    data.append(number)
                                print(data)
                            return data

                    def func_get_quantity(name, list_time):
                            data: list = []
                            for time in list_time:
                                subquery = (
                                    InventoryOut.objects.filter(
                                        id_inventory_into__id_article__designation=name,
                                        entreprise__id=user__organisation__id,
                                    )
                                    .values("quantity")
                                    .distinct()
                                )
                                subquery = [
                                    dictionnaire["quantity"] for dictionnaire in subquery
                                ]
                                for number in subquery:
                                    data.append(number)
                                print(data)
                            return data

                    def func_get_capacity(name, list_time): 
                            data: list = []
                            for time in list_time:
                                subquery = (
                                    InventoryOut.objects.filter(
                                        id_inventory_into__id_article__designation=name,
                                        entreprise__id=user__organisation__id,
                                    )
                                    .values("capacity")
                                    .distinct()
                                )
                                subquery = [
                                    dictionnaire["capacity"] for dictionnaire in subquery
                                ]
                                for number in subquery:
                                    data.append(number)
                                print(data)
                            return data
                    
                    def func_get_weight(name, list_time):
                            data: list = []
                            for time in list_time:
                                subquery = (
                                    InventoryOut.objects.filter(
                                        id_inventory_into__id_article__designation=name,
                                        entreprise__id=user__organisation__id,
                                    )
                                    .values('weight')
                                    .distinct()
                                )
                                subquery = [
                                    dictionnaire['weight'] for dictionnaire in subquery
                                ]
                                for number in subquery:
                                    data.append(number)
                                print(data)
                            return data

                    def func_get_numbres_of_pieces(name, list_time):
                            data: list = []
                            for time in list_time:
                                subquery = (
                                    InventoryOut.objects.filter(
                                        id_inventory_into__id_article__designation=name,
                                        entreprise__id=user__organisation__id,
                                    )
                                    .values("numbres_of_pieces")
                                    .distinct()
                                )
                                subquery = [
                                    dictionnaire["numbres_of_pieces"]
                                    for dictionnaire in subquery
                                ]
                                for number in subquery:
                                    data.append(number)
                                print(data)
                            return data
                    
                    def func_get_price(name, list_time):
                            data: list = []
                            for time in list_time:
                                subquery = (
                                    InventoryOut.objects.filter(
                                        id_inventory_into__id_article__designation=name,
                                        entreprise__id=user__organisation__id,
                                    )
                                    .values("price")
                                    .distinct()
                                )
                                subquery = [
                                    dictionnaire["price"] for dictionnaire in subquery
                                ]
                                for number in subquery:
                                    data.append(number)
                                print(data)
                            return data

                    for name in db:
                            time = func_get_time(name=name, year=year, month=month)
                            available = func_get_available(name=name, list_time=time)
                            quantity = func_get_quantity(name=name, list_time=time)
                            capacity = func_get_capacity(name=name, list_time=time)
                            weight = func_get_weight(name=name, list_time=time)
                            numbres_of_pieces = func_get_numbres_of_pieces(
                                name=name, list_time=time
                            )
                            price = func_get_price(name=name, list_time=time)
                            tmp = {
                                "name": name,
                                "datetime": time,
                                "available": available,
                                "quantity": quantity,
                                "capacity": capacity,
                                "weight": weight,
                                "numbres_of_pieces": numbres_of_pieces,
                                "price": price,
                            }
                            data.append(tmp)
                    print(data)       
                elif type == "category":
                    try:
                        bd = list(
                            CategoryInventory.objects.filter(
                                entreprise__id=user__organisation__id
                            )
                            .values("name")
                            .distinct()
                        )
                        bd = [dictionnaire["name"] for dictionnaire in bd]
                        print(bd)
                    except CategoryInventory.DoesNotExist:
                        return Response({"error": "Machines not found"}, status=404)

                    def func_get_time(name, year, month):
                            time_data = (
                                InventoryOut.objects.filter(
                                    id_inventory_into__id_article__id_category__name=name,
                                    entreprise__id=user__organisation__id,
                                )
                                .values("date_modification__day")
                                .distinct()
                            )
                            time_data = [
                                dictionnaire["date_modification__day"]
                                for dictionnaire in time_data
                            ]
                            print(time_data)
                            return time_data

                    def func_get_available(name, list_time):
                            data: list = []
                            for time in list_time:
                                subquery = (
                                    InventoryOut.objects.filter(
                                        id_inventory_into__id_article__id_category__name=name,
                                        entreprise__id=user__organisation__id,
                                    )
                                    .annotate(
                                        available_count=Coalesce(
                                            Count(
                                                "id",
                                                filter=Q(inventoryout__isAvailable=True),
                                                distinct=True,
                                            ),
                                            0,
                                        ),
                                    )
                                    .values("available_count")
                                    .distinct()
                                )
                                subquery = [
                                    dictionnaire["available_count"]
                                    for dictionnaire in subquery
                                ]
                                for number in subquery:
                                    data.append(number)
                                print(data)

                            return data

                    def func_get_quantity(name, list_time):
                            data: list = []
                            for time in list_time:
                                subquery = (
                                    InventoryOut.objects.filter(
                                        id_inventory_into__id_article__id_category__name=name,
                                        entreprise__id=user__organisation__id,
                                    )
                                    .annotate(
                                        quantity=Coalesce(Sum("quantity"), 0),
                                    )
                                    .values("quantity")
                                    .distinct()
                                )
                                subquery = [
                                    dictionnaire["quantity"] for dictionnaire in subquery
                                ]
                                for number in subquery:
                                    data.append(number)
                                print(data)

                            return data

                    def func_get_capacity(name, list_time):
                            data: list = []
                            for time in list_time:
                                subquery = (
                                    InventoryOut.objects.filter(
                                        id_inventory_into__id_article__id_category__name=name,
                                        entreprise__id=user__organisation__id,
                                    )
                                    .values("capacity")
                                    .distinct()
                                )
                                subquery = [
                                    dictionnaire["capacity"] for dictionnaire in subquery
                                ]
                                for number in subquery:
                                    data.append(number)
                                print(data)
                            return data

                    def func_get_price(name, list_time):
                            data: list = []
                            for time in list_time:
                                subquery = (
                                    InventoryOut.objects.filter(
                                        id_inventory_into__id_article__id_category__name=name,
                                        entreprise__id=user__organisation__id,
                                    )
                                    .annotate(
                                        price=Coalesce(
                                            Sum(
                                                F("quantity")
                                                * F("price_used_by_entreprise")
                                            ),
                                            0,
                                            output_field=DecimalField(),
                                        ),
                                    )
                                    .values("price")
                                    .distinct()
                                )
                                subquery = [
                                    dictionnaire["price"] for dictionnaire in subquery
                                ]
                                for number in subquery:
                                    data.append(number)
                                print(data)
                            return data

                    def func_get_numbres_of_pieces(name, list_time):
                            data: list = []
                            for time in list_time:
                                subquery = (
                                    InventoryOut.objects.filter(
                                        id_inventory_into__id_article__id_category__name=name,
                                        entreprise__id=user__organisation__id,
                                    )
                                    .values("numbres_of_pieces")
                                    .distinct()
                                )
                                subquery = [
                                    dictionnaire["numbres_of_pieces"]
                                    for dictionnaire in subquery
                                ]
                                for number in subquery:
                                    data.append(number)
                                print(data)
                            return data

                    def func_get_weight(name, list_time):
                            data: list = []
                            for time in list_time:
                                subquery = (
                                    InventoryOut.objects.filter(
                                        id_inventory_into__id_article__id_category__name=name,
                                        entreprise__id=user__organisation__id,
                                    )
                                    .values('weight')
                                    .distinct()
                                )
                                subquery = [
                                    dictionnaire['weight'] for dictionnaire in subquery
                                ]
                                for number in subquery:
                                    data.append(number)
                                print(data)
                            return data

                    for name in bd:
                            time = func_get_time(name=name, year=year, month=month)
                            available = func_get_available(name=name, list_time=time)
                            quantity = func_get_quantity(name=name, list_time=time)
                            capacity = func_get_capacity(name=name, list_time=time)
                            weight = func_get_weight(name=name, list_time=time)
                            numbres_of_pieces = func_get_numbres_of_pieces(
                                name=name, list_time=time
                            )
                            price = func_get_price(name=name, list_time=time)
                            tmp = {
                                "name": name,
                                "datetime": time,
                                "available": available,
                                "quantity": quantity,
                                "capacity": capacity,
                                "weight": weight,
                                "numbres_of_pieces": numbres_of_pieces,
                                "price": price,
                            }
                            data.append(tmp)
                    print(data)
            
        else:
            return Response({"error": "Invalid period parameter."}, status=400)

        """ if type == "article":
            serializer = MachineStatisticsSerializerForArticle(queryset, many=True)
        elif type == "category":
            serializer = MachineStatisticsSerializerForCategory(queryset, many=True)"""

        response_data = {
            "status": "success",
            "data": data,
            "message": "Data retrieved successfully",
        }
        return Response(response_data)


class DiagnosticsStatisticsView(APIView):
    def get(self, request):
        serializer = ""
        queryset = ""
        period = request.query_params.get("period", "years")
        year = request.query_params.get("year")
        user__organisation__id = funct__id__entreprise(request=request)
        print(period)
        period = str(period)
        if period == "days":
            month = request.query_params.get("month")
            queryset = (
                Diagnostics.objects.filter(
                    date_modification__year=year,
                    date_creation__month=month,
                    isDiagnostic=True,
                    entreprise__id=user__organisation__id,
                )
                .annotate(day=ExtractDay("date_modification"))
                .values("day")
                .annotate(count=Count("id"))
                .order_by("-day")
            )
            serializer = ValuesbyDaysPeriodSerializer(queryset, many=True)
        elif period == "month":
            queryset = (
                Diagnostics.objects.filter(
                    date_modification__year=year,
                    isDiagnostic=True,
                    entreprise__id=user__organisation__id,
                )
                .annotate(month=ExtractMonth("date_modification"))
                .values("month")
                .annotate(count=Count("id"))
                .order_by("-month")
            )
            serializer = ValuesbyMonthPeriodSerializer(queryset, many=True)
        elif period == "years":
            queryset = (
                Diagnostics.objects.filter(
                    isDiagnostic=True, entreprise__id=user__organisation__id
                )
                .annotate(year=ExtractYear("date_modification"))
                .values("year")
                .annotate(count=Count("id"))
                .order_by("-year")
            )
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
        period = request.query_params.get("period", "day")
        user__organisation__id = funct__id__entreprise(request=request)
        if period == "days":
            year = request.query_params.get("year")
            month = request.query_params.get("month")
            queryset = (
                PlanifierMaintenance.objects.filter(
                    date_modification__year=year,
                    date_creation__month=month,
                    entreprise__id=user__organisation__id,
                )
                .annotate(day=ExtractDay("date_modification"))
                .values("day")
                .annotate(count=Count("id"))
                .order_by("-day")
            )
            serializer = ValuesbyDaysPeriodSerializer(queryset, many=True)
        elif period == "month":
            year = request.query_params.get("year")
            queryset = (
                PlanifierMaintenance.objects.filter(
                    date_modification__year=year, entreprise__id=user__organisation__id
                )
                .annotate(month=ExtractMonth("date_modification"))
                .values("month")
                .annotate(count=Count("id"))
                .order_by("-month")
            )
            serializer = ValuesbyMonthPeriodSerializer(queryset, many=True)
        elif period == "years":
            queryset = (
                PlanifierMaintenance.objects.filter(
                    entreprise__id=user__organisation__id
                )
                .annotate(year=ExtractYear("date_modification"))
                .values("year")
                .annotate(count=Count("id"))
                .order_by("-year")
            )
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
        period = request.query_params.get("period", "days")
        user__organisation__id = funct__id__entreprise(request=request)
        if period == "days":
            year = request.query_params.get("year")
            month = request.query_params.get("month")
            queryset = (
                Diagnostics.objects.filter(
                    date_modification__year=year,
                    date_creation__month=month,
                    isRepair=True,
                    entreprise__id=user__organisation__id,
                )
                .annotate(day=ExtractDay("date_modification"))
                .values("day")
                .annotate(count=Count("id"))
                .order_by("-day")
            )
            serializer = ValuesbyDaysPeriodSerializer(queryset, many=True)
        elif period == "month":
            year = request.query_params.get("year")
            queryset = (
                Diagnostics.objects.filter(
                    date_modification__year=year,
                    isRepair=True,
                    entreprise__id=user__organisation__id,
                )
                .annotate(month=ExtractMonth("date_modification"))
                .values("month")
                .annotate(count=Count("id"))
                .order_by("-month")
            )
            serializer = ValuesbyMonthPeriodSerializer(queryset, many=True)
        elif period == "years":
            queryset = (
                Diagnostics.objects.filter(
                    isRepair=True, entreprise__id=user__organisation__id
                )
                .annotate(year=ExtractYear("date_modification"))
                .values("year")
                .annotate(count=Count("id"))
                .order_by("-year")
            )
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


class TrackingPiecesViewSetTest(viewsets.ModelViewSet):
    serializer_class = TrackingPiecesSerializer

    def get_queryset(self):
        period = self.request.query_params.get("period", "y")
        years = self.request.query_params.get("m", 4)
        user = self.request.user
        user__organisation__id = funct__id__entreprise(request=self.request)
        print(user.email)
        # Assuming you want to filter based on a date field in your model
        # For example, if you have a 'date_created' field and you want to filter by the last 7 days
        if period == "y":
            return TrackingPieces.objects.filter(
                date_modification__month=years, entreprise__id=user__organisation__id
            )
        # Add more conditions here if you have different periods
        else:
            return TrackingPieces.objects.filter(entreprise__id=user__organisation__id)


# views.py
from django.db.models import Subquery, OuterRef, Count, CharField, Prefetch
from django.db.models.functions import Cast
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Machine, Diagnostics, PlanifierMaintenance


@api_view(["GET"])
def MachineData(request):
    try:
        machines = list(Machine.objects.values("nom").distinct())
        machines = [dictionnaire["nom"] for dictionnaire in machines]
        print(machines)
    except Machine.DoesNotExist:
        return Response({"error": "Machines not found"}, status=404)

    def func_get_times(machine_name):
        time_data = (
            Diagnostics.objects.filter(id_machine__nom=machine_name)
            .values("date_modification__year")
            .distinct()
        )
        time_data = [
            dictionnaire["date_modification__year"] for dictionnaire in time_data
        ]
        print(time_data)
        return time_data

    def func_get_planned(machine_name, list_time):
        data: list = []
        for time in list_time:
            planned_subquery = (
                PlanifierMaintenance.objects.filter(
                    id_machine__nom=machine_name, date_modification__year=time
                )
                .annotate(presence_count=Count("id"))
                .values("presence_count")
                .distinct()
            )
            planned_subquery = [
                dictionnaire["presence_count"] for dictionnaire in planned_subquery
            ]
            for number in planned_subquery:
                data.append(number)
        print(data)

        return data

    def func_get_actual(machine_name, list_time):
        data: list = []
        for time in list_time:
            actual_subquery = (
                Diagnostics.objects.filter(
                    id_machine__nom=machine_name,
                    date_modification__year=time,
                    isDiagnostic=True,
                    isRepair=False,
                )
                .annotate(presence_count=Count("id"))
                .values("presence_count")
                .distinct()
            )
            actual_subquery = [
                dictionnaire["presence_count"] for dictionnaire in actual_subquery
            ]
            for number in actual_subquery:
                data.append(number)
        return data

    data = []
    for name in machines:
        planned = func_get_planned(
            machine_name=name, list_time=func_get_times(machine_name=name)
        )
        actual = func_get_actual(
            machine_name=name, list_time=func_get_times(machine_name=name)
        )
        tmp = {
            "name": name,
            "year": func_get_times(machine_name=name),
            "planned": planned,
            "actual": actual,
            "total": len(planned) + len(actual),
        }
        data.append(tmp)
    print(data)
    # Annotation des données avec les sous-requêtes

    # Sérialisation des données
    # serializer = MachineDataSerializer(machines_data, many=True)

    return Response(data)
