import unittest
import os
from dotenv import load_dotenv
import pprint
from pathlib import Path
from ..backend_server.riotwrapper import LeagueApi

load_dotenv(dotenv_path=Path('.') / 'LeagueAPI' / 'backend' / 'backend_server' / '.env')
token = os.environ["RIOT-API-TOKEN"]
name = "BusinessJoe"
account_id = "9iSz5T3joMpnYqMWfByPLNWQqQIlJR2Qo7Baz5zvfTmxzwqvDob46vWK"
puuid = "T3zCT08y6lGi7LuKwBRykIdQMc6V4G_Bcd4k8914MT9diXVkOL87pZR0nqjXBjtfBL_7v2___m_zEw"


class TestSummonerApi(unittest.TestCase):
    def test_get_summoner_by_account_id(self):
        api = LeagueApi(token, "NA1")
        result = api.get_summoner_by_account_id(account_id)

        self.assertEqual(result["accountId"], account_id)

    def test_get_summoner_by_name(self):
        api = LeagueApi(token, "NA1")
        result = api.get_summoner_by_name(name)

        self.assertEqual(result["accountId"], account_id)

    def test_get_summoner_by_puuid(self):
        api = LeagueApi(token, "NA1")
        result = api.get_summoner_by_puuid(puuid)

        self.assertEqual(result["accountId"], account_id)


class TestMatchApi(unittest.TestCase):
    def test_get_match_from_match_id(self):
        api = LeagueApi(token, "NA1")
        match_id = api.get_matchlist_by_account_id(account_id)["matches"][0]["gameId"]
        result = api.get_match_by_match_id(match_id)

    def test_matchlist_without_params(self):
        api = LeagueApi(token, "NA1")
        result = api.get_matchlist_by_account_id(account_id)

        self.assertIn('matches', result)

    def test_matchlist_with_single_champion_id(self):
        api = LeagueApi(token, "NA1")
        result = api.get_matchlist_by_account_id(account_id, champion=161)

        # assert that multiple matches were received
        self.assertTrue(result["matches"])
        for match in result["matches"]:
            self.assertEqual(match["champion"], 161)

    def test_matchlist_with_single_queue_id(self):
        api = LeagueApi(token, "NA1")
        result = api.get_matchlist_by_account_id(account_id, queue=420)

        # assert that multiple matches were received
        self.assertTrue(result["matches"])
        for match in result["matches"]:
            self.assertEqual(match["queue"], 420)

    def test_matchlist_with_many_queue_ids(self):
        api = LeagueApi(token, "NA1")
        result = api.get_matchlist_by_account_id(account_id, queue={420, 440})

        # assert that multiple matches were received
        self.assertTrue(result["matches"])
        # check that received matches were only of queue types 420 and 440
        for match in result["matches"]:
            self.assertIn(match["queue"], {420, 440})

    def test_timeline_from_match_id(self):
        api = LeagueApi(token, "NA1")
        match_id = api.get_matchlist_by_account_id(account_id)["matches"][0]["gameId"]
        result = api.get_timeline_by_match_id(match_id)

    # def test_rate_limit_exceeded(self):
    #     api = LeagueApi(self.token, "NA1")
    #     for i in range(100):
    #         print(i)
    #         result = api.get_summoner_by_name("BusinessJoe")


class TestLeagueEntries(unittest.TestCase):
    def test_get_diamond_1(self):
        api = LeagueApi(token, "NA1")
        result = api.get_league_entries("RANKED_SOLO_5x5", "DIAMOND", "I")

        pprint.pprint(result)
