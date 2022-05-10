import io
import pathlib
from app import app 
import flask_login
import rsa
from flask import Blueprint, after_this_request, current_app, flash, render_template, send_file, session, url_for
from flask import request , redirect
from flask import send_from_directory,abort
import os
from app.db import PrivateKey, db
from app.db import PublicKey, friendPubKey
from app.forms import AddKey, RsaForm, verifyForm 
from werkzeug.utils import secure_filename
from app.rsa_model import rsa_decrypt_file, rsa_encrypt_file, sign, verify



@app.route("/add-friendly-key", methods=["GET", "POST"])
def addFKey():
    form = AddKey()
    method_name = "Add key"

    if form.validate_on_submit():
      
        new_f_key = friendPubKey(user_id=flask_login.current_user.id,firnd_user=form.username.data ,PubKey = form.key.data)
        db.session.add(new_f_key)
        db.session.commit()
        
        return redirect(url_for('enc'))

    
    
    return render_template("/public/addpubkey.html",form=form ,method_name=method_name)



def files(wtf_file,KeyType,Rtype,Fkey=""):

        s_filename = secure_filename(wtf_file.filename)

        File_name = flask_login.current_user.username+"_"+s_filename
        
        Decrypt_File_name = flask_login.current_user.username+"_"+Rtype+"_"+s_filename
        
        filePath = os.path.join(app.config["UPLOAD_PATH"], File_name)

        wtf_file.save(filePath)

        if Rtype =="Verify":
            return filePath

        
        filePathToSave =  os.path.join(app.config["UPLOAD_PATH"],Decrypt_File_name)
        
 
        if Rtype=="Encryption":

            result = PublicKey.query.filter_by(user_id=flask_login.current_user.id).first()
            Public_Key = rsa.PublicKey.load_pkcs1( result.PubKey)
            rsa_encrypt_file(filePath,filePathToSave,Public_Key)

        if Rtype=="Encryption-with-Fkey":
            
            result = friendPubKey.query.filter_by(firnd_user=Fkey).first()
            
            Public_Key = rsa.PublicKey.load_pkcs1( result.PubKey)
            rsa_encrypt_file(filePath,filePathToSave,Public_Key)


        if KeyType=="Private_Key":
             result = PrivateKey.query.filter_by(user_id=flask_login.current_user.id).first()
             Private_Key = rsa.PrivateKey.load_pkcs1( result.PrvKey)
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


    
@app.route("/Encryption" , methods=["GET", "POST"])
@flask_login.login_required
def enc():
  
    form = RsaForm()

    if form.validate_on_submit():
        f = form.fileToProcess.data       
        fkey = request.form["keys"]
        if fkey=="My key":
           return_data=files(f,"PUB","Encryption")

        else:
           return_data=files(f,"PUB","Encryption-with-Fkey",fkey)
            

        try:   
             return send_file(return_data,attachment_filename=secure_filename(f.filename), as_attachment=True)

        except FileNotFoundError:
                     abort(404)
    
    method_name = "Encryption"
    Fkey = friendPubKey.query.with_entities(friendPubKey.firnd_user).filter(friendPubKey.user_id==flask_login.current_user.id).all()
   
    return render_template("/public/Encryption.html",form=form ,method_name=method_name, Fkey=Fkey)
    


@app.route("/Decryption" , methods=["GET", "POST"])
@flask_login.login_required
def de():
    form = RsaForm()

    if form.validate_on_submit():
        f = form.fileToProcess.data       
        
        try:   
               return_data=files(f,"Private_Key","Decryption")
               return send_file(return_data,attachment_filename=secure_filename(f.filename), as_attachment=True)
        except FileNotFoundError:
                     abort(404)
        except:
            flash("Could not decrypt the file ")
    method_name = "Decryption"
    return render_template("/public/decryption.html",form=form ,method_name=method_name)
   

@app.route("/signature", methods=["GET", "POST"])
@flask_login.login_required
def signature():
    form = RsaForm()
    if form.validate_on_submit():
      
        f = form.fileToProcess.data
        try: 
               return_data=files(f,"Private_Key","Signature")
               return send_file(return_data,attachment_filename="Signature.txt", as_attachment=True)
            
        except FileNotFoundError:
                     abort(404)
    method_name = "Signature"
    return render_template("/public/signature.html",form=form ,method_name=method_name)


@app.route("/verify", methods=["GET", "POST"])
@flask_login.login_required
def verify():
    form = verifyForm()

    if form.validate_on_submit():
      
        f = form.fileToProcess.data
        
        FilePath = files(f,"","Verify")

        f_sign = form.fileToProcess2.data

        s1_filename = secure_filename(f_sign.filename)
        
       

        Sign_File_name= flask_login.current_user.username+"_Signature_"+s1_filename

        Sign_File_path = os.path.join(app.config["UPLOAD_PATH"], Sign_File_name)
     
        

       
        f_sign.save(Sign_File_path)

       
        result = PublicKey.query.filter_by(user_id=flask_login.current_user.id).first()
        pubk = rsa.PublicKey.load_pkcs1( result.PubKey)
        
        p = verify(FilePath , Sign_File_path,pubk)
        os.remove(FilePath)
        os.remove(Sign_File_path)
    
        if p == True:

            flash("verify")
            return redirect(url_for("verify"))
        elif p==False:
            flash("not verify")
            return redirect(url_for("verify"))

    method_name = "Verify" 
    return render_template("/public/Verify.html",form=form ,method_name=method_name )

