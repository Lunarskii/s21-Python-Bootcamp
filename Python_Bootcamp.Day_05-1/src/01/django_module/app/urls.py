from django.urls import path
from . import views


app_name = 'app'
urlpatterns = [
    path('', views.index, name='audio_list'),
    path('add/', views.add_audio, name='add_audio'),
]
