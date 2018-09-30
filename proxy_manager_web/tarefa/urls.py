from tarefa import views
from django.urls import path
app_name = 'tarefa'

urlpatterns = [
    path('dispositivo_add', views.add_dispositivo, name='add_dispositivo'),

    path('<int:mqtt_id>/add_dispositivo', views.add_dispositivo, name='add_dispositivo'),
    path('add_dispositivo', views.add_dispositivo, name='add_dispositivo'),
    path('<int:dispo_id>/edit_dispositivo', views.edit_dispositivo, name='edit_dispositivo'),
    path('<int:proxy_id>/load_dispositivo', views.load_dispositivo, name='load_dispositivo'),

    path('ajax/load-mqtts/', views.load_mqtt, name='ajax_load_mqtts'),
    path('', views.index, name='index'),
]