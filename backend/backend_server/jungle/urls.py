from django.urls import path

from . import views

urlpatterns = [
    path('test/', views.update_summoner),
    path('summoner/', views.update_summoner),
    path('graphs/dragon-gold-diff/<summoner_name>/', views.dragon_gold_diff),
]