from django.contrib import admin

from .models import Space, ElectricityConsumption, Region

admin.site.register(ElectricityConsumption)
admin.site.register(Region)
admin.site.register(Space)
