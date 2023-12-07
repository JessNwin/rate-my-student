
from app import db 
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True)  # Username
    full_name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.LargeBinary)
    type = db.Column(db.String)

class Student(User):
    __tablename__ = 'students'
    # Inherits id, full_name, email, password from User
    ratings = db.relationship('Rating', 
                              foreign_keys='[Rating.student_id]', 
                              backref='rated_student', 
                              lazy=True) # Ratings recieved
    written_ratings = db.relationship('Rating', 
                                  foreign_keys='[Rating.reviewer_id]', 
                                  backref='reviewer', 
                                  lazy=True)  # Ratings written by this user

    recommendations = db.relationship('Recommendation', 
                                      foreign_keys='[Recommendation.student_id]', 
                                      backref='student_recommendations',  # student backref name
                                      lazy=True)
    
class Professor(User):
    __tablename__ = 'professors'
    # Inherits id, full_name, email, password from User
    recommendations = db.relationship('Recommendation', 
                                      foreign_keys='[Recommendation.professor_id]', 
                                      backref='professor_recommendations',  # professor backref name
                                      lazy=True)
    #average_rating = db.Column(db.Float) #This was causing an error for some reason
    
class Rating(db.Model):
    __tablename__ = 'ratings'
    id = db.Column(db.Integer, primary_key=True)

    rating_overall = db.Column(db.Float) # averaged rating of all rating attributes
    rating_participation = db.Column(db.Integer)
    rating_communication = db.Column(db.Integer)
    rating_skill = db.Column(db.Integer) # subject mastery

    description = db.Column(db.String)
    reviewer_id = db.Column(db.String, db.ForeignKey('users.id'))
    student_id = db.Column(db.String, db.ForeignKey('users.id'))

class Recommendation(db.Model):
    __tablename__ = 'recommendations'
    id = db.Column(db.Integer, primary_key=True)
    professor_id = db.Column(db.String, db.ForeignKey('users.id'))
    student_id = db.Column(db.String, db.ForeignKey('users.id'))
    description = db.Column(db.String)

##add admin user
class Administrator(User):
    __tablename__ = 'administrators'
    reported_ratings = db.relationship('Report',
                                       foreign_keys='[Report.reporter_id]',  
                                       backref='reported_rating',
                                       lazy=True)

##add report class
class Report(db.Model):
    __tablename__ = 'reports'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    rating_id = db.Column(db.Integer, db.ForeignKey('ratings.id'))
    reporter_id = db.Column(db.String, db.ForeignKey('users.id'))
    rating = db.relationship('Rating', backref='reports', lazy=True)
