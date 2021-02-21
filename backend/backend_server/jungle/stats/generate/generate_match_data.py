from riotwrapper import LeagueApi
from jungle.models import RankedGame, RankedMatch, RankedTimeline
from requests.exceptions import HTTPError


def get_players(api: LeagueApi, tier: str, division: str, amount: int):
    players = api.get_league_entries("RANKED_SOLO_5x5", tier, division)
    return players[:amount]


def get_matchlist(api: LeagueApi, summoner_name: str, number_of_matches: int):
    summoner_data = api.get_summoner_by_name(summoner_name)
    account_id = summoner_data['accountId']
    matchlist = api.get_matchlist_by_account_id(account_id, queue=420)
    return matchlist['matches'][:number_of_matches]


def save_matches(api: LeagueApi, matches, tier: str, division: str):
    for match in matches:
        game_id = match['gameId']

        match_data = api.get_match_by_match_id(game_id)
        timeline_data = api.get_timeline_by_match_id(game_id)

        game = RankedGame(tier=tier, division=division, gameId=game_id)
        match = RankedMatch(data=match_data, game=game)
        timeline = RankedTimeline(data=timeline_data, game=game)

        game.save()
        match.save()
        timeline.save()


def delete_games():
    RankedGame.objects.all().delete()


def download_tier_matches(api: LeagueApi, tier: str, division: str):
    print(f'{tier} {division}:')

    players = get_players(api, tier, division, 100)
    for idx, player in enumerate(players, start=1):
        summoner_name = player['summonerName']
        try:
            print(f'Summoner {idx}/{len(players)}: {summoner_name}')

            matches = get_matchlist(api, summoner_name, 10)
            save_matches(api, matches, tier, division)
        except HTTPError as e:
            print(f'Encountered exception for summoner {summoner_name}')
            print(e)
