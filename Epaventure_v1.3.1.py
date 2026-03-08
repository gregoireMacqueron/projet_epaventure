#Minimum viable product du jeu "Epaventure spatiale"
# Contenu : Description d’ambiance et début du jeu
# Choix (1 seul)
# Obstacle (fixe) 1 ou 2
# Gain (fixe) 1 ou 2
# Description d’ambiance et début du jeu

#Import des librairies/Libraries import
import random
import os

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
    scenes = {
        "couloir_1": {
            "description": 
            "Vous avez pénétré dans le couloir attenant au sas. Sur votre droite, il vous semble percevoir un mouvement dans l'obscurité, plus loin dans le couloir. A gauche, une porte fermée donne sur le couloir, qui continue plus loin dans l'obscurité.",
            #Choix
            "choix": {
                "1": ("aller à droite pour découvrir ce qu'était le mouvement.", "creature1"),
                "2": ("tenter d'ouvrir la porte de gauche.", "porte1")
            }
        },

        "creature1": {
            "description": 
            "\nTu avances lentement et précautionneusement dans le couloir obscur, le faisceau de ta lampe torche déchirant les ombres. Tu arrives à un embranchement et là, soudain, une créature te saute dessus et tente de déchirer ta combinaison !\n",
            #Epreuve
            "test": "combat",
            #Résultats contextualisés
            "resultats": {
                "reussite": "Tu parviens à tuer cette créature avec ton cutter à plasma. A tes pieds se trouve le corps de la créature et un corps, sans doute sa victime. Le corps en combinaison agrippe toujours un fusil énergétique que tu récupères.",
                "partielle":"Tu lui enfonces dans le flanc la lame-plasma de ton cutter, et elle s'enfuit dans le noir.",
                "echec": "La créature déchire ta combinaison et ton abdomen avant de disparaître à nouveau. Tu es blessé et perd de l'oxygène."
            }
        },

        "porte1": {
            "description": 
            "\nLe mécanisme de la porte de sécurité est bloqué en position fermée. Tu démontes le panneau de la commande et tentes de réactiver son fonctionnement.\n",
            #Epreuve
            "test": "fute",
            #Résultats contextualisés
            "resultats": {
                "reussite": "Tu parviens à ouvrir la porte mécanique. De l'autre côté, tu découvres une soute remplie de rubémeraudes !",
                "partielle": "Le corps d'un officier de pont flotte dans la pièce de l'autre côté. En fouillant sa combinaison, tu récupères sa montre en platine céleste.",
                "echec": "Tu déclenches un court-circuit et tu te brûles ! Quant à la porte, elle est définitivement bloquée..."
        }
    }
    }      
    
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
        print("Bienvenue dans Epaventure spatiale, le jeu où vous incarnez un pill... heu, un explorateur et sauveteur de l'espace.")
        
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

        #Intro première scène
        print("\nVous venez de quitter le havre de votre vaisseau de récupération et vous êtes désormais devant l'un des sas de l'énorme épave qui dérive dans le vide spatial.\n")
        self.scene = {
            "couloir": {
                "description": "Tu es dans un couloir sombre.",
                "choix": {
                    "1": ("Explorer le couloir", "creature"),
                    "2": ("Tenter d'ouvrir la porte", "porte")
                }
            },

            "creature": {
                "description": "Une créature surgit !",
                "test": "combat"
            },

            "porte": {
                "description": "La porte semble verrouillée.",
                "test": "crochetage"
            }
        }

    def afficher_resultats(self, scene, resultat):
        if "resultats" in scene:
            print(scene["resultats"][resultat])
        else:
            print(self.resultats_generiques[resultat])

    #Débuter l'aventure 
    def start(self):
        scene_actuelle = "couloir_1"

        while True:
            scene = self.scenes[scene_actuelle]

            print("\n" + scene["description"])

            #Scène avec choix
            if "choix" in scene:
                for numero, (texte, destination) in scene["choix"].items():
                    print(numero, ":", texte)
                choix = input("Choisis 1 ou 2 \n >")

                if choix in scene["choix"]:
                    scene_actuelle = scene["choix"][choix][1]
                else:
                    print("Choix invalide.")

            #Scène avec test
            elif "test" in scene:
                if scene["test"] == "combat":
                    total, resultat = self.lancer_des(modificateur=self.coriace)
                    print("Tu obtiens un", total, "en combat, avec un modificateur de Coriace de :", self.coriace)
                    self.afficher_resultats(scene, resultat)
                elif scene["test"] == "fute":
                    total, resultat = self.lancer_des(modificateur=self.fute)
                    print("Tu obtiens un", total, "en combat, avec un modificateur de Coriace de :", self.coriace)
                    self.afficher_resultats(scene, resultat)
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