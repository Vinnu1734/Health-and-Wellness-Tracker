# models.py

from db import db  # Import db from db.py

# User Model
class User(db.Model):
    __tablename__ = 'users'
    UserID = db.Column(db.Integer, primary_key=True)
    Fname = db.Column(db.String(100), nullable=False)
    Lname = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(120), unique=True, nullable=False)
    Gender = db.Column(db.String(10))
    DOB = db.Column(db.Date)
    goals = db.relationship('Goal', backref='user', lazy=True)
    diet_logs = db.relationship('DietLog', backref='user', lazy=True)
    exercise_logs = db.relationship('ExerciseLog', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.Fname} {self.Lname}>"

# Goal Model
class Goal(db.Model):
    __tablename__ = 'goals'
    GoalID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('users.UserID'), nullable=False)
    GoalType = db.Column(db.String(50), nullable=False)
    TargetValue = db.Column(db.Float, nullable=False)
    Status = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"<Goal {self.GoalType} for User {self.UserID}>"

# Diet Log Model
class DietLog(db.Model):
    __tablename__ = 'diet_log'
    MealID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('users.UserID'), nullable=False)
    Date = db.Column(db.Date, nullable=False)
    MealType = db.Column(db.String(50), nullable=False)
    Calories = db.Column(db.Float, nullable=False)
    Protein = db.Column(db.Float)
    Carbs = db.Column(db.Float)
    Fats = db.Column(db.Float)

    def __repr__(self):
        return f"<Diet Log for User {self.UserID} on {self.Date}>"

# Exercise Log Model
class ExerciseLog(db.Model):
    __tablename__ = 'exercise_log'
    ActivityID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('users.UserID'), nullable=False)
    Date = db.Column(db.Date, nullable=False)
    ActivityType = db.Column(db.String(50), nullable=False)
    Duration = db.Column(db.Float, nullable=False)  # Duration in minutes
    CaloriesBurned = db.Column(db.Float)

    def __repr__(self):
        return f"<Exercise Log for User {self.UserID} on {self.Date}>"