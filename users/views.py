from django.shortcuts import render

# Create your views here.
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication,
    TokenAuthentication,
)
from rest_framework import generics, authentication
from users.models import *


class GetUserDetailsView(APIView):

    authentication_classes = [
        authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    ]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        userModel = User.objects.get(id=user.id)
        userAgent = "Admin"  # Default value
        user_agent_type = ""
        user__isChief = False
        # Check if userModel.agent exists before accessing its 'team' attribute
        if userModel.agent:
            if userModel.agent:
                userAgent = userModel.agent.team.name
                user_agent_type = userModel.agent.team.team_type
                if (
                    userModel.agent.isSupervisor == True
                    or userModel.agent.isAssistant == True
                ):
                    user__isChief = True

        return Response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "poste": user.poste,
                "team": userAgent,
                "isChief": user__isChief,
                "type_agent": user_agent_type,
                "profil": user.profil,
            }
        )
