from django.db import models
from riotwrapper.models import Summoner, Match, Timeline


class RankedGame(models.Model):
    tier = models.CharField(max_length=50)
    division = models.CharField(max_length=10)
    gameId = models.BigIntegerField()

    def __str__(self):
        return f'{self.tier} {self.division} ({self.gameId})'


class RankedMatch(models.Model):
    data = models.JSONField()
    game = models.OneToOneField(
        RankedGame,
        on_delete=models.CASCADE,
    )


class RankedTimeline(models.Model):
    data = models.JSONField()
    game = models.OneToOneField(
        RankedGame,
        on_delete=models.CASCADE
    )
