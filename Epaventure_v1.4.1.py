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
air = 50

class Epaventure:  #Classe pour manipuler le jeu

    #Données / Dictionnaire de scènes
    #Partie basculée dans Aventure_scenes.json
    
    #Données / Résultats génériques de scènes (mécanique de fallback)
    resultats_generiques =  {
    "reussite": {
        "texte": "Tu réussis parfaitement.",
        "conso": {}
    },
    "partielle":{
        "texte": "Tu réussis, mais avec une complication",
        "conso": {"air": 2}
    },
    "echec": {
        "texte": "Tu échoues complètement." ,
        "conso": {"air": 5}
    }   
}
#==================
#Fonctions outils
#==================
    #Effacer le terminal
    def ecran_propre(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    #Fonction debug
    def debug_print(self, message): 
        if self.debug:
            print("[DEBUG]", message)

    def debug_etat(self):
        if not self.debug:
            return
        print("\n[DEBUG] Etat du personnage")
        for ressource, valeur in self.ressources.items():
            print(f"{ressource.vapitalize()} : {valeur}")
        print("Inventaire :", self.inventaire)

        distance = self.distance_sortie(self.scene_actuelle)
        if distance is not None:
            print("Air minimum pour sortir :", distance)

    #Distance minimale entre la scène actuelle et la sortie
    def distance_sortie(self, scene_depart, scene_fin="fin"):
        from collections import deque
        file = deque()
        file.append((scene_depart, 0))
        visites = set()
        while file:
            scene, distance = file.popleft()
            if scene == scene_fin:
                return distance
            if scene in visites:
                continue
            visites.add(scene)
            data = self.scenes[scene]

            ##transition simple
            if "suivant" in data:
                file.append((data["suivant"], distance + 1))

            ##transitions par choix
            if "choix" in data:
                for choix in data["choix"].values():
                    file.append((choix["suivant"], distance + 1))
        return None
    
    #Profondeur max de l'épave
    def profondeur_max(self):
        max_dist = 0
        for scene in self.scenes:
            d = self.distance_sortie(scene)
            if d and d > max_dist:
                max_dist = d
        return max_dist

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

    #Consommation d'air
    def consommer_air(self,quantite=1):
        self.ressources["air"] = max(0, self.ressources["air"] - quantite)
        print("Air -", quantite, "%")
        print("Réserve d'air restante :", self.ressources["air"], "%")
        if self.debug:
            print("[DEBUG] Air consommé :", quantite, "%")


    #Lancement du jeu
    def __init__(self):
        
        #Mode débug
        self.debug = input("Mode debug ? (o/n) ").lower() == "o"
        
        # self.ecran_propre()
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
        
        #Gestion des ressources
        self.ressources = {
        "air": 50
        }
        
        
        print("\n====================================")
        print("\nFélicitation, vous êtes", self.nom_perso, "l'intrépide explorateur·rice et serviable sauveteur·euse de l'espace (officiellement du moins...).")
        print("\nVotre score de coriace est de", self.coriace, "et votre score de futé est", self.fute, ".")
        print("Votre réserve d'air est de", self.ressources["air"], "%.")
        print("\n====================================")

        chemin = os.path.join(os.path.dirname(__file__),"Aventure_scenes.json")
        
        with open(chemin, "r", encoding="utf-8") as fichier:
            self.scenes = json.load(fichier) #Transforme le fichier json en dictionnaire de scènes

        self.inventaire = []

    def appliquer_effets(self, effets):

        for cle, valeur in effets.items():

            if cle == "loot":

                self.inventaire.append(valeur)
                print("Tu trouves :", valeur)

            else:
                if cle not in self.ressources:
                    self.ressources[cle] = 0

                self.ressources[cle] += valeur

                print(cle, valeur)

    def afficher_resultats(self, scene, resultat):
        if "resultats" in scene:
            texte = scene["resultats"][resultat]
        else:
            texte = self.resultats_generiques[resultat]["texte"]
        print(texte)
        if "effets" in scene and resultat in scene["effets"]:
            self.appliquer_effets(scene["effets"][resultat])
            #data = self.resultats_generiques[resultat]
            #texte = data["texte"]
            #conso = data["conso"]

        print(texte)

        #for ressource, perte in conso.items():
        #    self.ressources[ressource] = max(0, self.ressources[ressource] - perte)
        #    print(ressource, "-", perte)

        if "conso" in scene and resultat in scene["conso"]:
            for ressource, perte in scene["conso"][resultat].items():

            self.ressources[ressource] = max(0, self.ressources[ressource] - perte)

            print(ressource, "-", perte)
            print("Réserve restante :", self.ressources[ressource], "%")

    #Débuter l'aventure 
    def start(self):
        scene_actuelle = "debut"

        #=================
        ##Pour mode débug
        scene = self.scenes[scene_actuelle]
        #self.debug_print(f"Scène actuelle : {scene_actuelle}")    #(reporté dans boucle While True)

        if self.debug:
            distance = self.distance_sortie(scene_actuelle)
        if distance is not None:
            print(f"[DEBUG] Distance de sortie : {distance} scènes")
            print(f"[DEBUG] Air minimum pour sortir : {distance}")
        else:
            print("[DEBUG] Aucune sortie trouvée.")
        
        if self.debug:
            print("[DEBUG] Profondeur maximale de l'épave :", self.profondeur_max())
        #=================
        while True:

            #Debug "air minimum pour sortir"
            self.scene_actuelle = scene_actuelle 

            #Eviter le bug KeyError: 'scene_inexistante'
            if scene_actuelle not in self.scenes: 
                print("Erreur : scène inconnue", scene_actuelle)
                break
            
            #Début de scène
            scene = self.scenes[scene_actuelle]
            ##Pour mode débug
            self.debug_print(f"Scène actuelle : {scene_actuelle}")
            
            #Consommation d'air par défaut (sauf début)
            if scene_actuelle != "debut":
                self.consommer_air(1)
            #Game over par manque d'air
            if self.ressources["air"] <= 0:
                print("Ton air est épuisé... tu suffoques dans le vide.")
                break

            #Affichage description
            print("\n" + scene["description"])

            resultat = None         #Evite bug si la scène n'a pas de test.
            scene_suivante = None

            #================
            #Scène avec choix          
            if "choix" in scene:
                for numero, choix_data in scene["choix"].items():
                    print(numero, ":", choix_data["texte"])
                choix = input("Choisis 1 ou 2 \n >")

                #Commande debug : liste des scènes
                if self.debug and choix == "scenes":
                    print("Scènes disponibles :")
                    for s in self.scenes.keys():
                        print("-", s)
                    continue
                #Commande debug : téléportation
                if self.debug and choix.startswith("debug"):
                    commande = choix.split()

                    if len(commande) == 2 and commande[1] in self.scenes:
                        scene_actuelle = commande[1]
                        self.debug_print(f"Téléportation vers : {scene_actuelle}")
                        continue

                #Pour éviter des bugs
                if choix in scene["choix"]:
                    scene_actuelle = scene["choix"][choix]["suivant"]
                    continue
                else:
                    print("Choix invalide.")
                    continue

            #================
            #Scène avec test
            elif "test" in scene:
                if scene["test"] == "combat":
                    total, resultat = self.lancer_des(modificateur=self.coriace)
                
                elif scene["test"] == "fute":
                    total, resultat = self.lancer_des(modificateur=self.fute)
                
                self.debug_print(f"Jet : {total} → {resultat}")

                print("Tu obtiens un résultat de", total)

                self.afficher_resultats(scene, resultat)  

            #Gestion automatique de la consommation d'air supplémentaire
            #    if "conso" in scene and resultat in scene["conso"]:
            #        perte = scene["conso"][resultat]
            #        self.consommer_air(perte)
            #        print("Réserve d'air restante :", self.ressources["air"], "%.")

            #Gestion automatique du butin
            #    if "loot" in scene and resultat in scene["loot"]:
            #        objet = scene["loot"][resultat]
            #        self.inventaire.append(objet)
            #        print("tu trouves :", objet)

                #if "suivant" in scene:
                #    scene_actuelle = scene["suivant"]
                #    continue
                #else:
                #    break 

                scene_suivante = scene.get("suivant")

            #================
            #Scène simple (ni choix, ni test)
            else:
                scene_suivante = scene.get("suivant")

            #================
            #Transition automatique (Passage automatique à la scène suivante)
            if scene_suivante:
                self.debug_print(f"Transition vers : {scene_suivante}")
                scene_actuelle = scene_suivante
            else:
                break   

            #Pour mode débug (dont état)
            self.debug_etat()
            #print(self.scenes.keys())
                      
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