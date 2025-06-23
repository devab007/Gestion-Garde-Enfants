from sqlalchemy import Column, Integer, String, BigInteger, Date, Time, Boolean, ForeignKey, Float, Text
from sqlalchemy.orm import relationship, declarative_base         #ces deux lignes servent à préparer l'utilisation de sqlalchemy pour créer des modèles. Ca importe des classes utiles pour l'importation de la base de donnée

Base = declarative_base()       #c'est pour  initialiser la base des modèles SQLAlchemy. Obligatoire !!! Toutes tes classes de tables hériteront de Base.

class Parent(Base): #Base: fonction fournie par SQLAlchemy qui crée une classe de base à partir de laquelle tous tes modèles (tables) vont hériter.
  __tablename__ = 'Parent'  #nom de la table

  id= Column(Integer, primary_key=True, autoincrement=True)       #Column c'est pour définir les colonnes d'une table
  prenomPere = Column(String(50))
  nomPere = Column(String(50))
  numeroCarteIdentite= Column(BigInteger, unique=True, index=True)
  email = Column(String(50), unique=True, index=True)
  adresse = Column(String(50))
  prenomMere = Column(String(50))
  nomMere = Column(String(50))

  enfants = relationship("Enfant", back_populates="parent") #"Enfant": nom classe, "parent": nom attribut
  factures = relationship("Facture", back_populates="parent") #back_populates permet de faire le lien dans les deux sens.
  telephones = relationship("Telephone", back_populates="parent")


class Enfant(Base):
  __tablename__ = 'Enfant'

  id = Column(Integer, primary_key=True, autoincrement=True)
  nom = Column(String(50))
  prenom = Column(String(50))
  dateNaissance = Column(Date)
  sexe = Column(Boolean)
  prenomTuteur = Column(String(50))
  nomTuteur = Column(String(50))
  infoSante = Column(Text)

  id_groupe = Column(Integer, ForeignKey("Groupe.id")) 
  id_classe = Column(Integer, ForeignKey("Classe.id"))
  id_parent = Column(Integer, ForeignKey("Parent.id"))

  parent = relationship("Parent", back_populates="enfants")
  presences = relationship("Presence", back_populates="enfant")
  activites = relationship("Activite", secondary='faire', back_populates="enfants")
  inscriptions = relationship("Inscription", back_populates="enfant")
  groupe = relationship("Groupe", back_populates="enfants")
  classe = relationship("Classe", back_populates="enfants")

class Employe(Base):
  __tablename__ = 'Employe'

  id = Column(Integer, primary_key=True, autoincrement=True)
  prenom = Column(String(50), index=True)
  nom = Column(String(50))
  matricule = Column(String(50), unique=True, index=True)
  dateNaissance = Column(Date)
  sexe = Column(Boolean)
  email = Column(String(50), unique=True, index=True)
  dateEmbauche = Column(Date)

  telephones = relationship("Telephone", back_populates="employe")
  specialites = relationship("Specialite", secondary='estSpecialise', back_populates="employes")
  utilisateurs = relationship("Utilisateur", back_populates="employe")

class Facture(Base):
  __tablename__ = 'Facture'

  id = Column(Integer, primary_key=True, autoincrement=True)
  libelle = Column(String(50))
  sommeTotal = Column(Float)
  numeroFacture = Column(Integer, unique=True)
  dateFacture = Column(Date)
  statut= Column(String(50))
  enfant = Column(String(350))

  id_parent = Column(Integer, ForeignKey("Parent.id"))

  parent = relationship("Parent", back_populates="factures")
  payements = relationship("Payement", back_populates="facture")

class Presence(Base):
  __tablename__ = 'Presence'

  id = Column(Integer, primary_key=True, autoincrement=True)
  date = Column(Date)
  statut = Column(String(50))

  id_enfant = Column(Integer, ForeignKey("Enfant.id"))

  enfant = relationship("Enfant", back_populates="presences")

class Activite(Base):
  __tablename__ = 'Activite'

  id = Column(Integer, primary_key=True, autoincrement=True)
  nom = Column(String(50))
  description = Column(String(50))

  enfants = relationship("Enfant", secondary='faire', back_populates="activites")

class Inscription(Base):
  __tablename__ = 'Inscription'

  id = Column(Integer, primary_key=True, autoincrement=True)
  dateInscription = Column(Date)
  anneeScolaire = Column(Date)

  id_enfant = Column(Integer, ForeignKey("Enfant.id"))

  enfant = relationship("Enfant", back_populates="inscriptions")

class Groupe(Base):
  __tablename__ = 'Groupe'

  id = Column(Integer, primary_key=True, autoincrement=True)
  nomGroupe = Column(String(50))
  trancheAge = Column(String(50))
  numero = Column(Integer)
  capaciteMax = Column(Integer)

  enfants = relationship("Enfant", back_populates="groupe")

class Classe(Base):
  __tablename__ = 'Classe'

  id = Column(Integer, primary_key=True, autoincrement=True)
  nomClasse = Column(String(50), unique=True)
  quota = Column(Integer)

  enfants = relationship("Enfant", back_populates="classe")

class PlanningGarde(Base):
  __tablename__ = 'PlanningGarde'

  id = Column(Integer, primary_key=True, autoincrement=True)
  date = Column(Date)
  heureDebut = Column(Time)
  heureFin = Column(Time)
  RapportDuJour = Column(Text)

  id_utilisateur = Column(Integer, ForeignKey("Utilisateur.id"))

  utilisateur = relationship("Utilisateur", back_populates="plannings_garde")


class ModePayement(Base):
  __tablename__ = 'ModePayement'

  id = Column(Integer, primary_key=True, autoincrement=True)

  payements = relationship("Payement", back_populates="modePayement")

class Specialite(Base):
  __tablename__ = 'Specialite'

  id = Column(Integer, primary_key=True, autoincrement=True)
  nomRole = Column(String(50))
  description = Column(String(50))

  employes = relationship("Employe", secondary='estSpecialise', back_populates="specialites")

class Utilisateur(Base):
  __tablename__ = 'Utilisateur'

  id = Column(Integer, primary_key=True, autoincrement=True)
  prenom = Column(String(50))
  email = Column(String(50), unique=True, index=True)
  username = Column(String(50), unique=True)
  motdepasse = Column(String(250))
  # role = Column()

  id_employe = Column(Integer, ForeignKey("Employe.id"))

  plannings_garde = relationship("PlanningGarde", back_populates="utilisateur")
  employe = relationship("Employe", back_populates="utilisateurs")

class Payement(Base):
  __tablename__ = 'Payement'

  id = Column(Integer, primary_key=True, autoincrement=True)
  numeroPayement = Column(Integer, unique=True, index=True)
  datePayement = Column(Date)
  montantPayement = Column(Float)

  id_facture = Column(Integer, ForeignKey("Facture.id"))
  id_modepayement = Column(Integer, ForeignKey("ModePayement.id"))

  facture = relationship("Facture", back_populates="payements")
  modePayement = relationship("ModePayement", back_populates="payements")

class Telephone(Base):
  __tablename__ = 'Telephone'

  id = Column(Integer, primary_key=True, autoincrement=True)
  numero = Column(BigInteger, unique=True)
  nomProprietaire = Column(String(50))

  id_parent = Column(Integer, ForeignKey("Parent.id"))
  id_employe = Column(Integer, ForeignKey("Employe.id"))

  parent = relationship("Parent", back_populates="telephones")
  employe = relationship("Employe", back_populates="telephones")

class Faire(Base):
  __tablename__ = 'faire'

  id_enfant = Column(Integer, ForeignKey("Enfant.id"), primary_key=True)
  id_activite = Column(Integer, ForeignKey("Activite.id"), primary_key=True)


class EstSpecialise(Base):
  __tablename__ = 'estSpecialise'

  id_employe = Column(Integer, ForeignKey("Employe.id"), primary_key=True)
  id_specialite = Column(Integer, ForeignKey("Specialite.id"), primary_key=True)