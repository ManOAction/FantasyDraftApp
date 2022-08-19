from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from app.models import Player
from app import db

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Jacob'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


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
    UndraftedPlayers = Player.query.filter(Player.ownership_group == 0).all()
    DraftedPlayers = Player.query.filter(Player.ownership_group > 0).all()    
    return render_template('players.html',
                           title='Players',                           
                           UndraftedPlayers=UndraftedPlayers,
                           DraftedPlayers=DraftedPlayers
                          )

@app.route('/updateplayerownership/<int:PlayerID>', methods=['GET', 'POST'])
def updateplayerownership(PlayerID):
    RelevantPlayer = Player.query.filter(Player.id == PlayerID).first()

    if RelevantPlayer.ownership_group == 0:
        RelevantPlayer.ownership_group=1
        db.session.commit()
    else:
        RelevantPlayer.ownership_group=0
        db.session.commit()

    return redirect('/players')
