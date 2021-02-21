import jungle.stats.generate.generate_match_data as generate
from riotwrapper import LeagueApi
from django.core.management.base import BaseCommand, CommandError
import dotenv
import os


class Command(BaseCommand):
    help = 'Downloads diamond games'

    def handle(self, *args, **options):
        dotenv.load_dotenv()
        token = os.environ['RIOT-API-TOKEN']
        api = LeagueApi(token, "NA1")

        for division in ("I", "II", "III", "IV"):
            generate.download_tier_matches(api, "DIAMOND", division)
