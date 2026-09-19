from elosports.elo import Elo
import pandas as pd
from sklearn.preprocessing import LabelEncoder


# Add elo rating features to every game
def elo_ratings(df: pd.DataFrame) -> pd.DataFrame:
    allTeams = set(df.away.tolist())
    allTeams.update(df.home.tolist())
    eloLeague = Elo(k=20)

    for team in allTeams:
        eloLeague.addPlayer(team)
    for game in df.iterrows():
        df.loc[game[0], 'away_elo_pre'] = eloLeague.ratingDict[game[1].away]
        df.loc[game[0], 'home_elo_pre'] = eloLeague.ratingDict[game[1].home]
        df.loc[game[0], 'elo_prob_away'] = eloLeague.expectResult(eloLeague.ratingDict[game[1].away], eloLeague.ratingDict[game[1].home])
        df.loc[game[0], 'elo_prob_home'] = eloLeague.expectResult(eloLeague.ratingDict[game[1].home], eloLeague.ratingDict[game[1].away])
        if game[1].away_score > game[1].home_score:
            eloLeague.gameOver(game[1].away, game[1].home, True)
        else:
            eloLeague.gameOver(game[1].home, game[1].away, 0)
        df.loc[game[0], 'away_elo_post'] = eloLeague.ratingDict[game[1].away]
        df.loc[game[0], 'home_elo_post'] = eloLeague.ratingDict[game[1].home]
    for team in eloLeague.ratingDict.keys():
        print(team, eloLeague.ratingDict[team])

    return df


# Preprocess the data for model inference.
def preprocess(data: dict) -> dict:
    data = dict(data)

    away_team = data.get('away_team')
    home_team = data.get('home_team')
    if not away_team or not home_team:
        raise ValueError('away_team and home_team are required.')

    team_list = [away_team, home_team]
    le = LabelEncoder()
    le.fit(sorted(set(team_list)))

    data['away_encode'] = int(le.transform([away_team])[0])
    data['home_encode'] = int(le.transform([home_team])[0])

    if 'winning_team' in data and data['winning_team'] is not None:
        data['winning_team_encode'] = int(le.transform([data['winning_team']])[0])
        data['home_win'] = int(data['winning_team'] == home_team)

    return data