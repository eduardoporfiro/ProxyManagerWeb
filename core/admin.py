from django.contrib import admin
from .models import *

admin.site.register(Celery)
admin.site.site_title = 'Proxy Manager Web'
admin.site.site_header = 'Proxy Manager Web'
admin.site.index_title = 'Administração do ProxyManager Web'