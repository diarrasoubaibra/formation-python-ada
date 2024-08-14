import mysql.connector
import bcrypt
from mysql.connector import Error
import time

def create_connection(database=None):
    """Crée une connexion au serveur MySQL, avec ou sans une base de données spécifiée."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''
            # Connexion sans base de données spécifique par défaut
        )
        if database:
            connection.database = database  # Sélectionne la base de données si spécifiée
        return connection
    except Error as e:
        print(f"Erreur de connexion: {e}")
        return None

def create_database(curseur):
    """Crée la base de données 'etab_db' si elle n'existe pas déjà."""
    try:
        curseur.execute("CREATE DATABASE IF NOT EXISTS etab_db;")
        print("Base de données 'etab_db' créée ou déjà existante.")
    except Error as e:
        print(f"Erreur lors de la création de la base de données: {e}")

def create_tables(curseur):
    """Crée les tables nécessaires dans la base de données 'etab_db'."""
    curseur.execute("USE etab_db;")  # Sélectionne la base de données

    # Liste des requêtes SQL pour créer les tables nécessaires
    tables = [
        """
        CREATE TABLE IF NOT EXISTS utilisateurs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            pseudo VARCHAR(50) NOT NULL UNIQUE,
            mot_de_passe VARCHAR(255) NOT NULL,
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS personnes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            date_naissance DATE NOT NULL,
            ville VARCHAR(100) NOT NULL,
            prenom VARCHAR(50) NOT NULL,
            nom VARCHAR(50) NOT NULL,
            telephone VARCHAR(15) NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS eleves (
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_personne INT,
            classe VARCHAR(50),
            matricule VARCHAR(50) UNIQUE,
            FOREIGN KEY (id_personne) REFERENCES personnes(id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS professeurs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_personne INT,
            vacant BOOLEAN,
            matiere_enseigne VARCHAR(100),
            prochain_cours VARCHAR(100),
            sujet_prochaine_reunion VARCHAR(100),
            FOREIGN KEY (id_personne) REFERENCES personnes(id)
        );
        """
    ]

    # Exécution de chaque requête pour créer les tables
    for table in tables:
        curseur.execute(table)
    print("Tables créées ou déjà existantes.")

def setup_admin_user(curseur):
    """Vérifie et ajoute l'utilisateur administrateur par défaut si nécessaire."""
    pseudo_admin = 'admin'
    mot_de_passe_admin = bcrypt.hashpw('admin'.encode('utf-8'), bcrypt.gensalt())

    # Vérifie si l'utilisateur administrateur existe déjà
    curseur.execute("SELECT * FROM utilisateurs WHERE pseudo = %s", (pseudo_admin,))
    if curseur.fetchone() is None:
        # Ajoute l'utilisateur administrateur s'il n'existe pas
        curseur.execute("INSERT INTO utilisateurs (pseudo, mot_de_passe) VALUES (%s, %s);", (pseudo_admin, mot_de_passe_admin))
        print("Administrateur par défaut ajouté.")
    else:
        print("Administrateur par défaut déjà existant.")

def main():
    # Connexion initiale sans base de données
    connection = create_connection()
    if connection and connection.is_connected():
        print("CONNEXION RÉUSSIE AU SERVEUR")
    else:
        print("ÉCHEC DE CONNEXION AU SERVEUR")
        return

    if connection:  # Si la connexion est réussie
        try:
            curseur = connection.cursor()
            create_database(curseur)  # Crée la base de données si elle n'existe pas

            # Reconnexion à la base de données créée
            connection.database = 'etab_db'
            create_tables(curseur)  # Crée les tables nécessaires
            time.sleep(1)

            setup_admin_user(curseur)  # Ajoute l'utilisateur administrateur par défaut
            time.sleep(1)

            connection.commit()  # Valide les changements dans la base de données
        except Error as e:
            print(f"Erreur: {e}")
            connection.rollback()  # Annule les changements en cas d'erreur
        finally:
            if connection.is_connected():
                curseur.close()  # Ferme le curseur
                connection.close()  # Ferme la connexion

if __name__ == "__main__":
    main()
