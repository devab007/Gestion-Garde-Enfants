from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:passer@localhost:5432/garderie_enfants'
app.config['SQLALCHEMY_DATABASE_TRACK_MODIFICATIONS']=False
DATABASE_URL = "postgresql://postgres:passer@localhost:5432/garderie_enfants"
db=SQLAlchemy(app)

#Test de la connexion avec la base de donnée
if __name__=='__main__':
  try:
    with app.app_context():
      connection = db.engine.connect()
      print("Connexion a la base de donnees reussie!")
      connection.close()
  except Exception as e:
    print("Erreur de connexion: ",e)

