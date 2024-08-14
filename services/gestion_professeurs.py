import time
from menus import afficherSousMenuProf, accueil
from Professeur.professeur import Professeur

def ajouterProfesseur():
    dateNaissance = input("Entrez la date de naissance (YYYY-MM-DD) : ")
    ville = input("Entrez la ville : ")
    prenom = input("Entrez le prénom : ")
    nom = input("Entrez le nom : ")
    telephone = input("Entrez le numéro de téléphone : ")
    vacant = input("Est-ce vacant ? (oui/non) : ").lower() == 'oui'
    matiereEnseigne = input("Entrez la matière enseignée : ")
    prochainCours = input("Entrez le sujet du prochain cours : ")
    sujetProchaineReunion = input("Entrez le sujet de la prochaine réunion : ")

    professeur = Professeur(dateNaissance, ville, prenom, nom, telephone, vacant, matiereEnseigne, prochainCours, sujetProchaineReunion)
    Professeur.ajouter(professeur)
    print(f"Professeur {prenom} {nom} ajouté avec succès.")

def listerProfesseurs():
    professeurs = Professeur.obtenirProfesseur()  
    if professeurs:
        for prof in professeurs:
            print(prof)
    else:
        print("Aucun professeur trouvé.")


def modifierProfesseur():
    identifiant = input("Entrez l'identifiant du professeur à modifier : ")
    professeur = Professeur.obtenir(identifiant)
    if professeur:
        # Demande de nouvelles valeurs pour les champs du professeur
        nouveau_vacant = input("Le professeur est-il vacant ? (Oui/Non) : ").lower() == 'oui'
        nouvelle_matiere = input("Entrez la nouvelle matière enseignée : ")
        nouveau_cours = input("Entrez le sujet du prochain cours : ")
        nouveau_sujet_reunion = input("Entrez le sujet de la prochaine réunion : ")
        
        professeur.set_vacant(nouveau_vacant)
        professeur.set_matiereEnseigne(nouvelle_matiere)
        professeur.set_prochainCours(nouveau_cours)
        professeur.set_sujetProchaineReunion(nouveau_sujet_reunion)
        
        if Professeur.modifier(professeur):
            print("Professeur modifié avec succès.")
        else:
            print("Échec de la modification du professeur.")
    else:
        print(f"Aucun professeur trouvé avec l'identifiant {identifiant}.")


def supprimerProfesseur():
    identifiant = int(input("Entrez l'identifiant du professeur à supprimer : "))
    if Professeur.supprimer(identifiant):
        print(f"Professeur avec identifiant {identifiant} supprimé avec succès.")
    else:
        print(f"Aucun professeur trouvé avec l'identifiant {identifiant}.")

def gestionProfesseurs():
    accueil("GESTION DES PROFESSEURS")
    while True:
        afficherSousMenuProf()
        try:
            choix = int(input("\033[0;37mChoisissez une option dans le menu : \033[0m"))
        except ValueError:
            print('\033[0;93mVous devez entrer un chiffre du menu !!\033[0m')
            time.sleep(0.5)
            continue

        match choix:
            case 1:
                ajouterProfesseur()
            case 2:
                supprimerProfesseur()
            case 3:
                modifierProfesseur()
            case 4:
                listerProfesseurs()               
            case 5:
                break             
            case 0:
                return                   
            case _:
                print("\033[0;93mOption invalide, veuillez réessayer !!\033[0m")
                time.sleep(0.5)
                continue