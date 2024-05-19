
from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('vision/', views.vision, name='vision'),
    path('tips/', views.tips, name='tips')
]