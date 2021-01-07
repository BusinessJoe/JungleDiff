from django.urls import path

from . import views

urlpatterns = [
    path('summoner/', views.update_summoner),
    path('summoner/<summoner_name>/graph/dragon-gold-diff/', views.dragon_gold_diff_view),
]