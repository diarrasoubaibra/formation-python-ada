import time
from menus import afficherSousMenuElev, accueil
from Eleve.eleve import Eleve

def ajouterEleve():
    dateNaissance = input("Entrez la date de naissance (YYYY-MM-DD) : ")
    ville = input("Entrez la ville : ")
    prenom = input("Entrez le prénom : ")
    nom = input("Entrez le nom : ")
    telephone = input("Entrez le numéro de téléphone : ")
    classe = input("Entrez la classe : ")
    matricule = input("Entrez le matricule : ")

    eleve = Eleve(dateNaissance, ville, prenom, nom, telephone, classe, matricule)
    Eleve.ajouter(eleve)
    print(f"Élève {prenom} {nom} ajouté avec succès.")

def listerEleves():
    eleves = Eleve.obtenirEleve()
    if eleves:
        print("Liste des élèves :")
        for eleve in eleves:
            print(eleve)
    else:
        print("Aucun élève enregistré.")

def modifierEleve():
    matricule = input("Entrez le matricule de l'élève à modifier : ")
    eleve = Eleve.obtenir(matricule)
    if eleve:
        print(f"Modification de l'élève : {eleve}")
        while True:
            print("\nQue souhaitez-vous modifier ?")
            print("1. Date de naissance")
            print("2. Ville")
            print("3. Prénom")
            print("4. Nom")
            print("5. Téléphone")
            print("6. Classe")
            print("7. Quitter")

            choix = input("Entrez le numéro de l'option : ")

            if choix == '1':
                nouvelle_date_naissance = input(f"Nouvelle date de naissance (YYYY-MM-DD) : ") or eleve.get_date_naissance
                eleve.set_date_naissance(nouvelle_date_naissance)
                print(f"Date de naissance mise à jour : {eleve.get_date_naissance}")

            elif choix == '2':
                nouvelle_ville = input(f"Nouvelle ville : ") or eleve.get_ville
                eleve.set_ville(nouvelle_ville)
                print(f"Ville mise à jour : {eleve.get_ville}")

            elif choix == '3':
                nouveau_prenom = input(f"Nouveau prénom : ") or eleve.get_prenom
                eleve.set_prenom(nouveau_prenom)
                print(f"Prénom mis à jour : {eleve.get_prenom}")

            elif choix == '4':
                nouveau_nom = input(f"Nouveau nom : ") or eleve.get_nom
                eleve.set_nom(nouveau_nom)
                print(f"Nom mis à jour : {eleve.get_nom}")

            elif choix == '5':
                nouveau_telephone = input(f"Nouveau téléphone : ") or eleve.get_telephone
                eleve.set_telephone(nouveau_telephone)
                print(f"Téléphone mis à jour : {eleve.get_telephone}")

            elif choix == '6':
                nouvelle_classe = input(f"Nouvelle classe : ") or eleve.get_classe
                eleve.set_classe(nouvelle_classe)
                print(f"Classe mise à jour : {eleve.get_classe}")

            elif choix == '7':
                print("Modification terminée.")
                break

            else:
                print("Option invalide. Veuillez réessayer.")

        # Sauvegarde des modifications
        Eleve.modifier(eleve)
        print(f"Erreur lors de la sauvegarde des modifications pour l'élève {eleve.get_nom} {eleve.get_prenom}.")
    else:
        print(f"Aucun élève trouvé avec le matricule {matricule}.")



def supprimerEleve():
    matricule = input("Entrez le matricule de l'élève à supprimer : ")
    if Eleve.supprimer(matricule):
        print(f"Élève avec matricule {matricule} supprimé avec succès.")
    else:
        print(f"Aucun élève trouvé avec le matricule {matricule}.")

def gestionEleves():
    accueil("GESTION DES ÉLÈVES")
    while True:
        afficherSousMenuElev()
        try:
            choix = int(input("\033[0;37mChoisissez une option dans le menu : \033[0m"))
        except ValueError:
            print('\033[0;93mVous devez entrer un chiffre du menu !!\033[0m')
            time.sleep(0.5)
            continue

        match choix:
            case 1:
                ajouterEleve()
            case 2:
                supprimerEleve()
            case 3:
                modifierEleve()
            case 4:
                listerEleves()               
            case 5:
                break             
            case 0:
                return                   
            case _:
                print("\033[0;93mOption invalide, veuillez réessayer !!\033[0m")
                time.sleep(0.5)
                continue