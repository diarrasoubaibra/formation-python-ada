import mysql.connector
from models.personne import Personne
from Eleve.ICrudEleve import ICRUDEleve
from base import db

class Eleve(Personne, ICRUDEleve):
    """
    Classe représentant un élève, héritant de la classe Personne et de l'interface ICRUDEleve.
    """

    def __init__(self, dateNaissance, ville, prenom, nom, telephone, classe, matricule):
        super().__init__(dateNaissance, ville, prenom, nom, telephone)
        self.__classe = classe
        self.__matricule = matricule

    def __str__(self):
        return (f"Eleve n° {self.get_id} : {self.get_nom} {self.get_prenom}, "
                f"née le {self.get_date_naissance} à {self.get_ville}, "
                f"classe: {self.__classe}, matricule: {self.__matricule}, "
                f"téléphone: {self.get_telephone}")

    @property
    def get_matricule(self):
        return self.__matricule
    
    @property 
    def get_classe(self):
        return self.__classe

    @get_classe.setter
    def set_classe(self, classe):
        self.__classe = classe            


    @get_matricule.setter
    def set_matricule(self, matricule):
        self.__matricule = matricule

    # Implémentation des méthodes CRUD
    @staticmethod
    def ajouter(eleve):
        conn = db.create_connection(database='etab_db')
        if conn:
            try:
                cursor = conn.cursor()

                cursor.execute(
                    "SELECT id FROM personnes WHERE prenom = %s AND nom = %s AND date_naissance = %s",
                    (eleve.get_prenom, eleve.get_nom, eleve.get_date_naissance)
                )
                personne = cursor.fetchone()

                if personne:
                    id_personne = personne[0]
                else:
                    cursor.execute(
                        "INSERT INTO personnes (prenom, nom, date_naissance, ville, telephone) VALUES (%s, %s, %s, %s, %s)",
                        (eleve.get_prenom, eleve.get_nom, eleve.get_date_naissance, eleve.get_ville, eleve.get_telephone)
                    )
                    id_personne = cursor.lastrowid

                query = ("INSERT INTO eleves (id_personne, classe, matricule) VALUES (%s, %s, %s)")
                cursor.execute(query, (id_personne, eleve.get_classe, eleve.get_matricule))
                conn.commit()
                print(f"Élève {eleve.get_nom} {eleve.get_prenom} ajouté avec succès.")
            except mysql.connector.Error as e:
                print(f"Erreur lors de l'ajout de l'élève: {e}")
                conn.rollback()
            finally:
                cursor.close()
                conn.close()

    @staticmethod
    def modifier(eleve):
        """Modifie les informations de l'élève et de la personne correspondante dans la base de données."""
        conn = db.create_connection(database='etab_db')
        if conn:
            try:
                cursor = conn.cursor()
                
                # Mise à jour des informations dans la table personnes
                query_personne = ("UPDATE personnes SET date_naissance = %s, ville = %s, prenom = %s, nom = %s, telephone = %s "
                                  "WHERE id = (SELECT id_personne FROM eleves WHERE matricule = %s)")
                cursor.execute(query_personne, (eleve.get_date_naissance, eleve.get_ville, eleve.get_prenom, eleve.get_nom, eleve.get_telephone, eleve.get_matricule))
                
                # Mise à jour des informations dans la table eleves
                query_eleve = ("UPDATE eleves SET classe = %s WHERE matricule = %s")
                cursor.execute(query_eleve, (eleve.get_classe, eleve.get_matricule))
                
                conn.commit()
                print(f"Élève {eleve.get_nom} {eleve.get_prenom} modifié avec succès.")
                return True
            except mysql.connector.Error as e:
                print(f"Erreur lors de la modification de l'élève : {e}")
                conn.rollback()
                return False
            finally:
                cursor.close()
                conn.close()
        return False


    @staticmethod
    def supprimer(identifiant):
        conn = db.create_connection(database='etab_db')
        if conn:
            try:
                cursor = conn.cursor()
                query = "DELETE FROM eleves WHERE matricule = %s"
                cursor.execute(query, (identifiant,))
                conn.commit()
                print(f"Élève avec matricule {identifiant} supprimé avec succès.")
                return cursor.rowcount > 0
            except mysql.connector.Error as e:
                print(f"Erreur lors de la suppression de l'élève: {e}")
                conn.rollback()
                return False
            finally:
                cursor.close()
                conn.close()

    @staticmethod
    def obtenirEleve():
        conn = db.create_connection(database='etab_db')
        if conn:
            try:
                cursor = conn.cursor()
                query = ("SELECT p.id, p.prenom, p.nom, p.date_naissance, p.ville, p.telephone, "
                         "e.classe, e.matricule "
                         "FROM personnes p JOIN eleves e ON p.id = e.id_personne")
                cursor.execute(query)
                eleves = cursor.fetchall()
                return [f"ID: {eleve[0]}, Prénom: {eleve[1]}, Nom: {eleve[2]}, Date de naissance: {eleve[3]}, "
                        f"Ville: {eleve[4]}, Téléphone: {eleve[5]}, Classe: {eleve[6]}, Matricule: {eleve[7]}"
                        for eleve in eleves]
            except mysql.connector.Error as e:
                print(f"Erreur lors de la récupération des élèves: {e}")
                return []
            finally:
                cursor.close()
                conn.close()

    @staticmethod
    def obtenir(identifiant):
        conn = db.create_connection(database='etab_db')
        if conn:
            try:
                cursor = conn.cursor()
                query = ("SELECT p.id, p.prenom, p.nom, p.date_naissance, p.ville, p.telephone, "
                         "e.classe, e.matricule "
                         "FROM personnes p JOIN eleves e ON p.id = e.id_personne "
                         "WHERE e.matricule = %s")
                cursor.execute(query, (identifiant,))
                eleve = cursor.fetchone()
                if eleve:
                    return Eleve(eleve[3], eleve[4], eleve[1], eleve[2], eleve[5], eleve[6], eleve[7])
                return None
            except mysql.connector.Error as e:
                print(f"Erreur lors de la récupération de l'élève: {e}")
                return None
            finally:
                cursor.close()
                conn.close()
