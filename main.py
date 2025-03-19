import random
import streamlit as st
from datetime import datetime
random.seed(datetime.now().microsecond)
import pandas as pd

bracket = pd.read_csv('bracket.csv')
teams = pd.read_csv('teams.csv')

def predict(round):
    for row in bracket.loc[bracket.Round == round].itertuples():
        team1ID, team2ID = row.T1, row.T2
        team1Seed = teams[teams.TeamID == team1ID].Seed.iloc[0]
        team2Seed = teams[teams.TeamID == team2ID].Seed.iloc[0]
        prob_1 = team2Seed / (team1Seed + team2Seed)
        if random.random() < prob_1:
            bracket.loc[bracket.gID == row.gID, 'Result'] = team1ID
        else:
            bracket.loc[bracket.gID == row.gID, 'Result'] = team2ID

    
def fillRound(round):
    for row in bracket.loc[bracket.Round == round].itertuples():
        bracket.loc[bracket.gID == row.gID, "T1"] = bracket.loc[bracket.gID == row.gIDT1, "Result"].iloc[0]
        bracket.loc[bracket.gID == row.gID, "T2"] = bracket.loc[bracket.gID == row.gIDT2, "Result"].iloc[0]

def predictAll():
    predict(1)
    for i in range(2, 7):
        fillRound(i)
        predict(i)

def showBracket():    
    currentRound = 0
    for row in bracket.itertuples():
        if row.Round != currentRound:
            currentRound = row.Round
            print("#"*60)
            print(f"Round {currentRound}:")
        t1 = teams.loc[teams.TeamID == row.T1].TeamName.iloc[0]
        s1 = teams.loc[teams.TeamID == row.T1].Seed.iloc[0]
        t2 = teams.loc[teams.TeamID == row.T2].TeamName.iloc[0]
        s2 = teams.loc[teams.TeamID == row.T2].Seed.iloc[0]
        winner = teams.loc[teams.TeamID == row.Result].TeamName.iloc[0]
        winnerSeed = teams.loc[teams.TeamID == row.Result].Seed.iloc[0]
        print(f"{s1} {t1} vs {s2} {t2}")
        print(f"Winner: {winnerSeed} {winner}")
        print("-"*50)
        
def showBracketStream():
    rounds = sorted(bracket['Round'].unique())
    for r in rounds:
        st.header(f"Round {r}")
        data = []
        for row in bracket.loc[bracket.Round == r].itertuples():
            t1 = teams.loc[teams.TeamID == row.T1].TeamName.iloc[0]
            s1 = teams.loc[teams.TeamID == row.T1].Seed.iloc[0]
            t2 = teams.loc[teams.TeamID == row.T2].TeamName.iloc[0]
            s2 = teams.loc[teams.TeamID == row.T2].Seed.iloc[0]
            winner = teams.loc[teams.TeamID == row.Result].TeamName.iloc[0]
            winnerSeed = teams.loc[teams.TeamID == row.Result].Seed.iloc[0]
            data.append({
                "Team 1": f"{s1} {t1}",
                "Team 2": f"{s2} {t2}",
                "Winner": f"{winnerSeed} {winner}"
            })
        round_df = pd.DataFrame(data)
        st.table(round_df)

predictAll()

st.set_page_config(page_title="March Madness Predictions", layout="wide")

st.title("March Madness Predictions")

if st.button("Generate Random Predictions"):
    predictAll()
    showBracketStream()