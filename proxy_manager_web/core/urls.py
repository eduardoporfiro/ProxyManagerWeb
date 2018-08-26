from django.urls import include, path
from django.contrib import admin
from . import views

admin.autodiscover()
app_name='core'
urlpatterns =[
    path('', views.home, name='home'),
]