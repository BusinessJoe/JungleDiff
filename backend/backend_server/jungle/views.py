from dataclasses import asdict
import os
import json
from requests.exceptions import HTTPError

from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseNotFound
from riotwrapper.graph import Graph

from riotwrapper.models import Summoner, Match, Timeline
from riotwrapper.api import LeagueApi


def summoner_matches(request):
    if request.method == 'POST':
        # Received data is not part of a form so request.body must be used instead of request.POST
        body = json.loads(request.body.decode('utf-8'))
        try:
            summoner_name = body['summoner_name']
        except KeyError:
            return HttpResponseBadRequest('Expected key `summoner_name`')
        else:
            api = LeagueApi(os.environ['RIOT-API-TOKEN'], 'NA1')
            try:
                summoner_dict = api.get_summoner_by_name(summoner_name)
            except HTTPError as err:
                if err.response.status_code == 404:
                    return HttpResponseNotFound()
                else:
                    raise

            summoner_dict['summonerId'] = summoner_dict['id']
            del summoner_dict['id']

            s = Summoner(**summoner_dict)
            s.save()

            match_list = api.get_matchlist_by_account_id(s.accountId, queue={420})
            for match_summary in match_list['matches'][:5]:
                game_id = match_summary['gameId']

                match_dict = api.get_match_by_match_id(game_id)
                match = Match(gameId=game_id, data=match_dict, summoner=s)
                match.save()

                timeline_dict = api.get_timeline_by_match_id(game_id)
                timeline = Timeline(gameId=game_id, data=timeline_dict, summoner=s)
                timeline.save()
            return HttpResponse()
    return HttpResponseNotAllowed(['POST'])


def dragon_gold_diff(request, summoner_name):
    graph = Graph(0, 0, 10, 10, [(1, 1), (2, 2), (3, 1)])
    return JsonResponse(asdict(graph))
