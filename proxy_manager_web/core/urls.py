from django.urls import include, path
from django.contrib import admin
from . import views

admin.autodiscover()

urlpatterns =[
    path('', views.home, name='core.home'),
]