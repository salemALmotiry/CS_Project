
from re import T
from time import sleep
from app import app 

if __name__ == "__main__":
     
  while True : 
     try :
        app.run()
     except: 
          sleep(1)

