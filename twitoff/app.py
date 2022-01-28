##code is mostly written by Ryan Allread, but it is tested and works on my machine

#libraries
from flask import Flask, render_template, request
from os import getenv

#our code files
from .models import DB, User, Tweet
from .twitter import add_or_update_user
from .predict import predict_user

def create_app():
    # Initilaize our app
    app = Flask(__name__)

    # Database configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = getenv('DATABASE_URI')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    DB.init_app(app)

    #home page, use base template and display all existing users and their tweets
    @app.route("/")
    def home_page():
        # query for all users in the database
        users = User.query.all()
        return render_template('base.html', title='Home', users=users)


    @app.route('/update')
    def update():
        #uses function created below and one imported from twitter.py
    
        usernames = get_usernames()
        for username in usernames:
            add_or_update_user(username)
        users = User.query.all()
        return render_template('base.html', title='Database has been updated.', users=users)

    @app.route('/reset')
    def reset():
        #all data dropped and reinitialized
        DB.drop_all()
        DB.create_all()

        return render_template('base.html', title='Database has been reset.')

    # user route is a more traditional API endpoint
    # This endpoint can only accept certain kinds of http requests.
    @app.route('/user', methods=['POST'])
    @app.route('/user/<username>', methods=['GET'])
    def user(username=None, message=''):
        username = username or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(username)
                message = f"User '{username}' has been successfully added!"
            tweets = User.query.filter(User.username == username).one().tweets
        except Exception as e:
            message = f'Error adding {username}: {e}'
            tweets = []

        return render_template('user.html', title=username, tweets=tweets, message=message)

    @app.route('/compare', methods=['POST'])
    def compare():
        user0, user1 = sorted(
            [request.values['user0'], request.values['user1']])

        if user0 == user1:
            message = "Cannot compare a user to themselves!"

        else:
            prediction = predict_user(
                user0, user1, request.values['tweet_text'])
            message = "'{}' is more likely to be said by {} than {}!".format(request.values['tweet_text'],
                                                                             user1 if prediction else user0,
                                                                             user0 if prediction else user1)

        return render_template('prediction.html', title="Prediction", message=message)


#outdated function, perhaps reuse for entry tab?
    @app.route('/populate')
    # Test my database functionality
    # by inserting some fake data into the DB
    def populate():

        
        add_or_update_user('ryanallred')
        add_or_update_user('tylercowen')
        add_or_update_user('anniecarpenter')

        users = User.query.all()
        message = 'Database has been populated with default users.'

        return render_template('base.html', title=message, users=users)

    return app


def get_usernames():
    # get all of the usernames of existing users
    Users = User.query.all()
    usernames = []
    for user in Users:
        usernames.append(user.username)

    return usernames
