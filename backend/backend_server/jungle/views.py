from dataclasses import asdict

from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseBadRequest, HttpResponseNotAllowed
from riotwrapper.graph import Graph


def summoner_matches(request):
    if request.method == 'POST':
        if 'summoner_name' in request.POST:
            summoner_name = request.POST['summoner_name']
            print(summoner_name)
            # Download match history
            return HttpResponse()
        else:
            return HttpResponseBadRequest('Expected key `summoner_name`')
    return HttpResponseNotAllowed(['POST'])


def dragon_gold_diff(request, summoner_name):
    graph = Graph(0, 0, 10, 10, [(1, 1), (2, 2), (3, 1)])
    return JsonResponse(asdict(graph))
