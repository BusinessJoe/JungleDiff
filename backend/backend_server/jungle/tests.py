from django.test import Client
from django.test import TestCase

from riotwrapper.models import Summoner, Match, Timeline


class SummonerPostTestCase(TestCase):
    def test_summoner_post_status_ok(self):
        c = Client()
        response = c.post('/api/summoner/', {'summoner_name': 'BusinessJoe'})
        self.assertEqual(response.status_code, 200)

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
