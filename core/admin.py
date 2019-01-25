from django.contrib import admin
from .models import *

admin.site.register(Celery)
admin.site.site_title = 'Aquele Teste'
admin.site.site_header = 'outro Teste'
admin.site.index_title = 'outro Teste ao quadrado'