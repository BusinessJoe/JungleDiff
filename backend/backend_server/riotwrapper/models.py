from django.db import models


class Summoner(models.Model):
    accountId = models.CharField(max_length=56)
    profileIconId = models.IntegerField()
    revisionDate = models.BigIntegerField()
    name = models.CharField(max_length=120)
    summonerId = models.CharField(max_length=63)
    puuid = models.CharField(max_length=78)
    summonerLevel = models.BigIntegerField()

    def __str__(self):
        return self.name


class Match(models.Model):
    gameId = models.BigIntegerField()
    data = models.JSONField()
    summoner = models.ForeignKey(
        Summoner,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.gameId)


class Timeline(models.Model):
    data = models.JSONField()
    summoner = models.ForeignKey(
        Summoner,
        on_delete=models.CASCADE
    )