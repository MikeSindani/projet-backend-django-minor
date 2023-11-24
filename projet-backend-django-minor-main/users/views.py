from django.shortcuts import render

# Create your views here.
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from rest_framework import generics, authentication
from users.models import *

class GetUserDetailsView(APIView):
    authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated] 

    def get(self, request):
        user = request.user
        userModel = User.objects.get(id=user.id)
        userAgent = "Admin"  # Default value

        # Check if userModel.agent exists before accessing its 'team' attribute
        if userModel.agent:
            if userModel.agent:
                userAgent = userModel.agent.team.nom
                
                
        return Response({
            'id':user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'poste': user.poste,
            "team": userAgent,
        })
