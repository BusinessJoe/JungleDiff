from django.test import Client
from django.test import TestCase

from riotwrapper.models import Summoner, Match, Timeline
from jungle.stats import dragon_gold_diff


class SummonerPostTestCase(TestCase):
    def test_summoner_post_status_ok(self):
        c = Client()
        response = c.post('/api/summoner/', {'summoner_name': 'BusinessJoe'})
        self.assertEqual(response.status_code, 201)

    def test_summoner_post_no_name_status_400(self):
        c = Client()
        response = c.post('/api/summoner/')
        self.assertEqual(response.status_code, 400)

    def test_summoner_post_creates_database_entry(self):
        c = Client()
        response = c.post('/api/summoner/', {'summoner_name': 'BusinessJoe'})
        s = Summoner.objects.get(name='BusinessJoe')
        self.assertEqual(s.name, 'BusinessJoe')

    def test_summoner_post_saves_match(self):
        c = Client()
        response = c.post('/api/summoner/', {'summoner_name': 'BusinessJoe'})
        s = Summoner.objects.get(name='BusinessJoe')
        matches = Match.objects.filter(summoner=s)
        self.assertTrue(matches)

    def test_summoner_post_saves_timeline(self):
        c = Client()
        response = c.post('/api/summoner/', {'summoner_name': 'BusinessJoe'})
        s = Summoner.objects.get(name='BusinessJoe')
        timelines = Timeline.objects.filter(summoner=s)
        self.assertTrue(timelines)


class GraphsTestCase(TestCase):
    def test_gold_dragon_diff_model(self):
        from riotwrapper.api import LeagueApi
        from jungle.views import save_summoner_match_history
        import os
        token = os.environ["RIOT-API-TOKEN"]
        api = LeagueApi(token, "NA1")

        summoner_name = "JJamali"
        save_summoner_match_history(summoner_name, 5)
        dataset = dragon_gold_diff.dataset_for_summoner(summoner_name, api)
        self.assertTrue(dataset)

    def test_gold_dragon_diff_endpoint(self):
        from jungle.views import save_summoner_match_history
        import json

        c = Client()

        summoner_name = "JJamali"
        save_summoner_match_history(summoner_name, 5)
        response = c.get('/api/summoner/JJamali/graph/dragon-gold-diff/')
        content = response.content.decode('utf-8')
        data = json.loads(content)
        self.assertEqual(data['label'], "First Dragon Change vs. Botlane Gold Diff")
        self.assertGreater(len(data['data']), 0)
