from typing import Tuple
import os

from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction, IntegrityError
from requests.exceptions import HTTPError

from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseNotFound
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from riotwrapper.models import Summoner, Match, Timeline
from riotwrapper.api import LeagueApi
from jungle.stats import dragon_gold_diff
import utils.utils as utils


@api_view(['POST'])
@csrf_exempt
def update_summoner(request):
    if request.method == 'POST':
        try:
            summoner_name = request.data['summoner_name']
            summoner_name = utils.sanitize_name(summoner_name)
            num_matches = request.data.get('matches', 5)
            num_matches = min(int(num_matches), 5)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                num_new_matches, summoner = save_summoner_match_history(summoner_name, num_matches)
        except HTTPError as err:
            if err.response.status_code == 404:
                print('got 404')
                return Response(status=status.HTTP_404_NOT_FOUND)
            raise
        except IntegrityError:
            # Tried to make a summoner that already exists
            # another process made the summoner so it should be okay
            num_new_matches = 0

        return Response(
            {
                "summoner_name": summoner_name,
                "account_id": summoner.accountId,
                "profile_icon_id": summoner.profileIconId,
                "matches": num_new_matches,
                "Location": f'{request.build_absolute_uri()}{summoner_name}/'
            },
            status=status.HTTP_201_CREATED,
        )


def save_summoner_match_history(summoner_name, num_matches) -> Tuple[int, Summoner]:
    """Save the summoner's most recent ranked solo games to the database.

    Returns the new number of matches saved for the summoner.
    """
    api = LeagueApi(os.environ['RIOT-API-TOKEN'], 'NA1')
    summoner_dict = api.get_summoner_by_name(summoner_name)

    summoner_dict['summonerId'] = summoner_dict['id']
    del summoner_dict['id']

    # Update existing summoner entry if it exists, otherwise create a new one
    try:
        s = Summoner.objects.select_for_update().get(accountId=summoner_dict['accountId'])
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

    existing_matches = Match.objects.select_for_update().filter(summoner=s)
    existing_match_ids = {m.gameId for m in existing_matches}
    new_match_ids = {m['gameId'] for m in match_list[:num_matches]}

    # Preexisting matches that aren't present in the new match list should be deleted
    to_delete = existing_match_ids - new_match_ids
    # Matches that don't already exist should be acquired from Riot's api
    to_create = new_match_ids - existing_match_ids

    Match.objects.select_for_update().filter(gameId__in=to_delete).delete()
    Timeline.objects.select_for_update().filter(gameId__in=to_delete).delete()

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
    return min(len(match_list), num_matches), s


def match_exists(summoner, game_id) -> bool:
    try:
        Match.objects.get(summoner=summoner, gameId=game_id)
        return True
    except ObjectDoesNotExist:
        return False


def dragon_gold_diff_view(request, summoner_name):
    api = LeagueApi(os.environ['RIOT-API-TOKEN'], 'NA1')
    dataset = dragon_gold_diff.dataset_for_summoner(summoner_name, api)
    return JsonResponse(dataset)


@api_view(['GET'])
def comparison_dragon_gold_diff_view(request):
    if request.method == 'GET':
        dataset = dragon_gold_diff.comparison_dataset(1)
        return Response(dataset)
