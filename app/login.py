import flask_login
from app import app 
from flask import Flask, flash, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,BooleanField
from wtforms.validators import InputRequired, Length, ValidationError
from werkzeug.security import check_password_hash ,generate_password_hash
from flask_bcrypt import Bcrypt
from app.db import LoginForm,RegisterForm,User,PublicKey,PrivateKey,db
from app.rsa_model import generatorKeys



login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




@app.route("/login" ,methods=["GET", "POST"] )
def login():
    logform = LoginForm()
    re = request.form
    
    if logform.validate_on_submit() and "sign in" in re:
        user = User.query.filter_by(username=logform.username.data).first()
        
        if user:
            check = check_password_hash(user.password_hash ,logform.password.data)
        
            if check == True:
                login_user(user)
                
                return redirect(url_for('enc'))
   
   
    regform = RegisterForm()  
    
    if regform.validate_on_submit() and "sign up" in re :
       

        hush = generate_password_hash(regform.password.data,"sha256")
 
        new_user = User(username=regform.username.data,userEmail=regform.userEmail.data ,password_hash=hush)
        db.session.add(new_user)
        db.session.commit()
       
        (public_pem,private_pem) = generatorKeys()
        
        new_public = PublicKey(user_id=new_user.id ,PubKey=public_pem.save_pkcs1('PEM') )
        db.session.add(new_public)
        db.session.commit()
     
        new_private = PrivateKey(user_id=new_user.id ,PrvKey=private_pem.save_pkcs1('PEM') )
        db.session.add(new_private)
        db.session.commit()
        return redirect(url_for('login'))
      
       

    return render_template("/public/login.html",regform=regform,logform=logform)



@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
	logout_user()
	
	return redirect(url_for('login'))