from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

# This class is for the user to login
class LoginForm(FlaskForm):
    username = StringField('username', validators = [DataRequired(), Length(min=4, max=20)])
    password = PasswordField('password', validators = [DataRequired(), Length(min=8, max=20)])
    submit = SubmitField('Login')

# This class is for the user to register
class RegisterForm(FlaskForm):
    username = StringField('username', validators = [DataRequired(), Length(min=4, max=20)])
    password = PasswordField('password', validators = [DataRequired(), Length(min=8, max=20)])
    submit = SubmitField('Register')

# This class is for the user to input the URL
class URLForm(FlaskForm):
    url = StringField('url', validators = [DataRequired()])
    submit = SubmitField('Parse')