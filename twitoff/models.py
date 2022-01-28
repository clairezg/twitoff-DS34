"""SQLAlchemy User and Tweet models for out database"""

##code is mostly written by Ryan Allread, but it is tested and works on my machine

from flask_sqlalchemy import SQLAlchemy

# creates a DB Object from SQLAlchemy class
DB = SQLAlchemy()


# Making a User table using SQLAlchemy
class User(DB.Model):
    """Creates a User Table with SQlAlchemy"""
    # id column
    id = DB.Column(DB.BigInteger, primary_key=True)
    # name column
    username = DB.Column(DB.String, nullable=False)

    # def __repr__(self):
    #     return "<User: {}>".format(self.username) --- used yesterday for more classic interactions
    newest_tweet_id = DB.Column(DB.BigInteger)


class Tweet(DB.Model):
    """Keeps track of Tweets for each user"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))  # allows for text and links
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey(
        'user.id'), nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    # def __repr__(self):
    #     return "<Tweet: {}>".format(self.text) --- used yesterday for more classic interactions
    vect = DB.Column(DB.PickleType, nullable=False)
    

