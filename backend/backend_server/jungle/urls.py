from django.urls import path

from . import views

urlpatterns = [
    path('dragon-gold-diff/<summoner_name>/', views.dragon_gold_diff),
]