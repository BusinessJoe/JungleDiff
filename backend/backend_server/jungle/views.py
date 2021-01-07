from dataclasses import asdict
import os
import json

from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from requests.exceptions import HTTPError

from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseNotFound
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from riotwrapper.graph import Graph
from riotwrapper.models import Summoner, Match, Timeline
from riotwrapper.api import LeagueApi


@api_view(['POST'])
@csrf_exempt
def update_summoner(request):
    if request.method == 'POST':
        try:
            summoner_name = request.data['summoner_name']
            num_matches = request.data.get('matches', 5)
            num_matches = min(int(num_matches), 5)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                num_new_matches = save_summoner_match_history(summoner_name, num_matches)
            except HTTPError as err:
                if err.response.status_code == 404:
                    print('got 404')
                    return Response(status=status.HTTP_404_NOT_FOUND)
                raise
            else:
                return Response(
                    {
                        "summoner_name": summoner_name,
                        "matches": num_new_matches,
                        "Location": f'{request.build_absolute_uri()}{summoner_name}/'
                    },
                    status=status.HTTP_201_CREATED,
                )


def save_summoner_match_history(summoner_name, num_matches) -> int:
    """Save the summoner's most recent ranked solo games to the database.

    Returns the new number of matches saved for the summoner.
    """
    api = LeagueApi(os.environ['RIOT-API-TOKEN'], 'NA1')
    summoner_dict = api.get_summoner_by_name(summoner_name)

    summoner_dict['summonerId'] = summoner_dict['id']
    del summoner_dict['id']

    # Update existing summoner entry if it exists, otherwise create a new one
    try:
        s = Summoner.objects.get(accountId=summoner_dict['accountId'])
        for (key, value) in summoner_dict.items():
            setattr(s, key, value)
        s.save()
        print('updated')
    except ObjectDoesNotExist:
        s = Summoner(**summoner_dict)
        print('created')
    s.save()

    try:
        match_list = api.get_matchlist_by_account_id(s.accountId, queue={420})
        match_list = match_list['matches']
    except HTTPError as err:
        # If there are no matches a 404 error is raised
        if err.response.status_code == 404:
            match_list = []
        else:
            raise

    existing_matches = Match.objects.filter(summoner=s)
    existing_match_ids = {m.gameId for m in existing_matches}
    new_match_ids = {m['gameId'] for m in match_list[:num_matches]}

    # Preexisting matches that aren't present in the new match list should be deleted
    to_delete = existing_match_ids - new_match_ids
    # Matches that don't already exist should be acquired from Riot's api
    to_create = new_match_ids - existing_match_ids

    Match.objects.filter(gameId__in=to_delete).delete()
    Timeline.objects.filter(gameId__in=to_delete).delete()

    # Request new matches from Riot
    for game_id in to_create:
        match_dict = api.get_match_by_match_id(game_id)
        match = Match(gameId=game_id, data=match_dict, summoner=s)
        match.save()

        timeline_dict = api.get_timeline_by_match_id(game_id)
        timeline = Timeline(gameId=game_id, data=timeline_dict, summoner=s)
        timeline.save()

    print(f'deleted {len(to_delete)} matches')
    print(f'created {len(to_create)} matches')
    return min(len(match_list), num_matches)


def dragon_gold_diff(request, summoner_name):
    graph = Graph(0, 0, 10, 10, [(1, 1), (2, 2), (3, 1)])
    return JsonResponse(asdict(graph))
