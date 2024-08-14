import mysql.connector
from models.personne import Personne
from Professeur.ICrudProfesseur import ICRUDProfesseur
from Professeur.IEducation import IEducation
from base import db

class Professeur(Personne, IEducation, ICRUDProfesseur):
    """
    Classe représentant un professeur, héritant de Personne et implémentant des interfaces éducatives.
    """

    def __init__(self, dateNaissance, ville, prenom, nom, telephone, vacant, matiereEnseigne, prochainCours, sujetProchaineReunion):
        super().__init__(dateNaissance, ville, prenom, nom, telephone)
        self.__vacant = vacant
        self.__matiereEnseigne = matiereEnseigne
        self.__prochainCours = prochainCours
        self.__sujetProchaineReunion = sujetProchaineReunion

    def __str__(self):
        statut_affiche = "Oui" if self.__vacant else "Non"
        return (f"Professeur n° {self.get_id} : {self.get_nom} {self.get_prenom}, née le {self.get_date_naissance} à {self.get_ville}, "
                f"numéro de téléphone : {self.get_telephone}, vacant: {statut_affiche}, enseigne {self.__matiereEnseigne}")

    @property 
    def vacant(self):
        return self.__vacant
    
    @property 
    def matiereEnseigne(self):
        return self.__matiereEnseigne

    @property 
    def prochainCours(self):
        return self.__prochainCours
    
    @property 
    def sujetProchaineReunion(self):
        return self.__sujetProchaineReunion

    def set_sujetProchaineReunion(self, sujetProchaineReunion):
        self.__sujetProchaineReunion = sujetProchaineReunion            

    def set_prochainCours(self, prochainCours):
        self.__prochainCours = prochainCours

    def set_matiereEnseigne(self, matiereEnseigne):
        self.__matiereEnseigne = matiereEnseigne            

    def set_vacant(self, vacant):
        self.__vacant = vacant    
  
    def enseigner(self, matiere):
        """Retourne un message indiquant la matière enseignée par le professeur."""
        self.__matiereEnseigne = matiere
        return f"Enseigne la matière {self.__matiereEnseigne}"
    
    def preparerCours(self, cours):
        """Retourne un message indiquant le sujet du prochain cours à préparer."""
        self.__prochainCours = cours
        return f"Prépare le contenu d'un cours sur le sujet {self.__prochainCours}"
    
    def assisterReunion(self, sujet):
        """Retourne un message indiquant le sujet de la prochaine réunion à laquelle le professeur doit assister."""
        self.__sujetProchaineReunion = sujet
        return f"Doit assister à une réunion sur {self.__sujetProchaineReunion}"

    # Implémentation des méthodes CRUD
    @staticmethod
    def ajouter(professeur):
        """Ajoute un professeur à la base de données."""
        conn = db.create_connection(database='etab_db')
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO professeurs (id_personne, vacant, matiere_enseigne, prochain_cours, sujet_prochaine_reunion) "
                    "VALUES (%s, %s, %s, %s, %s)",
                    (professeur.get_id, professeur.vacant, professeur.matiereEnseigne, professeur.prochainCours, professeur.sujetProchaineReunion)
                )
                conn.commit()
                print(f"Professeur {professeur.get_nom} {professeur.get_prenom} ajouté avec succès.")
            except mysql.connector.Error as e:
                print(f"Erreur lors de l'ajout du professeur : {e}")
                conn.rollback()
            finally:
                cursor.close()
                conn.close()

    @staticmethod
    def modifier(professeur):
        """Modifie les informations d'un professeur dans la base de données."""
        conn = db.create_connection(database='etab_db')
        if conn:
            try:
                cursor = conn.cursor()

                # Mise à jour des informations dans la table personnes
                query_personne = (
                    "UPDATE personnes SET date_naissance = %s, ville = %s, prenom = %s, nom = %s, telephone = %s "
                    "WHERE id = %s"
                )
                cursor.execute(query_personne, (
                    professeur.get_date_naissance, professeur.get_ville, professeur.get_prenom, professeur.get_nom, professeur.get_telephone, professeur.get_id
                ))

                # Mise à jour des informations dans la table professeurs
                query_professeur = (
                    "UPDATE professeurs SET vacant = %s, matiere_enseigne = %s, prochain_cours = %s, sujet_prochaine_reunion = %s "
                    "WHERE id_personne = %s"
                )
                cursor.execute(query_professeur, (
                    professeur.vacant, professeur.matiereEnseigne, professeur.prochainCours, professeur.sujetProchaineReunion, professeur.get_id
                ))

                conn.commit()
                print(f"Professeur {professeur.get_nom} {professeur.get_prenom} modifié avec succès.")
                return cursor.rowcount > 0
            except mysql.connector.Error as e:
                print(f"Erreur lors de la modification du professeur : {e}")
                conn.rollback()
                return False
            finally:
                cursor.close()
                conn.close()
        return False


    @staticmethod
    def supprimer(identifiant):
        """Supprime un professeur de la base de données."""
        conn = db.create_connection(database='etab_db')
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM professeurs WHERE id_personne = %s", (identifiant,))
                conn.commit()
                print(f"Professeur avec ID {identifiant} supprimé avec succès.")
                return cursor.rowcount > 0
            except mysql.connector.Error as e:
                print(f"Erreur lors de la suppression du professeur : {e}")
                conn.rollback()
                return False
            finally:
                cursor.close()
                conn.close()

    @staticmethod
    def obtenirProfesseur():
        """Récupère tous les professeurs de la base de données."""
        conn = db.create_connection(database='etab_db')
        professeurs = []
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT p.id, p.prenom, p.nom, p.date_naissance, p.ville, p.telephone, "
                    "pr.vacant, pr.matiere_enseigne, pr.prochain_cours, pr.sujet_prochaine_reunion "
                    "FROM personnes p JOIN professeurs pr ON p.id = pr.id_personne"
                )
                for professeur in cursor.fetchall():
                    professeurs.append(Professeur(
                        professeur[3], professeur[4], professeur[1], professeur[2], professeur[5],
                        professeur[6], professeur[7], professeur[8], professeur[9]
                    ))
                return professeurs
            except mysql.connector.Error as e:
                print(f"Erreur lors de la récupération des professeurs : {e}")
            finally:
                cursor.close()
                conn.close()
        return professeurs

    @staticmethod
    def obtenir(identifiant):
        """Récupère un professeur par son identifiant."""
        conn = db.create_connection(database='etab_db')
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT p.id, p.prenom, p.nom, p.date_naissance, p.ville, p.telephone, "
                    "pr.vacant, pr.matiere_enseigne, pr.prochain_cours, pr.sujet_prochaine_reunion "
                    "FROM personnes p JOIN professeurs pr ON p.id = pr.id_personne "
                    "WHERE pr.id_personne = %s", (identifiant,)
                )
                professeur = cursor.fetchone()
                # Vérifie si le professeur existe, puis s'assure qu'il n'y a pas d'autres résultats non lus
                if professeur:
                    return Professeur(
                        professeur[3], professeur[4], professeur[1], professeur[2], professeur[5],
                        professeur[6], professeur[7], professeur[8], professeur[9]
                    )
                cursor.fetchall()  # Assure que tous les autres résultats sont consommés
            except mysql.connector.Error as e:
                print(f"Erreur lors de la récupération du professeur : {e}")
            finally:
                cursor.close()  # Ferme le curseur
                conn.close()  # Ferme la connexion
        return None
