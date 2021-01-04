import requests
import time


class LeagueApi:
    """Very simple League API wrapper"""

    def __init__(self, token, region):
        self.token = token
        self.region = region
        self.domain = self.domain_from_region(region)
        self.session = requests.Session()

    def domain_from_region(self, region):
        domains = {
            "BR1":  "br1.api.riotgames.com",
            "EUN1": "eun1.api.riotgames.com",
            "EUW1": "euw1.api.riotgames.com",
            "JP1":  "jp1.api.riotgames.com",
            "KR":   "kr.api.riotgames.com",
            "LA1":  "la1.api.riotgames.com",
            "LA2":  "la2.api.riotgames.com",
            "NA1":  "na1.api.riotgames.com",
            "OC1":  "oc1.api.riotgames.com",
            "TR1":  "tr1.api.riotgames.com",
            "RU":   "ru.api.riotgames.com"
        }
        return f'https://' + domains[region]

    def get_league_entries(self, queue, tier, division, page=None):
        endpoint = "/lol/league-exp/v4/entries/{queue}/{tier}/{division}"
        uri = self.domain + endpoint.format(queue=queue, tier=tier, division=division)

        return self.make_request(uri, page=page)

    def get_summoner_by_account_id(self, account_id):
        """Get a summoner by account id"""
        endpoint = "/lol/summoner/v4/summoners/by-account/{encryptedAccountId}"
        uri = self.domain + endpoint.format(encryptedAccountId=account_id)

        return self.make_request(uri)

    def get_summoner_by_name(self, summoner_name):
        """Get a summoner by summoner name"""
        endpoint = "/lol/summoner/v4/summoners/by-name/{summonerName}"
        uri = self.domain + endpoint.format(summonerName=summoner_name)

        return self.make_request(uri)

    def get_summoner_by_puuid(self, puuid):
        """Get a summoner by puuid"""
        endpoint = "/lol/summoner/v4/summoners/by-puuid/{encryptedPUUID}"
        uri = self.domain + endpoint.format(encryptedPUUID=puuid)

        return self.make_request(uri)

    def get_match_by_match_id(self, match_id):
        """Get match by match id"""
        endpoint = "/lol/match/v4/matches/{matchId}"
        uri = self.domain + endpoint.format(matchId=match_id)

        return self.make_request(uri)

    def get_matchlist_by_account_id(self, account_id, **params):
        endpoint = "/lol/match/v4/matchlists/by-account/{encryptedAccountId}"
        uri = self.domain + endpoint.format(encryptedAccountId=account_id)

        return self.make_request(uri, **params)

    def get_timeline_by_match_id(self, match_id):
        endpoint = "/lol/match/v4/timelines/by-match/{matchId}"
        uri = self.domain + endpoint.format(matchId=match_id)

        return self.make_request(uri)

    def make_request(self, uri, **params):
        """Send a get request to Riot's API

        If a 429 response is received, wait before retrying the request.
        Any other non-200 status codes will raise an exception."""
        token = {"X-Riot-Token": self.token}
        response = self.session.get(uri, params=params, headers=token)

        if response.status_code == 429:
            retry_after = int(response.headers["Retry-After"])
            time.sleep(retry_after)
            return self.make_request(uri, **params)

        elif response.status_code == 504:
            # If a 504 response is received, immediately resend a request.
            return self.make_request(uri, **params)

        else:
            response.raise_for_status()

        return response.json()
