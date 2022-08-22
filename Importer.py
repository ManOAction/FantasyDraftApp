import pandas as pd
from app import db
from app.models import Player

print("Loading sheet to dataframe.")
df = pd.read_csv("""C:/Users/jacob/Downloads/FantasyPros_Fantasy_Football_Projections_QB.csv""")

# print(df)

ImportDF = pd.DataFrame()

ImportDF['PlayerName'] = df['Player']
ImportDF['ProjPoints'] = df['FPTS']

print(ImportDF)

for row in ImportDF.itertuples():

        if str(ImportDF['PlayerName']) != 'NaN':
                
                PlayerName = row[1]
                ProjPoints = row[2]
                p = Player(playername=PlayerName, pointprojection=ProjPoints)
                db.session.add(p)
                db.session.commit()


print('We\'re done here.')