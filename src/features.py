from elosports.elo import Elo
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np

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

# Preprocess the data
# Task: Finish modifying preprocessing
def preprocess(data: dict) -> dict:
    print(f"data: {data}")
    # Label encode the categorical features (away, home)
    team_cols = ['home_team', 'away_team']
    # Combine all columns to find every unique team name
    all_unique_teams = pd.concat([data[col] for col in team_cols]).unique()

    # fit the encoder once in the entire list of unique teams
    le = LabelEncoder()
    le.fit(all_unique_teams)

    data['away_encode'] = le.transform(data['away'])
    data['home_encode'] = le.transform(data['home'])
    data['winning_team_encode'] = le.transform(data['winning_team'])
    data['home_win'] = (data['winning_team'] == data['home']).astype(int)

    return data