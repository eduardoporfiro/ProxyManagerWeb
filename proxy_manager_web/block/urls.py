from block import views
from django.urls import path, include
app_name = 'block'

urlpatterns = [
    path('', views.index, name='index'),
    path('proxy_add', views.add_proxy, name='add_proxy'),
    path('proxy_edit', views.edit_proxy, name='edit_proxy'),
    path('broker_add', views.add_broker, name='add_broker'),
    path('mqtt_add', views.MqttCreateView.as_view(), name='add_mqtt'),
    path('ajax/load-brokers/', views.load_broker, name='ajax_load_brokers')
]