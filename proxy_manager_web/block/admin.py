from django.contrib import admin
from block.models import Broker, Mqtt, Dado, Relation, Proxy
from solo.admin import SingletonModelAdmin
admin.site.register(Broker, SingletonModelAdmin)
admin.site.register(Mqtt)
admin.site.register(Dado)
admin.site.register(Proxy)
admin.site.register(Relation)