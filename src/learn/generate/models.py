import pymongo
import roleml
import matplotlib.pyplot as plt
import sklearn
import numpy as np
from scipy.special import expit
from joblib import dump, load

from src.api import LeagueApi



def find_gold_diff_and_dragon(match, timeline):
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

def gold_diffs_and_dragons_from_database():
    """Calculate the gold difference in botlane at 10 minutes and if the first dragon was taken"""
    gold_diffs = []
    first_dragons = []

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["match-info"]

    match_col = mydb["matches"]
    timeline_col = mydb["timelines"]

    matches = [m['match'] for m in match_col.find()]
    timelines = [t['timeline'] for t in timeline_col.find()]

    for m, t in zip(matches, timelines):
        result = find_gold_diff_and_dragon(m, t)
        if result:
            gold_diffs.append(result[0][0])
            gold_diffs.append(result[1][0])
            first_dragons.append(result[0][1])
            first_dragons.append(result[1][1])

    return gold_diffs, first_dragons


def train_gold_diff_dragon_model():
    """Train and save a logistic model on match data stored in the database"""
    gold_diffs, first_dragons = gold_diffs_and_dragons_from_database()

    clf = sklearn.linear_model.LogisticRegression(C=1e5, solver='liblinear')
    clf.fit(np.reshape(gold_diffs, (-1, 1)), first_dragons)

    dump(clf, 'models/gold_diff_dragon.joblib')


def plot_gold_diff_dragon_model():
    gold_diffs, first_dragons = gold_diffs_and_dragons_from_database()
    plt.scatter(gold_diffs, first_dragons)

    clf = load('models/gold_diff_dragon.joblib')

    X_test = np.linspace(-600, 600, 50)
    loss = expit(X_test * clf.coef_ + clf.intercept_).ravel()
    plt.plot(X_test, loss, color='red', linewidth=3)
    plt.show()


def predict_model_for_summoner(token, name, region):
    """Create a logistic model for the summoner's last 30 ranked games"""
    api = LeagueApi(token, region)
    summoner = api.get_summoner_by_name(name)
    matchlist = api.get_matchlist_by_account_id(summoner['accountId'], queue=420)

    gold_diffs = []
    first_dragons = []
    print(len(matchlist['matches']))
    for idx, brief_match in enumerate(matchlist['matches'][:30]):
        print(f'match {idx} of 30')
        game_id = brief_match['gameId']
        match = api.get_match_by_match_id(game_id)
        timeline = api.get_timeline_by_match_id(game_id)

        # find summoner's team
        for indentity in match['participantIdentities']:
            if indentity['player']['accountId'] == summoner['accountId']:
                participant_id = indentity['participantId']
        for participant in match['participants']:
            if participant['participantId'] == participant_id:
                team_id = participant['teamId']

        result = find_gold_diff_and_dragon(match, timeline)
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
    return clf


if __name__ == '__main__':
    import os
    token = os.getenv("riot-api-token")
    if token is None:
        exit()

    summoner_name = "trolljames"
    clf = predict_model_for_summoner(token, summoner_name, "NA1")
    clf2 = load('models/gold_diff_dragon.joblib')

    X_test = np.linspace(-600, 600, 50)

    loss = expit(X_test * clf.coef_ + clf.intercept_).ravel()
    plt.plot(X_test, loss, color='red', linewidth=3, label=summoner_name)
    loss2 = expit(X_test * clf2.coef_ + clf2.intercept_).ravel()
    plt.plot(X_test, loss2, color='blue', linewidth=3, label='Average diamond game')
    plt.legend()

    plt.show()
