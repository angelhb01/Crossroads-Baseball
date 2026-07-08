from elosports.elo import Elo
from fastapi import File
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Add Elo Ratings to every game
def elo_ratings(file: File):
    df = pd.read_csv(file)
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
    
    return preprocess(df)

# Preprocess the data
def preprocess(df):
    # Convert datetime to a numerical format
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day

    # Label encode the categorical features (away, home, winning_team)
    team_cols = ['home', 'away', 'winning_team']
    # Combine all columns to find every unique team name
    all_unique_teams = pd.concat([df[col] for col in team_cols]).unique()

    # fit the encoder once in the entire list of unique teams
    le = LabelEncoder()
    le.fit(all_unique_teams)

    df['away_encode'] = le.transform(df['away'])
    df['home_encode'] = le.transform(df['home'])
    df['winning_team_encode'] = le.transform(df['winning_team'])
    df['home_win'] = (df['winning_team'] == df['home']).astype(int)

    return df