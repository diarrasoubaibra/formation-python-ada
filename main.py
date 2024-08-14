import time
import bcrypt
from base import db
from menus import afficher_menu, accueil, quitter
from services import gestion_eleves, gestion_professeurs, gestion_utilisateurs

# Fonction pour récupérer un utilisateur depuis la base de données
def recuperer_utilisateur(identifiant):
    """Récupère un utilisateur de la base de données par son identifiant."""
    conn = db.create_connection(database="etab_db")
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT pseudo, mot_de_passe FROM utilisateurs WHERE pseudo = %s", (identifiant,))
        utilisateur = cursor.fetchone()
        cursor.close()
        conn.close()
        return utilisateur
    return None

def authentification():
    """Gère l'authentification de l'utilisateur."""
    identifiant = input("Entrez votre identifiant : ")
    mot_de_passe = input("Entrez votre mot de passe : ")
    
    utilisateur_data = recuperer_utilisateur(identifiant)
    
    if utilisateur_data and bcrypt.checkpw(mot_de_passe.encode('utf-8'), utilisateur_data[1].encode('utf-8')):
        print("Authentification réussie !!")
        return True
    else:
        print("Échec de l'authentification, veuillez vérifier les informations saisies !")
        return False

def menu_principal():
    """Affiche le menu principal et gère les choix de l'utilisateur."""
    while True:
        afficher_menu()
        try:
            choix = int(input("Choisissez une option dans le menu : "))
        except ValueError:
            print('Vous devez entrer un chiffre du menu !!')
            continue

        match choix:
            case 1:
                gestion_eleves.gestionEleves()
            case 2:
                gestion_professeurs.gestionProfesseurs()
            case 3:
                gestion_utilisateurs.gestionUtilisateurs()
            case 0:
                return "quit"  # Indique la sortie de l'application
            case _:
                print("Option invalide, veuillez réessayer !!")
                continue

def main():
    """Point d'entrée principal de l'application."""
    debut = time.time() 
    accueil("BIENVENUE DANS L'APPLICATION ETAB v1.3")

    if authentification():
        accueil("BIENVENUE DANS L'APPLICATION ETAB v1.3")
        if menu_principal() == "quit":
            quitter(debut)

if __name__ == "__main__":
    main()
