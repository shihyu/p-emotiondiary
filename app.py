#Packages to include
from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash
from flask.ext.sqlalchemy import SQLAlchemy
from flask_oauth import OAuth
import random, math, time, os
import sqlite3, pprint
from collections import namedtuple
#  from facepy.utils import get_extended_access_token

#Files to include (from here)
from utilities import facebook, DEBUG, SECRET_KEY, TrapErrors, Objects as O, OFFLINE, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET
from tipsData import buildTips

#Setting up Tips
Tips = buildTips()

#Setting up the Application
app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
app.config['TRAP_BAD_REQUEST_ERRORS'] = TrapErrors

#Setting path to DB depending on DEBUG setting
if DEBUG == True:
    dbURL = 'sqlite:////tmp/test.db'
    # dbURL = os.environ['DATABASE_URL']
else: 
    dbURL = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_DATABASE_URI'] = dbURL

userCache = {}

db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    authID = db.Column(db.Unicode, unique=True)
    facebookID = db.Column(db.Unicode, unique=True)
    name = db.Column(db.Unicode)
    locale = db.Column(db.Unicode)
    friendNum = db.Column(db.Integer)
    target = db.Column(db.String(10))
    points = db.Column(db.Integer)
    testscore = db.Column(db.PickleType)    ## Shall be modified
    tip = db.Column(db.PickleType)          ## Shall be modified
    crawldata = db.Column(db.PickleType)
    # dateAdded: time.time(),
    # friends: len(friends.data['data']),
    # points: 1,
    # locale: me.data['locale'],
    # target: 'control',
    # scores:{},
    # tips:{} #tip ID keys with answers as values

    # def __init__(self, authID, facebookID, name, locale):
    def __init__(self, authID, facebookID, name, locale, friendNum, target, points, testscore, tip, crawlData):
        self.authID = authID
        self.facebookID = facebookID
        self.name = name
        self.locale = locale
        self.friendNum = friendNum
        self.target = target
        self.points = points
        self.testscore = testscore
        self.tip = tip
        self.crawldata = crawlData

    def __repr__(self):
        return str(self.name) + ' ' + str(self.authID)

if DEBUG == True:
  db.drop_all()
  db.create_all()

#Routes
@app.route('/', methods=['GET', 'POST'])
def index():

    sessionID = get_facebook_oauth_token()

    #Deal with a POST request
    if request.method == 'POST':
        flash("Just a test Flash")
        return str(dir(request.form['CESDForm']))
    
    #Deal with a GET request
    else:

        #Check for user authentication
        if sessionID in userCache:
            user = userCache[sessionID]

            #Handling the base state of authenticated users
            if userCache[sessionID].points <= 2: # Original: == 1:
                # userCache[sessionID].points =  userCache[sessionID].points + 1
                return render_template('firstTime.html', user = user)
            return render_template('returningUser.html', user = user)

        #Authenticate new users
        else: return redirect(url_for('login'))
 
@app.route('/login')
def login():
    if OFFLINE: #Loading an off line test user
        sessionID = get_facebook_oauth_token()
        userCache[sessionID] =  O.User('John Smith', 'Test ID', sessionID, time.time(), 203, 1, 'ko_KR', 'control', {}, {}, ['TEMP_Data'])
        newUser = User('Debug Mode', 'TEST ID', 'John Smith', 'ko_KR', 203, 'control', 1, {}, {}, {'TEMP_crawlData'})
        db.session.add(newUser)
        db.session.commit()

        return redirect(url_for('index'))

    #If not OFFLINE:
    return facebook.authorize(callback=url_for('facebook_authorized',
    next=request.args.get('next') or request.referrer or None,
    _external=True))

@app.route('/database')
def database(): #A function to render raw data - can be improved later
    # return pprint.pformat(Tips) #For rendering Tips
    # return pprint.pformat(User.query.all()) #For rendering User DB
    # return pprint.pformat(userCache) #For rendering userCache
    return pprint.pformat(userCache) #For rendering userCache

@app.route('/about')
def about():
    sessionID = get_facebook_oauth_token()
    return render_template('about.html', user=userCache[sessionID])

@app.route('/privacy')
def userInfo():
    sessionID = get_facebook_oauth_token()
    return render_template('userInfo.html', user=userCache[sessionID])

@app.route('/share')
def share():
    rsp = facebook.post('/me', data={'caption': 'Testing', 'method':'feed', 'name':'A test'})
    return str(pprint.pprint(rsp))

# @app.route('/invite')
# def invite():
#     rsp = facebook.post('/me', data={'caption': 'Testing', 'method':'feed', 'name':'A test'})
#     return str(pprint.pprint(rsp))

# @app.route('/tips', methods=['GET', 'POST'])
# def tips():
#     sessionID = get_facebook_oauth_token()

#     # Testing
#     user = userCache[sessionID]
    
#     # Finding the current tip
#     userTips = [tip for tip in Tips if tip not in user.tips]
#     tip = userTips[0][locale]
#     print tip

#     if request.method == 'POST':
#         #Write new state for current tips ID

#         answer = request.form.get('answer')
#         # if answer == tip.correctAnswer:
#         #   response = 'Right!\n' + tip.tipText
#         # else: response = "Try Again"
#         response = tip.tipText
#         userCache[sessionID]['points'] += 10
#         flash(response, 'tip')

#         return render_template('tips.html', user=userCache[sessionID], tip=tip, answer=answer)

#     if request.method == 'GET':
#         answer = None
#         return render_template('tips.html', user=userCache[sessionID], tip=tip)

@app.route('/tips')
def tips():
    sessionID = get_facebook_oauth_token()
    return render_template('tips.html', user=userCache[sessionID])

@app.route('/game')
def game():
    sessionID = get_facebook_oauth_token()
    return render_template('game.html', user=userCache[sessionID])

@app.route('/test', methods=['GET', 'POST'])
def test():

    #Gives the right test to the current user and stores the score

    Tests = (O.Test('CESD1','ces-d.html',0), O.Test('BDI','bdi.html',4), O.Test('PHQ9','phq9.html',7))
    sessionID = get_facebook_oauth_token()

    if request.method == 'GET':

        #Check the users complete tests
        #Check other test schedule data
        currentTest = Tests[0]
          #If there are no tests now, return otherActivitesPage
        
        #Load test
        return render_template('tests/' + currentTest.url, testName=currentTest.name, user=userCache[sessionID])

    if request.method == 'POST':
                
        #Store test scores at TEST NAME (which is returned)
        #Load an outgoing URL

        score = []
        for i in range(20):
            scoreItem = eval("request.form.get('var" + str(i) + "')")
            if scoreItem:
                score.append(int(scoreItem))
        scoresum = int(sum(score))

        userCache[sessionID].testscores['CESD1'] = [scoresum, time.time()]

        # put the test score to user DB (User.testscore)
        me = facebook.get('/me')
        user_fbID = me.data['id']
        sessionUser = User.query.filter_by(facebookID=user_fbID).first()
        tempDict = dict(sessionUser.testscore)
        tempDict['CESD1'] = [scoresum, time.time()]
        User.query.filter_by(facebookID=user_fbID).update(dict(testscore = tempDict))
        db.session.commit()

        if scoresum < 10:
            return render_template('feedback1.html', user=userCache[sessionID])
        elif 10 <= scoresum < 21:
            return render_template('feedback2.html', user=userCache[sessionID])
        else:
            return render_template('feedback3.html', user=userCache[sessionID])

@app.route('/userSession/')
def userSession():
    sessionID = get_facebook_oauth_token()
    me = facebook.get('/me')
    user_fbID = me.data['id']
    sessionUser = User.query.filter_by(facebookID=user_fbID).first()
        # check whether user exists in DB

    if sessionID in userCache:
        #The user exists in userCache.
        return render_template('returningUser.html', user=userCache[sessionID])

    elif sessionUser != None:
        #Returning user :: The user exists in DB. apply user to cache and show them a game
        userCache[sessionID] = O.User(sessionUser.name, sessionUser.facebookID, sessionID, time.time(), sessionUser.friendNum,
                                        sessionUser.points + 1, sessionUser.locale, sessionUser.target, sessionUser.testscore, sessionUser.tip, sessionUser.crawldata)

        # me = facebook.get('/me')
        # timelineFeed = facebook.get('/me/feed')
        # groups = facebook.get('/me/groups?fields=name')
        # interest = facebook.get('/me/interests')
        # likes = facebook.get('/me/likes?fields=name')
        # location = facebook.get('/me/locations?fields=place')
        # notes = facebook.get('me/notes')
        # messages = facebook.get('me/inbox?fields=comments')
        # friendRequest = facebook.get('me/friendrequests?fields=from')
        # events = facebook.get('me/events')
        
        # # refresh crawling Data
        # crawlData = [timelineFeed.data, me.data['relationship_status'], groups.data, interest.data, likes.data, location.data, notes.data, messages.data, friendRequest.data, events.data]
        # sessionUser.crawldata = crawlData       
        # sessionUser.points = userCache[sessionID].points
        # db.session.commit()

        #store the updated values to the database
        return render_template('returningUser.html', user=userCache[sessionID])
    
    else:
        #The user does not exist. Lets create them
        me = facebook.get('/me')
        friends = facebook.get('/me/friends')

        timelineFeed = facebook.get('/me/feed')
        groups = facebook.get('/me/groups?fields=name')
        interest = facebook.get('/me/interests')
        likes = facebook.get('/me/likes?fields=name')
        location = facebook.get('/me/locations?fields=place')
        notes = facebook.get('me/notes')
        messages = facebook.get('me/inbox?fields=comments')
        friendRequest = facebook.get('me/friendrequests?fields=from')
        events = facebook.get('me/events')

        #Instantiate user in database
        
        crawlData = [timelineFeed.data, me.data['relationship_status'], groups.data, interest.data, likes.data, location.data, notes.data, messages.data, friendRequest.data, events.data]
        newUser = User(sessionID, me.data['id'], me.data['name'], me.data['locale'], len(friends.data['data']), 'control', 1, {}, {}, crawlData)
        db.session.add(newUser)
        db.session.commit()
        
        #Instantiate local user
        userCache[sessionID] = O.User(me.data['name'], me.data['id'], sessionID, time.time(), len(friends.data['data']), 1, me.data['locale'], 'control', {}, {}, crawlData)
        return redirect(url_for('index'))

@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )

    session['oauth_token'] = (resp['access_token'], '')

    return redirect(url_for('userSession'))

@facebook.tokengetter
def get_facebook_oauth_token():
    if OFFLINE:
        return 'Debug Mode'
    try: 
        return session.get('oauth_token')
        # short_token = session.get('oauth_token')
        # extended_token = get_extended_access_token(short_token, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET)
        # return extended_token[0]
        #### This code makes an internal servor error
    except ValueError:
        pass
    return None

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)