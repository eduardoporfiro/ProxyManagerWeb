from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'accounts/login.html'}, name='accounts.login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'accounts/home.html'}, name='accounts.logout'),
    path('signup/', views.register, name='signup'),
    path('', views.dashboard, name='accounts.dashboard'),
    path('nova-senha/', views.password_reset, name='accounts.password_reset'),
    path('confirmar-nova-senha/(?P<key>\w+)/$', views.password_reset_confirm, name='accounts.password_reset_confirm'),
    path('editar/', views.edit, name='accounts.edit'),
    path('editar-senha/', views.edit_password, name='accounts.edit_password'),
]