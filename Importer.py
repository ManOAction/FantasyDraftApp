import pandas as pd
from app import db
from app.models import Player

print("Loading sheet to dataframe.")
df = pd.read_csv("""G:/My Drive/Repos/FantasyDraftApp/DraftApp_DataSet.csv""")

# print(df)

ImportDF = pd.DataFrame()

ImportDF['PlayerName'] = df['Player']
ImportDF['DraftRank'] = df['Rank']
ImportDF['DraftTier'] = df['Tiers']
ImportDF['Team'] = df['Team']
ImportDF['Position'] = df['Position']
ImportDF['PointProjection'] = df['Points']

# print(ImportDF)

for row in ImportDF.itertuples():

        if str(ImportDF['PlayerName']) != 'NaN':
                
                PlayerName = row[1]
                DraftRank = row[2]
                DraftTier = row[3]
                Team = row[4]
                Position = row[5]
                Points = row[6]
                p = Player(playername=PlayerName, 
                           position=Position,
                           team=Team, 
                           tier=DraftTier, 
                           draftrank=DraftRank, 
                           pointprojection=Points
                           )
                db.session.add(p)
                db.session.commit()


print('We\'re done here.')