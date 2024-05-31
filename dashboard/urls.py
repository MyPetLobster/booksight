
from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('vision/', views.vision, name='vision'),
    path('tips/', views.tips, name='tips'),
    path('vision_status/', views.vision_status, name='vision_status'),
    path('vision_complete/', views.vision_complete, name='vision_complete'),
    path('vision_failed/', views.vision_failed, name='vision_failed')
]