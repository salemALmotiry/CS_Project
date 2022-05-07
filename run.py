import pathlib
from app import app 

if __name__ == "__main__":
     print(pathlib.Path("run.py").parent.absolute())
     print(pathlib.Path("run.py").parent.resolve())

     app.run()

