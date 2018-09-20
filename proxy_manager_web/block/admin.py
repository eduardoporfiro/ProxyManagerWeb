from django.contrib import admin
from block.models import Broker, Mqtt, Dado, Proxy
admin.site.register(Broker)
admin.site.register(Mqtt)
admin.site.register(Dado)
admin.site.register(Proxy)