import time
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from minor_dash.bussiness import Domain
import json

class OneConsumer(AsyncWebsocketConsumer):
    def connect(self):
        self.accept()
        for i in range(100):
            self.send(json.dumps({"message":"mike"}))
            time.sleep(2)

class NotificationConsumer(AsyncWebsocketConsumer):
  async def connect(self):
      await self.channel_layer.group_add("Notification", self.channel_name)
      await self.accept()
      ''' await self.send(text_data=json.dumps({
          'message': 'You are now connected.'
      }))'''

  async def disconnect(self, close_code):
      await self.channel_layer.group_discard("Notification", self.channel_name)
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
      print(event)
      message = event['message']
      await self.send(text_data=json.dumps({
          'message': message
      }))



 
           