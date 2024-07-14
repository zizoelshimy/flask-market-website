from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError #we use this imports below inside validators 
#i make valdiation here to make sure that the user enter the correct information
#after i make valditions here i will go to routes.py to handel this
from market.models import user


class RegisterForm(FlaskForm):
    #this functions to be check if the user us exist befor or not
    def validate_username(self, username_to_check):
        existing_user = user.query.filter_by(username=username_to_check.data).first()
        if existing_user:
            raise ValidationError('Username already exists. Please try a different username.')
    
    def validate_email_address(self, email_address_to_check):
        existing_email  = user.query.filter_by(email_address=email_address_to_check.data).first()
        if existing_email:
            raise ValidationError('Email Address already exists. Please try a different email address.')
    username = StringField(label='Username', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address', validators=[Email(), DataRequired()])#we put Email to make sure that the user enter the correct email with @ for ex 
    password_hash = PasswordField(label='Password',validators=[Length(min=6),DataRequired() ,EqualTo('password_confirmation')])#to valditae that password and password confirmation are the same
    password_confirmation = PasswordField(label='Confirm Password')
    submit = SubmitField(label='Create Account')
    
class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Sign in') 
    
class PurchessItemForm(FlaskForm):
   submit = SubmitField(label='Purche Item!')
   
   
class SellItemForm(FlaskForm):
   submit = SubmitField(label='Sell Item!')    
   
   