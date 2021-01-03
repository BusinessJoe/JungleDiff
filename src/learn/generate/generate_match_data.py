import os
import csv
import requests
import pymongo
from pprint import pprint
from backend_server.api import LeagueApi


token = os.getenv('riot-api-token')
if token is None:
    exit(1)


def get_players(api):
    players = []

    for tier in ("I", "II", "III", "IV"):
        result = api.get_league_entries("RANKED_SOLO_5x5", "DIAMOND", tier)
        players.extend(result[:20])

    print(len(players))
    return players


def save_match_ids(api):
    players = get_players(api)
    names = [p["summonerName"] for p in players]

    account_ids = []
    for name in names:
        print(name)
        try:
            result = api.get_summoner_by_name(name)
        except requests.exceptions.HTTPError as err:
            pass

        account_ids.append(result["accountId"])

    matches = []
    for account_id in account_ids:
        result = api.get_matchlist_by_account_id(account_id, queue=420)
        matches.extend(result["matches"][:10])

    match_ids = [m["gameId"] for m in matches]
    match_ids = list(set(match_ids))

    with open('matchIds.csv', 'w', newline='') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_ALL)
        for match_id in match_ids:
            wr.writerow([match_id])

    pprint(matches)


def load_match_ids():
    with open('matchIds.csv', newline='') as f:
        reader = csv.reader(f)
        ids = list(reader)
    return [e[0] for e in ids]


def save_matches():
    api = LeagueApi(token, "NA1")

    ids = load_match_ids()

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["match-info"]

    match_col = mydb["matches"]
    timeline_col = mydb["timelines"]

    for match_id in ids:
        print(match_id)
        match = api.get_match_by_match_id(match_id)
        timeline = api.get_timeline_by_match_id(match_id)

        match_data = {'match_id': match_id, 'match': match}
        timeline_data = {'match_id': match_id, 'timeline': timeline}

        match_col.insert_one(match_data)
        timeline_col.insert_one(timeline_data)