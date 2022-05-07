from collections import UserList
from app import app 
from flask_sqlalchemy import Model, SQLAlchemy
from flask_login import UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from werkzeug.security import check_password_hash ,generate_password_hash


db = SQLAlchemy(app)

class User(db.Model,UserMixin):
    __tablename__= "User"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    userEmail = db.Column(db.String(25), nullable=False, unique=True)
    password_hash = db.Column(db.String(128) ,nullable=False)

    # User Can Have Many Posts 
    
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)



class API_Key(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id =  db.Column(db.Integer, db.ForeignKey('User.id'),nullable=False)
    ApiKey = db.Column(db.String(50), nullable=False)



class PublicKey(db.Model):
    # __tablename__= "PublicKey"

    id = db.Column(db.Integer, primary_key=True)
    user_id =  db.Column(db.Integer, db.ForeignKey('User.id'),nullable=False)
    PubKey = db.Column(db.String(600), nullable=False)


class PrivateKey(db.Model):
      __tablename__="PrivateKey"
      id = db.Column(db.Integer, primary_key=True)
      user_id =  db.Column(db.Integer, db.ForeignKey('User.id'),nullable=False)
      PrvKey = db.Column(db.String(600), nullable=False)

    
class friendPubKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id =  db.Column(db.Integer, db.ForeignKey('User.id'),nullable=False)
    firnd_user= db.Column(db.String(20), nullable=False)
    PubKey = db.Column(db.String(600), nullable=False)




class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    userEmail = StringField(validators=[
                           InputRequired(), Length(min=4, max=30)], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')
    

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')
