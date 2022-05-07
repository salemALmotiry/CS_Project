import base64
import rsa 


def generatorKeys():
     (pubKey, privKey) = rsa.newkeys(1024)
     return pubKey,privKey

def rsa_encrypt_binfile(file_path,save_path,pub_key):
    
      with open(file_path, 'rb') as f:
        message = f.read()
       
      length = len(message)
      default_length = 117 # 1024 / 8 - 11 1024 is the key length
      # rsakey = RSA.importKey(pub_key)
      # cipher = Cipher_pkcs1_v1_5.new(rsakey)
    

      # No segmentation required
      result = []
      if length <= default_length:
        result.append(base64.b64encode(rsa.encrypt(message,pub_key)))
    
      # Need segmentation
      offset = 0
      while length - offset > 0:
        if length - offset > default_length:
          result.append(base64.b64encode(rsa.encrypt(message[offset:offset+default_length],pub_key)))
        else:
          result.append(base64.b64encode(rsa.encrypt(message[offset:],pub_key)))
        offset += default_length
      
      with open(save_path,"ab+") as w:
        for ciphertext in result:
          ciphertext += b"\n"
          w.write(ciphertext)

def rsa_decrypt_binfile(file_path,save_path,priv_key):
      '''
      rsa Decrypt binary
      :file_path:File path to decrypt
      :save_path:File path stored after decryption
      :priv_key:Private key
      '''
      with open(file_path,"rb") as f:
        line = f.readline()
        while line:
          message = base64.b64decode(line.strip(b"\n"))
         
          plaintext = rsa.decrypt(message, priv_key)
          with open(save_path, 'ab+') as w: #Append write
            w.write(plaintext)
          line = f.readline()
        
        

def sign_sha1(file_path,save_path, privkey):
    with open(file_path, 'rb') as f:
        message = f.read()
   
    sign =  base64.b64encode(rsa.sign(message, privkey, 'SHA-1'))
  
    with open(save_path,"wb") as f :
        f.write(sign)

    

def verify_sha1(file_path, signature_path, pubkey):
    try:
        with open(signature_path, 'rb') as f:
             signature =base64.b64decode( f.read())
       
        with open(file_path, 'rb') as f:
             message =f.read()

        return rsa.verify(message, signature, pubkey) == 'SHA-1'
    except:
        return False


