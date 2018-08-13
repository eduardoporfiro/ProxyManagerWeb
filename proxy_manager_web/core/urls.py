from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'core/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'core/home.html'}, name='logout'),
    path('signup/', views.register, name='signup'),
]