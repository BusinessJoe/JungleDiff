from django.urls import path

from . import views

urlpatterns = [
    path('summoner/', views.update_summoner),
    # path('summoner/<account_id>/', views.get_summoner_data),
    path('summoner/<summoner_name>/graph/dragon-gold-diff/', views.dragon_gold_diff_view),
    path('comparison/graph/dragon-gold-diff/', views.comparison_dragon_gold_diff_view)
]