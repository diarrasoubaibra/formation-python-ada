# Fonctions de gestion des utilisateurs
import time
from menus import afficherSousMenuUtil, accueil
from models.utilisateur import Utilisateur
import bcrypt

def ajouterUtilisateur():
    pseudo = input("Entrez le pseudo : ")
    motDePasse = input("Entrez le mot de passe : ")
    hash_mdp = bcrypt.hashpw(motDePasse.encode('utf-8'), bcrypt.gensalt())
    utilisateur = Utilisateur.ajouterCompte(pseudo, hash_mdp)  # Pas besoin de dateCreation
    print(utilisateur)

def supprimerUtilisateur():
    pseudo = input("Entrez le pseudo de l'utilisateur à supprimer : ")
    if not Utilisateur.supprimerCompte(pseudo):
        print(f"L'utilisateur {pseudo} n'existe pas.")

def modifierUtilisateur():
    pseudo = input("Entrez le pseudo de l'utilisateur dont vous voulez modifier le mot de passe : ")
    utilisateur = Utilisateur.recuperer_utilisateur(pseudo)  
    if utilisateur:
        nouveauMotDePasse =  bcrypt.hashpw(input("Entrez le nouveau mot de passe : ").encode('utf-8'), bcrypt.gensalt())
        utilisateur.modifierMotDePasse(nouveauMotDePasse)
    else:
        print(f"L'utilisateur {pseudo} n'existe pas.")

def listerUtilisateurs():
    Utilisateur.listerUtilisateurs()

def gestionUtilisateurs():
    accueil("GESTION DES UTILISATEURS")
    while True:
        afficherSousMenuUtil()
        try:
            choix = int(input("Choisissez une option dans le menu : "))
        except ValueError:
            print('Vous devez entrer un chiffre du menu !!')
            time.sleep(0.5)
            continue

        match choix:
            case 1:
                ajouterUtilisateur()
            case 2:
                supprimerUtilisateur()
            case 3:
                modifierUtilisateur()
            case 4:
                listerUtilisateurs()               
            case 5:
                break             
            case 0:
                return                   
            case _:
                print("Option invalide, veuillez réessayer !!")
                time.sleep(0.5)
                continue