from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name='accounts'

urlpatterns = [
    url(r'^accounts/', include('allauth.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/home.html'), name='logout'),
    path('signup/', views.register, name='signup'),
    path('', views.dashboard, name='dashboard'),
    path('nova-senha/', views.password_reset, name='password_reset'),
    path('confirmar-nova-senha/(?P<key>\w+)/$', views.password_reset_confirm, name='password_reset_confirm'),
    path('editar/', views.edit, name='edit'),
    path('editar-senha/', views.edit_password, name='edit_password'),
]