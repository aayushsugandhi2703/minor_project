from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField, RadioField, IntegerField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileRequired

class LoginForm(FlaskForm):
    username= StringField('username', validators=[DataRequired(), Length(min = 2, max = 20)])
    password = PasswordField('passowrd', validators=[DataRequired(), Length(min = 8, max = 20)])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min = 2, max = 20)])
    email = StringField('Email', validators=[DataRequired(), Length(min = 2, max = 30)])
    organization = StringField('Organization', validators=[DataRequired(), Length(min = 2, max = 20)])
    phone = StringField('phone', validators=[DataRequired(), Length(min = 2, max = 20)])
    username= StringField('username', validators=[DataRequired(), Length(min = 2, max = 20)])
    password = PasswordField('passowrd', validators=[DataRequired(), Length(min = 8, max = 20)])
    submit = SubmitField('Register')

class upload_form(FlaskForm):
    file = FileField('Select File', validators=[FileRequired()])
    fields = SelectMultipleField(
        "Choose Required Fields",
        choices=[
            ("ip", "IP Address"),
            ("timestamp", "Timestamp"),
            ("status", "Status Code"),
            ("method", "HTTP Method"),
            ("url", "URL"),
            ('user_agent', 'User Agent'),
        ],
    )    
    sortby = RadioField(
        "Sort Logs By",
        choices=[("ip", "IP Address"), ("status", "Status Code"), ("timestamp", "Timestamp")],
    )
    submit = SubmitField('Upload')

