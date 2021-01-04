from django.urls import path

from . import views

urlpatterns = [
    path('summoner/', views.summoner_matches),
    path('graphs/dragon-gold-diff/<summoner_name>/', views.dragon_gold_diff),
]