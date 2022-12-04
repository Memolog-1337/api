from django.contrib import admin
from django.urls import path

from .views import get_eccn

urlpatterns = [
    path('eccn/<str:partnumber>', get_eccn, name='get_eccn'),
    path('admin/', admin.site.urls),
]
