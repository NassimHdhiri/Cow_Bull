from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('start_game', views.StartGame,name='start game'),  # Assuming StartGame is a view in cow_bull_app's views
    path('about_game', views.AboutGame,name='about game'),  # Assuming AboutGame is a view in cow_bull_app's views
    path('play_game', views.PlayGame,name='play game'),  # Assuming PlayGame is a view in cow_bull_app's views
]
