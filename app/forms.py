from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, PasswordField, TextAreaField, DateField, SubmitField, BooleanField
from wtforms.validators import DataRequired

class SignUpForm(FlaskForm):
    id = StringField('Id', validators=[DataRequired()])
    full_name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email')
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    professor_check = BooleanField('Professor Check')
    submit = SubmitField('Confirm')

class SignInForm(FlaskForm):
    id = StringField('Id', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Confirm')

class RatingForm(FlaskForm):
    rating_choices = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')]

    rating_participation = RadioField('Participation Rating', 
                                      choices=rating_choices, 
                                      validators=[DataRequired()])
    rating_communication = RadioField('Communication Rating', 
                                      choices=rating_choices, 
                                      validators=[DataRequired()])
    rating_skill = RadioField('Skill Rating', 
                              choices=rating_choices, 
                              validators=[DataRequired()])

    description = TextAreaField('Review Description', validators=[DataRequired()])
    submit = SubmitField('Submit Rating')

class ReportForm(FlaskForm):
    report_description = TextAreaField('Report Reason', validators=[DataRequired()])
    submit = SubmitField('Submit Report')

class RecommendationForm(FlaskForm):
    description = TextAreaField('Rating Description', validators=[DataRequired()])
    submit = SubmitField('Submit Recommendation')