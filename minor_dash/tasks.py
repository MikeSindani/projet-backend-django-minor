from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery import shared_task
from datetime import datetime, timedelta
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from minor_asset.models import Remind,RemindRepair
from django.shortcuts import get_list_or_404
from minor_asset.serializers import RemindSerializerForWebSockets


'''@app.task
def add(x, y):
    z = x + y
    print(z)'''
def send_data_to_channels(models_to_send):
        print('channel')
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'Notification',
            {
                'type': 'send_data',
                'message': models_to_send,
            } )

@shared_task
def verify_and_send_data():
    

    # Get the current date and time
    current_datetime = datetime.now()

    # Format the datetime object into a string
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M")

    print(formatted_datetime)

    # Get the list of Remind objects and serialize them
    remind = Remind.objects.filter(datetime_remind__icontains=formatted_datetime)
    serializer = RemindSerializerForWebSockets(remind, many=True)
    models_to_send = serializer.data

    print(models_to_send)

    # Send the models to the group
    if models_to_send:
        print("models to send")
        send_data_to_channels(models_to_send)


    remind_repair = RemindRepair.objects.filter(datetime_remind__icontains=formatted_datetime)
    serializer = RemindSerializerForWebSockets(remind_repair, many=True)
    models_to_send_remind_planned_repair = serializer.data

    print(models_to_send_remind_planned_repair)

    # Send the models to the group
    if models_to_send_remind_planned_repair:
        print("models to send remind repair")
        send_data_to_channels(models_to_send_remind_planned_repair)

    
       
'''
@shared_task
def verify_and_send_data():
       channel_layer = get_channel_layer()
       async_to_sync(channel_layer.group_send)(
           'my_group',
           {
               'type': 'send_data',
               'message': f"mike {datetime.now()}",
           }
       )'''


'''
@app.task
def add(x, y):
   print(datetime.now())
   return x + y
# Planifier la tâche pour une heure spécifique.
eta = datetime.now() + timedelta(hours=1)
result = add.apply_async((4, 4), eta=eta)
print(result)
'''


