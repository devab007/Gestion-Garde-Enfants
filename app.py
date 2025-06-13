from flask import Flask, render_template

app = Flask(__name__)

@app.route('/Accueil/')
def Accueil():
  return render_template('Accueil.html')
#inscription et connexion des utilisateurs  

@app.route('/')
def connexion():
  return render_template('connexion.html')

@app.route('/Inscription/')
def Inscription():
  return render_template('Inscription.html')


@app.route('/modifier_inscription/')
def modifier_Inscription():
  return render_template('modifier_inscription.html')


@app.route('/planning/')
def planning():
  return render_template('planning.html')

@app.route('/specialite/')
def specialite():
  return render_template('specialite.html')

@app.route('/telephone/')
def telephone():
  return render_template('telephone.html')

@app.route('/user/')
def user():
  return render_template('user.html')


@app.route('/MFEN/')
def MFEN():
  return render_template('modifier_enfant.html')

@app.route('/parent/')
def parent():
  return render_template('parent.html')


@app.route('/FEM/')
def FEM():
  return render_template('FEM.html')


@app.route('/FEN/')
def FEN():
  return render_template('Enfant.html')

@app.route('/FAC/')
def FAC():
  return render_template('FAC.html')










if __name__=='__main__':
  app.run(debug=True)

