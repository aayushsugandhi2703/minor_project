from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,IntegerField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username= StringField('username', validators=[DataRequired(), Length(min = 2, max = 20)])
    password = PasswordField('passowrd', validators=[DataRequired(), Length(min = 8, max = 20)])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username= StringField('username', validators=[DataRequired(), Length(min = 2, max = 20)])
    password = PasswordField('passowrd', validators=[DataRequired(), Length(min = 8, max = 20)])
    submit = SubmitField('Register')

