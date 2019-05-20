from tarefa import views
from django.urls import path
app_name = 'tarefa'

urlpatterns = [
    path('dispositivo_add', views.add_dispositivo, name='add_dispositivo'),

    path('<int:mqtt_id>/add_dispositivos', views.add_dispositivos, name='add_dispositivos'),
    path('add_dispositivo', views.add_dispositivo, name='add_dispositivo'),
    path('<int:dispo_id>/edit_dispositivo', views.edit_dispositivo, name='edit_dispositivo'),
    path('<int:proxy_id>/load_dispositivo', views.load_dispositivo, name='load_dispositivo'),

    path('<int:pk>/delete_dispositivo', views.ViewDeleteDispo.as_view(), name='delete_dispositivo'),

    path('<int:pk>/job', views.index, name='job'),

    path('ajax/load-mqtts/', views.load_mqtt, name='ajax_load_mqtts'),
    path('ajax/<int:dispo_id>/post_task', views.post_task, name='ajax_post_task'),
    path('ajax/<int:pk>/get_xml', views.get_xml, name='ajax_get_xml'),
    path('ajax/<int:dispo_id>/load_dado', views.load_dado, name='load_dado'),
    path('ajax/<int:proxy_pk>/load_dado_tab', views.TesteTabela.as_view(), name='load_dado_tab'),
    path('ajax/<int:dispo_id>/load_dado_graph', views.load_dado_graph, name='load_dado_graph'),
]