from models.personne import Personne
from Professeur.ICrudProfesseur import ICRUDProfesseur
from Professeur.IEducation import IEducation


class Professeur(Personne, IEducation, ICRUDProfesseur):
    """
        Classe représentant un professeur, héritant de Personne et implémentant des interfaces éducatives.
    """

    __professeurs = []
    
    # Initialise un nouveau professeur avec ses informations personnelles et ses responsabilités.
    def __init__(self, dateNaissance, ville, prenom, nom, telephone, vacant, matiereEnseigne, prochainCours, sujetProchaineReunion):
        super().__init__(dateNaissance, ville, prenom, nom, telephone)
        self.__vacant = vacant
        self.__matiereEnseigne = matiereEnseigne
        self.__prochainCours = prochainCours
        self.__sujetProchaineReunion = sujetProchaineReunion

    # Retourne une représentation sous forme de chaîne du professeur.
    def __str__(self):
        statut_affiche = "Oui" if self.__vacant else "Non"
        return f"Professeur n° {self.id} : {self.nom} {self.prenom}, née le {self.date_naissance} à {self.ville}, numéro de téléphone : {self.telephone}, vacant: {statut_affiche}, enseigne {self.__matiereEnseigne}"

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
  
    # Retourne un message indiquant la matière enseignée par le professeur.
    def enseigner(self, matiere):
        self.__matiereEnseigne = matiere
        return f"Enseigne la matière {self.__matiereEnseigne}"
    
    # Retourne un message indiquant le sujet du prochain cours à préparer.
    def preparerCours(self, cours):
        self.__prochainCours = cours
        return f"Prépare le contenu d'un cours sur le sujet {self.__prochainCours}"
    
    # Retourne un message indiquant le sujet de la prochaine réunion à laquelle le professeur doit assister.
    def assisterReunion(self, sujet):
        self.__sujetProchaineReunion = sujet
        return f"Doit assister à une reunion sur {self.__sujetProchaineReunion}"

    # Implémentation des méthodes CRUD
    def ajouter(professeur):
        Professeur.__professeurs.append(professeur)

    def modifier(professeur):
        for index, prof_existe in enumerate(Professeur.__professeurs):
            if prof_existe.id == professeur.id:
                Professeur.__professeurs[index] = professeur
                return True 
        return False

    def supprimer(identifiant):
        for index, prof in enumerate(Professeur.__professeurs):
            if prof.id == identifiant:
                del Professeur.__professeurs[index]
                return True
        return False

    def obtenir_professeur():
        return [str(prof) for prof in Professeur.__professeurs]

    def obtenir(identifiant):
        for prof in Professeur.__professeurs:
            if prof.id == identifiant:
                return prof
        return None