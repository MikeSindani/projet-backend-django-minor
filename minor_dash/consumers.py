import time
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from minor_dash.bussiness import Domain
import json
from minor_asset.models import InventoryInto
from minor_asset.serializers import InventorySerializerForWebSockets
from channels.db import database_sync_to_async
import asyncio
from minor_asset.models import Remind,RemindRepair,PlanifierRepair,PlanifierMaintenance,PlanifierTeam,RemindTeam
from django.shortcuts import get_list_or_404
from minor_asset.serializers import RemindSerializerForWebSockets,RemindRepairSerializerForWebSockets,PlanifierRepairSerializerForWebSockets,PlanifierMaintenanceForWebSockets,PlanifierTeamForWebSockets
from datetime import datetime, timedelta
from django.utils import timezone
from asgiref.sync import sync_to_async
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class OneConsumer(AsyncWebsocketConsumer):
    def connect(self):
        self.accept()
        for i in range(100):
            self.send(json.dumps({"message":"mike"}))
            time.sleep(2)


'''class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        print(self.user)
        await self.channel_layer.group_add("Notification", self.channel_name)
        await self.accept()
        
        # Exécuter get_data_in_database_of_invnetory_into en arrière-plan
        asyncio.create_task(self.send_available_inventory())

    async def send_available_inventory(self):
        try:
            available_inventory = await self.get_data_in_database_of_invnetory_into()
            if available_inventory:
                print("unavailable realtime")
                await asyncio.sleep(1) # Adjust the sleep duration as needed
                await self.send(text_data=json.dumps({
                    'message': available_inventory
                }))
        except Exception as e:
            print(f"Error fetching inventory: {e}")

    @database_sync_to_async
    def get_data_in_database_of_invnetory_into(self):
        inventory_data = InventoryInto.objects.all()
        serializer = InventorySerializerForWebSockets(inventory_data, many=True)
        available_inventory = [item for item in serializer.data if item["etat"] == "unavailable"]
        return available_inventory

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("Notification", self.channel_name)
        await self.send(text_data=json.dumps({
            'message': 'User disconnected'
        }))


    async def receive(self, text_data):
        print(text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def send_data(self, event): 
        print("send_data")
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
'''


class ContentConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        await self.channel_layer.group_add("Content", self.channel_name) # nom du groupe
      # Accept the connection
        await self.accept() # code qui accepte la connection.
      # Fetch data from the InventoryInto database
       
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("Content", self.channel_name)# nom du groupe a change 
        '''await self.send(text_data=json.dumps({
          'message': 'You are now disconnected.'
        }))'''

    async def receive(self, text_data):
        print("receive_data")
        print(text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)
        await self.send(text_data=json.dumps({
          'message': message
        }))

    ''' async def send_data(self, event):
      print("send_data")
      message = event['message']
      print(message)
      await self.send(text_data=json.dumps({
          'message': message
      }))
'''


  # Assurez-vous d'avoir importé le modèle

class NotificationConsumer(AsyncWebsocketConsumer):
    def connect(self):
        self.accept()
        
    async def connect(self):
        self.user = self.scope["user"]
        print(self.user)
        # Extraire le nom d'organisation de l'URL
        organization_id = self.scope['url_route']['kwargs'].get('organization_id')
        print(f"Organization ID: {organization_id}")
        # Ajouter l'utilisateur au groupe de notification spécifique à l'organisation
        group_name = f'Notification_{organization_id}'
        await self.channel_layer.group_add(group_name, self.channel_name)
        await self.accept()

        asyncio.create_task(self.schedule_verify_and_send_data(organization_id=organization_id))

        # Exécuter get_data_in_database_of_invnetory_into en arrière-plan
        asyncio.create_task(self.schedule_send_available_inventory(organization_id=organization_id))
        
    async def schedule_verify_and_send_data(self,organization_id):
        while True:
            await self.verify_and_send_data(organization_id=organization_id)
            await asyncio.sleep(50)

    async def disconnect(self, close_code):
        # Supprimez l'utilisateur du groupe de notification spécifique à l'organisation
        group_name = f'Notification_{self.scope["url_route"]["kwargs"].get("organization_id")}'
        await self.channel_layer.group_discard(group_name, self.channel_name)
        self.verify_task.cancel()
        
    async def schedule_send_available_inventory(self,organization_id):
        
            await self.send_available_inventory(organization_id=organization_id)
            await asyncio.sleep(1)

    @sync_to_async
    def send_available_inventory(self, organization_id=None):
        try:
            available_inventory =  self.get_data_in_database_of_invnetory_into(organization_id)
            if available_inventory:
                print("Unavailable realtime")
                # Adjust the sleep duration as needed
                # Construire le nom du groupe spécifique à l'organisation
                self.send_data_to_channels(available_inventory, organization_id)
        except Exception as e:
            print(f"Error fetching inventory: {e}")

    
    def get_data_in_database_of_invnetory_into(self, organization_id=None):
        query = InventoryInto.objects.all()
        if organization_id:
            query = query.filter(entreprise__id=organization_id)
        serializer = InventorySerializerForWebSockets(query, many=True)
        available_inventory = [item for item in serializer.data if item["etat"] == "unavailable"]
        return available_inventory

    async def receive(self, text_data):
        #print(text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)
        await self.send(text_data=json.dumps({
            'message': message
        }))

    def send_data_to_channels(self, data, organization_id: str):
        #print(data)
        group_name = f'Notification_{organization_id}'
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'send_data',
                'message': data,
            } )
    
    
    async def send_data(self, event):
      #print("send_data")
      message = event['message']
      print(message)
      await self.send(text_data=json.dumps({
          'message': message
      }))
    
    @sync_to_async
    def verify_and_send_data(self, organization_id=None):
        try:
            # Get the current date and time
            current_datetime = datetime.now()

            # Format the datetime object into a string
            formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M")
            formatted_date = current_datetime.strftime("%Y-%m-%d")
            formatted_time = current_datetime.strftime("%H:%M")
            day_of_week = current_datetime.weekday()
            #print(organization_id)
            print(formatted_datetime)
            print(formatted_date)
            print(formatted_time)
            print(day_of_week)

            # Get reminders
            remind =  self.get_reminders(formatted_datetime,organisation=organization_id)
            serializer = RemindSerializerForWebSockets(remind, many=True)
            models_to_send = serializer.data
            #print(models_to_send)

            if models_to_send:
                 self.send_data_to_channels(models_to_send, organization_id)

            
            remind_repair =  self.get_remind_repair(formatted_datetime=formatted_datetime,organisation=organization_id)
            serializer = RemindRepairSerializerForWebSockets(remind_repair, many=True)
            models_to_send_remind_planned_repair = serializer.data
            #print(models_to_send_remind_planned_repair)

            # Send the models to the group
            if models_to_send_remind_planned_repair:
                print("models to send remind repair")
                self.send_data_to_channels(models_to_send_remind_planned_repair,organization_id)
            

            # Get planned repairs
            
            planned_repair =  self.get_planned_repairs(formatted_date, formatted_time , organization_id)
            serializer = PlanifierRepairSerializerForWebSockets(planned_repair, many=True)
            models_to_send_planned_repair = serializer.data
            #print(models_to_send_planned_repair)
            if models_to_send_planned_repair:
                self.send_data_to_channels(models_to_send_planned_repair, organization_id)

            # Get planned maintenance
            planned_maintenance = self.get_planned_maintenance(formatted_date, formatted_time , organization_id)
            serializer = PlanifierMaintenanceForWebSockets(planned_maintenance, many=True)
            models_to_send_planned_maintenance = serializer.data
            #print(models_to_send_planned_maintenance)
            if models_to_send_planned_maintenance:
                self.send_data_to_channels(models_to_send_planned_maintenance,organization_id)


            # FOR PLANNED TEAM 
            planned_team_every_day =  self.get_planned_team_every_day(day_of_week, formatted_time,organization_id)
            planned_team_every_day_1 =  self.get_planned_team_every_day_1(day_of_week,formatted_date,formatted_time,organization_id)
            planned_team_every_day_2 =  self.get_planned_team_every_day_2(formatted_datetime,organization_id)
            serializer = PlanifierTeamForWebSockets(planned_team_every_day, many=True)
            serializer_1 = PlanifierTeamForWebSockets(planned_team_every_day_1, many=True)
            serializer_2 = PlanifierTeamForWebSockets(planned_team_every_day_2, many=True)
            models_to_send_planned_team_every_day = serializer.data
            models_to_send_planned_team_every_day_1 = serializer_1.data
            models_to_send_planned_team_every_day_2 = serializer_2.data

            #print(models_to_send_planned_team_every_day)
            #print(models_to_send_planned_team_every_day_1)
            #print(models_to_send_planned_team_every_day_2)

            # Send the models to the group
            if models_to_send_planned_team_every_day:
                print("models to send remind team everyday")
                self.send_data_to_channels(models_to_send_planned_team_every_day, organization_id)
            # Send the models to the group
            if models_to_send_planned_team_every_day_1:
                print("models to send remind team date")
                self.send_data_to_channels(models_to_send_planned_team_every_day_1, organization_id)
            if models_to_send_planned_team_every_day_2:
                print("models to send remind team date")
                self.send_data_to_channels(models_to_send_planned_team_every_day_2, organization_id)
        except Exception as e:
            print(f"Error fetching data remind: {e}")

    
    def get_reminders(self, formatted_datetime: str,organisation):
        # Get reminders
        remind = Remind.objects.filter(datetime_remind__icontains=formatted_datetime,entreprise__id=organisation)
        return remind
    
    def get_remind_repair(self,formatted_datetime:str,organisation):
        remind = RemindRepair.objects.filter(datetime_remind__icontains=formatted_datetime,entreprise__id=organisation)
        return remind 
    
    def get_planned_repairs(self, formatted_date: str, formatted_time: str,organisation):
        # Get planned repairs
        planned_repair = PlanifierRepair.objects.filter(date_of_taking_action__icontains=formatted_date, time_of_taking_action__icontains=formatted_time,entreprise__id=organisation)
        return planned_repair
    
    def get_planned_maintenance(self, formatted_date: str, formatted_time: str,organisation):
        # Get planned maintenance
        planned_maintenance = PlanifierMaintenance.objects.filter(date_of_taking_action__icontains=formatted_date, time_of_taking_action__icontains=formatted_time,entreprise__id=organisation)
        return planned_maintenance
    
    def get_planned_team_every_day(self, day_of_week: int, formatted_time: str,organisation : str):
        # Get planned team
        planned_team_every_day = PlanifierTeam.objects.filter(day=day_of_week, time_of_taking_action__icontains=formatted_time,entreprise__id=organisation)
        return planned_team_every_day
    
    def get_planned_team_every_day_1(self, day_of_week: int, formatted_date: str,formatted_time: str,organisation : str):
        # Get planned team
        planned_team_every_day = PlanifierTeam.objects.filter(day='1000',date_of_taking_action__icontains=formatted_date,time_of_taking_action__icontains=formatted_time,entreprise__id=organisation)
        return planned_team_every_day
    
    def get_planned_team_every_day_2(self, formatted_datetime: str, organisation : str):
        # Get planned team
        planned_team_every_day = RemindTeam.objects.filter(datetime_remind__icontains=formatted_datetime,entreprise__id=organisation)
        return planned_team_every_day
    

 
