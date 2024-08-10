from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .filter import *
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
from rest_framework.pagination import BasePagination
from django.core.mail import send_mail
from django.template.loader import render_to_string

User = get_user_model()

# Create your views here.

#class CategorieMachineViewSet(viewsets.ModelViewSet):
    #queryset = CategorieMachine.objects.all()
    #serializer_class = CategorieMachineSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
class CustomPagination(BasePagination):
    page_size = 10
    page_size_query_param = 'page_size'
    limit_query_param = 'limit'
    offset_query_param = 'offset'

    def paginate_queryset(self, queryset, request, view=None):
        offset = self.get_offset(request)
        limit = self.get_limit(request)
        return queryset[offset:offset + limit]

    def get_offset(self, request):
        return int(request.query_params.get(self.offset_query_param, 0))

    def get_limit(self, request):
        return int(request.query_params.get(self.limit_query_param, self.page_size))

    def get_paginated_response(self, data):
        response_data = {
            "status": "success",
            "data": data,
            "message": "Data retrieved successfully"
        }
        return Response(response_data, status=status.HTTP_200_OK)

class CategorieMachineViewSet(viewsets.ModelViewSet):
    queryset = CategorieMachine.objects.all()
    serializer_class = CategorieMachineSerializer
    # a ajouter manuelement partout 
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = CategorieMachineFilter # Remplacez 'nom' par le nom de votre champ
    #pagination_class = CustomPagination
    authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        # Récupérer l'utilisateur actuellement connecté
        user = self.request.user
        userModel = User.objects.get(id=user.id)
        user__organisation__id = ''
        if userModel.entreprise:
            if userModel.entreprise.id:
                user__organisation__id = userModel.entreprise.id
                print("categorie machine")
                print(user__organisation__id)
                
                # Filtrer les posts de blog appartenant à l'utilisateur et à son organisation
                return queryset.filter(entreprise__id=user__organisation__id)
        else : 
             return queryset.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        total_data = queryset.count()

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
                serializer.save(createdBy=request.user,entreprise=request.user.entreprise)
                return Response({"status": "success", "data": serializer.data, "message": "Data added successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": "error", "data": serializer.errors, "message": "Data error!"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(createdBy=request.user,entreprise=request.user.entreprise)
                return Response({"status": "success", "data": serializer.data, "message": "Data updated successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": serializer.errors, "message": "Update error!"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
            instance = self.get_object()
            #instance.id_UserAgent= request.user
            instance.save()
            instance.delete()
            return Response({"status": "success", "message": "Data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class CategorieMachineCountView(APIView):
    def get(self, request):
        user = request.user
        userModel = User.objects.get(id=user.id)
        user__organisation__id = ''
        if userModel.entreprise:
            if userModel.entreprise.id:
                user__organisation__id = userModel.entreprise.id
                print("categorie machine")
                print(user__organisation__id)
                # Filtrer les posts de blog appartenant à l'utilisateur et à son organisation
                total_categorieMachine = CategorieMachine.filter(entreprise__id=user__organisation__id)
        else : 
           total_categorieMachine = CategorieMachine.all().count()
        return Response({"total": total_categorieMachine })
class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer

    serializer_class_post = MachineSerializerTwo
    serializer_class_put = MachineSerializerTwo

    #filter_backends = [DjangoFilterBackend, SearchFilter]
    #filterset_class = MachineFilter # Remplacez 'nom' par le nom de votre champ
    # a ajouter manuelement partout
    authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return self.serializer_class_post
        elif self.request.method in ['PUT', 'PATCH']:
            return self.serializer_class_put
        return self.serializer_class
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Récupérer l'utilisateur actuellement connecté
        user = self.request.user
        userModel = User.objects.get(id=user.id)
        user__organisation__id = ''
        if userModel.entreprise:
            if userModel.entreprise.id:
                user__organisation__id = userModel.entreprise.id
                print("categorie machine")
                print(user__organisation__id)
                
                # Filtrer les posts de blog appartenant à l'utilisateur et à son organisation
                return queryset.filter(entreprise__id=user__organisation__id)
        else : 
             return queryset.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        total_data = queryset.count()

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
                serializer.save(createdBy=request.user,entreprise=request.user.entreprise)
                return Response({"status": "success", "data": serializer.data, "message": "Data added successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": "error", "data": serializer.errors, "message": "Data error!"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(createdBy=request.user,entreprise=request.user.entreprise)
                return Response({"status": "success", "data": serializer.data, "message": "Data updated successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": serializer.errors, "message": "Update error!"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
            instance = self.get_object()
            #instance.id_UserAgent= request.user
            instance.save()
            instance.delete()
            return Response({"status": "success", "message": "Data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class MachineCountView(APIView):
    def get(self, request):
        total_machine = Machine.objects.all().count()
        return Response({ "total": total_machine})


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    '''filterset_class = ClientFilter
    filter_backends = [DjangoFilterBackend, SearchFilter]'''
    '''pagination_class = CustomPagination'''
    authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        # Récupérer l'utilisateur actuellement connecté
        user = self.request.user
        userModel = User.objects.get(id=user.id)
        user__organisation__id = ''
        if userModel.entreprise:
            if userModel.entreprise.id:
                user__organisation__id = userModel.entreprise.id
                print("categorie machine")
                print(user__organisation__id)
                
                # Filtrer les posts de blog appartenant à l'utilisateur et à son organisation
                return queryset.filter(entreprise__id=user__organisation__id)
        else : 
             return queryset.all()
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        total_data = self.queryset.count()  # Get the total number of data

        response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "message": "Data retrieved successfully"
        }
        return Response(response_data, status=status.HTTP_200_OK)
        
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        total_data = queryset.count()

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
                serializer.save(createdBy=request.user,entreprise=request.user.entreprise)
                return Response({"status": "success", "data": serializer.data, "message": "Data added successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": "error", "data": serializer.errors, "message": "Data error!"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(createdBy=request.user,entreprise=request.user.entreprise)
                return Response({"status": "success", "data": serializer.data, "message": "Data updated successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": serializer.errors, "message": "Update error!"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
            instance = self.get_object()
            #instance.id_UserAgent= request.user
            instance.save()
            instance.delete()
            return Response({"status": "success", "message": "Data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProviderFilter
    #pagination_class = CustomPagination
    authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        # Récupérer l'utilisateur actuellement connecté
        user = self.request.user
        userModel = User.objects.get(id=user.id)
        user__organisation__id = ''
        if userModel.entreprise:
            if userModel.entreprise.id:
                user__organisation__id = userModel.entreprise.id
                print("categorie machine")
                print(user__organisation__id)
                
                # Filtrer les posts de blog appartenant à l'utilisateur et à son organisation
                return queryset.filter(entreprise__id=user__organisation__id)
        else : 
             return queryset.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        data = serializer.data
        total_data =  self.queryset.count()  # Get the total number of data

        response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "message": "Data retrieved successfully"
        }
        return Response(response_data, status=status.HTTP_200_OK)
        
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        total_data = queryset.count()

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
                serializer.save(createdBy=request.user,entreprise=request.user.entreprise)
                return Response({"status": "success", "data": serializer.data, "message": "Data added successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": "error", "data": serializer.errors, "message": "Data error!"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(createdBy=request.user,entreprise=request.user.entreprise)
                return Response({"status": "success", "data": serializer.data, "message": "Data updated successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": serializer.errors, "message": "Update error!"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
            instance = self.get_object()
            #instance.id_UserAgent= request.user
            instance.save()
            instance.delete()
            return Response({"status": "success","data":"", "message": "Data deleted successfully"},status=status.HTTP_200_OK )
'''status=status.HTTP_204_NO_CONTENT'''
class ProviderCountView(APIView):
    def get(self, request):
        user = self.request.user
        userModel = User.objects.get(id=user.id)
        user__organisation__id = ''
        if userModel.entreprise:
            if userModel.entreprise.id:
                user__organisation__id = userModel.entreprise.id
                total_provider = Provider.objects.filter(entreprise__id=user__organisation__id).count()
        return Response({ "count": total_provider})
'''
class MacintView(APIView):
    def get(self, request):
        current_date = timezone.now().date()
        total_categorieMachine = CategorieMachine.objects.filter(date=current_date).count()
        total_machine = Machine.objects.filter(date=current_date).count()
        return Response({ "total": total_machine, "current_date" : current_date})
class Cat(APIView):
    def get(self, request):
        current_date = timezone.now().date()
        total_categorieMachine = CategorieMachine.objects.filter(date=current_date).count()
        total_machine = Machine.objects.filter(date=current_date).count()
        return Response({"total": total_categorieMachine , "current_date" : current_date })
'''

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        # Récupérer l'utilisateur actuellement connecté
        user = self.request.user
        userModel = User.objects.get(id=user.id)
        user__organisation__id = ''
        if userModel.entreprise:
            if userModel.entreprise.id:
                user__organisation__id = userModel.entreprise.id
                print("categorie machine")
                print(user__organisation__id)
                
                # Filtrer les posts de blog appartenant à l'utilisateur et à son organisation
                return queryset.filter(entreprise__id=user__organisation__id)
        else : 
             return queryset.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        data = serializer.data
        total_data = self.queryset.count()  # Get the total number of data

        response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "message": "Data retrieved successfully"
        }
        return Response(response_data, status=status.HTTP_200_OK)
        
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        total_data = queryset.count()

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
                serializer.save(createdBy=request.user,entreprise=request.user.entreprise)
                return Response({"status": "success", "data": serializer.data, "message": "Data added successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": "error", "data": serializer.errors, "message": "Data error!"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(createdBy=request.user,entreprise=request.user.entreprise)
                return Response({"status": "success", "data": serializer.data, "message": "Data updated successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": serializer.errors, "message": "Update error!"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
            instance = self.get_object()
            #instance.id_UserAgent= request.user
            instance.save()
            instance.delete()
            return Response({"status": "success","data":"", "message": "Data deleted successfully"},status=status.HTTP_200_OK )
    
class CategoryInventoryViewSet(viewsets.ModelViewSet):
    queryset = CategoryInventory.objects.all()
    serializer_class = CategoryInventorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        # Récupérer l'utilisateur actuellement connecté
        user = self.request.user
        userModel = User.objects.get(id=user.id)
        user__organisation__id = ''
        if userModel.entreprise:
            if userModel.entreprise.id:
                user__organisation__id = userModel.entreprise.id
                print("categorie machine")
                print(user__organisation__id)
                
                # Filtrer les posts de blog appartenant à l'utilisateur et à son organisation
                return queryset.filter(entreprise__id=user__organisation__id)
        else : 
             return queryset.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        total_data = self.queryset.count()  # Get the total number of data

        response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "message": "Data retrieved successfully"
        }
        return Response(response_data, status=status.HTTP_200_OK)
        
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        total_data = queryset.count()

        response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "message": "Data retrieved successfully"
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
            serializer = self.get_serializer(data=request.data)
            print(request.data)
            if serializer.is_valid():
                serializer.save(createdBy=request.user,entreprise=request.user.entreprise)
                return Response({"status": "success", "data": serializer.data, "message": "Data added successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": "error", "data": serializer.errors, "message": "Data error!"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(createdBy=request.user,entreprise=request.user.entreprise)
                return Response({"status": "success", "data": serializer.data, "message": "Data updated successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": serializer.errors, "message": "Update error!"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
            instance = self.get_object()
            #instance.id_UserAgent= request.user
            instance.save()
            instance.delete()
            return Response({"status": "success","data":"", "message": "Data deleted successfully"},status=status.HTTP_200_OK )

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    serializer_class_post = InventorySerializerTwo
    serializer_class_put = InventorySerializerTwo
    authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        # Récupérer l'utilisateur actuellement connecté
        user = self.request.user
        userModel = User.objects.get(id=user.id)
        user__organisation__id = ''
        if userModel.entreprise:
            if userModel.entreprise.id:
                user__organisation__id = userModel.entreprise.id
                print("categorie machine")
                print(user__organisation__id)
                
                # Filtrer les posts de blog appartenant à l'utilisateur et à son organisation
                return queryset.filter(entreprise__id=user__organisation__id)
        else : 
             return queryset.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            print("mike")
            return self.serializer_class_post
        elif self.request.method in ['PUT', 'PATCH']:
            return self.serializer_class_put
        return self.serializer_class

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        total_data = self.queryset.count() # Get the total number of data

        response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "message": "Data retrieved successfully"
        }
        return Response(response_data, status=status.HTTP_200_OK)
        
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        total_data = queryset.count()

        response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "message": "Data retrieved successfully"
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
            serializer = self.get_serializer(data=request.data)
            print(request.data)
            if serializer.is_valid():
                serializer.save(createdBy=request.user,entreprise=request.user.entreprise)
                return Response({"status": "success", "data": serializer.data, "message": "Data added successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": "error", "data": serializer.errors, "message": "Data error!"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(createdBy=request.user,entreprise=request.user.entreprise)
                return Response({"status": "success", "data": serializer.data, "message": "Data updated successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": serializer.errors, "message": "Update error!"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
            instance = self.get_object()
            #instance.id_UserAgent= request.user
            instance.save()
            instance.delete()
            return Response({"status": "success","data":"", "message": "Data deleted successfully"},status=status.HTTP_200_OK )

class InventoryCountView(APIView):
    def get(self, request):
        current_date = timezone.now().date()
        total = Inventory.objects.filter(date_creation__icontains=current_date).count() or Inventory.objects.filter(date_modification=current_date).count() 
        return Response({ "count": total,"date":current_date})

class InventoryIntoCountView(APIView):
    def get(self, request):
        current_date = timezone.now().date()
        total = InventoryInto.objects.filter(date_creation__icontains=current_date).count() or InventoryInto.objects.filter(date_modification=current_date).count() 
        return Response({ "count": total,"date":current_date})
class InventoryOutCountView(APIView):
    def get(self, request):
        current_date = timezone.now().date()
        total = InventoryOut.objects.filter(date_creation__icontains=current_date).count() or InventoryOut.objects.filter(date_modification=current_date).count() 
        return Response({ "count": total,"date":current_date})

class InventoryIntoViewSet(viewsets.ModelViewSet):
    queryset = InventoryInto.objects.all()
    serializer_class = InventoryIntoSerializer
    serializer_class_post = InventoryIntoSerializerTwo
    serializer_class_put = InventoryIntoSerializerTwo
    authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        # Récupérer l'utilisateur actuellement connecté
        user = self.request.user
        userModel = User.objects.get(id=user.id)
        user__organisation__id = ''
        if userModel.entreprise:
            if userModel.entreprise.id:
                user__organisation__id = userModel.entreprise.id
                print("categorie machine")
                print(user__organisation__id)
                
                # Filtrer les posts de blog appartenant à l'utilisateur et à son organisation
                return queryset.filter(entreprise__id=user__organisation__id)
        else : 
             return queryset.all()


    def get_serializer_class(self):
        print("chose sterialiser")
        if self.request.method == 'POST':
            print("chose sterialiser post")
            return self.serializer_class_post
        elif self.request.method in ['PUT', 'PATCH']:
            print("chose sterialiser put and patch")
            return self.serializer_class_put
        return self.serializer_class

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        total_data = self.queryset.count()  # Get the total number of data

        response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "message": "Data retrieved successfully"
        }
        return Response(response_data, status=status.HTTP_200_OK)
        
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        total_data = queryset.count()

        response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "message": "Data retrieved successfully"
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
            print(request.data)
            print(type(request.data))
            data = request.data
            data["user"] = request.user.id
            print(data)
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "data": serializer.data, "message": "Data added successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": "error", "data": serializer.errors, "message": "Data error!"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
            instance = self.get_object()
            data = request.data
            data["user"] = request.user.id
            print(request)
            serializer = self.get_serializer(instance, data=data, partial=True)
            if serializer.is_valid():
                serializer.save(createdBy=request.user,entreprise=request.user.entreprise)
                return Response({"status": "success", "data": serializer.data, "message": "Data updated successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": serializer.errors, "message": "Update error!"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
            instance = self.get_object()
            #instance.id_UserAgent= request.user
            instance.save()
            instance.delete()
            return Response({"status": "success","data":"", "message": "Data deleted successfully"},status=status.HTTP_200_OK )


class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    #pagination_class = CustomPagination
    serializer_class_post = AgentSerializerTwo
    serializer_class_put = AgentSerializerTwo
    #authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]
    #permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        # Récupérer l'utilisateur actuellement connecté
        user = self.request.user
        userModel = User.objects.get(id=user.id)
        user__organisation__id = ''
        if userModel.entreprise:
            if userModel.entreprise.id:
                user__organisation__id = userModel.entreprise.id
                print("categorie machine")
                print(user__organisation__id)
                
                # Filtrer les posts de blog appartenant à l'utilisateur et à son organisation
                return queryset.filter(entreprise__id=user__organisation__id)
        else : 
             return queryset.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            print("mike")
            return self.serializer_class_post
        elif self.request.method in ['PUT', 'PATCH']:
            return self.serializer_class_put
        return self.serializer_class
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        total_data = self.queryset.count()  # Get the total number of data

        response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "message": "Data retrieved successfully"
        }
        return Response(response_data, status=status.HTTP_200_OK)
        
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        total_data = queryset.count()

        response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "message": "Data retrieved successfully"
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()  # Créer une copie des données pour éviter les modifications sur l'objet de requête
        data["user"] = request.user.id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            instance = serializer.save(entreprise=request.user.entreprise)
            subject = f'Your pass from {request.user.entreprise} company'
            template_name = '/templates/email.html'
            context = {
                'name': instance.nom,
                'prenom': instance.prenom
            }
            message = render_to_string(template_name, context)
            from_email = request.user.email
            recipient_list = [instance.email]

            send_mail(
                subject=subject,
                message='',
                from_email=from_email,
                recipient_list=recipient_list,
                html_message=message,
            )

            return Response({
                "status": "success",
                "data": serializer.data,
                "message": "Agent added successfully and mail sent"
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "status": "error",
                "data": serializer.errors,
                "message": "Data error!"
            }, status=status.HTTP_400_BAD_REQUEST)
    def update(self, request, *args, **kwargs):
            instance = self.get_object()
            data = request.data
            data["user"] = request.user.id
            serializer = self.get_serializer(instance, data=data, partial=True)
            if serializer.is_valid():
                serializer.save(createdBy=request.user,entreprise=request.user.entreprise)
                return Response({"status": "success", "data": serializer.data, "message": "Agent updated successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": serializer.errors, "message": "Update error!"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
            instance = self.get_object()
            #instance.id_UserAgent= request.user
            instance.save()
            instance.delete()
            return Response({"status": "success", "message": "Data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class RegisterAPI(APIView):
    def post(self, request):
        print("+"*100)
        print(request.data)
        username = request.data.get("username")
        password = request.data.get("password")
        password2 = request.data.get("password2")
        firstname = request.data.get("prenom")
        lastname = request.data.get("nom")
        poste = request.data.get("poste")
        profil = request.data.get("profil")
        #recupere le user 
        user = request.user
        userModel = User.objects.get(id=user.id)
        user__organisation = ''
        if userModel.entreprise:
            if userModel.entreprise.id:
                user__organisation = userModel.entreprise

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        #if password != password2:
            #return Response({"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)
        User.objects.create(username=username, password=make_password(password), first_name=firstname, last_name=lastname,poste=poste,profil=profil,entreprise=user__organisation)
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)


class InventoryOutViewSet(viewsets.ModelViewSet):
    queryset = InventoryOut.objects.all()
    serializer_class = InventoryOutSerializer
    serializer_class_post = InventoryOutSerializerTwo
    serializer_class_put = InventoryOutSerializerTwo
    #authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]
    #permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        # Récupérer l'utilisateur actuellement connecté
        user = self.request.user
        userModel = User.objects.get(id=user.id)
        user__organisation__id = ''
        if userModel.entreprise:
            if userModel.entreprise.id:
                user__organisation__id = userModel.entreprise.id
                print("inventory")
                print(user__organisation__id)
                
                # Filtrer les posts de blog appartenant à l'utilisateur et à son organisation
                return queryset.filter(entreprise__id=user__organisation__id)
        else : 
             return queryset.all()


    def get_serializer_class(self):
        print("chose sterialiser")
        if self.request.method == 'POST':
            print("chose sterialiser post")
            return self.serializer_class_post
        elif self.request.method in ['PUT', 'PATCH']:
            print("chose sterialiser put and patch")
            return self.serializer_class_put
        return self.serializer_class

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        total_data = self.queryset.count()  # Get the total number of data
        #print("*"*100)
        #print(total_data)

        response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "message": "Data retrieved successfully"
        }
        return Response(response_data, status=status.HTTP_200_OK)
        
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        total_data = queryset.count()

        response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "message": "Data retrieved successfully"
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
            #print(request.data)
            #print(type(request.data))
            data = request.data
            data["createdBy"] = request.user.id
            total_quantity = InventoryOut.objects.filter(id_inventory_into= data["id_inventory_into"] ).aggregate(total=Sum('quantity'))['total']
            if total_quantity is None :
                 total_quantity = 0
            if total_quantity > int(data['quantity']) :
                data["isAvailable"] = False
            else:
                data["isAvailable"] = True
            
            #print(data)
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "data": serializer.data, "message": "Data added successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": "error", "data": serializer.errors, "message": "Data error!"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
            instance = self.get_object()
            data = request.data
            data["user"] = request.user.id
            total_quantity = InventoryOut.objects.filter(id_inventory_into= data["id_inventory_into"] ).aggregate(total=Sum('quantity'))['total']
            if total_quantity > int(data['quantity']) :
                data["isAvailable"] = False
            else:
                data["isAvailable"] = True
            print(data)
            serializer = self.get_serializer(instance, data=data, partial=True)
            if serializer.is_valid():
                serializer.save(createdBy=request.user,entreprise=request.user.entreprise)
                return Response({"status": "success", "data": serializer.data, "message": "Data updated successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": serializer.errors, "message": "Update error!"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
            instance = self.get_object()
            #instance.id_UserAgent= request.user
            instance.save()
            instance.delete()
            return Response({"status": "success", "message": "Data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class TeamViewSet(viewsets.ModelViewSet):

    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    serializer_class_post = TeamSerializerTwo
    serializer_class_put = TeamSerializerTwo
    authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        # Récupérer l'utilisateur actuellement connecté
        user = self.request.user
        userModel = User.objects.get(id=user.id)
        user__organisation__id = ''
        if userModel.entreprise:
            if userModel.entreprise.id:
                user__organisation__id = userModel.entreprise.id
                print("categorie machine")
                print(user__organisation__id)
                
                # Filtrer les posts de blog appartenant à l'utilisateur et à son organisation
                return queryset.filter(entreprise__id=user__organisation__id)
        else : 
             return queryset.all()

    def get_serializer_class(self):
        print("chose sterialiser")
        if self.request.method == 'POST':
            print("chose sterialiser post")
            return self.serializer_class_post
        elif self.request.method in ['PUT', 'PATCH']:
            print("chose sterialiser put and patch")
            return self.serializer_class_put
        return self.serializer_class

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        total_data = Provider.objects.all().count()  # Get the total number of data

        response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "message": "Data retrieved successfully"
        }
        return Response(response_data, status=status.HTTP_200_OK)
        
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        total_data = queryset.count()

        response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "message": "Data retrieved successfully"
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
            print(request.data)
            print(type(request.data))
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(entreprise=request.user.entreprise)
                return Response({"status": "success", "data": serializer.data, "message": "Data added successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": "error", "data": serializer.errors, "message": "Data error!"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(createdBy=request.user,entreprise=request.user.entreprise)
                return Response({"status": "success", "data": serializer.data, "message": "Data updated successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": serializer.errors, "message": "Update error!"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
            instance = self.get_object()
            #instance.id_UserAgent= request.user
            instance.save()
            instance.delete()
            return Response({"status": "success", "message": "Data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
class CodePanneViewSet(viewsets.ModelViewSet):
    queryset = CodePanne.objects.all()
    serializer_class = CodePanneSerializer
    authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        total_data = Provider.objects.all().count()  # Get the total number of data

        response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "message": "Data retrieved successfully"
        }
        return Response(response_data, status=status.HTTP_200_OK)
        
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        total_data = queryset.count()

        response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "message": "Data retrieved successfully"
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
            print(request.data)
            print(type(request.data))
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(createdBy=request.user,entreprise=request.user.entreprise)
                return Response({"status": "success", "data": serializer.data, "message": "Data added successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": "error", "data": serializer.errors, "message": "Data error!"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(createdBy=request.user,entreprise=request.user.entreprise)
                return Response({"status": "success", "data": serializer.data, "message": "Data updated successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": serializer.errors, "message": "Update error!"}, status=status.HTTP_400_BAD_REQUEST)
    def destroy(self, request, *args, **kwargs):
            instance = self.get_object()
            #instance.id_UserAgent= request.user
            instance.save()
            instance.delete()
            return Response({"status": "success", "message": "Data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    

class CategoriePanneViewSet(viewsets.ModelViewSet):
    queryset = CategoriePanne.objects.all()
    serializer_class = CategoriePanneSerializer
    def get_queryset(self):
        queryset = super().get_queryset()
        # Récupérer l'utilisateur actuellement connecté
        user = self.request.user
        userModel = User.objects.get(id=user.id)
        user__organisation__id = ''
        if userModel.entreprise:
            if userModel.entreprise.id:
                user__organisation__id = userModel.entreprise.id
                print("categorie machine")
                print(user__organisation__id)
                
                # Filtrer les posts de blog appartenant à l'utilisateur et à son organisation
                return queryset.filter(entreprise__id=user__organisation__id)
        else : 
             return queryset.all()

class WorkOrderViewSet(viewsets.ModelViewSet):
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderSerializer
    serializer_class_post = WorkOrderSerializerTwo
    serializer_class_put = WorkOrderSerializerTwo
    #authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]
    #permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination
    pagination_class = LimitOffsetPagination


    def get_serializer_class(self):
        print("chose sterialiser")
        if self.request.method == 'POST':
            print("chose sterialiser post")
            return self.serializer_class_post
        elif self.request.method in ['PUT', 'PATCH']:
            print("chose sterialiser put and patch")
            return self.serializer_class_put
        return self.serializer_class
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Récupérer l'utilisateur actuellement connecté
        user = self.request.user
        userModel = User.objects.get(id=user.id)
        user__organisation__id = ''
        if userModel.entreprise:
            if userModel.entreprise.id:
                user__organisation__id = userModel.entreprise.id
                print("categorie machine")
                print(user__organisation__id)
                
                # Filtrer les posts de blog appartenant à l'utilisateur et à son organisation
                return queryset.filter(entreprise__id=user__organisation__id)
        else : 
             return queryset.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        total_data = self.queryset.count()  # Get the total number of data

        response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "message": "Data retrieved successfully"
        }
        return Response(response_data, status=status.HTTP_200_OK)
        
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        total_data = queryset.count()

        response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "message": "Data retrieved successfully"
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
                print(request.data)
                print(type(request.data))
                serializer = self.get_serializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(createdBy=request.user,entreprise=request.user.entreprise)
                    message = f"Work Order(WO) #{serializer.data['work_order']} added successfully"
                    return Response({"status": "success", "data": serializer.data, "message": message}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"status": "error", "data": serializer.errors, "message": "Data error!"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
                instance = self.get_object()
                serializer = self.get_serializer(instance, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save(createdBy=request.user,entreprise=request.user.entreprise)
                    return Response({"status": "success", "data": serializer.data, "message": "Data updated successfully"}, status=status.HTTP_200_OK)
                else:
                    return Response({"status": "error", "data": serializer.errors, "message": "Update error!"}, status=status.HTTP_400_BAD_REQUEST)
    def destroy(self, request, *args, **kwargs):
            instance = self.get_object()
            #instance.id_UserAgent= request.user
            instance.save()
            instance.delete()
            return Response({"status": "success", "message": "Data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class WorkOrderCurrentCountView(APIView):
    def get(self, request):
        current_date = timezone.now().date()
        user = request.user
        userModel = User.objects.get(id=user.id)
        user__organisation__id = ''
        if userModel.entreprise:
                if userModel.entreprise.id:
                    user__organisation__id = userModel.entreprise.id
                    # Filtrer les posts de blog appartenant à l'utilisateur et à son organisation
                    total = WorkOrder.objects.filter(date_creation__icontains=current_date,entreprise__id=user__organisation__id).count() or InventoryOut.objects.filter(date_modification=current_date,entreprise__id=user__organisation__id).count()   
        else : 
                total = 0
        return Response({ "count": total,"date":current_date})
        
class WorkOrderWeekCountView(APIView):
    def get(self, request):
        # Get the current date
        now = timezone.now()
        # Calculate the start of the week (Monday)
        start_week = now - timedelta(days=now.weekday())
        # Calculate the end of the week (Sunday)
        end_week = start_week + timedelta(days=6)
        user = request.user
        userModel = User.objects.get(id=user.id)
        user__organisation__id = ''
        if userModel.entreprise:
                if userModel.entreprise.id:
                    user__organisation__id = userModel.entreprise.id
                    # Filtrer les posts de blog appartenant à l'utilisateur et à son organisation
                    total = WorkOrder.objects.filter(date_creation__range=[start_week, end_week],entreprise__id=user__organisation__id).count()
                    
        else : 
                total = 0
        # Query the databas
        return Response({ "count": total,"date":"this week"})

class WorkOrderMounthCountView(APIView):
    def get(self, request):
         # Obtenez la date du début du mois en cours
        start_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        user = request.user
        userModel = User.objects.get(id=user.id)
        user__organisation__id = ''
        if userModel.entreprise:
                if userModel.entreprise.id:
                    user__organisation__id = userModel.entreprise.id
                    # Filtrer les posts de blog appartenant à l'utilisateur et à son organisation
                    total = WorkOrder.objects.filter(date_creation__gte=start_of_month,entreprise__id=user__organisation__id).count()
                    
        else : 
                total = 0
        
        return Response({ "count": total,"date":"this month"})


class DiagnosticsViewSet(viewsets.ModelViewSet):
    queryset = Diagnostics.objects.all()
    serializer_class = DiagnosticsSerializer
    pagination_class = CustomPagination
    serializer_class_post = DiagnosticsSerializerTwo
    serializer_class_put = DiagnosticsSerializerTwo
    authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination


    def get_serializer_class(self):
        print("chose sterialiser")
        if self.request.method == 'POST':
            print("chose sterialiser post")
            return self.serializer_class_post
        elif self.request.method in ['PUT', 'PATCH']:
            print("chose sterialiser put and patch")
            return self.serializer_class_put
        return self.serializer_class
    def get_queryset(self):
        queryset = super().get_queryset()
        # Récupérer l'utilisateur actuellement connecté
        user = self.request.user
        userModel = User.objects.get(id=user.id)
        user__organisation__id = ''
        if userModel.entreprise:
            if userModel.entreprise.id:
                user__organisation__id = userModel.entreprise.id
                print("categorie machine")
                print(user__organisation__id)
                
                # Filtrer les posts de blog appartenant à l'utilisateur et à son organisation
                return queryset.filter(entreprise__id=user__organisation__id)
        else : 
             return queryset.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        total_data = Diagnostics.objects.all().count()  # Get the total number of data

        response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "message": "Data retrieved successfully"
        }
        return Response(response_data, status=status.HTTP_200_OK)
        
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(isRepair=False)) # Appliquer le filtre et la pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": "success",
            "data": serializer.data,
            "count": queryset.count(),
            "message": "Data retrieved successfully"
        }, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
            print(request.data)
            print(type(request.data))
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(createdBy=request.user,entreprise=request.user.entreprise)
                return Response({"status": "success", "data": serializer.data, "message": "Data added successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": "error", "data": serializer.errors, "message": "Data error!"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(createdBy=request.user,entreprise=request.user.entreprise)
                return Response({"status": "success", "data": serializer.data, "message": "Data updated successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": serializer.errors, "message": "Update error!"}, status=status.HTTP_400_BAD_REQUEST)
    def destroy(self, request, *args, **kwargs):
            instance = self.get_object()
            #instance.id_UserAgent= request.user
            instance.save()
            instance.delete()
            return Response({"status": "success", "message": "Data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class DiagnosticsCurrentCountView(APIView):
    def get(self, request):
        current_date = timezone.now().date()
        user = request.user
        userModel = User.objects.get(id=user.id)
        user__organisation__id = ''
        if userModel.entreprise:
                if userModel.entreprise.id:
                    user__organisation__id = userModel.entreprise.id
                    # Filtrer les posts de blog appartenant à l'utilisateur et à son organisation
                    total = Diagnostics.objects.filter(date_creation__icontains=current_date,entreprise__id=user__organisation__id).count() or InventoryOut.objects.filter(date_modification=current_date,entreprise__id=user__organisation__id).count()   
        else : 
                total = 0
        return Response({ "count": total,"date":current_date})

class DiagnosticsWeekCountView(APIView):
    def get(self, request):
         # Get the current date
        now = timezone.now()
        # Calculate the start of the week (Monday)
        start_week = now - timedelta(days=now.weekday())
        # Calculate the end of the week (Sunday)
        end_week = start_week + timedelta(days=6)
        user = request.user
        userModel = User.objects.get(id=user.id)
        user__organisation__id = ''
        if userModel.entreprise:
                if userModel.entreprise.id:
                    user__organisation__id = userModel.entreprise.id
                    # Filtrer les posts de blog appartenant à l'utilisateur et à son organisation
                    total = Diagnostics.objects.filter(date_creation__range=[start_week, end_week],entreprise__id=user__organisation__id).count()
                    
        else : 
                total = 0
        # Query the databas
        return Response({ "count": total,"date":"this week"})

class DiagnosticsMounthCountView(APIView):
    def get(self, request):
        start_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        user = request.user
        userModel = User.objects.get(id=user.id)
        user__organisation__id = ''
        if userModel.entreprise:
                if userModel.entreprise.id:
                    user__organisation__id = userModel.entreprise.id
                    
                    # Filtrer les posts de blog appartenant à l'utilisateur et à son organisation
                    total = Diagnostics.objects.filter(date_creation__gte=start_of_month,entreprise__id=user__organisation__id).count()
                    
        else : 
                total = 0
        return Response({ "count": total,"date":"this month"})

class TrackingPiecesViewSet(viewsets.ModelViewSet):
    queryset = TrackingPieces.objects.all()
    serializer_class = TrackingPiecesSerializer
    '''serializer_class_post = WorkOrderSerializerTwo
    serializer_class_put = WorkOrderSerializerTwo'''
    authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination


    '''def get_serializer_class(self):
        print("chose sterialiser")
        if self.request.method == 'POST':
            print("chose sterialiser post")
            return self.serializer_class_post
        elif self.request.method in ['PUT', 'PATCH']:
            print("chose sterialiser put and patch")
            return self.serializer_class_put
        return self.serializer_class'''
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Récupérer l'utilisateur actuellement connecté
        user = self.request.user
        userModel = User.objects.get(id=user.id)
        user__organisation__id = ''
        if userModel.entreprise:
            if userModel.entreprise.id:
                user__organisation__id = userModel.entreprise.id
                print("categorie machine")
                print(user__organisation__id)
                
                # Filtrer les posts de blog appartenant à l'utilisateur et à son organisation
                return queryset.filter(entreprise__id=user__organisation__id)
        else : 
             return queryset.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        total_data = self.queryset.count()  # Get the total number of data

        response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "message": "Data retrieved successfully"
        }
        return Response(response_data, status=status.HTTP_200_OK)
        
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        total_data = queryset.count()

        response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "message": "Data retrieved successfully"
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
                print(request.data)
                serializer = self.get_serializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(createdBy=request.user,entreprise=request.user.entreprise)
                    message = f"Data added successfully"
                    return Response({"status": "success", "data": serializer.data, "message": message}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"status": "error", "data": serializer.errors, "message": "Data error!"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
                instance = self.get_object()
                serializer = self.get_serializer(instance, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save(createdBy=request.user,entreprise=request.user.entreprise)
                    return Response({"status": "success", "data": serializer.data, "message": "Data updated successfully"}, status=status.HTTP_200_OK)
                else:
                    return Response({"status": "error", "data": serializer.errors, "message": "Update error!"}, status=status.HTTP_400_BAD_REQUEST)
    def destroy(self, request, *args, **kwargs):
            instance = self.get_object()
            #instance.id_UserAgent= request.user
            instance.save()
            instance.delete()
            return Response({"status": "success", "message": "Data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class PlanifierMaintenanceCurrentCountView(APIView):
    def get(self, request):
        current_date = timezone.now().date()
        user = request.user
        userModel = User.objects.get(id=user.id)
        user__organisation__id = ''
        if userModel.entreprise:
                if userModel.entreprise.id:
                    user__organisation__id = userModel.entreprise.id
                    # Filtrer les posts de blog appartenant à l'utilisateur et à son organisation
                    total = PlanifierMaintenance.objects.filter(date_creation__icontains=current_date,entreprise__id=user__organisation__id).count() or InventoryOut.objects.filter(date_modification=current_date,entreprise__id=user__organisation__id).count()   
        else : 
                total = 0
        return Response({ "count": total,"date":current_date})

class PlanifierMaintenanceWeekCountView(APIView):
    def get(self, request):
        # Get the current date
        now = timezone.now()
        # Calculate the start of the week (Monday)
        start_week = now - timedelta(days=now.weekday())
        # Calculate the end of the week (Sunday)
        end_week = start_week + timedelta(days=6)
        user = request.user
        userModel = User.objects.get(id=user.id)
        user__organisation__id = ''
        if userModel.entreprise:
                if userModel.entreprise.id:
                    user__organisation__id = userModel.entreprise.id
                    # Filtrer les posts de blog appartenant à l'utilisateur et à son organisation
                    total = PlanifierMaintenance.objects.filter(date_creation__range=[start_week, end_week],entreprise__id=user__organisation__id).count()
                    
        else : 
                total = 0
        # Query the database
        
        return Response({ "count": total,"date":"this week"})

class PlanifierMaintenanceMounthCountView(APIView):
    def get(self, request):
         # Obtenez la date du début du mois en cours
        start_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        user = request.user
        userModel = User.objects.get(id=user.id)
        user__organisation__id = ''
        if userModel.entreprise:
                if userModel.entreprise.id:
                    user__organisation__id = userModel.entreprise.id
                    
                    # Filtrer les posts de blog appartenant à l'utilisateur et à son organisation
                    total = PlanifierMaintenance.objects.filter(date_creation__gte=start_of_month,entreprise__id=user__organisation__id).count()
                    
        else : 
                total = 0
        
        return Response({ "count": total,"date":"this month"})

class PlanifierMaintenanceViewSet(viewsets.ModelViewSet):
    queryset = PlanifierMaintenance.objects.all()
    serializer_class = PlanifierMaintenanceSerializer
    serializer_class_post = PlanifierMaintenanceSerializerTwo
    serializer_class_put = PlanifierMaintenanceSerializerTwo
    authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination


    def get_serializer_class(self):
        print("chose sterialiser")
        if self.request.method == 'POST':
            print("chose sterialiser post")
            return self.serializer_class_post
        elif self.request.method in ['PUT', 'PATCH']:
            print("chose sterialiser put and patch")
            return self.serializer_class_put
        return self.serializer_class
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Récupérer l'utilisateur actuellement connecté
        user = self.request.user
        userModel = User.objects.get(id=user.id)
        user__organisation__id = ''
        if userModel.entreprise:
            if userModel.entreprise.id:
                user__organisation__id = userModel.entreprise.id
                print("categorie machine")
                print(user__organisation__id)
                
                # Filtrer les posts de blog appartenant à l'utilisateur et à son organisation
                return queryset.filter(entreprise__id=user__organisation__id)
        else : 
             return queryset.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        total_data = self.queryset.count()  # Get the total number of data
        print(data)
        response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "message": "Data retrieved successfully"
        }
        return Response(response_data, status=status.HTTP_200_OK)
        
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        total_data = queryset.count()

        response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "message": "Data retrieved successfully"
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
                print(request.data)
                print(type(request.data))
                serializer = self.get_serializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(createdBy=request.user,entreprise=request.user.entreprise)
                    message = f"Data added successfully"
                    return Response({"status": "success", "data": serializer.data, "message": message}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"status": "error", "data": serializer.errors, "message": "Data error!"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
                instance = self.get_object()
                serializer = self.get_serializer(instance, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save(createdBy=request.user,entreprise=request.user.entreprise)
                    return Response({"status": "success", "data": serializer.data, "message": "Data updated successfully"}, status=status.HTTP_200_OK)
                else:
                    return Response({"status": "error", "data": serializer.errors, "message": "Update error!"}, status=status.HTTP_400_BAD_REQUEST)
    def destroy(self, request, *args, **kwargs):
            instance = self.get_object()
            #instance.id_UserAgent= request.user
            instance.save()
            instance.delete()
            return Response({"status": "success", "message": "Data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class RemindViewSet(viewsets.ModelViewSet):
        queryset = Remind.objects.all()
        serializer_class = RemindSerializer
        serializer_class_post = RemindSerializerTwo
        serializer_class_put = RemindSerializerTwo
        authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]
        permission_classes = [permissions.IsAuthenticated]
        pagination_class = CustomPagination


        def get_serializer_class(self):
            print("chose sterialiser")
            if self.request.method == 'POST':
                print("chose sterialiser post")
                return self.serializer_class_post
            elif self.request.method in ['PUT', 'PATCH']:
                print("chose sterialiser put and patch")
                return self.serializer_class_put
            return self.serializer_class
        
        def get_queryset(self):
            queryset = super().get_queryset()
            # Récupérer l'utilisateur actuellement connecté
            user = self.request.user
            userModel = User.objects.get(id=user.id)
            user__organisation__id = ''
            if userModel.entreprise:
                if userModel.entreprise.id:
                    user__organisation__id = userModel.entreprise.id
                    
                    # Filtrer les posts de blog appartenant à l'utilisateur et à son organisation
                    return queryset.filter(entreprise__id=user__organisation__id)
            else : 
                return queryset.all()

        def retrieve(self, request, *args, **kwargs):
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            data = serializer.data
            total_data = self.queryset.count()  # Get the total number of data
            print(data)
            response_data = {
                "status": "success",
                "data": data,
                "count": total_data,
                "message": "Data retrieved successfully"
            }
            return Response(response_data, status=status.HTTP_200_OK)
            
        def list(self, request, *args, **kwargs):
            queryset = self.get_queryset()
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
            else:
                serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
            total_data = queryset.count()

            response_data = {
                "status": "success",
                "data": data,
                "count": total_data,
                "message": "Data retrieved successfully"
            }
            return Response(response_data, status=status.HTTP_200_OK)

        def create(self, request, *args, **kwargs):
                    print(request.data)
                    print(type(request.data))
                    serializer = self.get_serializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save(createdBy=request.user,entreprise=request.user.entreprise)
                        message = f"Data added successfully"
                        return Response({"status": "success", "data": serializer.data, "message": message}, status=status.HTTP_201_CREATED)
                    else:
                        return Response({"status": "error", "data": serializer.errors, "message": "Data error!"}, status=status.HTTP_400_BAD_REQUEST)

        def update(self, request, *args, **kwargs):
                    instance = self.get_object()
                    serializer = self.get_serializer(instance, data=request.data, partial=True)
                    if serializer.is_valid():
                        serializer.save(createdBy=request.user,entreprise=request.user.entreprise)
                        return Response({"status": "success", "data": serializer.data, "message": "Data updated successfully"}, status=status.HTTP_200_OK)
                    else:
                        return Response({"status": "error", "data": serializer.errors, "message": "Update error!"}, status=status.HTTP_400_BAD_REQUEST)
        def destroy(self, request, *args, **kwargs):
                instance = self.get_object()
                #instance.id_UserAgent= request.user
                instance.save()
                instance.delete()
                return Response({"status": "success", "message": "Data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



@api_view(['GET'])
#@authentication_classes([authentication.SessionAuthentication, authentication.TokenAuthentication])
#@permission_classes([permissions.IsAuthenticated])
def remind_retrieve(request, id_planifierMaintenance):
    remind = get_list_or_404(Remind, id_planifierMaintenance=id_planifierMaintenance)
    print(remind)
    serializer = RemindSerializer(remind, many=True)
    total_data = Remind.objects.filter(id_planifierMaintenance=id_planifierMaintenance).count()
    data = serializer.data
    response_data = {
        "status": "success",
        "data": data,
        "count": total_data,
        "message": "Data retrieved successfully"
    }
    return Response(response_data, status=status.HTTP_200_OK)

class PlanifierRepairViewSet(viewsets.ModelViewSet):
    queryset = PlanifierRepair.objects.all()
    serializer_class = PlanifierRepairSerializer
    serializer_class_post = PlanifierRepairSerializerTwo
    serializer_class_put = PlanifierRepairSerializerTwo
    authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        # Récupérer l'utilisateur actuellement connecté
        user = self.request.user
        userModel = User.objects.get(id=user.id)
        user__organisation__id = ''
        if userModel.entreprise:
            if userModel.entreprise.id:
                user__organisation__id = userModel.entreprise.id
                print("categorie machine")
                print(user__organisation__id)
                
                # Filtrer les posts de blog appartenant à l'utilisateur et à son organisation
                return queryset.filter(entreprise__id=user__organisation__id)
        else : 
             return queryset.all()

    def get_serializer_class(self):
        print("chose sterialiser")
        if self.request.method == 'POST':
            print("chose sterialiser post")
            return self.serializer_class_post
        elif self.request.method in ['PUT', 'PATCH']:
            print("chose sterialiser put and patch")
            return self.serializer_class_put
        return self.serializer_class

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        total_data = self.queryset.count()  # Get the total number of data
        print(data)
        response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "message": "Data retrieved successfully"
        }
        return Response(response_data, status=status.HTTP_200_OK)
        
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        total_data = queryset.count()

        response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "message": "Data retrieved successfully"
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
                print(request.data)
                print(type(request.data))
                serializer = self.get_serializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(createdBy=request.user,entreprise=request.user.entreprise)
                    message = f"Data added successfully"
                    return Response({"status": "success", "data": serializer.data, "message": message}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"status": "error", "data": serializer.errors, "message": "Data error!"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
                instance = self.get_object()
                serializer = self.get_serializer(instance, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save(createdBy=request.user,entreprise=request.user.entreprise)
                    return Response({"status": "success", "data": serializer.data, "message": "Data updated successfully"}, status=status.HTTP_200_OK)
                else:
                    return Response({"status": "error", "data": serializer.errors, "message": "Update error!"}, status=status.HTTP_400_BAD_REQUEST)
    def destroy(self, request, *args, **kwargs):
            instance = self.get_object()
            #instance.id_UserAgent= request.user
            instance.save()
            instance.delete()
            return Response({"status": "success", "message": "Data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class RemindRepairViewSet(viewsets.ModelViewSet):
    queryset = RemindRepair.objects.all()
    serializer_class = RemindRepairSerializer
    authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        # Récupérer l'utilisateur actuellement connecté
        user = self.request.user
        userModel = User.objects.get(id=user.id)
        user__organisation__id = ''
        if userModel.entreprise:
            if userModel.entreprise.id:
                user__organisation__id = userModel.entreprise.id
                print("categorie machine")
                print(user__organisation__id)
                
                # Filtrer les posts de blog appartenant à l'utilisateur et à son organisation
                return queryset.filter(entreprise__id=user__organisation__id)
        else : 
             return queryset.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        total_data = self.queryset.count()  # Get the total number of data
        print(data)
        response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "message": "Data retrieved successfully"
        }
        return Response(response_data, status=status.HTTP_200_OK)
        
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        total_data = queryset.count()

        response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "message": "Data retrieved successfully"
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
                print(request.data)
                print(type(request.data))
                serializer = self.get_serializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(createdBy=request.user,entreprise=request.user.entreprise)
                    message = f"Data added successfully"
                    return Response({"status": "success", "data": serializer.data, "message": message}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"status": "error", "data": serializer.errors, "message": "Data error!"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
                instance = self.get_object()
                serializer = self.get_serializer(instance, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save(createdBy=request.user,entreprise=request.user.entreprise)
                    return Response({"status": "success", "data": serializer.data, "message": "Data updated successfully"}, status=status.HTTP_200_OK)
                else:
                    return Response({"status": "error", "data": serializer.errors, "message": "Update error!"}, status=status.HTTP_400_BAD_REQUEST)
    def destroy(self, request, *args, **kwargs):
            instance = self.get_object()
            #instance.id_UserAgent= request.user
            instance.save()
            instance.delete()
            return Response({"status": "success", "message": "Data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class PlanifierRepairCurrentCountView(APIView):
    def get(self, request):
        current_date = timezone.now().date()
        total = PlanifierRepair.objects.filter(date_creation__icontains=current_date).count()
        return Response({ "count": total,"date":current_date})

class PlanifierRepairWeekCountView(APIView):
    def get(self, request):
        # Get the current date
        now = timezone.now()
        # Calculate the start of the week (Monday)
        start_week = now - timedelta(days=now.weekday())
        # Calculate the end of the week (Sunday)
        end_week = start_week + timedelta(days=6)
        # Query the database
        total = PlanifierRepair.objects.filter(date_creation__range=[start_week, end_week]).count()
        return Response({ "count": total,"date":"this week"})

class PlanifierRepairMounthCountView(APIView):
    def get(self, request):
        # Get the current date
        # Obtenez la date du début du mois en cours
        start_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        # Obtenez le nombre d'éléments pendant le mois en cours
        total = PlanifierRepair.objects.filter(date_creation__gte=start_of_month).count()
        return Response({ "count": total,"date":"this month"})


@api_view(['GET'])
#@authentication_classes([authentication.SessionAuthentication, authentication.TokenAuthentication])
#@permission_classes([permissions.IsAuthenticated])
def remind_repair_retrieve(request, id_planifierRepair):
    remind = get_list_or_404(RemindRepair, id_PlanifierRepair=id_planifierRepair)
    print(remind)
    serializer = RemindRepairSerializer(remind, many=True)
    total_data = RemindRepair.objects.filter(id_PlanifierRepair=id_planifierRepair).count()
    data = serializer.data
    response_data = {
        "status": "success",
        "data": data,
        "count": total_data,
        "message": "Data retrieved successfully"
    }
    return Response(response_data, status=status.HTTP_200_OK)


class PlanifierTeamViewSet(viewsets.ModelViewSet):
    queryset = PlanifierTeam.objects.all()
    serializer_class = PlanifierTeamSerializer
    serializer_class_post = PlanifierTeamSerializerTwo
    serializer_class_put = PlanifierTeamSerializerTwo
    authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        print("chose sterialiser")
        if self.request.method == 'POST':
            print("chose sterialiser post")
            return self.serializer_class_post
        elif self.request.method in ['PUT', 'PATCH']:
            print("chose sterialiser put and patch")
            return self.serializer_class_put
        return self.serializer_class
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Récupérer l'utilisateur actuellement connecté
        user = self.request.user
        userModel = User.objects.get(id=user.id)
        user__organisation__id = ''
        if userModel.entreprise:
            if userModel.entreprise.id:
                user__organisation__id = userModel.entreprise.id
                print("categorie machine")
                print(user__organisation__id)
                
                # Filtrer les posts de blog appartenant à l'utilisateur et à son organisation
                return queryset.filter(entreprise__id=user__organisation__id)
        else : 
             return queryset.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        total_data = self.queryset.count()  # Get the total number of data
        print(data)
        response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "message": "Data retrieved successfully"
        }
        return Response(response_data, status=status.HTTP_200_OK)
        
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        total_data = queryset.count()

        response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "message": "Data retrieved successfully"
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
                print(request.data)
                print(type(request.data))
                serializer = self.get_serializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(createdBy=request.user,entreprise=request.user.entreprise)
                    message = f"Data added successfully"
                    return Response({"status": "success", "data": serializer.data, "message": message}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"status": "error", "data": serializer.errors, "message": "Data error!"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
                instance = self.get_object()
                serializer = self.get_serializer(instance, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save(createdBy=request.user,entreprise=request.user.entreprise)
                    return Response({"status": "success", "data": serializer.data, "message": "Data updated successfully"}, status=status.HTTP_200_OK)
                else:
                    return Response({"status": "error", "data": serializer.errors, "message": "Update error!"}, status=status.HTTP_400_BAD_REQUEST)
    def destroy(self, request, *args, **kwargs):
            instance = self.get_object()
            #instance.id_UserAgent= request.user
            instance.save()
            instance.delete()
            return Response({"status": "success", "message": "Data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class RemindTeamViewSet(viewsets.ModelViewSet):
    queryset = RemindTeam.objects.all()
    serializer_class = RemindTeamSerializer
    authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        # Récupérer l'utilisateur actuellement connecté
        user = self.request.user
        userModel = User.objects.get(id=user.id)
        user__organisation__id = ''
        if userModel.entreprise:
            if userModel.entreprise.id:
                user__organisation__id = userModel.entreprise.id
                print("categorie machine")
                print(user__organisation__id)
                
                # Filtrer les posts de blog appartenant à l'utilisateur et à son organisation
                return queryset.filter(entreprise__id=user__organisation__id)
        else : 
             return queryset.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        total_data = self.queryset.count()  # Get the total number of data
        print(data)
        response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "message": "Data retrieved successfully"
        }
        return Response(response_data, status=status.HTTP_200_OK)
        
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        total_data = queryset.count()

        response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "message": "Data retrieved successfully"
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
                print(request.data)
                print(type(request.data))
                serializer = self.get_serializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(createdBy=request.user,entreprise=request.user.entreprise)
                    message = f"Data added successfully"
                    return Response({"status": "success", "data": serializer.data, "message": message}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"status": "error", "data": serializer.errors, "message": "Data error!"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
                instance = self.get_object()
                serializer = self.get_serializer(instance, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save(createdBy=request.user,entreprise=request.user.entreprise)    
                    return Response({"status": "success", "data": serializer.data, "message": "Data updated successfully"}, status=status.HTTP_200_OK)
                else:
                    return Response({"status": "error", "data": serializer.errors, "message": "Update error!"}, status=status.HTTP_400_BAD_REQUEST)
    def destroy(self, request, *args, **kwargs):
            instance = self.get_object()
            #instance.id_UserAgent= request.user
            instance.save()
            instance.delete()
            return Response({"status": "success", "message": "Data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)






@api_view(['GET'])
#@authentication_classes([authentication.SessionAuthentication, authentication.TokenAuthentication])
#@permission_classes([permissions.IsAuthenticated])
def remind_team_retrieve(request, id_PlanifierTeam):
    remind = get_list_or_404(RemindTeam, id_PlanifierTeam=id_PlanifierTeam)
    print(remind)
    serializer = RemindTeamSerializerSpecialGet(remind, many=True)
    total_data = RemindTeam.objects.filter(id_PlanifierTeam=id_PlanifierTeam).count()
    data = serializer.data
    response_data = {
        "status": "success",
        "data": data,
        "count": total_data,
        "message": "Data retrieved successfully"
    }
    return Response(response_data, status=status.HTTP_200_OK)

class RepairViewSet(viewsets.ModelViewSet):
    queryset = Diagnostics.objects.all()
    serializer_class = DiagnosticsSerializer
   
    serializer_class_post = DiagnosticsSerializerTwo
    serializer_class_put = DiagnosticsSerializerTwo
    authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination


    def get_serializer_class(self):
        print("chose sterialiser")
        if self.request.method == 'POST':
            print("chose sterialiser post")
            return self.serializer_class_post
        elif self.request.method in ['PUT', 'PATCH']:
            print("chose sterialiser put and patch")
            return self.serializer_class_put
        return self.serializer_class
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Récupérer l'utilisateur actuellement connecté
        user = self.request.user
        userModel = User.objects.get(id=user.id)
        user__organisation__id = ''
        if userModel.entreprise:
            if userModel.entreprise.id:
                user__organisation__id = userModel.entreprise.id
                print("categorie machine")
                print(user__organisation__id)
                
                # Filtrer les posts de blog appartenant à l'utilisateur et à son organisation
                return queryset.filter(entreprise__id=user__organisation__id)
        else : 
             return queryset.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        total_data = Provider.objects.all().count()  # Get the total number of data

        response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "message": "Data retrieved successfully"
        }
        return Response(response_data, status=status.HTTP_200_OK)
        
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(isRepair=True)  # Add the filter condition here
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        total_data = queryset.count()  # Get the total number of data

        response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "message": "Data retrieved successfully"
        }
        return Response(response_data, status=status.HTTP_200_OK)
    def update(self, request, *args, **kwargs):
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(createdBy=request.user,entreprise=request.user.entreprise)
                return Response({"status": "success", "data": serializer.data, "message": "Data updated successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": serializer.errors, "message": "Update error!"}, status=status.HTTP_400_BAD_REQUEST)
    def destroy(self, request, *args, **kwargs):
            instance = self.get_object()
            #instance.id_UserAgent= request.user
            instance.save()
            instance.delete()
            return Response({"status": "success", "message": "Data deleted successfully"}, status=status.HTTP_204_NO_CONTENT) 

class RepairCurrentCountView(APIView):
    def get(self, request):
        current_date = timezone.now().date()
        total = Diagnostics.objects.filter(date_creation__icontains=current_date,isRepair=True).count()
        return Response({ "count": total,"date":current_date})

class RepairWeekCountView(APIView):
    def get(self, request):
        # Get the current date
        now = timezone.now()
        # Calculate the start of the week (Monday)
        start_week = now - timedelta(days=now.weekday())
        # Calculate the end of the week (Sunday)
        end_week = start_week + timedelta(days=6)
        # Query the database
        total = Diagnostics.objects.filter(date_creation__range=[start_week, end_week],isRepair=True).count()
        return Response({ "count": total,"date":"this week"})

class RepairMounthCountView(APIView):
    def get(self, request):
        # Get the current date
        # Obtenez la date du début du mois en cours
        start_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        # Obtenez le nombre d'éléments pendant le mois en cours
        total = Diagnostics.objects.filter(date_creation__gte=start_of_month,isRepair=True).count()
        return Response({ "count": total,"date":"this month"})


@api_view(['GET'])
#@authentication_classes([authentication.SessionAuthentication, authentication.TokenAuthentication])
#@permission_classes([permissions.IsAuthenticated])
def team_retrieve(request, team):
    agent = get_list_or_404(Agent, team=team)
    print(agent)
    serializer = AgentSerializer(agent, many=True)
    total_data = Agent.objects.filter(team=team).count()
    data = serializer.data
    print(data)
    response_data = {
        "status": "success",
        "data": data,
        "count": total_data,
        "message": "Data retrieved successfully"
    }
    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['GET'])
def TrackingPieces_retrieve(request, work_order):
    pieces = get_list_or_404(TrackingPieces, id_work_order=work_order)
    serializer = TrackingPiecesSerializerforDetails(pieces,many=True)
    total_data = len(serializer.data)
    '''data = []
    data_list = []
    for i in range(0, total_data):
           data_list.append(serializer.data[i]['id_inventory_out'])
           data.append(serializer.data[i]['id_inventory_out'])
    for i in data_list:
       if not i:
          continue
    data.append(i[0])'''
    
    data = serializer.data
    print(data)

    response_data = {
        "status": "success",
        "data": data,
        "count": total_data,
        "message": "Data retrieved successfully"
    }
    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['GET'])
def InventoryInto_list(request):
    inventoryInto = get_list_or_404(InventoryInto) 
    serializer = InventoryIntoSerializer(inventoryInto, many=True)
    print(serializer.data)
    available_inventory = [item for item in serializer.data if item["etat"] == "available"]
    total_data = len(available_inventory)
    data = available_inventory
    response_data = {
        "status": "success",
        "data": data,
        "count": total_data,
        "message": "Data retrieved successfully"
    }
    return Response(response_data, status=status.HTTP_200_OK)
@api_view(['GET'])
def InventoryInto_list_2(request):
    inventoryInto = get_list_or_404(InventoryInto) 
    serializer = InventoryIntoSerializer(inventoryInto, many=True)
    print(serializer.data)
    available_inventory = [item for item in serializer.data if item["etat"] == "unavailable"]
    total_data = len(available_inventory)
    data = available_inventory
    response_data = {
        "status": "success",
        "data": data,
        "count": total_data,
        "message": "Data retrieved successfully"
    }
    return Response(response_data, status=status.HTTP_200_OK)
@api_view(['GET'])
def InventoryOut_list_available(request):
    inventoryOut = get_list_or_404(InventoryOut) 
    serializer = InventoryOutSerializer(inventoryOut, many=True)
    print(serializer.data)
    available_inventory = [item for item in serializer.data if item["etat"] == "unavailable"]
    total_data = len(available_inventory)
    data = available_inventory
    response_data = {
        "status": "success",
        "data": data,
        "count": total_data,
        "message": "Data retrieved successfully"
    }
    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['GET'])
def Code_panne_retrieve(request, work_order):
    wo = get_list_or_404(WorkOrder, work_order=work_order)
    serializer = WorkOrderSerializerforDetails(wo, many=True)
    total_data = len(serializer.data)
    data = []
    data_list = []
    for i in range(0, total_data):
       data_list.append(serializer.data[i]['id_code_panne'])
    for i in data_list:
       if not i:
          continue
       data.append(i[0])

    response_data = {
        "status": "success",
        "data": data,
        "count": total_data,
        "message": "Data retrieved successfully"
    }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def Inventory_list(request):
    inventory = Inventory.objects.all().values('id', 'designation').distinct()
    serializer = InventorySerializer(inventory, many=True)
    print(serializer.data)
    total_data = len(serializer.data)
    data = serializer.data
    response_data = {
        "status": "success",
        "data": data,
        "count": total_data,
        "message": "Data retrieved successfully"
    }
    return Response(response_data, status=status.HTTP_200_OK)

class UserAPIView(APIView):
    #permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination
    #authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]
    serializer = ""
    def get(self, request, user_id):
        try:
            user = User.objects.get(agent=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        data = serializer.data
        response_data = {
            "status": "success",
            "data": data,
            "message": "Data retrieved successfully"
        }
        return Response(response_data, status=status.HTTP_200_OK)


@api_view(["GET"])
def code_panne_get_list_for_machine_retrieve(request):
    id_WO = request.query_params.get("wo")
    data_WO = WorkOrder.objects.filter(work_order=id_WO)
    serializer = CodePanneDetailsSerializer(data_WO)
    data = serializer.data
    total_data = len(data)
    response_data = {
            "status": "success",
            "data": data,
            "count": total_data,
            "mike":"mike",
            "message": "Data retrieved successfully",
        }
    return Response(response_data, status=status.HTTP_200_OK)
