from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileRequired

class LoginForm(FlaskForm):
    username= StringField('username', validators=[DataRequired(), Length(min = 2, max = 20)])
    password = PasswordField('passowrd', validators=[DataRequired(), Length(min = 8, max = 20)])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
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

    submit = SubmitField('Upload')

