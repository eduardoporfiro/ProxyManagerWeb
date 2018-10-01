from django.contrib import admin
from block.models import Broker, Mqtt, Proxy
admin.site.register(Broker)
admin.site.register(Mqtt)
admin.site.register(Proxy)