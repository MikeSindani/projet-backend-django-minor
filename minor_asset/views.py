from django.shortcuts import render
from rest_framework import viewsets
from .models import CategorieMachine
from .serializers import CategorieMachineSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .filter import CategorieMachineFilter
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from rest_framework import generics, authentication
from rest_framework import permissions

# Create your views here.

#class CategorieMachineViewSet(viewsets.ModelViewSet):
    #queryset = CategorieMachine.objects.all()
    #serializer_class = CategorieMachineSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'data': data
        })


class CategorieMachineViewSet(viewsets.ModelViewSet):
    queryset = CategorieMachine.objects.all()
    serializer_class = CategorieMachineSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = CategorieMachineFilter # Remplacez 'nom' par le nom de votre champ
    pagination_class = CustomPagination
    authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

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
            return Response({"status": "success", "message": "Data deleted successfully"}, status=status.HTTP_200_OK)