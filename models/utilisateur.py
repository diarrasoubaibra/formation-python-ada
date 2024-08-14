from datetime import datetime
from base import db
from base import req_utilisateur
import bcrypt

class Utilisateur:
    """
    Classe représentant un utilisateur avec un pseudo et un mot de passe.
    """
    __idUnique = 0

    def __init__(self, pseudo, motDePasse, dateCreation):
        """
        Initialise un nouvel utilisateur avec le pseudo, le mot de passe et la date de création.
        """
        Utilisateur.__idUnique += 1
        self.__id = Utilisateur.__idUnique
        self.__pseudo = pseudo
        self.__motDePasse = motDePasse
        self.__dateCreation = dateCreation

    def __str__(self):
        """
        Retourne une représentation sous forme de chaîne de l'utilisateur.
        """
        return f"Utilisateur n° {self.__id} : {self.__pseudo} créé le {self.__dateCreation}"

    @property
    def id(self):
        """Retourne l'identifiant unique de l'utilisateur."""
        return self.__id

    @property
    def pseudo(self):
        """Retourne le pseudo de l'utilisateur."""
        return self.__pseudo

    @property
    def dateCreation(self):
        """Retourne la date de création du compte de l'utilisateur."""
        return self.__dateCreation

    def nouveauMotDePasse(self, nouveauMotDePasse):
        """Modifie le mot de passe de l'utilisateur localement."""
        self.__motDePasse = nouveauMotDePasse

    def authentification(self, identifiant, motDePasse):
        """Vérifie si les identifiants fournis correspondent à ceux de l'utilisateur."""
        return self.__pseudo == identifiant and self.__motDePasse == motDePasse

    @classmethod
    def ajouterCompte(cls, pseudo, motDePasse):
        """Ajoute un nouvel utilisateur à la base de données."""
        dateCreation = datetime.now()
        nouvel_utilisateur = cls(pseudo, motDePasse, dateCreation)

        conn = db.create_connection(database='etab_db')
        if conn and conn.is_connected():
            try:
                curseur = conn.cursor()
                req_utilisateur.ajouter_utilisateur(curseur, pseudo, motDePasse)
                conn.commit()
                nouvel_utilisateur.__id = curseur.lastrowid  # Récupère l'ID de l'utilisateur créé
                return f"Compte créé avec succès !!\n-->Pseudo : {pseudo}"
            except Exception as e:
                print(f"Erreur lors de la création du compte : {e}")
            finally:
                curseur.close()
                conn.close()
        return "Échec de la connexion à la base de données."

    def modifierMotDePasse(self, nouveauMotDePasse):
        """Modifie le mot de passe de l'utilisateur dans la base de données."""
        self.__motDePasse = nouveauMotDePasse

        conn = db.create_connection(database='etab_db')
        if conn and conn.is_connected():
            try:
                curseur = conn.cursor()
                req_utilisateur.modifier_mot_de_passe(curseur, self.__pseudo, nouveauMotDePasse)
                conn.commit()
                print(f"Mot de passe modifié pour l'utilisateur {self.__pseudo}.")
            except Exception as e:
                print(f"Erreur lors de la modification du mot de passe : {e}")
            finally:
                curseur.close()
                conn.close()

    @classmethod
    def supprimerCompte(cls, pseudo):
        """Supprime un utilisateur de la base de données."""
        conn = db.create_connection(database='etab_db')
        if conn and conn.is_connected():
            try:
                curseur = conn.cursor()
                req_utilisateur.supprimer_utilisateur(curseur, pseudo)
                conn.commit()
                print(f"Utilisateur {pseudo} supprimé.")
            except Exception as e:
                print(f"Erreur lors de la suppression de l'utilisateur : {e}")
            finally:
                curseur.close()
                conn.close()

    @classmethod
    def listerUtilisateurs(cls):
        """Liste tous les utilisateurs de la base de données."""
        conn = db.create_connection(database='etab_db')
        utilisateurs = []
        if conn and conn.is_connected():
            try:
                curseur = conn.cursor()
                utilisateurs_db = req_utilisateur.lister_utilisateurs(curseur)
                for user in utilisateurs_db:
                    print(f"ID : {user[0]}, Pseudo : {user[1]}, Date de création : {user[2]}")
                    utilisateurs.append(user)  # Ajoute à la liste des utilisateurs
            except Exception as e:
                print(f"Erreur lors de la récupération des utilisateurs : {e}")
            finally:
                curseur.close()
                conn.close()
        return utilisateurs

    @classmethod
    def recuperer_utilisateur(cls, pseudo):
        """Récupère un utilisateur de la base de données par son pseudo."""
        conn = db.create_connection(database='etab_db')
        if conn and conn.is_connected():
            try:
                cursor = conn.cursor()
                result = req_utilisateur.recuperer_utilisateur(cursor, pseudo)
                if result:
                    return cls(result[0], result[1], result[2])
            except Exception as e:
                print(f"Erreur lors de la récupération de l'utilisateur : {e}")
            finally:
                cursor.close()
                conn.close()
        return None