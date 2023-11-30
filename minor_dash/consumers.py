import time
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from minor_dash.bussiness import Domain
import json
from minor_asset.models import InventoryInto
from minor_asset.serializers import InventorySerializerForWebSockets
from channels.db import database_sync_to_async

class OneConsumer(AsyncWebsocketConsumer):
    def connect(self):
        self.accept()
        for i in range(100):
            self.send(json.dumps({"message":"mike"}))
            time.sleep(2)

class NotificationConsumer(AsyncWebsocketConsumer):
  async def connect(self):
      await self.channel_layer.group_add("Notification", self.channel_name) # nom du groupe
      # Accept the connection
      await self.accept() # code qui accepte la connection.
      # Fetch data from the InventoryInto database
      available_inventory = await self.get_data_in_database_of_invnetory_into()
      # Add the connection to the group
      if available_inventory :
        print(available_inventory)
        print("unavailable hum")
        # Send the fetched data as a message
        compt = 2000000
        for i in range(0,compt):
            if i == compt:
                await self.send(text_data=json.dumps({
                    'message': available_inventory 
                }))
                break 
  @database_sync_to_async
  def get_data_in_database_of_invnetory_into(self):
        inventory_data = InventoryInto.objects.all()
        serializer = InventorySerializerForWebSockets(inventory_data,many=True)
        available_inventory = [item for item in serializer.data if item["etat"] == "unavailable"]
        
        return available_inventory

  async def disconnect(self, close_code):
      await self.channel_layer.group_discard("Notification", self.channel_name)# nom du groupe a change 
      '''await self.send(text_data=json.dumps({
          'message': 'You are now disconnected.'
      }))'''

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


 
           