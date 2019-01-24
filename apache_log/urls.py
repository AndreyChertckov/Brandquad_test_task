from django.urls import path
from . import views


urlpatterns = [
    path('get_page/', views.get_page),
    path('get_info/', views.get_info),
    path('download_logs/', views.download_logs),
]
