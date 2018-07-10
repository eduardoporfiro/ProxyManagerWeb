from block import views
from django.urls import path, include
app_name = 'block'

urlpatterns = [
    path('', views.index, name='index')
]