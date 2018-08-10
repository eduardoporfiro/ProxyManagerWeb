from django.contrib import admin
from block.models import Broker, Mqtt, Dado
from solo.admin import SingletonModelAdmin
admin.site.register(Broker, SingletonModelAdmin)
admin.site.register(Mqtt)
admin.site.register(Dado)