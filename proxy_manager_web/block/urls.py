from block import views
from django.urls import path, include
app_name = 'block'

urlpatterns = [
    path('proxy_add', views.add_proxy, name='add_proxy'),
    path('broker_add', views.add_broker, name='add_broker'),
    path('mqtt_add', views.add_mqtt, name='add_mqtt'),
    path('<int:proxy_id>/tab_edit', views.tab_edit, name='tab_edit'),
    path('<int:proxy_id>/proxy_edit', views.edit_proxy, name='edit_proxy'),
    path('<int:broker_id>/broker_edit', views.edit_broker, name='edit_broker'),
    path('<int:mqtt_id>/mqtt_edit', views.edit_mqtt, name='edit_mqtt'),

    path('<int:broker_id>/mqtt_load', views.load_mqtt, name='load_mqtt'),
    path('ajax/load-brokers/', views.load_broker, name='ajax_load_brokers')
]