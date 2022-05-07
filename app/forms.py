from app import app 
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash ,generate_password_hash




class RsaForm(FlaskForm):
    fileToProcess = FileField(validators= [FileRequired()])
    submit = SubmitField('Submit')




class AddKey(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)])

    key = TextAreaField(validators=[
                           InputRequired(), Length(min=50, max=1000)])

    submit = SubmitField('Submit')



class verifyForm(FlaskForm):
    fileToProcess = FileField(validators=[FileRequired()])
    fileToProcess2 = FileField(validators=[FileRequired()])
    submit = SubmitField('Submit')
