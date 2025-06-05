Pour la connexion à la base de donnée vous devez déjà avoir installé toutes les dépendances (postgres, SQLAlchemy, ...)
Vous entrez dans pg admin 4 (l'application de postgres) vous allez dans serveur puis database vous faites clique droit puis create pour le nom mettez garderie_enfants
Dans config.py si votre mot de passe est différent de passer vous devez modifier la 5e ligne la partie où j'ai mis "postgres:passer" vous changer le mot de passe "passer" par celui que vous aviez mis pour votre postgres ensuite vous lancez config.py sur le cmd et ça devrait marcher
