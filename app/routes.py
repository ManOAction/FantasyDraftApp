from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from app.models import Player, DraftStatus
from app import db
from sqlalchemy.sql import text


@app.route('/')
@app.route('/index')
def index():    
    
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/players')
def players():    
    UndraftedPlayers1 = Player.query.filter(Player.ownership_group == 0).order_by(text('draftrank asc')).limit(20)
    UndraftedPlayers2 = Player.query.filter(Player.ownership_group == 0).order_by(text('draftrank asc')).offset(20).limit(20)
    DraftedPlayers = Player.query.filter(Player.ownership_group > 0).order_by(text('draft_pick desc')).limit(20)    
    # PlayersTeam1 = Player.query.filter(Player.ownership_group == 1).limit(15).all()
    # PlayersTeam2 = Player.query.filter(Player.ownership_group == 2).limit(15).all()
    # PlayersTeam3 = Player.query.filter(Player.ownership_group == 3).limit(15).all()
    # PlayersTeam4 = Player.query.filter(Player.ownership_group == 4).limit(15).all()    

    CurrentDraftStatus = DraftStatus.query.filter(DraftStatus.id == 1).first()

    QBVorp = CurrentDraftStatus.PosVorp('QB')
    RBVorp = CurrentDraftStatus.PosVorp('RB')
    WRVorp = CurrentDraftStatus.PosVorp('WR')
    TEVorp = CurrentDraftStatus.PosVorp('TE')
    
    return render_template('players.html',
                           title='Players',                           
                           UndraftedPlayers1=UndraftedPlayers1,
                           UndraftedPlayers2=UndraftedPlayers2,
                           DraftedPlayers=DraftedPlayers,
                           DraftStatus=CurrentDraftStatus,
                           QBVorp = QBVorp,
                           RBVorp = RBVorp,
                           WRVorp = WRVorp,
                           TEVorp = TEVorp
                        #    PlayersTeam1=PlayersTeam1,
                        #    PlayersTeam2=PlayersTeam2,
                        #    PlayersTeam3=PlayersTeam3,
                        #    PlayersTeam4=PlayersTeam4
                          )

@app.route('/updateplayerownership/<int:PlayerID>', methods=['GET', 'POST'])
def updateplayerownership(PlayerID):

    CurrentDraftStatus = DraftStatus.query.filter(DraftStatus.id == 1).first()
    CurrentDraftStatus.CurrentTeam
    
    RelevantPlayer = Player.query.filter(Player.id == PlayerID).first()
    
    if CurrentDraftStatus.DraftDirection == 1:
        DraftIncrement = 1

    else:
        DraftIncrement = -1

    # Hitting the top and switching directions
    if CurrentDraftStatus.DraftDirection == 1 and CurrentDraftStatus.CurrentTeam == 4:
        CurrentDraftStatus.DraftDirection = 0        
        db.session.commit()
        DraftIncrement = 0

    # Hitting the bottom and switching directions
    if CurrentDraftStatus.DraftDirection == 0 and CurrentDraftStatus.CurrentTeam == 1:
        CurrentDraftStatus.DraftDirection = 1
        db.session.commit()    
        DraftIncrement = 0

    if RelevantPlayer.ownership_group == 0:

        RelevantPlayer.ownership_group = CurrentDraftStatus.CurrentTeam
        RelevantPlayer.draft_pick = CurrentDraftStatus.CurrentDraftPick
        CurrentDraftStatus.CurrentDraftPick += 1
        db.session.commit()

        CurrentDraftStatus.CurrentTeam += DraftIncrement
        db.session.commit()        

    else:
        RelevantPlayer.ownership_group = 0
        CurrentDraftStatus.CurrentDraftPick -= 1
        db.session.commit()

    return redirect('/players')


@app.route('/resetdraft', methods=['GET', 'POST'])
def resetdraft():

    CurrentDraftStatus = DraftStatus.query.filter(DraftStatus.id == 1).first()    
    CurrentDraftStatus.CurrentTeam = 1
    CurrentDraftStatus.CurrentDraftPick = 1 
    CurrentDraftStatus.DraftDirection = 1   
    CurrentDraftStatus.TotalQB = 1
    CurrentDraftStatus.TotalRB = 2
    CurrentDraftStatus.TotalWR = 2
    CurrentDraftStatus.TotalTE = 1
    CurrentDraftStatus.TotalFLEX = 2
    CurrentDraftStatus.TotalDST = 1
    CurrentDraftStatus.TotalTeams = 18
    db.session.commit()



    Player.query.update({Player.ownership_group: 0}) 
    db.session.commit()

    return redirect('/players')