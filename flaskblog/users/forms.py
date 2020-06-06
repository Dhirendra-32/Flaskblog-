from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User





class RegistrationForm (FlaskForm):
    username = StringField('Username', validators= [DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')
    # custom validators funcion

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("that username has been taken! Please choose different one  ")
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("that email has been taken! Please choose different one  ")

class LoginForm (FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password ', validators=[DataRequired()])
    remember = BooleanField('Remember me ')
    submit = SubmitField('Log in')


class UpdateAccountForm (FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField("Update profile picture", validators=[FileAllowed(['png', 'jpg', 'jpeg'])])
    submit = SubmitField('Save')

    def validate_username(self, username):
        if current_user.username != username.data:
            username = User.query.filter_by(username=username.data).first()
            if username:
                raise ValidationError("that username has been taken! Please choose different one  ")

    def validate_email(self, email):
        if current_user.email != email.data:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError("that email has been taken! Please choose different one ")

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Reset password')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("There is not email for account,you must regester first")
    
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset password')
    
