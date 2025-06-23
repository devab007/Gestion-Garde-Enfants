from flask import Flask, render_template, redirect, url_for, request, flash, session
from sqlalchemy.orm import sessionmaker
from main import db_session
from models import Base
from sqlalchemy import create_engine
from models import Employe, Parent, Enfant, Utilisateur, PlanningGarde, Presence, Facture, Groupe, Classe, Activite
from datetime import date, datetime
from sqlalchemy import func

app = Flask(__name__) 
app.secret_key = 'secretkey'  

@app.route('/')
def connexion():
    return render_template('connexion.html')

@app.route('/traitementConnexion', methods=['GET', 'POST'])
def traitementConnexion():
    if request.method == 'POST':
        donnee = request.form
        nomUser = donnee.get('nameUser')
        password = donnee.get('password')

        if nomUser and password:
            utilisateur = db_session.query(Utilisateur).filter_by(username=nomUser, motdepasse=password).first()

            if utilisateur:
                session['prenom'] = utilisateur.prenom  
                session['utilisateur_id'] = utilisateur.id  
                return redirect(url_for('dashboard')) 
            else:
                flash("Nom d'utilisateur ou mot de passe incorrect.", "danger")
                return render_template('connexion.html')


# @app.route('/traitementConnexion', methods=['GET', 'POST'])
# def traitementConnexion():
#     if request.method == 'POST':
#         donnee = request.form
#         nomUser = donnee.get('nameUser')
#         password = donnee.get('password')

#         if nomUser and password:
#             utilisateur = db_session.query(Utilisateur).filter_by(username=nomUser, motdepasse=password).first()

#             if utilisateur:
#                 return render_template('accueil.html', utilisateur=utilisateur)
#             else:
#                 flash("Nom d'utilisateur ou mot de passe incorrect.", "danger")
#                 # return render_template('connexion.html')
#                 return redirect(url_for('dashboard'))

# @app.route('/')
# def connexion():
#     return render_template('connexion.html')

# @app.route('/traitementConnexion', methods=['GET', 'POST'])
# def traitementConnexion():
#     if request.method == 'POST':
#         donnee = request.form
#         nomUser = donnee.get('nameUser')
#         password = donnee.get('password')

#         if nomUser and password:
#             utilisateur = db_session.query(Utilisateur).filter_by(username=nomUser, motdepasse=password).first()
#             utilisateur = 1
#             if utilisateur:
#                 return render_template('accueil.html', utilisateur=utilisateur)
#             else:
#                 flash("Nom d'utilisateur ou mot de passe incorrect.", "danger")
#                 return render_template('connexion.html')

@app.route('/dashboard/')
def dashboard():
    utilisateur = get_current_user()

    nb_enfants = db_session.query(func.count(Enfant.id)).scalar()
    nb_presences = db_session.query(func.count(Presence.id)).scalar()
    nb_paiements = db_session.query(func.count(Facture.id)).scalar()
    nb_groupes = db_session.query(func.count(Groupe.id)).scalar()

    return render_template('accueil.html', utilisateur=utilisateur,
                           nb_enfants=nb_enfants, nb_presences=nb_presences,
                           nb_paiements=nb_paiements, nb_groupes=nb_groupes)

@app.route('/accueil/')
def accueil():
    utilisateur = get_current_user()

    nb_enfants = db_session.query(func.count(Enfant.id)).scalar()
    nb_presences = db_session.query(func.count(Presence.id)).scalar()
    nb_paiements = db_session.query(func.count(Facture.id)).scalar()
    nb_groupes = db_session.query(func.count(Groupe.id)).scalar()
    return render_template('accueil.html', utilisateur=utilisateur,
                           nb_enfants=nb_enfants, nb_presences=nb_presences,
                           nb_paiements=nb_paiements, nb_groupes=nb_groupes)

def get_current_user():
    class UtilisateurMock:
        prenom = session.get('prenom', 'Admin')
    return UtilisateurMock()

@app.route('/deconnexion')
def deconnexion():
    session.clear()  
    return redirect(url_for('connexion'))

@app.route('/planning/')
def planning():
    return render_template('planning.html')

@app.route('/specialite/')
def specialite():
    return render_template('specialite.html')

@app.route('/telephone/')
def telephone():
    return render_template('telephone.html')

@app.route('/user1/')
def user1():
    return render_template('user.html')

@app.route('/MFEN/')
def MFEN():
    return render_template('modifier_enfant.html')

############################################################################################################

#Partie Parents/Enfants

@app.route('/parent/', methods=['GET', 'POST'])
def parent():
    parents = db_session.query(Parent).all()
    return render_template('parent.html', parents=parents)

@app.route('/inscriptionParent/', methods=['GET', 'POST'])
def inscriptionParent():
    enfants = db_session.query(Enfant).all()
    return render_template('inscriptionParent.html', enfants=enfants)

@app.route("/afficherParentsEnfants/", methods=['GET', 'POST'])
def afficherParentsEnfants():
    enfants = db_session.query(Enfant).all()
    parents = db_session.query(Parent).all()
    return render_template("afficherParentsEnfants.html", enfants=enfants, parents=parents)

@app.route('/traitementInscriptionEnfants', methods=['GET', 'POST'])
def traitementInscriptionEnfants():
    if request.method == 'POST':
        # Infos enfant
        prenom = request.form.get('prenom')
        nom = request.form.get('nom')
        dateNaissance = request.form.get('dateNaissance')
        sexe = request.form.get('sexe') == 'True'
        infoSante = request.form.get('infoSante')
        id_groupe = request.form.get('id_groupe')
        id_classe = request.form.get('id_classe')
        numeroCI = request.form.get('numeroCarteIdentite')
        
        # Infos parent
        prenomPere = request.form.get('prenom_pere')
        nomPere = request.form.get('nom_pere')
        prenomMere = request.form.get('prenom_mere')
        nomMere = request.form.get('nom_mere')
        
        # Récupération directe des champs visibles
        choice = request.form.get('contact_choice')
        email = request.form.get('email')
        adresse = request.form.get('adresse')
        
        parent = Parent(
            prenomPere=prenomPere,
            nomPere=nomPere,
            prenomMere=prenomMere,
            nomMere=nomMere,
            numeroCarteIdentite=numeroCI,
            email=email,
            adresse=adresse
        )
        
        enfant = Enfant(
            prenom=prenom,
            nom=nom,
            dateNaissance=dateNaissance,
            sexe=sexe,
            infoSante=infoSante,
            id_groupe=id_groupe,
            id_classe=id_classe,
            parent=parent
        )
        
        try:
            db_session.add(parent)
            db_session.add(enfant)
            db_session.commit()
            flash("Enfant et parent ajoutés avec succès", "success")
        except Exception as e:
            db_session.rollback()
            flash(f"Erreur lors de l'ajout : {str(e)}", "danger")
        
        return redirect(url_for('afficherParentsEnfants'))
    
    # Partie GET
    groupes = db_session.query(Groupe).all()
    classes = db_session.query(Classe).all()
    return render_template('parent.html', groupes=groupes, classes=classes)

# Affichage et ajout d'un enfant avec son parent associé
# @app.route('/traitementInscriptionEnfants/', methods=['GET', 'POST'])
# def traitementInscriptionEnfants():
#     if request.method == 'POST':
#         # Infos enfant
#         prenom = request.form.get('prenom')
#         nom = request.form.get('nom')
#         dateNaissance = request.form.get('dateNaissance')
#         sexe = request.form.get('sexe') == 'True'
#         infoSante = request.form.get('infoSante')
#         id_groupe = request.form.get('id_groupe')
#         id_classe = request.form.get('id_classe')
#         # Infos parent
#         prenomPere = request.form.get('prenom_pere')
#         nomPere = request.form.get('nom_pere')
#         prenomMere = request.form.get('prenom_mere')
#         nomMere = request.form.get('nom_mere')
#         numeroCI = request.form.get('numeroCarteIdentite')
#         # Coordonnées dynamiques selon sélection
#         choice = request.form.get('contact_choice')
#         email = request.form.get(f'email_{choice}')
#         adresse = request.form.get(f'adresse_{choice}')
#         # telephone = request.form.get(f'telephone_{choice}')

#         parent = Parent(
#             prenomPere=prenomPere,
#             nomPere=nomPere,
#             prenomMere=prenomMere,
#             nomMere=nomMere,
#             numeroCarteIdentite=numeroCI,
#             email=email,
#             adresse=adresse
#         )
#         enfant = Enfant(
#             prenom=prenom,
#             nom=nom,
#             dateNaissance=dateNaissance,
#             sexe=sexe,
#             infoSante=infoSante,
#             id_groupe=id_groupe,
#             id_classe=id_classe,
#             parent=parent
#         )
#         try:
#             db_session.add(parent)
#             db_session.add(enfant)
#             db_session.commit()
#             flash("Enfant et parent ajoutés avec succès", "success")
#         except Exception as e:
#             db_session.rollback()
#             flash(f"Erreur lors de l'ajout : {e}", "danger")
#         return redirect(url_for('afficherParentsEnfants'))

#     # GET -> affichage de la liste et des formulaires
#     enfants = db_session.query(Enfant).all()
#     parents = db_session.query(Parent).all()
#     groupes = db_session.query(Groupe).all()
#     classes = db_session.query(Classe).all()
#     return render_template(
#         'afficherParentsEnfants.html',
#         enfants=enfants,
#         parents=parents,
#         groupes=groupes,
#         classes=classes
#     )

# Modification d'un enfant et de son parent
@app.route('/modifier_enfant/modifier/<int:id>', methods=['GET', 'POST'])
def modifier_enfant(id):
    enf = db_session.query(Enfant).get(id)
    par = enf.parent
    if request.method == 'POST':
        # Mise à jour des champs enfant
        enf.prenom = request.form.get('prenom')
        enf.nom = request.form.get('nom')
        # ... (autres champs enfant à mettre à jour)
        # Mise à jour des champs parent
        par.prenomPere = request.form.get('prenom_pere')
        # ... (autres champs parent à mettre à jour)
        try:
            db_session.commit()
            flash("Données modifiées", "success")
        except Exception as e:
            db_session.rollback()
            flash(f"Erreur lors de la modification : {e}", "danger")
        return redirect(url_for('afficherParentsEnfants'))

    groupes = db_session.query(Groupe).all()
    classes = db_session.query(Classe).all()
    return render_template(
        'modifier_enfant.html',
        enfant=enf,
        parent=par,
        groupes=groupes,
        classes=classes
    )

# Suppression d'un enfant et de son parent lié
@app.route('/confirmerSuppressionEnfant/supprimer/<int:id>', methods=['GET'])
def confirmerSuppressionEnfant(id):
    enf = db_session.query(Enfant).get(id)
    try:
        # Supprimer le parent associé et l'enfant
        db_session.delete(enf.parent)
        db_session.delete(enf)
        db_session.commit()
        flash("Suppression réussie", "success")
    except Exception as e:
        db_session.rollback()
        flash(f"Erreur lors de la suppression : {e}", "danger")
    return redirect(url_for('afficherParentsEnfants'))

#################################################################################################################

# Gestion Employe
@app.route('/FEM/')
def FEM():
    employes = db_session.query(Employe).all()
    return render_template('FEM.html', employes=employes)

@app.route('/ajouter_employe/', methods=['GET', 'POST'])
def ajouter_employe():
    if request.method == 'POST':
        prenom = request.form['prenom']
        nom = request.form['nom']
        matricule = request.form['matricule']
        dateNaissance = request.form['dateNaissance']
        sexe = request.form['sexe'] == 'True'
        email = request.form['email']
        dateEmbauche = request.form['dateEmbauche']

        nouvel_employe = Employe(
            prenom=prenom,
            nom=nom,
            matricule=matricule,
            dateNaissance=dateNaissance,
            sexe=sexe,
            email=email,
            dateEmbauche=dateEmbauche
        )
        try:
            db_session.add(nouvel_employe)
            db_session.commit()
            flash("Employé ajouté avec succès !", "success")
        except Exception as e:
            db_session.rollback()
            flash(f"Erreur lors de l'ajout : {str(e)}", "danger")
        return redirect(url_for('FEM'))

    employes = db_session.query(Employe).all()
    return render_template('Ajouter_employe.html', employes=employes)

@app.route('/updateEmploye/<int:id>', methods=['GET', 'POST'])
def updateEmploye(id):
    employe = db_session.query(Employe).filter_by(id=id).first()
    
    if request.method == 'POST':
        employe.prenom = request.form['prenom']
        employe.nom = request.form['nom']
        employe.matricule = request.form['matricule']
        employe.dateNaissance = request.form['dateNaissance']
        employe.sexe = request.form['sexe'] == 'True'
        employe.email = request.form['email']
        employe.dateEmbauche = request.form['dateEmbauche']
        
        try:
            db_session.commit()
            flash("Employé mis à jour avec succès !", "success")
            return redirect(url_for('FEM'))
        except Exception as e:
            db_session.rollback()
            flash(f"Erreur lors de la mise à jour : {str(e)}", "danger")
    
    return render_template('updateEmploye.html', employe=employe)

@app.route('/supprimerEmploye/<int:id>', methods=['POST'])
def supprimerEmploye(id):
    employe = db_session.query(Employe).filter_by(id=id).first()
    if employe:
        try:
            db_session.delete(employe)
            db_session.commit()
            flash("Employé supprimé avec succès !", "success")
        except Exception as e:
            db_session.rollback()
            flash(f"Erreur lors de la suppression : {str(e)}", "danger")
    return redirect(url_for('FEM'))

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Gestion des utilisateurs

# Ajout d'un utilisateur
@app.route('/Inscription/')
def Inscription():
    utilisateurs = db_session.query(Utilisateur).all()
    return render_template('Inscription.html', utilisateurs=utilisateurs)

@app.route('/TraitementInscription', methods=['POST'])
def TraitementInscription():
    if request.method == 'POST':
        donnee = request.form
        nouvel_user = Utilisateur(
            prenom=donnee.get('prenom'),
            email=donnee.get('email'),
            username=donnee.get('username'),
            motdepasse=donnee.get('password')
        )
        
        try:
            db_session.add(nouvel_user)
            db_session.commit()
            flash("Inscription réussie !", "success")
        except Exception as e:
            db_session.rollback()
            flash(f"Erreur lors de l'inscription : {str(e)}", "danger")
    
    return redirect(url_for('afficherUtilisateur'))

# Affichage
@app.route('/afficherUtilisateur/')
def afficherUtilisateur(): 
    utilisateurs = db_session.query(Utilisateur).all()
    return render_template('afficherUtilisateur.html', utilisateurs=utilisateurs)

# Modification
@app.route('/modifierUtilisateur/<int:id>')
def modifierUtilisateur(id):
    utilisateur = db_session.query(Utilisateur).get(id)
    if not utilisateur:
        flash("Utilisateur non trouvé", "danger")
        return redirect(url_for('afficherUtilisateur'))
    return render_template('modifierUtilisateur.html', utilisateur=utilisateur)

@app.route('/traitementModification/<int:id>', methods=['POST'])
def traitementModification(id):
    utilisateur = db_session.query(Utilisateur).get(id)
    if not utilisateur:
        flash("Utilisateur non trouvé", "danger")
        return redirect(url_for('afficherUtilisateur'))
    
    utilisateur.prenom = request.form.get('prenom')
    utilisateur.email = request.form.get('email')
    utilisateur.username = request.form.get('username')
    
    try:
        db_session.commit()
        flash("Modification réussie !", "success")
    except Exception as e:
        db_session.rollback()
        flash(f"Erreur lors de la modification : {str(e)}", "danger")
    
    return redirect(url_for('afficherUtilisateur'))

# Suppression
@app.route('/supprimerUtilisateur/<int:id>', methods=['GET', 'POST'])
def supprimerUtilisateur(id):
    utilisateur = db_session.query(Utilisateur).get(id)
    
    if not utilisateur:
        flash("Utilisateur non trouvé", "danger")
        return redirect(url_for('afficherUtilisateur'))
    
    if request.method == 'POST':
        try:
            db_session.delete(utilisateur)
            db_session.commit()
            flash("Utilisateur supprimé avec succès", "success")
            return redirect(url_for('afficherUtilisateur'))
        except Exception as e:
            db_session.rollback()
            flash(f"Erreur lors de la suppression : {str(e)}", "danger")
            return redirect(url_for('afficherUtilisateur'))
    
    return render_template('confirmerSuppression.html', utilisateur=utilisateur)

 ####################################################################################################################

# Gestion des présences

# Ajout d'une présence
@app.route('/ajouterPresence/')
def ajouterPresence():
    enfants = db_session.query(Enfant).all()
    presences = db_session.query(Presence).all()
    return render_template('ajouterPresence.html', enfants=enfants, presences=presences)

@app.route('/TraitementAjoutPresence', methods=['POST'])
def TraitementAjoutPresence():
    if request.method == 'POST':
        date_presence = request.form.get('date')
        enfants = db_session.query(Enfant).all()
        
        try:
            for enfant in enfants:
                status = request.form.get(f'enfant_{enfant.id}_status')
                
                nouvelle_presence = Presence(
                    enfant_id=enfant.id,
                    date=date_presence,
                    status=status,
                    heure_arrivee=request.form.get(f'enfant_{enfant.id}_heure') if status == 'R' else None
                )
                
                db_session.add(nouvelle_presence)
            
            db_session.commit()
            flash("Présences enregistrées avec succès !", "success")
        except Exception as e:
            db_session.rollback()
            flash(f"Erreur lors de l'enregistrement : {str(e)}", "danger")
    
    return redirect(url_for('afficherPresence'))




# Affichage
@app.route('/afficherPresence/')
def afficherPresence():
    try:
        status_filter = request.args.get('status')
        query = db_session.query(Presence).options(joinedload(Presence.enfant))
        if status_filter in ['P', 'A', 'R']:
            query = query.filter(Presence.status == status_filter)
            flash_message = f"Affichage des présences avec statut: {'Présent' if status_filter == 'P' else 'Absent' if status_filter == 'A' else 'Retard'}"
            flash(flash_message, "info")
        presences = query.order_by(Presence.date.desc()).all()
        if not presences:
            if status_filter:
                flash(f"Aucune présence avec ce statut trouvée", "warning")
            else:
                flash("Aucune présence enregistrée pour le moment", "info")
        
        return render_template('afficherPresence.html', 
                            presences=presences,
                            today=date.today().isoformat(),
                            current_filter=status_filter)
    
    except Exception as e:
        flash(f"Erreur lors de la récupération des données: {str(e)}", "danger")
        return render_template('afficherPresence.html', 
                           presences=None,
                           today=date.today().isoformat(),
                           current_filter=None)

# Modification
@app.route('/modifierPresence/<int:id>')
def modifierPresence(id):
    presence = db_session.query(Presence).get(id)
    enfants = db_session.query(Enfant).all()
    if not presence:
        flash("Présence non trouvée", "danger")
        return redirect(url_for('afficherPresence'))
    return render_template('modifierPresence.html', presence=presence, enfants=enfants)

@app.route('/traitementModifPresence/<int:id>', methods=['POST'])
def traitementModifPresence(id):
    presence = db_session.query(Presence).get(id)
    if not presence:
        flash("Présence non trouvée", "danger")
        return redirect(url_for('afficherPresence'))
    
    presence.enfant_id = request.form.get('enfant_id')
    presence.date = request.form.get('date')
    presence.status = request.form.get('status')
    presence.heure_arrivee = request.form.get('heure_arrivee') if request.form.get('status') == 'R' else None
    
    try:
        db_session.commit()
        flash("Modification réussie !", "success")
    except Exception as e:
        db_session.rollback()
        flash(f"Erreur lors de la modification : {str(e)}", "danger")
    
    return redirect(url_for('afficherPresence'))

# Suppression
@app.route('/supprimerPresence/<int:id>', methods=['GET', 'POST'])
def supprimerPresence(id):
    presence = db_session.query(Presence).get(id)
    
    if not presence:
        flash("Présence non trouvée", "danger")
        return redirect(url_for('afficherPresence'))
    
    if request.method == 'POST':
        try:
            db_session.delete(presence)
            db_session.commit()
            flash("Présence supprimée avec succès", "success")
            return redirect(url_for('afficherPresence'))
        except Exception as e:
            db_session.rollback()
            flash(f"Erreur lors de la suppression : {str(e)}", "danger")
            return redirect(url_for('afficherPresence'))
    
    return render_template('confirmerSuppressionPresence.html', presence=presence)


@app.route('/FEN/')
def FEN():
    return render_template('Enfant.html')

# Facture
@app.route('/factures')
def liste_factures():
    factures = db_session.query(Facture).all()
    enfants = db_session.query(Enfant)
    return render_template('liste_factures.html', factures=factures,enfants=enfants)


@app.route('/creer', methods=['GET', 'POST'])
def creer_facture():
    if request.method == 'POST':
        libelle=request.form['libelle'],
        sommeTotal=float(request.form['sommeTotal']),
        numeroFacture=request.form['numeroFacture'],
        dateFacture=datetime.strptime(request.form['dateFacture'], '%Y-%m-%d').date(),
        statut=request.form['statut'],
        enfant =request.form['enfant_id']
       
        try:
            nouvelle_facture = Facture(
                libelle=libelle,
                sommeTotal = sommeTotal,
                numeroFacture = numeroFacture,
                dateFacture = dateFacture,
                statut = statut,
                enfant= enfant,
            )
           

            db_session.add(nouvelle_facture)
            db_session.commit()
            flash("Facture créée avec succès", "success")
            return redirect(url_for('liste_factures'))
        except Exception as e:
            db_session.rollback()
            flash(f"Erreur lors de la création : {str(e)}", "danger")
    enfants = db_session.query(Enfant).all()
    
    return render_template('creer_facture.html',enfants=enfants)

@app.route('/factures/<int:id>')
def voir_facture(id):
    facture = db_session.query(Facture)\
             .options(joinedload(Facture.parent), joinedload(Facture.payements))\
             .get(id)
    if not facture:
        flash("Facture non trouvée", "danger")
        return redirect(url_for('liste_factures'))
    return render_template('voir_facture.html', facture=facture)

@app.route('/factures/<int:id>/modifier', methods=['GET', 'POST'])
def modifier_facture(id):
    facture = db_session.query(Facture).get(id)
    enfants = db_session.query(Enfant)
    if not facture:
        flash("Facture non trouvée", "danger")
        return redirect(url_for('liste_factures'))
    
    if request.method == 'POST':
        try:
            facture.libelle = request.form['libelle']
            facture.sommeTotal = float(request.form['sommeTotal'])
            facture.numeroFacture = request.form['numeroFacture']
            facture.dateFacture = datetime.strptime(request.form['dateFacture'], '%Y-%m-%d').date()
            facture.statut = request.form['statut']
            db_session.commit()
            flash("Facture modifiée avec succès", "success")
            return redirect(url_for('voir_facture', id=facture.id))
        except Exception as e:
            db_session.rollback()
            flash(f"Erreur lors de la modification : {str(e)}", "danger")
    
    parents = db_session.query(Parent).all()
    return render_template('modifier_facture.html', facture=facture, enfants=enfants)

@app.route('/factures/<int:id>/supprimer', methods=['POST'])
def supprimer_facture(id):
    facture = db_session.query(Facture).get(id)
    if not facture:
        flash("Facture non trouvée", "danger")
        return redirect(url_for('liste_factures'))
    
    try:
        # Supprimer d'abord les paiements associés
        for payement in facture.payements:
            db_session.delete(payement)
        
        db_session.delete(facture)
        db_session.commit()
        flash("Facture et paiements associés supprimés avec succès", "success")
    except Exception as e:
        db_session.rollback()
        flash(f"Erreur lors de la suppression : {str(e)}", "danger")
    
    return redirect(url_for('liste_factures'))

################################################################################################################

# Affichage des groupes et classes
@app.route('/affichageGroupeClasse/', methods=['GET', 'POST'])
def affichageGroupeClasse():
    groupes = db_session.query(Groupe).all()
    classes = db_session.query(Classe).all()
    return render_template('affichageGroupeClasse.html', groupes=groupes, classes=classes)

# Ajout d'un groupe
@app.route('/ajouterGroupeClasse/ajouter', methods=['GET', 'POST'])
def ajouterGroupeClasse():
    if request.method == 'POST':
        nomGroupe = request.form.get('nomGroupe')
        trancheAge = request.form.get('trancheAge')
        numero = request.form.get('numero')
        capaciteMax = request.form.get('capaciteMax')
        nouveau_groupe = Groupe(nomGroupe=nomGroupe, trancheAge=trancheAge, numero=numero, capaciteMax=capaciteMax)
        try:
            db_session.add(nouveau_groupe)
            db_session.commit()
            flash("Groupe ajouté avec succès", "success")
        except Exception as e:
            db_session.rollback()
            flash(f"Erreur lors de l'ajout du groupe : {e}", "danger")
        return redirect(url_for('affichageGroupeClasse'))
    return render_template('ajouterGroupeClasse.html')

#Ajout d'une classe
@app.route('/ajouterClasse/ajouter', methods=['GET', 'POST'])
def ajouterClasse():
    if request.method == 'POST':
        nomClasse = request.form.get('nomClasse')
        quota = request.form.get('quota')
        nouvelle_classe = Classe(nomClasse=nomClasse, quota=quota)
        try:
            db_session.add(nouvelle_classe)
            db_session.commit()
            flash("Classe ajoutée avec succès", "success")
        except Exception as e:
            db_session.rollback()
            flash(f"Erreur lors de l'ajout de la classe : {e}", "danger")
        return redirect(url_for('affichageGroupeClasse'))
    return render_template('ajouterClasse.html')

#Modif d'un groupe
@app.route('/modifierGroupeClasse/modifier/<int:id>', methods=['GET', 'POST'])
def modifierGroupeClasse(id):
    groupe = db_session.query(Groupe).get(id)
    if not groupe:
        flash("Groupe introuvable", "danger")
        return redirect(url_for('afficherGroupeClasse'))

    if request.method == 'POST':
        groupe.nomGroupe = request.form.get('nomGroupe')
        groupe.trancheAge = request.form.get('trancheAge')
        groupe.numero = request.form.get('numero')
        groupe.capaciteMax = request.form.get('capaciteMax')
        try:
            db_session.commit()
            flash("Groupe modifié avec succès", "success")
            return redirect(url_for('afficherGroupeClasse'))
        except Exception as e:
            db_session.rollback()
            flash(f"Erreur lors de la modification : {e}", "danger")
    return render_template('modifierGroupeClasse.html', groupe=groupe)

#Modif d'une classe
@app.route('/modifierClasse/modifier/<int:id>', methods=['GET', 'POST'])
def modifierClasse(id):
    classe = db_session.query(Classe).get(id)
    if not classe:
        flash("Classe introuvable", "danger")
        return redirect(url_for('afficherGroupeClasse'))

    if request.method == 'POST':
        classe.nomClasse = request.form.get('nomClasse')
        classe.quota = request.form.get('quota')
        try:
            db_session.commit()
            flash("Classe modifiée avec succès", "success")
            return redirect(url_for('afficherGroupeClasse'))
        except Exception as e:
            db_session.rollback()
            flash(f"Erreur lors de la modification : {e}", "danger")
    return render_template('modifierClasse.html', classe=classe)

@app.route('/supprimer/<string:type>/<int:id>', methods=['GET'])
def supprimer_element(type, id):
    try:
        if type == 'groupe':
            element = db_session.query(Groupe).get(id)
            if not element:
                flash("Groupe introuvable", "danger")
                return redirect(url_for('affichageGroupeClasse'))
        elif type == 'classe':
            element = db_session.query(Classe).get(id)
            if not element:
                flash("Classe introuvable", "danger")
                return redirect(url_for('affichageGroupeClasse'))
        else:
            flash("Type invalide", "danger")
            return redirect(url_for('affichageGroupeClasse'))

        db_session.delete(element)
        db_session.commit()
        flash(f"{type.capitalize()} supprimé avec succès", "success")
    except Exception as e:
        db_session.rollback()
        flash(f"Erreur lors de la suppression : {e}", "danger")

    return redirect(url_for('affichageGroupeClasse'))

#########################################################################################################

#Activite

@app.route('/activite/')
def activite():
    activites = db_session.query(Activite).all()
    return render_template('activite.html', activites=activites)

#ajouter

@app.route('/activite/ajouter', methods=['GET', 'POST'])
def ajouter_activite():
    if request.method == 'POST':
        nom = request.form.get('nom')
        description = request.form.get('description')

        nouvelle_activite = Activite(nom=nom, description=description)

        try:
            db_session.add(nouvelle_activite)
            db_session.commit()
            flash("Activité ajoutée avec succès", "success")
            return redirect(url_for('activite'))
        except Exception as e:
            db_session.rollback()
            flash(f"Erreur lors de l'ajout de l'activité : {e}", "danger")

    return render_template('ajouter_activite.html')

#modifier

@app.route('/activite/modifier/<int:id>', methods=['GET', 'POST'])
def modifier_activite(id):
    activite = db_session.query(Activite).get(id)
    if not activite:
        flash("Activité introuvable", "danger")
        return redirect(url_for('activite'))

    if request.method == 'POST':
        activite.nom = request.form.get('nom')
        activite.description = request.form.get('description')

        try:
            db_session.commit()
            flash("Activité modifiée avec succès", "success")
            return redirect(url_for('activite'))
        except Exception as e:
            db_session.rollback()
            flash(f"Erreur lors de la modification : {e}", "danger")

    return render_template('modifier_activite.html', activite=activite)

#supprimer

@app.route('/activite/supprimer/<int:id>', methods=['GET'])
def supprimer_activite(id):
    activite = db_session.query(Activite).get(id)
    if not activite:
        flash("Activité introuvable", "danger")
        return redirect(url_for('activite'))

    try:
        db_session.delete(activite)
        db_session.commit()
        flash("Activité supprimée avec succès", "success")
    except Exception as e:
        db_session.rollback()
        flash(f"Erreur lors de la suppression : {e}", "danger")

    return redirect(url_for('activite'))

#########################################################################################################

#Planning

# Affichage de la liste des plannings
@app.route("/planningGarde/")
def planningGarde():
    plannings = db_session.query(PlanningGarde).order_by(PlanningGarde.date.desc()).all()
    return render_template("planningGarde.html", plannings=plannings)

# Affichage du formulaire d'ajout
@app.route("/ajouterPlanning", methods=["GET", "POST"])
def ajouter_planning():
    if request.method == "POST":
        date = request.form.get("date")
        heure_debut = request.form.get("heureDebut")
        heure_fin = request.form.get("heureFin")
        rapport = request.form.get("rapport")

        try:
            nouveau = PlanningGarde(
                date=datetime.strptime(date, "%Y-%m-%d").date(),
                heureDebut=datetime.strptime(heure_debut, "%H:%M").time(),
                heureFin=datetime.strptime(heure_fin, "%H:%M").time(),
                RapportDuJour=rapport
            )
            db_session.add(nouveau)
            db_session.commit()
            flash("Planning ajouté avec succès", "success")
        except Exception as e:
            db_session.rollback()
            flash(f"Erreur : {e}", "danger")

        return redirect(url_for("planningGarde"))

    return render_template("ajouter_planning.html")

# Modification d’un planning
@app.route("/modifierPlanning/<int:id>", methods=["GET", "POST"])
def modifier_planning(id):
    planning = db_session.query(PlanningGarde).get(id)
    if not planning:
        flash("Planning introuvable", "danger")
        return redirect(url_for("planningGarde"))

    if request.method == "POST":
        try:
            planning.date = datetime.strptime(request.form.get("date"), "%Y-%m-%d").date()
            # planning.heureDebut = datetime.strptime(request.form.get("heureDebut"), "%H:%M").time()
            planning.heure_debut = datetime.strptime(request.form.get('heureDebut'), '%H:%M:%S').time()
            planning.heure_fin = datetime.strptime(request.form.get('heureFin'), '%H:%M:%S').time()
            # planning.heureFin = datetime.strptime(request.form.get("heureFin"), "%H:%M").time()
            planning.RapportDuJour = request.form.get("rapport")

            db_session.commit()
            flash("Planning modifié avec succès", "success")
        except Exception as e:
            db_session.rollback()
            flash(f"Erreur : {e}", "danger")

        return redirect(url_for("planningGarde"))

    return render_template("modifier_planning.html", planning=planning)

# Suppression d’un planning
@app.route("/supprimerPlanning/<int:id>")
def supprimer_planning(id):
    planning = db_session.query(PlanningGarde).get(id)
    if not planning:
        flash("Planning introuvable", "danger")
    else:
        try:
            db_session.delete(planning)
            db_session.commit()
            flash("Planning supprimé avec succès", "success")
        except Exception as e:
            db_session.rollback()
            flash(f"Erreur : {e}", "danger")

    return redirect(url_for("planningGarde"))

if __name__ == '__main__':
    app.run(debug=True)
