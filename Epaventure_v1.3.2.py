#Minimum viable product du jeu "Epaventure spatiale"
# Contenu : Description d’ambiance et début du jeu
# Choix (1 seul)
# Obstacle (fixe) 1 ou 2
# Gain (fixe) 1 ou 2
# Description d’ambiance et début du jeu

#Import des librairies/Libraries import
import random
import os
import json 

#Variables
nom_perso = "Alain Connu"
score = 0
coriace = 0
fute = 0
und6 = 0
deuxd6 = 0
jet = 0

class Epaventure:  #Classe pour manipuler le jeu

    #Données / Dictionnaire de scènes
    #Partie basculée dans Aventure_scenes.json
    
    #Données / Résultats génériques de scènes (mécanique de fallback)
    resultats_generiques =  {
    "reussite": "Tu réussis parfaitement.",
    "partielle":"Tu réussis, mais avec une complication",
    "echec": "Tu échoues complètement."  
}
#==================
#Fonctions outils
#==================

    def ecran_propre(self):
        #Effacer le terminal
        os.system('cls' if os.name == 'nt' else 'clear')

#==================
#Moteur de jeu
#==================
    #Moteur de résolution
    def lancer_des(self, nb_des=2, faces=6, modificateur=0):
        total = sum(random.randint(1, faces) for _ in range(nb_des))
        total += modificateur
        if total >= 10:
            resultat = "reussite"
        elif total < 10 and total >=7:
            resultat = "partielle"
        else:
            resultat = "echec"
        return total, resultat
    
    #Lancement du jeu
    def __init__(self):
        
        self.ecran_propre()
        print("Bienvenue dans Epaventures spatiales, le jeu où vous incarnez un pill... heu, un explorateur et sauveteur de l'espace.")
        
        #Création du personnage
        print("Qui est votre personnage, que sait-il faire ?")
        self.nom_perso = input("Quel est son nom ?\n")
        score = input("\nEst-il plutôt coriace (C) ou futé (F) ? Si tu tapes C, il sera bon en combat et activités physiques, F il sera bon dans les aspects techniques et analytiques.\n").upper()
        self.coriace = 0
        self.fute = 0
        #Boucle d'acquisition des stats des capacités
        while True:
            if score == "C":
                self.coriace += 1
                break
            elif score == "F":
                self.fute += 1
                break
            else:
                score = input("Réponse invalide, indiquez C ou F :")
        
        
        print("\n====================================")
        print("\nFélicitation, vous êtes", self.nom_perso, "l'intrépide explorateur·rice et serviable sauveteur·euse de l'espace (officiellement du moins...).")
        print("\nVotre score de coriace est de", self.coriace, "et votre score de futé est", self.fute, ".")
        print("\n====================================")

        with open("Aventure_scenes.json", "r", encoding="utf-8") as fichier:
            self.scenes = json.load(fichier) #Transforme le fichier json en dictionnaire de scènes

    def afficher_resultats(self, scene, resultat):
        if "resultats" in scene:
            print(scene["resultats"][resultat])
        else:
            print(self.resultats_generiques[resultat])

    #Débuter l'aventure 
    def start(self):
        scene_actuelle = "debut"

        while True:
            #Eviter le bug KeyError: 'scene_inexistante'
            if scene_actuelle not in self.scenes: 
                print("Erreur : scène inconnue", scene_actuelle)
                break
            
            #Début de scène
            scene = self.scenes[scene_actuelle]

            print("\n" + scene["description"])

            #Scène avec choix          
            if "choix" in scene:
                for numero, choix_data in scene["choix"].items():
                    print(numero, ":", choix_data["texte"])
                choix = input("Choisis 1 ou 2 \n >")

                if choix in scene["choix"]:
                    scene_actuelle = scene["choix"][choix]["suivant"]
                    continue
                else:
                    print("Choix invalide.")
                    continue

            #Scène avec test
            elif "test" in scene:
                if scene["test"] == "combat":
                    total, resultat = self.lancer_des(modificateur=self.coriace)
                
                elif scene["test"] == "fute":
                    total, resultat = self.lancer_des(modificateur=self.fute)
                
                print("Tu obtiens un résultat de", total)

                self.afficher_resultats(scene, resultat)

                if "suivant" in scene:
                    scene_actuelle = scene["suivant"]
                    continue
                else:
                    break 

            #Scène simple (ni choix, ni test) : transition automatique
            elif "suivant" in scene:
                    scene_actuelle = scene["suivant"]
                    continue
            
            #Fin
            else:
                break                
#==========================
# Lancement du jeu
#==========================
jeu = Epaventure()
# Début de l'aventure
jeu.start()


#==========================
#Fin de jeu
#==========================
print("\nLa démo de ce jeu est terminée, merci d'avoir joué et au revoir !")
print("=====================================================")
print("Un jeu codé en Python par Grégoire Macqueron (2026), sous double licence GNU GPL v3 et Creative Commons CC BY-SA 4.0. Le système de résolution est propulsé par l'Apocalypse (PbtA), d'après le jeu Apocalypse World (2010) de D. Vincent Baker & Meguey Baker.")
quit()