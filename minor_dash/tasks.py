from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery import shared_task
from datetime import datetime, timedelta
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from minor_asset.models import Remind,RemindRepair,PlanifierRepair,PlanifierMaintenance,PlanifierTeam
from django.shortcuts import get_list_or_404
from minor_asset.serializers import RemindSerializerForWebSockets,RemindRepairSerializerForWebSockets,PlanifierRepairSerializerForWebSockets,PlanifierMaintenanceForWebSockets,PlanifierTeamForWebSockets


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
    formatted_date = current_datetime.strftime("%Y-%m-%d")
    formatted_time = current_datetime.strftime("%H:%M")
    day_of_week = current_datetime.weekday()
    print(formatted_datetime)
    print(formatted_date)
    print(formatted_time)
    print(day_of_week)

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
    serializer = RemindRepairSerializerForWebSockets(remind_repair, many=True)
    models_to_send_remind_planned_repair = serializer.data

    print(models_to_send_remind_planned_repair)

    # Send the models to the group
    if models_to_send_remind_planned_repair:
        print("models to send remind repair")
        send_data_to_channels(models_to_send_remind_planned_repair)
    
    planned_repair = PlanifierRepair.objects.filter(date_of_taking_action__icontains=formatted_date,time_of_taking_action__icontains=formatted_time)
    serializer = PlanifierRepairSerializerForWebSockets(planned_repair, many=True)
    models_to_send_planned_repair = serializer.data

    print(models_to_send_planned_repair)

    # Send the models to the group
    if models_to_send_planned_repair:
        print("models to send remind repair")
        send_data_to_channels(models_to_send_planned_repair)

    planned_repair = PlanifierMaintenance.objects.filter(date_of_taking_action__icontains=formatted_date,time_of_taking_action__icontains=formatted_time)
    serializer = PlanifierMaintenanceForWebSockets(planned_repair, many=True)
    models_to_send_planned_maintenance = serializer.data

    print(models_to_send_planned_maintenance)

    # Send the models to the group
    if models_to_send_planned_maintenance:
        print("models to send remind repair")
        send_data_to_channels(models_to_send_planned_maintenance)

    # FOR PLANNED TEAM 
    planned_team_every_day = PlanifierTeam.objects.filter(day=day_of_week,time_of_taking_action__icontains=formatted_time)
    planned_team_every_day_1 = PlanifierTeam.objects.filter(day='1000',date_of_taking_action__icontains=formatted_date,time_of_taking_action__icontains=formatted_time)
    serializer = PlanifierTeamForWebSockets(planned_team_every_day, many=True)
    serializer_1 = PlanifierTeamForWebSockets(planned_team_every_day_1, many=True)
    models_to_send_planned_team_every_day = serializer.data
    models_to_send_planned_team_every_day_1 = serializer_1.data

    print(models_to_send_planned_team_every_day)

    # Send the models to the group
    if models_to_send_planned_team_every_day:
        print("models to send remind team everyday")
        send_data_to_channels(models_to_send_planned_team_every_day)
    # Send the models to the group
    if models_to_send_planned_team_every_day_1:
        print("models to send remind team date")
        send_data_to_channels(models_to_send_planned_team_every_day_1)

    
       
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


