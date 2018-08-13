from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='core/home.html'), name='home'),
    path('admin/', admin.site.urls),
    path('block/', include('block.urls')),
    path('accounts/', include('core.urls')),
    path('accounts/', include('allauth.urls'))
]
