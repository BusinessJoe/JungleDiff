from django.test import TestCase
from django.test import Client


class SummonerPostTestCase(TestCase):
    def test_summoner_post_status_ok(self):
        c = Client()
        response = c.post('/api/summoner/', {'summoner_name': 'BusinessJoe'})
        self.assertEqual(response.status_code, 200)

    def test_summoner_post_no_name_status_400(self):
        c = Client()
        response = c.post('/api/summoner/')
        self.assertEqual(response.status_code, 400)