from dataclasses import asdict

from django.http import JsonResponse
from riotwrapper.graph import Graph


# Create your views here.
def dragon_gold_diff(request, summoner_name):
    graph = Graph(0, 0, 10, 10, [(1, 1), (2, 2), (3, 1)])
    return JsonResponse(asdict(graph))
