import roleml
import sklearn
import numpy as np
from scipy.special import expit
from joblib import dump, load

from riotwrapper.models import Summoner, Match, Timeline
from .graph import Graph


def dataset_for_summoner(summoner_name, api):
    """Return a dataset containing graph data in the format chart.js expects"""
    clf = _predict_model_for_summoner(api, summoner_name)
    data = _quantize_logistic_model(clf)
    graph = Graph("Your games", data)
    return graph.chart_js_dataset()


def comparison_dataset(division):
    clf = load('backend/backend_server/jungle/stats/dragon_gold_diff.joblib')
    data = _quantize_logistic_model(clf)
    graph = Graph("Diamond __", data)
    return graph.chart_js_dataset()


def _find_gold_diff_and_dragon(match, timeline):
    try:
        lanes = roleml.predict(match, timeline)

        team_gold = {100: 0, 200: 0}

        # calculate total gold in each botlane
        for player in match['participants']:
            if lanes[player['participantId']] in ('bot', 'supp'):
                team_gold[player['teamId']] += player['timeline']['goldPerMinDeltas']['0-10']

        gold_diff = team_gold[100] - team_gold[200]

        first_dragon = None
        for team in match['teams']:
            if team['teamId'] == 100:
                first_dragon = team['firstDragon']

        return [[gold_diff, first_dragon], [-gold_diff, not first_dragon]]
    except roleml.exceptions.exceptions.MatchTooShort:
        pass
    except roleml.exceptions.exceptions.IncorrectMap:
        pass
    return []


def _predict_model_for_summoner(api, name):
    """Create a logistic model for the summoner's last 30 ranked games"""
    summoner_data = api.get_summoner_by_name(name)
    account_id = summoner_data['accountId']
    summoner = Summoner.objects.get(accountId=account_id)
    matches = Match.objects.filter(summoner=summoner)

    gold_diffs = []
    first_dragons = []
    for match in matches:
        game_id = match.gameId
        timeline = Timeline.objects.get(summoner=summoner, gameId=game_id)

        match = match.data
        timeline = timeline.data

        # find summoner's team
        for identity in match['participantIdentities']:
            if identity['player']['accountId'] == summoner.accountId:
                participant_id = identity['participantId']
        for participant in match['participants']:
            if participant['participantId'] == participant_id:
                team_id = participant['teamId']

        result = _find_gold_diff_and_dragon(match, timeline)
        if result:
            if team_id == 100:
                gold_diffs.append(result[0][0])
                first_dragons.append(result[0][1])
            else:
                gold_diffs.append(result[1][0])
                first_dragons.append(result[1][1])

    print("Training")

    clf = sklearn.linear_model.LogisticRegression(C=1e5, solver='liblinear')
    clf.fit(np.reshape(gold_diffs, (-1, 1)), first_dragons)
    # plt.scatter(gold_diffs, first_dragons)
    # plot_gold_diff_dragon_model(clf)
    return clf


def _quantize_logistic_model(clf):
    X = np.linspace(-600, 600, 10)
    loss = expit(X * clf.coef_ + clf.intercept_).ravel()
    return list(zip(X, loss))

