from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('block/', include('block.urls')),
    path('tarefa/', include('tarefa.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls'))
]
