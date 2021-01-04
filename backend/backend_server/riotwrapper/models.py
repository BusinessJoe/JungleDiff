from djongo import models


class Match(models.Model):
    gameId = models.BigIntegerField()

    class Meta:
        abstract = True


class Summoner(models.Model):
    accountId = models.CharField(max_length=56)
    profileIconId = models.IntegerField()
    revisionDate = models.BigIntegerField()
    name = models.CharField(max_length=120)
    summonerId = models.CharField(max_length=63)
    puuid = models.CharField(max_length=78)
    summonerLevel = models.BigIntegerField()

    matches = models.ArrayField(
        model_container=Match
    )

    def __str__(self):
        return self.name
