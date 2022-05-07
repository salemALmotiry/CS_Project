import io
import re
import secrets

import werkzeug
from app import app 
import flask_login
import rsa
from flask import Blueprint, after_this_request, current_app, flash, make_response, render_template, send_file, session, url_for
from flask import request , redirect
from flask import send_from_directory,abort
import os
from app.db import API_Key, PrivateKey, User, db
from app.db import PublicKey, friendPubKey
from app.forms import AddKey, RsaForm, verifyForm 
from werkzeug.utils import secure_filename
from app.rsa_model import generatorKeys, rsa_decrypt_binfile, rsa_encrypt_binfile, sign_sha1, verify_sha1
from werkzeug.security import check_password_hash ,generate_password_hash
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with


api= Api(app)

class Public_Key(Resource):
        
        def get(self,key):
                result = API_Key.query.filter_by(ApiKey=key).first()
                if not result : 
                   abort(404, message="Could not find API key")
                result = PublicKey.query.filter_by(user_id=result.user_id).first()
                return {"public_key":str(result.PubKey)}


class Private_Key(Resource):
        
        def get(self,key):
                
                result = API_Key.query.filter_by(ApiKey=key).first()
                if not result : 
                   abort(404, message="Could not find API key")
                
                result = PrivateKey.query.filter_by(user_id=result.user_id).first()
                return {"Private_key":str(result.PrvKey)}


class ApiGenerated(Resource):

        def get(self,username,password):
                try :
                        hush = generate_password_hash(password,"sha256")
                        new_user = User(username=username,userEmail=username+"API R",password_hash=hush)
                        db.session.add(new_user)
                        db.session.commit()
                except :
                        abort(404, message="user already exist try (psot) to login and get key")
                (public_pem,private_pem) = generatorKeys()
                
                new_public = PublicKey(user_id=new_user.id ,PubKey=public_pem.save_pkcs1('PEM') )
                db.session.add(new_public)
                db.session.commit()
        
                new_private = PrivateKey(user_id=new_user.id ,PrvKey=private_pem.save_pkcs1('PEM') )
                db.session.add(new_private)
                db.session.commit()
                
                generated_key = secrets.token_urlsafe(45)

                NewApiKey = API_Key(user_id=new_user.id ,ApiKey=generated_key)
                db.session.add(NewApiKey)
                db.session.commit()
        
                return {"API_key":str(generated_key)}

        def post(self,username,password):
                 user = User.query.filter_by(username=username).first()
        
                 if user:
                        check = check_password_hash(user.password_hash ,password)
                        if check == True:
                                result = API_Key.query.filter_by(user_id=user.id).first()
                                return {"key":str(result.ApiKey)}
                 return   abort(404, message="user not exist")


encr = reqparse.RequestParser()
encr.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')

def files(file,user_id,KeyType,Rtype,Fkey=""):
        s_filename = secure_filename(file.filename)
        temName = secrets.token_urlsafe(6)
        
        File_name = temName+"_"+s_filename
        
        Decrypt_File_name= File_name
        
        filePath = os.path.join(app.config["UPLOAD_PATH"], File_name)

        file.save(filePath)

        if Rtype =="Verify":
            return filePath

        
        filePathToSave =  os.path.join(app.config["RSA_PATH"],Decrypt_File_name)
        
 
        if Rtype=="Encryption":

            result = PublicKey.query.filter_by(user_id=user_id).first()
            Public_Key = rsa.PublicKey.load_pkcs1( result.PubKey)
            rsa_encrypt_binfile(filePath,filePathToSave,Public_Key)

        if Rtype=="Encryption-with-Fkey":
            
            result = friendPubKey.query.filter_by(firnd_user=Fkey).first()
            
            Public_Key = rsa.PublicKey.load_pkcs1( result.PubKey)
            rsa_encrypt_binfile(filePath,filePathToSave,Public_Key)


        if KeyType=="Private_Key":
             result = PrivateKey.query.filter_by(user_id=user_id).first()
             Private_Key = rsa.PrivateKey.load_pkcs1( result.PrvKey)
             if Rtype=="Decryption":
                  rsa_decrypt_binfile(filePath,filePathToSave,Private_Key)
             elif Rtype=="Signature":
                sign_sha1(filePath,filePathToSave,Private_Key)

       
        return_data = io.BytesIO()
        with open(filePathToSave, 'rb') as fo:
                    return_data.write(fo.read())
                # (after writing, cursor will be at last byte, so move it to start)
        return_data.seek(0)

        os.remove(filePathToSave)
        os.remove(filePath)
        return return_data


class Encryption(Resource):
    def post(self,key):
        result = API_Key.query.filter_by(ApiKey=key).first()
        if not result : 
                abort(404, message="Could not find API key")

        args = encr.parse_args()
        temName = secrets.token_urlsafe(6)
        file = args["file"]
        
        return_data = files(file,result.user_id,"","Encryption")

        return send_file(return_data,attachment_filename=secure_filename(file.filename))
        

class Decryption(Resource):
    def post(self,key):
        result = API_Key.query.filter_by(ApiKey=key).first()
        if not result : 
                abort(404, message="Could not find API key")

        args = encr.parse_args()
        temName = secrets.token_urlsafe(6)
        file = args["file"]
        try:
         return_data = files(file,result.user_id,"Private_Key","Decryption")
        except:
                abort(404,message="Could not decrypt the file")

        return send_file(return_data,attachment_filename=secure_filename(file.filename))


class Sign(Resource):
    def post(self,key):
        result = API_Key.query.filter_by(ApiKey=key).first()
        if not result : 
                abort(404, message="Could not find API key")

        args = encr.parse_args()
        
        file = args["file"]
        try:
             return_data = files(file,result.user_id,"Private_Key","Signature")
             return send_file(return_data,attachment_filename=secure_filename(file.filename))

        except:
                abort(404,message="Could not Signature the file")

encr.add_argument('file2', type=werkzeug.datastructures.FileStorage, location='files')

class verifyA(Resource):

        def post(self,key):
                result = API_Key.query.filter_by(ApiKey=key).first()
                if not result : 
                        abort(404, message="Could not find API key")

                args = encr.parse_args()
                
                file = args["file"]
 

                FilePath = files(file,result.user_id,"","Verify")

                f_sign = args["file2"]
             
        
                s1_filename = secrets.token_urlsafe(6)+secure_filename(f_sign.filename)
               
        

                Sign_File_path = os.path.join(app.config["UPLOAD_PATH"], s1_filename)
        
                

        
                f_sign.save(Sign_File_path)

        
                result = PublicKey.query.filter_by(user_id=result.user_id).first()
                pubk = rsa.PublicKey.load_pkcs1( result.PubKey)
                
                p = verify_sha1(FilePath , Sign_File_path,pubk)
                os.remove(FilePath)
                os.remove(Sign_File_path)
        
                if p == True:


                        return {"state":"verify"}
                elif p==False:
                        return {"state":"not verify"}



adf = reqparse.RequestParser()
adf.add_argument("key name",type=str,help="not ",location="form")
adf.add_argument("key data",type=str,help="not",location="form")

class AddFKey(Resource):

        def post(self,key):
                args = adf.parse_args()
             
               
                result = API_Key.query.filter_by(ApiKey=key).first()

                if not result : 
                        abort(404, message="Could not add key")
                try:
                        new_f_key = friendPubKey(user_id=result.user_id,firnd_user=args["key name"],PubKey = args["key data"])
                        db.session.add(new_f_key)
                        db.session.commit()
                        return {"state":"successful"}
                except:
                        return {"state":"field"}
                                
        
api.add_resource(ApiGenerated, "/api/<username>/<password>")                      
api.add_resource(Public_Key, "/getPublic/<key>")
api.add_resource(Private_Key, "/getPrivate/<key>")
api.add_resource(Encryption, "/encrypt/<key>")
api.add_resource(Decryption, "/decrypt/<key>")
api.add_resource(verifyA, "/verify/<key>")        
api.add_resource(Sign, "/sign/<key>")        
api.add_resource(AddFKey, "/add_key/<key>")        


