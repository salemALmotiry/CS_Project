import io
import secrets
from requests import delete
import werkzeug
from app import app 
import flask_login
import rsa
from flask import Blueprint, after_this_request, current_app, flash, make_response, render_template, send_file, session, url_for
from flask import request , redirect
from flask import send_from_directory,abort
import os
from app.db import API_Key, PrivateKey, PrivateKey_API, Publickey_API, User, db
from app.db import PublicKey, friendPubKey
from app.forms import AddKey, RsaForm, verifyForm 
from werkzeug.utils import secure_filename
from app.rsa_model import generatorKeys, rsa_decrypt_file, rsa_encrypt_file, sign, verify
from werkzeug.security import check_password_hash ,generate_password_hash
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with


api= Api(app)


class ApiG(Resource):

      
        def post(self,username,password):
                 user = User.query.filter_by(username=username).first()
        
                 if user:
                        check = check_password_hash(user.password_hash ,password)
                        if check == True:
                                result = API_Key.query.filter_by(user_id=user.id).first()
                                return {"key":str(result.ApiKey)}
                 return   abort(404, message="user not exist")


class custom_keys(Resource):
        def post(self,key,username):
                result = API_Key.query.filter_by(ApiKey=key).first()
                if not result : 
                        abort(404, message="Could not find API key")
                (public_pem,private_pem) = generatorKeys()
                
                new_public_API = Publickey_API(user_id=result.user_id,username=username,PubKey=public_pem.save_pkcs1('PEM') )
                db.session.add(new_public_API)
                db.session.commit()

                new_private_API =  PrivateKey_API(user_id=result.user_id,username=username ,PrvKey=private_pem.save_pkcs1('PEM') )
                db.session.add(new_private_API)
                db.session.commit()
                return {"state":"successfully"}
         

class Public_Key(Resource):
        
        def post(self,key):
                result = API_Key.query.filter_by(ApiKey=key).first()
                if not result : 
                   abort(404, message="Could not find API key")
                result = PublicKey.query.filter_by(user_id=result.user_id).first()
                return {"public_key":str(result.PubKey)}


class Private_Key(Resource):
        
        def post(self,key):
                
                result = API_Key.query.filter_by(ApiKey=key).first()
                if not result : 
                   abort(404, message="Could not find API key")
                
                result = PrivateKey.query.filter_by(user_id=result.user_id).first()
                return {"Private_key":str(result.PrvKey)}



encr = reqparse.RequestParser()
encr.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')


def files(file,Key,KeyType,Rtype,Fkey=""):
        s_filename = secure_filename(file.filename)
        temName = secrets.token_urlsafe(6)
        
        File_name = temName+"_"+s_filename
        
        Decrypt_File_name= Rtype+"_"+File_name

        
        filePath = os.path.join(app.config["UPLOAD_PATH"], File_name)

        file.save(filePath)

        if Rtype =="Verify":
            return filePath

        
        filePathToSave =  os.path.join(app.config["UPLOAD_PATH"],Decrypt_File_name)
        
 
        if Rtype=="Encryption":
            Public_Key = rsa.PublicKey.load_pkcs1(Key)
            rsa_encrypt_file(filePath,filePathToSave,Public_Key)

        

        if KeyType=="Private_Key":
             
             Private_Key = rsa.PrivateKey.load_pkcs1(Key)
           
             if Rtype=="Decryption":
                  rsa_decrypt_file(filePath,filePathToSave,Private_Key)
             elif Rtype=="Signature":
                sign(filePath,filePathToSave,Private_Key)

       
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
        file = args["file"]
        
        

        if 'friend key' in request.form: 
                try:
                 
                 result = friendPubKey.query.filter_by(firnd_user=request.form['friend key']).first()
                
                except:
                        return {"error":"could not find Fkey"}
        elif 'custom keys' in request.form:
                
                result = Publickey_API.query.filter(Publickey_API.user_id==result.user_id,Publickey_API.username==request.form["custom keys"]).first()
                
        else:
                 result = PublicKey.query.filter_by(user_id=result.user_id).first()
                 

        
       
        return_data = files(file,result.PubKey,"","Encryption")

        return send_file(return_data,attachment_filename=secure_filename(file.filename))


class Decryption(Resource):
    def post(self,key):
        result = API_Key.query.filter_by(ApiKey=key).first()
        if not result : 
                abort(404, message="Could not find API key")

        args = encr.parse_args()
        
        file = args["file"]
        if 'custom keys' in request.form:
                result = PrivateKey_API.query.filter(PrivateKey_API.user_id==result.user_id,PrivateKey_API.username==request.form["custom keys"]).first()
        else:
                result = PrivateKey.query.filter_by(user_id=result.user_id).first()

        try:
        
         return_data = files(file,result.PrvKey,"Private_Key","Decryption")
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
             if 'custom keys' in request.form:
                result = PrivateKey_API.query.filter(PrivateKey_API.user_id==result.user_id,PrivateKey_API.username==request.form["custom keys"]).first()
             else:
                result = PrivateKey.query.filter_by(user_id=result.user_id).first()
 
             return_data = files(file,result.PrvKey,"Private_Key","Signature")
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
                FilePath = files(file,"","","Verify")

                f_sign = args["file2"]
             
                s1_filename = secrets.token_urlsafe(6)+secure_filename(f_sign.filename)
                Sign_File_path = os.path.join(app.config["UPLOAD_PATH"], s1_filename)
        
                f_sign.save(Sign_File_path)

        
                if 'custom keys' in request.form:
                        result = Publickey_API.query.filter(Publickey_API.user_id==result.user_id,Publickey_API.username==request.form["custom keys"]).first()
                else:
                         result = PublicKey.query.filter_by(user_id=result.user_id).first()
        
                pubk = rsa.PublicKey.load_pkcs1( result.PubKey)
                
                p = verify(FilePath , Sign_File_path,pubk)
                os.remove(FilePath)
                os.remove(Sign_File_path)
        
                if p == True:
                        return {"state":"verify"}
                elif p==False:
                        return {"state":"not verify"}




class AddFKey(Resource):

        def post(self,key):
               
                result = API_Key.query.filter_by(ApiKey=key).first()

                if not result : 
                        abort(404, message="Could not add key")
                try:
                        new_f_key = friendPubKey(user_id=result.user_id,firnd_user=request.form["key name"],PubKey = request.form["key data"])
                        db.session.add(new_f_key)
                        db.session.commit()
                        return {"state":"successful"}
                except:
                        return {"state":"field"}
                                

class deleteFkey(Resource):
        def post(self,key):
                result = API_Key.query.filter_by(ApiKey=key).first()
                if not result : 
                        abort(404, message="Could not find API key")
                try:
                    result = friendPubKey.query.filter(friendPubKey.user_id==result.user_id,friendPubKey.firnd_user==request.form['friend key']).delete()
                    db.session.commit()
                    return {"state":"successful"}
                except:
                    return {"state":"failed"}
                

class deleteCustomkeys(Resource):

        def post(self,key):   
                result = API_Key.query.filter_by(ApiKey=key).first()
                if not result : 
                        abort(404, message="Could not find API key")
                try:
                    PrivateKey_API.query.filter(PrivateKey_API.user_id==result.user_id,PrivateKey_API.username==request.form["custom keys"]).delete()
                    Publickey_API.query.filter(Publickey_API.user_id==result.user_id,Publickey_API.username==request.form["custom keys"]).delete()
                    db.session.commit()
                    return {"state":"successful"}
                except:
                    return {"state":"failed"}           
      
api.add_resource(ApiG, "/api/<username>/<password>")                      
api.add_resource(Public_Key, "/getPublic/<key>")
api.add_resource(Private_Key, "/getPrivate/<key>")
api.add_resource(Encryption, "/encrypt/<key>")
api.add_resource(Decryption, "/decrypt/<key>")
api.add_resource(verifyA, "/verify/<key>")        
api.add_resource(Sign, "/sign/<key>")        
api.add_resource(AddFKey, "/add_Fkey/<key>")        
api.add_resource(deleteFkey, "/delete_Fkey/<key>")        
api.add_resource(deleteCustomkeys, "/delete_Ckey/<key>")        
api.add_resource(custom_keys,"/custom_keys/<key>/<username>")

