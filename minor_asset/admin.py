from django.contrib import admin
from .models import *

admin.site.register(Machine)
admin.site.register(Adresse)
admin.site.register(Agent)
admin.site.register(Client)
admin.site.register(Provider)
admin.site.register(Location)
admin.site.register(CategoryInventory)
admin.site.register(Inventory)
admin.site.register(InventoryInto)
admin.site.register(InventoryOut)
admin.site.register(Team)
# Register your models here.
